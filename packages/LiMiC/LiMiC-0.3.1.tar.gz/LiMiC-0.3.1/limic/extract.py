CACHE = (("file_name_in",),{'type':str,'help':"read map data from cache file CACHE",'metavar':'CACHE'})
LIM = (("file_name_in",),{'type':str,'help':"read map data from LiMiC file FILE",'metavar':'LIM'})
OSM = (("file_name_in",),{'type':str,'help':"read map data from OpenStreetMap file OSM",'metavar':'OSM'})
OUT = (("file_name_out",),{'type':str,'help':"save extracted graph to file GRAPH",'metavar':'GRAPH'})
EPS = (("-e","--epsilon"),{'type':float,'dest':'eps','default':0.01,'help':"set minimum percentage of  linear infrastructure segment to consider non-logical intersections to EPS",'metavar':'EPS'})
AROUND = (("-r","--around"),{'type':int,'dest':'around','default':1000,'help':"set maximum free flying distance in m around linear infrastructure nodes to AROUND",'metavar':'AROUND'})
SAFEDIST = (("-s","--safe-dist"),{'type':int,'dest':'safe_dist','default':100,'help':"set minimum safe distance from blacklisted areas and structures to SAFE",'metavar':'SAFE'})
PENALIZE = (("-p","--penalize"),{'type':int,'default':20,'dest':'penalize','help':"penalize free flying disrances by factor PENALTY",'metavar':'PENALTY'})
WHITE = (("--white",),{'type':str,'dest':'white','default':'{"power":"line"}','help':"linear infrastructure to include (default: {'power':'line'})",'metavar':'WHITELIST'})
BLACK = (("--black",),{'type':str,'dest':'black','default':'{"power":"substation"}','help':"areas and structures to avoid (default: {'power':'substation'})",'metavar':'BLACKLIST'})
CONSERVEMEM = (("-c","--conserve-memory"),{'action':'store_true','dest':'conserve_mem','default':False,'help':"lower memory usage but higher runtime"})

CONFIG = [
    ("cache",{'args':[
        (("-u","--overpass-url"),{'type':str,'dest':'overpass_url','help':"define url for Overpass API to be URL",'metavar':'URL'}),
        (("-a","--area"),{'type':str,'dest':'area','help':"set area to extract to AREA",'metavar':'AREA'}),
        AROUND,EPS,SAFEDIST,PENALIZE,CACHE,OUT
    ]}),
    ("osm",{'args':[BLACK,WHITE,CONSERVEMEM,AROUND,EPS,SAFEDIST,PENALIZE,OSM,OUT]}),
    ("osm_pre",{'args':[BLACK,WHITE,CONSERVEMEM,OSM,OUT]}),
    ("osm_post",{'args':[AROUND,EPS,SAFEDIST,PENALIZE,LIM,OUT]})
    #("esy",{'args':[OSM,OUT]})
]

def prune_incomplete(g):
    to_prune = set()
    for k in g.nodes():
        gk = g[k]
        for l in g.neighbors(k):
            if k < l:
                gl = g[l]
                for m in g.neighbors(l):
                    if g.has_edge(k,m) and gk[l]['weight'] > gk[m]['weight']+gl[m]['weight']:
                        to_prune.add((k,l))
    for u,v in to_prune:
        if g.has_edge(u,v):
            g.remove_edge(u,v)

def prune_complete(g):
    from networkx import astar_path_length
    to_prune = set()
    for k in g.nodes():
        for l in g.neighbors(k):
            if k < l and g[k][l]['weight'] > astar_path_length(g,k,l):
                to_prune.add((k,l))
    for u,v in to_prune:
        if g.has_edge(u,v):
            g.remove_edge(u,v)

