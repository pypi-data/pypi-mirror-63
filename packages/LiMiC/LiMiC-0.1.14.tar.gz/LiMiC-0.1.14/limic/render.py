GRAPH = (("file_name_in",),{'type':str,'help':"use graph file GRAPH",'metavar':'GRAPH'})
HTML = (("file_name_out",),{'type':str,'help':"render to file HTML",'metavar':'HTML'})
MARKERS = (("--markers",),{'action':'store_true','dest':'markers','default':False,'help':"include markers (HUGE FILE)"})
LINES = (("--lines",),{'action':'store_true','dest':'lines','default':False,'help':"include lines (HUGE FILE)"})
HOST = (("--host",),{'type':str,'dest':'host','default':'localhost','help':"hostname (default: localhost)",'metavar':'HOST'})
PORT = (("--port",),{'type':int,'dest':'port','default':5000, 'help':"port number (default: 5000)",'metavar':'PORT'})
PREFIX = (("--prefix",),{'type':str,'dest':'prefix','default':'','help':"URI prefix (default: '')",'metavar':'PREFIX'})

CONFIG = [
    ("nx",{'help':"count total length of edges in NX graph",'args':[HOST,PORT,PREFIX,LINES,MARKERS,GRAPH,HTML]})
]

def render_nx(file_name_in,file_name_out,markers=False,lines=False,host="localhost",port=5000,prefix=""):
    from limic.util import start, end, status, file_size, load_pickled
    from folium import Map, Marker, Icon, PolyLine
    from folium.plugins import BeautifyIcon
    from binascii import hexlify
    from pathlib import Path
    from math import log2
    start("Loading NX graph",file_name_in)
    g = load_pickled(file_name_in)
    end()
    start("Rendering graph")
    min_lat = min_long = float('inf')
    max_lat = max_long = -float('inf')
    for n in g.nodes():
        if n[1] < min_lat: min_lat = n[1]
        if n[2] < min_long: min_long = n[2]
        if n[1] > max_lat: max_lat = n[1]
        if n[2] > max_long: max_long = n[2]
    m = Map()
    m.fit_bounds([(min_lat,min_long),(max_lat,max_long)])
    if markers:
        for n in g.nodes():
            Marker(n[1:3],icon=BeautifyIcon(icon='none',                                       iconStyle="opacity: 0.1;",borderColor='#7f7f00',backgroundColor='#ffff00'),
               tooltip=("id: %d" % n[0])).add_to(m)
    if lines:
        for u,v,weight in g.edges.data('weight'):
            PolyLine([u[1:3],v[1:3]],color="#3f3f00",opacity=0.4,weight=6,tooltip=("weight: %.1f" % weight)).add_to(m)
    from branca.element import MacroElement, Template
    class LatLngListener(MacroElement):
        _template = Template(u"""
            {%% macro header(this, kwargs) %%}
                <link rel="stylesheet" href="https://rawcdn.githack.com/marslan390/BeautifyMarker/master/leaflet-beautify-marker-icon.css"/>
    <script src="https://rawcdn.githack.com/marslan390/BeautifyMarker/master/leaflet-beautify-marker-icon.js"></script>
            {%% endmacro %%}
            {%% macro script(this, kwargs) %%}
                function rgb2hex(rgb) {
                    return "#" + ((1 << 24) + (rgb[0] << 16) + (rgb[1] << 8) + rgb[2]).toString(16).slice(1);
                }
                const zip = (arr1, arr2) => arr1.map((k, i) => [k, arr2[i]]);
                var source;
                var target;
                var paths = [];
                var markers = [];
                var timer = 0;
                var delay = 200;
                var prevent = false;
                source_color = [63,255,63]
                target_color = [63,63,255]
                diff_color = target_color.map(function (x,i) {return x-source_color[i];})
                var source_icon = new L.BeautifyIcon.icon({"backgroundColor": rgb2hex(source_color), "borderColor": rgb2hex(source_color.map(function (x) {return Math.trunc(x/2);})), "borderWidth": 3, "icon": "flash", "iconStyle": "opacity:0.8", "innerIconStyle": "", "isAlphaNumericIcon": false, "spin": false, "textColor": "#000"});
                var target_icon = new L.BeautifyIcon.icon({"backgroundColor": rgb2hex(target_color), "borderColor": rgb2hex(target_color.map(function (x) {return Math.trunc(x/2);})), "borderWidth": 3, "icon": "flash", "iconStyle": "opacity:0.8", "innerIconStyle": "", "isAlphaNumericIcon": false, "spin": false, "textColor": "#000"});                            
                function latLngListener(e) {
                    $.getJSON( "http://%s:%d%s/tower",{'lat':e.latlng.lat,'lng':e.latlng.lng})
                    .done(function(data) {
                        if (e.originalEvent.detail > 1) {
                            return;
                        }
                        var marker = L.marker([data.tower[1],data.tower[2]],{}).addTo({{this._parent.get_name()}});
                        if (source == undefined) {
                            source = marker;
                            source.setIcon(source_icon);
                        } else if (target == undefined) {
                            target = marker;
                            target.setIcon(target_icon);
                        } else {
                            {{this._parent.get_name()}}.removeLayer(source);
                            for (path of paths) {
                                {{this._parent.get_name()}}.removeLayer(path);
                            }
                            for (mark of markers) {
                                {{this._parent.get_name()}}.removeLayer(mark);
                            }
                            source = target;
                            target = marker;
                            source.setIcon(source_icon);
                            target.setIcon(target_icon);
                        }
                        if (source != undefined && target != undefined) {
                            $.getJSON( "http://%s:%d%s/route",{'source[lat]':source.getLatLng().lat,'source[lng]':source.getLatLng().lng,
                            'target[lat]':target.getLatLng().lat,'target[lng]':target.getLatLng().lng})
                            .done(function (data) {
                                var latlon = data.path[1].map(function (x) {return [x[4],x[5]];});
                                {{this._parent.get_name()}}.fitBounds(L.polyline(latlon,{}).getBounds());
                                var cost = data.path[1].map(function (x) {return x[0];});
                                var dist = data.path[1].map(function (x) {return x[1];});
                                var air = data.path[1].map(function (x) {return x[2];});
                                var id = data.path[1].map(function (x) {return x[3];});
                                var i;
                                {{this._parent.get_name()}}.removeLayer(source);
                                {{this._parent.get_name()}}.removeLayer(target);
                                source = L.marker(source.getLatLng(),{title:`id: ${id[0]}, cost: ${cost[0]}, dist: ${dist[0]}, air: ${air[0]}, latlon: ${latlon[0]}`}).addTo({{this._parent.get_name()}});
                                target = L.marker(target.getLatLng(),{title:`id: ${id[latlon.length-1]}, cost: ${cost[latlon.length-1]}, dist: ${dist[latlon.length-1]}, air: ${air[latlon.length-1]}, latlon: ${latlon[latlon.length-1]}`}).addTo({{this._parent.get_name()}});
                                if (air[1]) {
                                    source.setIcon(new L.BeautifyIcon.icon({"backgroundColor": rgb2hex(source_color), "borderColor": "#7f1f1f", "borderWidth": 3, "icon": "plane", "iconStyle": "opacity: 0.8;", "innerIconStyle": "", "isAlphaNumericIcon": false, "spin": false, "textColor": "#000"}));
                                    source.update();
                                } else {
                                    source.setIcon(source_icon);
                                }
                                if (air[air.length-1]) {
                                    target.setIcon(new L.BeautifyIcon.icon({"backgroundColor": rgb2hex(target_color), "borderColor": "#7f1f1f", "borderWidth": 3, "icon": "plane", "iconStyle": "opacity: 0.8;", "innerIconStyle": "", "isAlphaNumericIcon": false, "spin": false, "textColor": "#000"}));
                                } else {
                                    target.setIcon(target_icon);
                                }
                                for (i = 0; i+1 < latlon.length; i++) {
                                    bgcolor = source_color.map(function (x,j) {return Math.trunc(x+parseFloat(i)*diff_color[j]/latlon.length);});
                                    bordercolor = rgb2hex(bgcolor.map(function (x) {return Math.trunc(x/2);}));
                                    bgcolor = rgb2hex(bgcolor);
                                    if (i > 0) {
                                        marker = L.marker(latlon[i],{title:`id: ${id[i]}, cost: ${cost[i]}, dist: ${dist[i]}, air: ${air[i]}, latlon: ${latlon[i]}`}).addTo({{this._parent.get_name()}});
                                        markers.push(marker);
                                        if (air[i]||air[i+1]) {
                                            marker.setIcon(new L.BeautifyIcon.icon({"backgroundColor": bgcolor, "borderColor": "#ff1f1f", "borderWidth": 3, "icon": "plane", "iconStyle": "opacity: 0.8;", "innerIconStyle": "", "isAlphaNumericIcon": false, "spin": false, "textColor": "#000"}));
                                        } else if (id[i] < 0) {
                                            marker.setIcon(new L.BeautifyIcon.icon({"backgroundColor": bgcolor, "borderColor": "#ff1f1f", "borderWidth": 3, "icon": "times", "iconStyle": "opacity: 0.8;", "innerIconStyle": "", "isAlphaNumericIcon": false, "spin": false, "textColor": "#000"}));
                                        } else {
                                            marker.setIcon(new L.BeautifyIcon.icon({"backgroundColor": bgcolor, "borderColor": bordercolor, "borderWidth": 3, "icon": "none", "iconStyle": "opacity: 0.1;", "innerIconStyle": "", "isAlphaNumericIcon": false, "spin": false, "textColor": "#000"}));
                                        }
                                    }
                                    if (data.path[0] != undefined) {
                                        paths.push(L.polyline([latlon[i],latlon[i+1]],{color:(air[i+1]?'#ff3f3f' :bgcolor),opacity:0.5,weight:6}).addTo({{this._parent.get_name()}}));
                                    }
                                }
                            })
                            .fail(function () {
                                alert('error');
                            });
                        }
                    })
                    .fail(function(jqxhr,textStatus,error) {
                        alert(error);
                    });
                }
                {{this._parent.get_name()}}.on('dblclick', function() {
                    prevent = true;
                    clearTimeout(timer);
                })
                .on('click', function(e) {
                    time = setTimeout(function() {
                        if (!prevent) {
                            latLngListener(e);
                        }
                        prevent = false;
                    }, delay);  
                })
                .on('contextmenu', function(e) {
                    if (source == undefined) {
                    } else if (target == undefined) {
                        {{this._parent.get_name()}}.removeLayer(source);
                        source = undefined;
                    } else {
                        {{this._parent.get_name()}}.removeLayer(target);
                        for (path of paths) {
                            {{this._parent.get_name()}}.removeLayer(path);
                        }
                        for (mark of markers) {
                            {{this._parent.get_name()}}.removeLayer(mark);
                        }
                        target = undefined;
                    }
                });

            {%% endmacro %%}
        """ % ((host,port,prefix)*2))
        def __init__(self):
            super(MacroElement, self).__init__()
            self._name = 'LatLngListener'
    LatLngListener().add_to(m)
    end()
    start("Saving result to HTML file",file_name_out)
    m.save(file_name_out)
    end('')
    file_size(file_name_out)
    return g
