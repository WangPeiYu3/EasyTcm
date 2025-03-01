from a_med_stand import read_excel_to_dict_list,save_dict_list_to_excel

def connect_columns(file_path,column_name1,column_name2,new_column_name,new_file_path):
    # read excel file to a dictionary list
    data_dict_list = read_excel_to_dict_list(file_path)

    # connect two columns and create a new column
    for data_dict in data_dict_list:
        if str(data_dict[column_name1]) == 'nan':
            data_dict[new_column_name] = data_dict[column_name2]
        if str(data_dict[column_name2]) == 'nan':
            data_dict[new_column_name] = data_dict[column_name1]
        if str(data_dict[column_name1])!= 'nan' and str(data_dict[column_name2])!= 'nan':
            data_dict[new_column_name] = data_dict[column_name1] + data_dict[column_name2]
        if str(data_dict[column_name1]) == 'nan' and str(data_dict[column_name2]) == 'nan':
            data_dict[new_column_name] = ''

    # save the updated dictionary list to a new excel file
    save_dict_list_to_excel(data_dict_list,new_file_path)

if __name__ == '__main__':
    a = []
    b = ['b1','b2','b3']
    c = a + b
    print(c)