def build_edges(g,find_all_neighbours,around,eps,safe_dist,penalize):
    from limic.overpass import pylon
    from limic.util import distance
    #count = 0
    neighbours2intersection = {}
    minusid = [0]
    latlon2id = {}
    for tower in list(g.nodes()):
        #count += 1
        #if verbosity >= 2: print(count,"of",total)
        for neighbour in find_all_neighbours(tower,around,eps,safe_dist,minusid,latlon2id,penalize):
            if neighbour.tower in g or neighbour.tower.id < 0:
                #if verbosity >= 2: print("adding",neighbour)
                g.add_edge(tower,pylon(neighbour.tower.id,neighbour.tower.latlon),weight=neighbour.dist,type=neighbour.air)
                if neighbour.tower.id < 0:
                    for intersection in neighbours2intersection.setdefault(neighbour.tower.neighbours,[]):
                        if intersection.latlon != neighbour.tower.latlon:
                            #if verbosity >= 2: print("double intersection:",intersection.latlon,neighbour.tower.latlon)
                            g.add_edge(intersection,neighbour.tower,weight=distance(intersection.latlon,neighbour.tower.latlon),type=False)
                    neighbours2intersection[neighbour.tower.neighbours].append(neighbour.tower)


def extract_cache(file_name_in,file_name_out,overpass_url,area=None,around=1000,eps=0.01,safe_dist=100,penalize=20):
    from limic.overpass import distance, find_all_neighbours, is_safe, set_server, pylon, region, get_towers_by_area
    from limic.util import start, end, file_size, status, load_pickled, save_pickled, replace, check_overwrite
    from networkx import Graph
    if not check_overwrite(file_name_in,file_name_out):
        return
    start("Loading",file_name_in)
    region.backend._cache = load_pickled(file_name_in)
    len_cache = len(region.backend._cache)
    end('')
    file_size(file_name_in)
    if not area:
        area = file_name_in.split(".")[1]
    start("Querying overpass for",area)
    set_server(overpass_url)
    towers = get_towers_by_area(area)
    end()
    start("Building safe nodes")
    g=Graph()
    for tower in towers:
        if is_safe(tower,safe_dist):
            g.add_node(tower)
#        else:
#        if verbosity >= 2: print("NOT safe!")
    end('')
    total = len(g.nodes())
    status(total)
    start("Building edges")
    build_edges(g,find_all_neighbours,around,eps,safe_dist,penalize)
    end('')
    status(len(g.edges()))
    if len_cache != len(region.backend._cache):
        file_name_tmp = file_name_in+".tmp"
        start("Saving to",file_name_in,"via",file_name_tmp)
        save_pickled(file_name_tmp,region.backend._cache)
        replace(file_name_tmp,file_name_in)
        end('')
        file_size(file_name_in)
    common_end(g,file_name_out)
        
def common_end(g,file_name_out,id2types=None):
    from limic.util import start, end, status, file_size, save_pickled
    from networkx import relabel_nodes
    start("Prune redundant edges (incomplete)")
    prune_incomplete(g)
    end('')
    status(len(g.edges()))
    start("Prune redundant edges (complete)")
    prune_complete(g)
    end('')
    status(len(g.edges()))
    start("Cleaning up graph")
    relabel = dict(map(lambda tower:(tower,(tower.id,tower.latlon[0],tower.latlon[1])),g.nodes()))
    relabel_nodes(g,relabel,copy=False)
    if id2types:
        for u,v,d in g.edges(data=True):
            if u[0] >= 0:
                current = u
            elif v[0] >= 0:
                current = v
            else:
                todo = [u]
                done = set()
                current = None
                while todo:
                    current = todo.pop()
                    if current[0] >= 0:
                        break
                    if current in done:
                        continue
                    done.add(current)
                    for n in g.neighbors(current):
                        if not n in done:
                            todo.append(n)
                assert(current is not None)
            d['type'] = -1 if d['type'] else id2types[current[0]]
    else:
        for u,v,d in g.edges(data=True):
            d['type'] = -1 if d['type'] else 0
    end()
    start("Saving graph to",file_name_out)
    save_pickled(file_name_out,g)
    end('')
    file_size(file_name_out)

