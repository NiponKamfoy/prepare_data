def Config():
    config = {
        # "F:\data_test", "F:\data_project"
        # "E:\Data_Project\PrepareData\data_project", "E:\Data_Project\PrepareData\Gen_data", "E:\Data_Project\PrepareData\Gen_data\ecearth"
                "raw_data_path" : r"F:\RegCM4.7_5km\mpi\indices", # path of NC file
                "output_path" : r"F:\Gen_data", # path of data json
                "data_index_path" : r"F:\data_project\ecearth", # path for api 
                "lat_lon_path": r"C:\Users\s6201\OneDrive\เดสก์ท็อป\lonlat_rcm_5km.txt"
            }
    return config

# "raw_data_path" : r"E:\Data_Project\PrepareData\data_project", # path of NC file
# "output_path" : r"E:\Data_Project\PrepareData\Gen_data", # path of data json
# "data_index_path" : r"E:\Data_Project\PrepareData\Gen_data\ecearth" # path for api 