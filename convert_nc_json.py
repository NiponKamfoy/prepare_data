from cmath import sin
import datetime, math, calendar, json
from netCDF4 import Dataset
from shapely.geometry import Point, MultiPolygon
from shapely.geometry.polygon import Polygon
from datetime import date, timedelta, datetime
# import sys
# # C:\Users\Administrator\Desktop\Project_I\flask_api
# # D:\Project\Mix_Project\Project_I\flask_api
# sys.path.insert(0, r"D:\Project\Mix_Project\Project_I\flask_api")
from get_province import GettingArea
shp_instance = GettingArea()

index_n = ""
data_index = []
def get_data(index, location_index, index_type):
    global data_index, index_n
    # if use same data with the last call don't want to read NC data 
    if (index_n == "" or index_n != index):
        index_n = index
        data_index = Dataset(rf"{data_path}\{index}.nc")
        
    time = data_index.variables['time']
    unit_nc = time.units.split(' ')[0].strip()
    if (unit_nc == "month"):
        variable_name = index.split("_")[-1]
        date_format = "%Y-%m"
    else :
        date_format = "%Y"
        variable_name = index.split("_")[-1]
        if(index.split("_")[-2] == "spi"):
            date_format = "%Y-%m"
            unit_nc = 'month'

    values = data_index.variables[variable_name]
    temp = values[0,65,72]
    lat = data_index.variables['lat'][:]
    lon = data_index.variables['lon'][:]
    t1 = lat[72]
    l = lon[63]

     # "days since 1900-1-1"
    start_nc = time.units.split('since')[1].strip() # "days since 1900-1-1"
    date_start = datetime.strptime(start_nc, date_format)
    return [values, lat, lon, date_start, time, date_format, unit_nc]