def is_safe(m_nodes,id2substations,id2elem,tower,around):
    from shapely.geometry import Point, Polygon
    nodes = [] if m_nodes[1] is None else list(map(lambda x:m_nodes[0][x],m_nodes[1].query_ball_point(m_nodes[2].transform(*tower.latlon),r=around)))
    if not nodes:
        return True
    p = Point(*tower.latlon)
    substations = []
    for node in nodes:
        for substation in id2substations[node.id]:
            if not substation in substations:
                substations.append(substation)
    for substation in substations:
        if len(substation) < 3:
            continue
        poly = Polygon(list(map(lambda x:id2elem[x].latlon,substation)))
        if p.within(poly):
            return False
    return True

def find_neighbours(tower,id2elem,id2lines):
    towers = set()
    if tower.id < 0:
        towers.update(tower.neighbours)
        return towers
    for line in id2lines[tower.id]:
        index = line.index(tower.id)
        if index > 0:
            towers.add(line[index-1])
        if index+1 < len(line):
            towers.add(line[index+1])
    return list(map(lambda id:id2elem[id],towers))

def find_segments(tower,around,id2elem,id2lines,neighbourhood):
    segments = []
    lines = []
    for other in neighbourhood:
        for line in id2lines[other.id]:
            if not line in lines:
                lines.append(line)
    for line in lines:
        for i in range(1,len(line)):
            segments.append((line[i-1],line[i]))
    return list(map(lambda x:(id2elem[x[0]],id2elem[x[1]]),segments))            

def find_all_neighbours(tower,around,eps,safe_dist,minusid,latlon2id,penalize,m_towers,m_nodes,id2elem,id2lines,id2substations,latlon2safe):
    from limic.overpass import dist, dist_towers, intersect, pylon
    from limic.util import distance
    direct_neighbours = find_neighbours(tower,id2elem,id2lines)
    neighbours = dist_towers(direct_neighbours,tower.latlon)
    direct_segments = list(map(lambda neighbour:(neighbour.tower,tower),neighbours))
    #print(tower)
    #print(direct_neighbours)
    #print(neighbours)
    neighbourhood = [] if m_towers[1] is None else list(map(lambda x:m_towers[0][x],m_towers[1].query_ball_point(m_towers[2].transform(*tower.latlon),r=around)))
    for neighbour in map(lambda x:dist(0.,False,x),neighbourhood):
        if not neighbour.tower in direct_neighbours and neighbour.tower.id != tower.id:
            neighbour.dist = distance(neighbour.tower.latlon,tower.latlon)*penalize
            neighbour.air = True
            neighbours.append(neighbour)
            #print(neighbour)
    indirect_segments = find_segments(tower,around,id2elem,id2lines,neighbourhood)
    for indirect_segment in indirect_segments:
        for direct_segment in direct_segments:
            intersection = intersect(direct_segment[0].latlon,direct_segment[1].latlon,indirect_segment[0].latlon,indirect_segment[1].latlon,eps)
            if intersection:
                #if verbosity >= 3:
                #    print("found intersection",direct_segment,indirect_segment,intersection)
                #    print("node(id:"+(",".join(map(lambda t:str(t.id),[direct_segment[0],direct_segment[1],indirect_segment[0],indirect_segment[1]])))+");out;")
                if not intersection in latlon2id:
                    minusid[0] -= 1
                    latlon2id[intersection] = minusid[0]
                neighbours.append(dist(distance(intersection,tower.latlon),False,pylon(latlon2id[intersection], intersection,neighbours=indirect_segment)))
    safe_neighbours = []
    for neighbour in neighbours:
        safe = latlon2safe.get(neighbour.tower.latlon,None)
        if safe == None:
            safe = is_safe(m_nodes,id2substations,id2elem,neighbour.tower,safe_dist)
            latlon2safe[neighbour.tower.latlon] = safe
        if safe:
            safe_neighbours.append(neighbour)
        #else:
            #if verbosity >= 4: print("unsafe and skipped:",neighbour.tower)
    return safe_neighbours

