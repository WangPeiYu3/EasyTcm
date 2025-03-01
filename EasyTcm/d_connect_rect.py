from a_med_stand import read_excel_to_dict_list, save_dict_list_to_excel


def connect_rect(rect1_file, rect2_file, dst_file):
    rect_list = read_excel_to_dict_list(rect1_file)
    rect2_list = read_excel_to_dict_list(rect2_file)
    dst = []
    for idx in range(len(rect_list)):
        rect1 = rect_list[idx]
        rect2 = rect2_list[idx]
        dict_v = {}
        for key in rect1.keys():
            dict_v[key] = rect1[key]
        for key in rect2.keys():
            dict_v[key] = rect2[key]
        dst.append(dict_v)
    save_dict_list_to_excel(dst, dst_file)
