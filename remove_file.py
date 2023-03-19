import os
temp = []
path = r"F:\Gen_data"
dir_list = os.listdir(path)
removed = ['Singapore.json', 'Brunei.json', 'Thailand.json', 'Indonesia.json', 'Vietnam.json', 'Philippines.json', 'Timor-Leste.json', 'Malaysia.json', 'Cambodia.json', 'Myanmar.json', 'Lao.json']
for i in dir_list:
    path1 = rf"{path}\{i}"
    dir_list1 = os.listdir(path1)
    for j in dir_list1:
        path2 = rf"{path1}\{j}"
        dir_list2 = os.listdir(path2)
        for k in dir_list2:
            path3 = rf"{path2}\{k}"
            dir_list3 = os.listdir(path3)
            for l in dir_list3:
                temp.append(l)
                if (l in removed):
                    os.remove(rf"{path3}\{l}")
                    print(i," : ",j," : ",k," : ",l)