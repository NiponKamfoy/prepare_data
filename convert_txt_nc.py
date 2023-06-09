from config import Config
import csv
config_path = Config()

def get_data_index(folder_name, pairs_lat_lon):
    data_index = open(folder_name, "r")
    index_formated = []
    

    #cut last index because last index is empty string ''
    data_index_split = data_index.read().split('\n')[:-1] 

    temp3 = len(data_index_split[0].split('\t'))
    temp2 = data_index_split[0].split('\t')

    # if txt data have date frequency is year data_split_t index will have 
    # 191(lat) x 253(lon) = 28323 values + 1 year = 48324 index 
    # but if it have date frequency is month data_split_t will have 28324 + 1 month = 48325 index

    # use for set unit of time for NC file
    # check! Is date frequency is monthly? and set date start for nc data
    num_data =  len(data_index_split)
    num_data_year = 129
    if(num_data == num_data_year):
        date_start = data_index_split[0].split("\t")[0] 
        date_end = data_index_split[-1].split("\t")[0]
    else:
        date_start = data_index_split[0].split("\t")[0] + "-" + data_index_split[0].split("\t")[1]
        date_end = data_index_split[-1].split("\t")[0] + "-" + data_index_split[-1].split("\t")[1]
    
    date_list = []
    month = 0
    for i in range(len(data_index_split)):
        print("get txt data : "+ str(i+1) + "/" + str(len(data_index_split)))
        data_split_t = data_index_split[i].split('\t')
        date_list.append(float(month))
        temp = []
        temp1  = len(data_split_t)
        if(len(data_split_t) != 48325):
            #loop data which split with \t begin index = 1 cause index 0 is date data
            for i in range(1, len(data_split_t)):
                if(data_split_t[i] == 'NA' or data_split_t[i] == '' or data_split_t[i] == ' '):
                    temp.append(0)
                else:
                    temp.append(float(data_split_t[i]))
        else :
            #loop data which split with \t begin index = 2 cause index 0 is year data and index 1 is month data
            for i in range(2, len(data_split_t)):
                if(data_split_t[i] == 'NA' or data_split_t[i] == '' or data_split_t[i] == ' '):
                    temp.append('NA')
                else:
                    temp.append(float(data_split_t[i]))
        index_formated.append(temp)
        month += 1
    data_index.close()
    return [index_formated, date_list, date_start, date_end]

# get data lat, lon from file 
def get_data_latlon():
    
    data_lat = []
    data_lon = []

    type_data = config_path['lat_lon_path'][-3:]
    if(type_data == 'txt'):
        data_lonlat = open(config_path['lat_lon_path'], "r")
        data_lonlat_split = data_lonlat.read().split('\n')[:-1]
        for i in range(len(data_lonlat_split)):
            lon_lat = [float(j) for j in data_lonlat_split[i].split('\t')]
            data_lon.append(lon_lat[0])
            data_lat.append(lon_lat[1])
    elif(type_data == 'csv'):
        data_lonlat = open(config_path['lat_lon_path'], "r")
        data_lonlat_split = list(csv.reader(data_lonlat, delimiter=","))
        first = True
        for i in data_lonlat_split:
            if (first):
                first = False
                continue
            data_lon.append(i[0])
            data_lat.append(i[1])
    

    
    lonlat_formated = [data_lat, data_lon]
    return lonlat_formated


def get_index_latlon_thai(data_lat, data_lon):
    list_index = []
    list_lat = []
    list_lon = []
    for i in range(len(data_lat)):
        # this use to crop data for over thailand
        # if (data_lat[i] >= 96.5 and data_lat[i] <= 106.5 and data_lon[i] >=5.2 and data_lon[i] <= 21.5):  
        list_index.append(i)
        list_lat.append(data_lat[i])
        list_lon.append(data_lon[i])
    return [list_index, list_lat, list_lon]




import netCDF4 as nc
import os

path = config_path['read_txt_path']
output_path = config_path["output_nc_paht"]
type_model = path.split('\\')[-3]
location_index = path.split('\\')[-2]
index_type = path.split('\\')[-1]
dir_list = os.listdir(path)

