def Config():
    config = {
                "read_nc_path" : r"F:\RegCM4.7_5km\mpi\indices", # path of NC file use to create Json data
                "output_json_path" : r"F:\Gen_data", # path data json output 
                "read_txt_path": r"F:\RegCM4.7_5km\mpi\indices", # path of txt file use to create NC data
                # "lat_lon_path": r"C:\Users\s6201\Downloads\Data_Project\lonlat_rcm_sea.txt", # paht of lat,lon file use to create NC data
                "lat_lon_path": r"C:\Users\s6201\OneDrive\เอกสาร\lonlat_rcm_5km.csv", # paht of lat,lon file use to create NC data
                "output_nc_paht": r"F:\New_data" # path data NC output
            }
    return config

# "raw_data_path" : r"E:\Data_Project\PrepareData\data_project", # path of NC file
# "output_path" : r"E:\Data_Project\PrepareData\Gen_data", # path of data json
# "data_index_path" : r"E:\Data_Project\PrepareData\Gen_data\ecearth" # path for api 