import geopandas
myshpfile = geopandas.read_file(r"F:\worldregions\worldregions.shp")
myshpfile.to_file('southeast-asia1.json', driver='GeoJSON')