def convert_nc_json(province, index, location_index, index_type):
    global str_date

    # get data from NC file by location
    data_index = get_data(index, location_index, index_type)
    values = data_index[0]
    lat = data_index[1]
    lon = data_index[2]
    date_start = data_index[3]
    time = data_index[4]
    date_format = data_index[5]
    time_unit = data_index[6]

    
    # get data of shapefile 
    shp = shp_instance.GetProvince(province) 

    # create polygon of province from shapefile for each province
    if(shp["features"][0]['geometry']['type'] == 'Polygon' ):
        polygon_province = Polygon(shp['features'][0]['geometry']['coordinates'][0])
    else :
        see_coordinates = shp['features'][0]['geometry']['coordinates']
        list_polygon = []
        for polygon in shp['features'][0]['geometry']['coordinates']:
            #if province == 'all' must use polygon not polygon[0]
            list_polygon.append(Polygon(polygon[0]))
        polygon_province = MultiPolygon(list_polygon)

    data_form = {
        "type": "FeaturesCollection",
        "properties": {
                        "date_type": time_unit,
                        "start_time": date_start.strftime(date_format),
                    },
        "fetures": []
    }

    count = 0
    #loop for check each point which intersect in polygon province 
    for ind_lat,lat_nc in enumerate(lat):
        for ind_lon,lon_nc in enumerate(lon):
            value = {}
            
            #create polygon of grid cell for check intersection with shapefile 
            #create by calculate distance grid by grid 
            # try :
            #     diff_lon_f = lon[ind_lon+1] - lon_nc 
            #     diff_lon_b = lon_nc - lon[ind_lon-1]
            #     diff_lat_t = lat[ind_lat+1] - lat_nc
            #     diff_lon_u = lat_nc - lat[ind_lat-1]
            #     dif_f = lat[ind_lat+1] - lat_nc
            #     if (ind_lat != 0):
            #         dif_b = lat_nc - lat[ind_lat-1]
            #     dif_t = lon[ind_lon+1] - lon_nc
            #     if (ind_lon != 0):
            #         dif_u = lon_nc - lon[ind_lon-1]
                
            #     grid_cell = [
            #                     # [lon_nc + diff_lon_f, lat_nc - diff_lon_u],
            #                     # [lon_nc + diff_lon_f, lat_nc + diff_lat_t],
            #                     # [lon_nc - diff_lon_b, lat_nc + diff_lat_t],
            #                     # [lon_nc - diff_lon_b, lat_nc - diff_lon_u],
            #                     # [lon_nc + diff_lon_f, lat_nc - diff_lon_u] 
                            
            #                     # [lat_nc + dif_f, lon_nc + dif_t],
            #                     # [lat_nc - dif_b, lon_nc + dif_t],
            #                     # [lat_nc - dif_b, lon_nc - dif_u],
            #                     # [lat_nc + dif_f, lon_nc - dif_u],
            #                     # [lat_nc + dif_f, lon_nc + dif_t] 

            #                     [lon_nc + dif_t,lat_nc + dif_f],
            #                     [lon_nc + dif_t,lat_nc - dif_b],
            #                     [lon_nc - dif_u,lat_nc - dif_b],
            #                     [lon_nc - dif_u,lat_nc + dif_f],
            #                     [lon_nc + dif_t,lat_nc + dif_f] 
            #                 ]
            # except:
            #     print("grid except",lon_nc, ',', lat_nc)
            #     grid_cell = [
            #                 [lon_nc - diff_lon, lat_nc - diff_lat],
            #                 [lon_nc + diff_lon, lat_nc - diff_lat],
            #                 [lon_nc + diff_lon, lat_nc + diff_lat],
            #                 [lon_nc - diff_lon, lat_nc + diff_lat],
            #                 [lon_nc - diff_lon, lat_nc - diff_lat] 
            #             ]
            
            if(ind_lat != 0 and ind_lon !=0):
                diff_lat = (lat[ind_lat]-lat[ind_lat-1])/2  
                diff_lon = (lon[ind_lon]-lon[ind_lon-1])/2  
                grid_cell = [
                                [lon_nc - diff_lon, lat_nc - diff_lat],
                                [lon_nc + diff_lon, lat_nc - diff_lat],
                                [lon_nc + diff_lon, lat_nc + diff_lat],
                                [lon_nc - diff_lon, lat_nc + diff_lat],
                                [lon_nc - diff_lon, lat_nc - diff_lat] 
                            ]
            else :
                diff_lat = (lat[1]-lat[0])/2  
                diff_lon = (lon[1]-lon[0])/2  
                grid_cell = [
                                [lon_nc - diff_lon, lat_nc - diff_lat],
                                [lon_nc + diff_lon, lat_nc - diff_lat],
                                [lon_nc + diff_lon, lat_nc + diff_lat],
                                [lon_nc - diff_lon, lat_nc + diff_lat],
                                [lon_nc - diff_lon, lat_nc - diff_lat] 
                            ]

            polygon_grid = Polygon(grid_cell)
            
            # check intersection with shapely module 
            if(polygon_province.intersects(polygon_grid)):
                print("grid intersect",lon_nc, ',', lat_nc)
                count += 1
                # insert pairs of values of index and index of date  
                for i, date_index in enumerate(time[:]):
                    temp = values[i, ind_lat, ind_lon]
                    value[i] = "{:.3f}".format(temp)

                intersect = polygon_province.intersection(polygon_grid)  

                # format coordinate to form of geojson 
                list_coordinates = []
                if(intersect.geom_type == 'Polygon'):
                    for i in list(intersect.exterior.coords):
                        list_coordinates.append(list(i))
                elif (intersect.geom_type == 'MultiPolygon'):
                    polygons = list(intersect.geoms) # use .geoms for fixed "Multipolygon" can't iteration
                    for poly in polygons:
                        tmp = []
                        for i in list(poly.exterior.coords):
                            tmp.append(list(i))
                        list_coordinates.append(tmp)

                grid ={
                    "type":"Feature",
                    "properties": {
                        "grid_id": count,
                        "time_index": value
                    },
                    "geometry":{
                        "type": intersect.geom_type,
                        "coordinates":[
                            list_coordinates
                        ]
                    }
                }
                data_form["fetures"].append(grid)
    return data_form

