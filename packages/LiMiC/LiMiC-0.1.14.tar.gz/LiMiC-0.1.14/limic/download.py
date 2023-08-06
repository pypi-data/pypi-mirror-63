COUNTRIES = (("countries",),{'type':str,'nargs':'*','help':"countries to work on",'metavar':'COUNTRY'})
SUFFIXES = (("suffixes",),{'type':str,'nargs':'+','help':"suffixes to download",'metavar':'SUFFIX'})
URL = (("-d","--download-url"),{'type':str,'dest':'url','help':"define url for download directory to be URL",'metavar':'URL'})
SHOW = (("-l","--list"),{'action':'store_true','dest':'show','default':False,'help':"list available countries (default: False)"})

CONFIG = [
    ("osm",{'help':"download map data",'args':[SHOW,URL,COUNTRIES]}),
    ("graph",{'help':"download graph files",'args':[
        ("nx",{'help':"download NX graph files",'args':[SHOW,URL,COUNTRIES]}),
        ("gt",{'help':"download GT graph files",'args':[SHOW,URL,COUNTRIES]}),
        ("npz",{'help':"download NPZ graph files",'args':[SHOW,URL,COUNTRIES]})
    ]}),
    ("cache",{'help':"download cache files from Overpass API",'args':[SHOW,URL,COUNTRIES]}),
    ("merged",{'help':"download merged graph file",'args':[URL,SUFFIXES]})
]
BASE_URL="http://caracal.imada.sdu.dk/d4e/"
COUNTRIES="Albania,Andorra,Austria,Belarus,Belgium,Bosnia and Herzegovina,Bulgaria,Croatia,Cyprus,Czechia,Denmark,Estonia,Faroe Islands,Finland,France,Georgia,Germany,Gibraltar,Greece,Guernsey,Hungary,Iceland,Ireland,Isle of Man,Italy,Jersey,Kosovo,Latvia,Liechtenstein,Lithuania,Luxembourg,Macedonia,Malta,Moldova,Monaco,Montenegro,Netherlands,Norway,Poland,Portugal,RU,Romania,San Marino,Serbia,Slovakia,Slovenia,Spain,Sweden,Switzerland,Turkey,Ukraine,United Kingdom"
OSM_COUNTRIES="albania,andorra,austria,azores,belarus,belgium,bosnia-herzegovina,bulgaria,croatia,cyprus,czech-republic,denmark,estonia,faroe-islands,finland,france,georgia,germany,great-britain,greece,hungary,iceland,ireland-and-northern-ireland,isle-of-man,italy,kosovo,latvia,liechtenstein,lithuania,luxembourg,macedonia,malta,moldova,monaco,montenegro,netherlands,norway,poland,portugal,romania,russia,serbia,slovakia,slovenia,spain,sweden,switzerland,turkey,ukraine"
OSM_URL="https://download.geofabrik.de/europe/"

def download_file(url,file_name):
    from requests import get
    from shutil import copyfileobj
    from sys import exit
    from limic.util import status
    r = get(url, stream=True)
    if r.status_code != 200:
        status("ERROR: HTTP status 200 expected, got "+str(r.status_code))
        exit(-1)
    f = open(file_name, 'wb')
    copyfileobj(r.raw, f)
    return file_name

def download_osm(countries,url=None,show=False):
    from limic.util import start,end,file_size
    countries, url = common(countries,url,show,osm=True)
    for country in countries:
        start("Downloading OSM map data for",country)
        file_url = OSM_URL+("../" if country == "russia" else "")+country+"-latest.osm.bz2"
        file_name = download_file(file_url,country+"-latest.osm.bz2")
        end('')
        file_size(file_name)

def download_cache(countries,url=None,show=False):
    from limic.util import start,end,file_size
    countries, url = common(countries,url,show)
    for country in countries:
        start("Downloading cache for",country)
        file_url = url+"cache."+country.replace(" ","%20")
        file_name = download_file(file_url,"cache."+country)
        end('')
        file_size(file_name)

def download_graph(suffix,countries,url=None,show=False):
    from limic.util import start,end,file_size
    countries, url = common(countries,url,show)
    for country in countries:
        start("Downloading",suffix.upper(),"graph for",country)
        file_url = url+"graph."+country.replace(" ","%20")+"."+suffix
        file_name = download_file(file_url,"graph."+country+"."+suffix)
        end('')
        file_size(file_name)

def download_graph_nx(countries,url=None,show=False):
    download_graph("nx",countries,url=url,show=show)

def download_graph_gt(countries,url=None,show=False):
    download_graph("gt",countries,url=url,show=show)

def download_graph_npz(countries,url=None,show=False):
    download_graph("npz",countries,url=url,show=show)
        
def download_merged(suffixes=("nx","gt","npz"),url=None):
    from limic.util import start,end,file_size
    for suffix in suffixes:
        start("Downloading merged",suffix.upper(),"graph for Europe")
        file_url = url+"merged.Europe."+suffix
        file_name = download_file(file_url,"merged.Europe."+suffix)
        end('')
        file_size(file_name)

def common(countries,url=None,show=False,osm=False):
    from limic.util import get_parser
    if show:
        get_parser().error("Available countries:\n"+" ".join((OSM_COUNTRIES if osm else COUNTRIES).split(",")))
    if not countries:
        countries = OSM_COUNTRIES.split(",") if osm else COUNTRIES.split(",")
    if not url:
        url = OSM_URL if osm else BASE_URL
    return countries, url