for folder_name in dir_list:
    if(folder_name[0] != '.'):
        if(folder_name != 'monthly'):
            # set output directory path
            fn = rf"{output_path}\{type_model}\{location_index}\{index_type}\{folder_name[:-4]}.nc"
            # create folder when doesn't exist
            if(not os.path.exists(f"{output_path}\{type_model}")):
                os.mkdir(f"{output_path}\{type_model}")
            if(not os.path.exists(f"{output_path}\{type_model}\{location_index}")):
                os.mkdir(f"{output_path}\{type_model}\{location_index}")
            if(not os.path.exists(f"{output_path}\{type_model}\{location_index}\{index_type}")):
                os.mkdir(f"{output_path}\{type_model}\{location_index}\{index_type}")

            # create NC file 
            ds = nc.Dataset(fn, 'w', format='NETCDF4')

            # get data from txt file 
            data_latlon = get_data_latlon()
            data_index = get_data_index(path+"\\"+ folder_name, len(data_latlon[0]))

            # get data for nc file 
            num_year_index = len(data_index[1])
            num_pairs_lonlat = len(data_latlon[0])

            #check if data index and data lat lon not support for create nc file
            if (len(data_index[0][0]) != len(data_latlon[0])):
                print("lat lon data not macth with index data!!!!")
                print("number of data : ", len(data_index[0][0]))
                print("number of lat, lon pairs : ", len(data_latlon[0]))
                exit()
                
            data_lat = list(dict.fromkeys(data_latlon[0]))
            data_lon = list(dict.fromkeys(data_latlon[1]))

            time = ds.createDimension('time', num_year_index)
            lat = ds.createDimension('lat', len(data_lat))
            lon = ds.createDimension('lon', len(data_lon))

            times = ds.createVariable('time', 'f4', ('time',))
            if (len(data_index[1]) == 129):
                times.units = 'year since ' + data_index[2]
            else :
                times.units = 'month since ' + data_index[2]
            lats = ds.createVariable('lat', 'f4', ('lat',))
            lons = ds.createVariable('lon', 'f4', ('lon',))
            name_index = folder_name.split('.')[0].split('_')
            value = ds.createVariable(name_index[-1], 'f4', ('time', 'lat', 'lon',))
            value.units = ""

            times[:] = data_index[1]
            lats[:] = data_lat
            lons[:] = data_lon
            print(index_type +"\\"+ folder_name)
            print(num_year_index)
            for i in range(num_year_index):
                t11 = data_index[0][i]
                value[i, :, :] = data_index[0][i]
                print(i)


            ds.close()
        else :
            dir_list_monthly = os.listdir(path+"\\monthly")
            for folder_name_monthly in dir_list_monthly:
                # set output directory path
                fn = rf"C:\Users\s6201\Downloads\Data_Project\data_project\{location_index}\{index_type}\monthly\{folder_name_monthly[:-4]}.nc"
                ds = nc.Dataset(fn, 'w', format='NETCDF4')

                # get data from txt file 
                data_latlon = get_data_latlon()
                data_index = get_data_index(path+"\\monthly\\"+ folder_name_monthly)

                # set data for nc file 
                num_year_index = len(data_index[1])
                num_pairs_lonlat = len(data_latlon[0])

                data_lat = list(dict.fromkeys(data_latlon[0]))
                data_lon = list(dict.fromkeys(data_latlon[1]))

                time = ds.createDimension('time', num_year_index)
                lat = ds.createDimension('lat', len(data_lat))
                lon = ds.createDimension('lon', len(data_lon))

                times = ds.createVariable('time', 'f4', ('time',))
                times.units = 'month since ' + data_index[2] 
                lats = ds.createVariable('lat', 'f4', ('lat',))
                lons = ds.createVariable('lon', 'f4', ('lon',))
                name_index = folder_name_monthly.split('.')[0].split('_')
                value = ds.createVariable(name_index[-2], 'f4', ('time', 'lat', 'lon',))
                value.units = ""

                times[:] = data_index[1]
                lats[:] = data_lat
                lons[:] = data_lon
                print(index_type +"\\"+ folder_name_monthly)
                print(num_year_index)
                for i in range(num_year_index):
                    value[i, :, :] = data_index[0][i]
                    print(i)
                ds.close()