province_load = open(r'province.json', encoding='utf-8')
SEA_load = open(r"southeast_asia.json", encoding='utf-8')
data_province = json.load(province_load)
data_SEA = json.load(SEA_load)
# load_config = open(r"D:\Project\Mix_Project\Project_I\flask_api\config.json")
# config = json.load(f_load)
import os
from config import Config

#get name of index in folder
config_data = Config() 
folder_data = config_data['read_nc_path']
output_path = config_data['output_json_path'] # path of output  output_path
dir_list2 = os.listdir(folder_data)

### create file each province
for grid_size in dir_list2:
    folder_grid_size = rf"{folder_data}\{grid_size}" # path of data 
    dir_list3 = os.listdir(folder_grid_size)
    for data_provider in dir_list3:
        folder_data_provider= rf"{folder_data}\{grid_size}\{data_provider}" # path of data 
        dir_list4 = os.listdir(folder_data_provider)
        for index_name in dir_list4:
            data_path = rf"{folder_data}\{grid_size}\{data_provider}\{index_name}" # path of data 
            location_index = data_path.split('\\')[-2]
            index_type = data_path.split('\\')[-1]
            dir_list = os.listdir(data_path)

            try:
                os.mkdir(f"{output_path}\{location_index}\{index_type}")
            except:
                pass

            for folder_name in dir_list:
                print(folder_name)
                if(folder_name != 'monthly'):
                    name_index = folder_name.split('.')[0].split('_')
                    name_subfolder = folder_name.split('.')[0] # mpi_hist_spi_m3 
                    dir_old_data = []
                    try:
                        if(not os.path.exists(f"{output_path}\{location_index}")):
                            os.mkdir(f"{output_path}\{location_index}")
                        if(not os.path.exists(f"{output_path}\{location_index}\{index_type}")):
                            os.mkdir(f"{output_path}\{location_index}\{index_type}")
                        if(not os.path.exists(f"{output_path}\{location_index}\{index_type}\{name_subfolder}")):
                            os.mkdir(f"{output_path}\{location_index}\{index_type}\{name_subfolder}")
                        # os.mkdir(f"{output_path}\{location_index}\{index_type}\{name_subfolder}") 
                    except:
                        if(not os.path.exists(f"{output_path}\{location_index}")):
                            os.mkdir(f"{output_path}\{location_index}")
                        if(not os.path.exists(f"{output_path}\{location_index}\{index_type}")):
                            os.mkdir(f"{output_path}\{location_index}\{index_type}")
                        if(not os.path.exists(f"{output_path}\{location_index}\{index_type}\{name_subfolder}")):
                            os.mkdir(f"{output_path}\{location_index}\{index_type}\{name_subfolder}")
                        old_data = os.listdir(f"{output_path}\{location_index}\{index_type}\{name_subfolder}")
                        for i in old_data:
                            temp = i.split(".")[0] 
                            dir_old_data.append(temp)

                    num_pro = 1
                    for i in data_province['features']:
                        name_province = i['properties']['name']
                        print("province: ",num_pro,"/",len(data_province['features']))
                        num_pro += 1
                        if(name_province not in dir_old_data):
                            data_json = convert_nc_json(name_province, name_subfolder, location_index, index_type)
                            json_object = json.dumps(data_json, indent=4)
                            # Writing to sample.json  , 'cdd_era', 'spei'
                            with open(f"{output_path}\{location_index}\{index_type}\{name_subfolder}\{name_province}.json", "w") as outfile:
                                outfile.write(json_object)
                    num_country = 1
                    for i in data_SEA['features']:
                        contry_name = i['properties']['name']
                        c_name = contry_name.split(' ')[0]
                        if(c_name not in dir_old_data):
                            data_json = convert_nc_json(contry_name, name_subfolder, location_index, index_type)
                            json_object = json.dumps(data_json, indent=4)
                            # Writing to sample.json  , 'cdd_era', 'spei'
                            with open(f"{output_path}\{location_index}\{index_type}\{name_subfolder}\{c_name}.json", "w") as outfile:
                                outfile.write(json_object)
                        print("country: ",num_country,"/",len(data_SEA['features']))
                        num_country += 1
                