def extract_osm(file_name_in,file_name_out,around=1000,eps=0.01,safe_dist=100,penalize=20,white="{'power':'line'}",black="{'power':'substation'}",conserve_mem=False):
    from limic.util import check_overwrite
    if not check_overwrite(file_name_in,file_name_out):
        return
    white,black = list(eval(white).items()), list(eval(black).items())
    lim = osm_pre(file_name_in,white,black,conserve_mem)
    osm_post(lim,file_name_out,around=1000,eps=0.01,safe_dist=100,penalize=20)

def extract_osm_pre(file_name_in,file_name_out,white="{'power':'line'}",black="{'power':'substation'}",conserve_mem=False):
    from limic.util import start, end, save_pickled, file_size, check_overwrite
    if not check_overwrite(file_name_in,file_name_out):
        return
    white,black = list(eval(white).items()), list(eval(black).items())
    lim = osm_pre(file_name_in,white,black,conserve_mem)
    start("Saving data to",file_name_out)
    save_pickled(file_name_out,lim)
    end('')
    file_size(file_name_out)

def extract_osm_post(file_name_in,file_name_out,around=1000,eps=0.01,safe_dist=100,penalize=20):
    from limic.util import start, end, file_size, load_pickled, check_overwrite
    if not check_overwrite(file_name_in,file_name_out):
        return
    start("Loading filtered OSM data from",file_name_in)
    lim = load_pickled(file_name_in)
    end('')
    file_size(file_name_in)
    osm_post(lim,file_name_out,around=1000,eps=0.01,safe_dist=100,penalize=20)

def osm_post(lim,file_name_out,around=1000,eps=0.01,safe_dist=100,penalize=20):
    from limic.util import start, end, status, file_size, load_pickled, haversine_distance
    #from limic.mtree import MTree
    from scipy.spatial import cKDTree as KDTree
    from networkx import Graph
    from pyproj import CRS, Transformer
    lines, substations, towers, nodes, id2elem, id2lines, id2substations, id2types = lim
    #start("Loading filtered OSM data from",file_name_in)
    #lines, substations, towers, nodes, id2elem, id2lines, id2substations = load_pickled(file_name_in)
    #end()
    start("Building KD-trees from nodes")
    #def distance(x,y):
    #    return haversine_distance(longx=x.latlon[1],latx=x.latlon[0],longy=y.latlon[1],laty=y.latlon[0])
    #m_towers = MTree(d=distance)
    #m_towers.add_all(towers)
    #m_nodes = MTree(d=distance)
    #m_nodes.add_all(nodes)
    crs_4326 = CRS("WGS84")
    crs_proj = CRS("EPSG:28992")
    transformer = Transformer.from_crs(crs_4326, crs_proj)
    list_towers = list(towers)
    towers_tree = KDTree(list(map(lambda x:transformer.transform(x.latlon[0],x.latlon[1]),list_towers))) if towers else None
    m_towers = (list_towers,towers_tree,transformer)
    list_nodes = list(nodes)
    nodes_tree = KDTree(list(map(lambda x:transformer.transform(x.latlon[0],x.latlon[1]),list_nodes))) if nodes else None
    m_nodes = (list_nodes,nodes_tree,transformer)
    end()
    #print(m_towers.size)
    #print(m_nodes.size)
    #print("node(id:"+(",".join(list(map(lambda x:str(x.obj.id) if x else "",m_towers.search(towers[0],r=3000)))))+");out;")
    from limic.overpass import pylon
    #find_segments(pylon(1847250054,(56.3973359,8.7254833)),around,m_towers,id2elem,id2lines)
    start("Building safe nodes")
    latlon2safe = {}
    g=Graph()
    for tower in towers:
        safe = is_safe(m_nodes,id2substations,id2elem,tower,safe_dist)
        latlon2safe[tower.latlon] = safe
        if safe:
            g.add_node(tower)
