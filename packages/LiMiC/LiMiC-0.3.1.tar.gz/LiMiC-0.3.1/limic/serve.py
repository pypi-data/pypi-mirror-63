COUNTRIES = (("countries",),{'type':str,'nargs':'*','help':"countries to route on",'metavar':'COUNTRY'})
GRAPH = (("graph_file",),{'type':str,'help':"use graph file GRAPH",'metavar':'GRAPH'})
HTML = (("html_file",),{'type':str,'help':"use rendered HTML file",'metavar':'HTML'})
RHOST = (("--render-host",),{'type':str,'dest':'r_host','default':'localhost','help':"render hostname (default: localhost)",'metavar':'HOST'})
RPORT = (("--render-port",),{'type':int,'dest':'r_port','default':5000, 'help':"render port number (default: 5000)",'metavar':'PORT'})
RPREFIX = (("--render-prefix",),{'type':str,'dest':'r_prefix','default':'','help':"render URI prefix (default: '')",'metavar':'PREFIX'})
HOST = (("--host",),{'type':str,'dest':'host','default':'localhost','help':"hostname (default: localhost)",'metavar':'HOST'})
PORT = (("--port",),{'type':int,'dest':'port','default':5000, 'help':"port number (default: 5000)",'metavar':'PORT'})
PREFIX = (("--prefix",),{'type':str,'dest':'prefix','default':'','help':"URI prefix (default: '')",'metavar':'PREFIX'})
OSM = (("--osm",),{'action':'store_true','dest':'osm','default':False,'help':"process from OSM file (SLOW)"})
NOBROWSER = (("-n","--no-browser"),{'action':'store_true','dest':'no_browser','default':False,'help':"do not open html in browser (headless)"})
URL = (("-d","--download-url"),{'type':str,'dest':'url','help':"define url for download directory to be URL",'metavar':'URL'})
SHOW = (("-l","--list"),{'action':'store_true','dest':'show','default':False,'help':"list available countries (default: False)"})

CONFIG = [
    ("auto",{'help':"start HTTP server for given COUNTRY (default: Europe)",'args':[SHOW,URL,NOBROWSER,HOST,PORT,PREFIX,RHOST,RPORT,RPREFIX,OSM,COUNTRIES]}),
    ("nx",{'help':"start HTTP server for given GRAPH and rendered HTML file",'args':[SHOW,URL,NOBROWSER,HOST,PORT,PREFIX,RHOST,RPORT,RPREFIX,GRAPH,HTML]}),
]

def serve_auto(countries,host="localhost",port=5000,prefix="",osm=False,url=None,show=False,no_browser=False,r_host="localhost",r_port=5000,r_prefix=""):
    from limic.download import common, download_graph, download_merged, download_osm
    from limic.init import extract_osm_all, merge_all
    from limic.render import render_nx
    graph_file = None
    if osm:
        download_osm(countries=countries,url=url)
        countries, url = common(countries=countries,url=url,show=show,osm=osm)
        extract_osm_all(countries=countries)
    elif not countries:
        _, url = common(countries=countries,url=url,show=show,osm=osm)
        countries = []
        download_merged(suffixes=("nx",),url=url)
    else:
        countries, url = common(countries=countries,url=url,show=show,osm=osm)
        download_graph(suffix="nx",countries=countries,url=url,show=show)
    if len(countries) > 1 :
        merge_all(countries)
    if len(countries) == 1:
        graph_file = "graph."+countries[0]+".nx"
    else:
        graph_file = "merged.Europe.nx"
    html_file = graph_file[:-2]+"html"
    serve_nx(graph_file,html_file,host=host,port=port,prefix=prefix,url=url,show=show,no_browser=no_browser,r_host=r_host,r_port=r_port,r_prefix=r_prefix)
        
    
def serve_nx(graph_file,html_file,host="localhost",port=5000,prefix="",url=None,show=False,no_browser=False,r_host="localhost",r_port=5000,r_prefix=""):
    from flask import Flask, jsonify, request
    from limic.util import load_pickled, start, end, status
    from limic.route import astar_nx
    from limic.render import render_nx
    from threading import Thread
    from time import sleep
    from webbrowser import open as wopen
    from scipy.spatial import cKDTree as KDTree
    from pyproj import CRS, Transformer
    g = render_nx(graph_file,html_file,host=r_host,port=r_port,prefix=r_prefix)
    start("Initializing KD-Tree")
    nodes = list(g.nodes())
    crs_4326 = CRS("WGS84")
    crs_proj = CRS("EPSG:28992")
    transformer = Transformer.from_crs(crs_4326, crs_proj)
    tree = KDTree(list(map(lambda x:transformer.transform(x[1],x[2]),nodes)))
    end()

    start("Setting up the app")
    app = Flask("LiMiC")

    @app.route(prefix+"/")
    def hello():
        return open(html_file).read()

    @app.route(prefix+"/tower")
    def tower():
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))
        start("Finding tower",lat,lng)
        tower = nodes[tree.query(transformer.transform(lat,lng))[1]]
        end('')
        res = jsonify(tower=tower)
        end()
        return res

    @app.route(prefix+"/route")
    def route():
        source_lat = float(request.args.get('source[lat]'))
        source_lng = float(request.args.get('source[lng]'))
        target_lat = float(request.args.get('target[lat]'))
        target_lng = float(request.args.get('target[lng]'))
        start("Routing",source_lat,source_lng,target_lat,target_lng)
        source = nodes[tree.query(transformer.transform(source_lat,source_lng))[1]]
        end('')
        target = nodes[tree.query(transformer.transform(target_lat,target_lng))[1]]
        end('')
        path = astar_nx(g,source,target)
        end('')
        if path[1][-1][0] == float('inf'):
            path[1][-1] = (path[1][-1][1],)+path[1][-1][1:]
        res = jsonify(path=path)
        end()
        return res
    end()

    class OpenThread(Thread):
        def run(self):
            delay = 0.5
            sleep(delay)
            url = "http://%s:%d%s/" % (host,port,prefix)
            start("Opening",url,"in browser")
            wopen(url,new=2)
            status("DONE")
    if not no_browser:
        OpenThread().start()
    app.run(host=host,port=port)