#        else:
#            if verbosity >= 2: print("NOT safe!")
    end('')
    total = len(g.nodes())
    status(total)
    start("Building edges")
    def fan(tower,around,eps,safe_dist,minusid,latlon2id,penalize):
        return find_all_neighbours(tower,around,eps,safe_dist,minusid,latlon2id,penalize,m_towers,m_nodes,id2elem,id2lines,id2substations,latlon2safe)
    build_edges(g,fan,around,eps,safe_dist,penalize)
    end('')
    status(len(g.edges()))
    common_end(g,file_name_out,id2types)

def osm_pre(file_name_in,white=[("power","line")],black=[("power","substation")],conserve_mem=False):
    from limic.util import start, end, status, file_size, save_pickled
    from xml.sax import parse
    from xml.sax.handler import ContentHandler
    from bz2 import open as bopen
    from limic.overpass import pylon
    start("Extracting ways for power lines from",file_name_in)
    class ways_handler(ContentHandler):
        def __init__(self):
            self.nodes = None
            self.power = None
            self.lines = []
            self.substations = []
            self.towers = []
            self.type = None
            self.id2types = {}
        def startElement(self, name, attrs):
            if name == 'way':
                self.nodes = []
                self.power = None
            elif name == 'tag':
                kv = (attrs['k'],attrs['v'])
                if kv in white:
                    self.power = "white"
                    self.type = white.index(kv)
                elif kv in black:
                    self.power = "black"
            elif name == 'nd':
                self.nodes.append(int(attrs['ref']))
            elif name == 'node':
                if not conserve_mem:
                    self.towers.append(pylon(int(attrs['id']),(float(attrs['lat']),float(attrs['lon']))))
        def endElement(self, name):
            if name == 'way':
                if self.power == 'white':
                    for node in self.nodes:
                        self.id2types[node] = self.type
                    self.lines.append(self.nodes)
                elif self.power == 'black':
                    self.substations.append(self.nodes)
    f = bopen(file_name_in,"rb") if file_name_in[-4:] == ".bz2" else open(file_name_in,"rb")
    ways = ways_handler()
    parse(f, ways)
    f.close()
    lines, substations, id2types = ways.lines, ways.substations, ways.id2types
    end('')
    status(len(lines),end='   ')
    status(len(substations))
    id2lines, id2substations = {}, {}
    for line in lines:
        for node in line:
            id2lines.setdefault(node,[]).append(line)
    for substation in substations:
        for node in substation:
            id2substations.setdefault(node,[]).append(substation)
    if conserve_mem:
        del ways
        start("Extracting nodes for white and black")
        class nodes_handler(ContentHandler):
            def __init__(self):
                self.towers = []
                self.nodes = set()
                self.id2elem = {}
            def startElement(self, name, attrs):
                if name == 'node':
                    i = int(attrs['id'])
                    if i in id2lines:
                        elem = pylon(i,(float(attrs['lat']),float(attrs['lon'])))
                        self.towers.append(elem)
                        self.id2elem[i] = elem
                    elif i in id2substations:
                        elem = pylon(i,(float(attrs['lat']),float(attrs['lon'])))
                        self.nodes.add(elem)
                        self.id2elem[i] = elem
        f = bopen(file_name_in,"rb") if file_name_in[-4:] == ".bz2" else open(file_name_in,"rb")
        ns = nodes_handler()
        parse(f, ns)
        f.close()
        towers, nodes, id2elem = ns.towers, ns.nodes, ns.id2elem
        del ns
        end('')
        status(len(towers),end='   ')
        status(len(nodes))
    else:
        start("Extracting nodes for white and black")
        towers = []
        nodes = set()
        id2elem = {}
        for tower in ways.towers:
            if tower.id in id2lines:
                id2elem[tower.id] = tower
                towers.append(tower)
            elif tower.id in id2substations:
                id2elem[tower.id] = tower
                nodes.add(tower)
        del ways
        end()
    start("Checking that all nodes were extracted")
    assert(set(id2lines.keys())==set(map(lambda x:x.id,towers)))
    assert(set(id2substations.keys())==set(map(lambda x:x.id,list(nodes))))
    end()
    return lines,substations,towers,nodes,id2elem,id2lines,id2substations,id2types
