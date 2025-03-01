from a_med_stand import read_excel_to_dict_list, save_dict_list_to_excel, medicine_stand
import os
from b_translate_feature import translate_feature, translate_feature_v2
from c_create_rect import creat_rect, extract_high_freq_columns
from d_statics import count_ones_in_columns, get_high_times, get_top_items
from d_connect_times import calculate_and_save_connect_similarities
from _baselib import modify_file_name, move_xlsx_to_result_folder, split_path_os


def dm1(src_file='data/test_for_main2.xlsx'):
    # config
    dst_folder, filename = split_path_os(src_file)

    try:

        print('folder:', dst_folder, 'filename:', filename)
        min_med = 1
        max_med = 30
        do_med_stand = False
        high_row = 20

        # step1 药物标准化
        step1_file = 'step1.药物标准化后.xlsx'
        if do_med_stand:
            medicine_stand(src_file, step1_file, min_num=min_med, max_num=max_med)
        if not os.path.exists(step1_file):
            medicine_stand(src_file, step1_file, min_num=min_med, max_num=max_med)

        print('------------step1 finished------------')

        # stepX 证型标准化、症状标准化等
        # dst_file = 'StepX.证型标准化后.xlsx'

        # step2 四气、五味、归经、治法属性转换
        step2_file = 'step2.四气、五味、归经、治法属性转换.xlsx'
        translate_feature_v2(step1_file, step2_file)
        print('------------step2 finished------------')

        # step3 药物矩阵生成
        col_names = ['处方S']
        step3_1_file = 'step3.1药物矩阵_10.xlsx'
        step3_2_file = 'step3.2药物矩阵_YN.xlsx'
        step3_3_file = 'step3.3药物矩阵_类型.xlsx'
        creat_rect(step1_file, col_names, step3_1_file, step3_2_file, step3_3_file)

        col_names = ['症状']
        step3_1_file = 'step3.1症状矩阵_10.xlsx'
        step3_2_file = 'step3.2症状矩阵_YN.xlsx'
        step3_3_file = 'step3.3症状矩阵_类型.xlsx'
        creat_rect(step1_file, col_names, step3_1_file, step3_2_file, step3_3_file)

        print('------------step3 finished-')

        # step4 转换矩阵生成
        col_names = ['四气', '五味', '归经', '治法']
        step4_1_file = 'step4.1统计_10.xlsx'
        step4_2_file = 'step4.2统计_YN.xlsx'
        step4_3_file = 'step4.3统计.xlsx'
        creat_rect(step2_file, col_names, step4_1_file, step4_2_file, step4_3_file)
        modify_file_name(directory='./', prefix='step2.四气、五味、归经、治法属性转换_', replace_prefix='step4.统计矩阵_')
        print('------------step4 finished-')

        # step5 药物、性味归经、治法统计
        count_ones_in_columns('step4.统计矩阵_四气_10矩阵.xlsx', 'step5.四气统计.xlsx')
        count_ones_in_columns('step4.统计矩阵_五味_10矩阵.xlsx', 'step5.五味统计.xlsx')
        count_ones_in_columns('step4.统计矩阵_归经_10矩阵.xlsx', 'step5.归经统计.xlsx')
        count_ones_in_columns('step4.统计矩阵_治法_10矩阵.xlsx', 'step5.治法统计.xlsx')
        count_ones_in_columns('step3.1药物矩阵_10.xlsx', 'step5.药物统计.xlsx')
        count_ones_in_columns('step3.1症状矩阵_10.xlsx', 'step5.症状统计.xlsx')

        calculate_and_save_connect_similarities('step3.1药物矩阵_10.xlsx', 'step6.药物连接度.xlsx')

        get_top_items('step5.药物统计.xlsx', 'step7.高频药物统计.xlsx', high_row - 1)
        get_top_items('step5.治法统计.xlsx', 'step7.高频治法统计.xlsx', high_row - 1)
        get_top_items('step5.症状统计.xlsx', 'step7.高频症状统计.xlsx', high_row - 1)

        extract_high_freq_columns('step3.1药物矩阵_10.xlsx', 'step7.高频药物统计.xlsx', 'step8.高频药物矩阵10.xlsx')
        extract_high_freq_columns('step3.2药物矩阵_YN.xlsx', 'step7.高频药物统计.xlsx', 'step8.高频药物矩阵YN.xlsx')
        extract_high_freq_columns('step4.统计矩阵_治法_10矩阵.xlsx', 'step7.高频治法统计.xlsx','step8.高频治法矩阵10.xlsx')
        extract_high_freq_columns('step4.统计矩阵_治法_YN矩阵.xlsx', 'step7.高频治法统计.xlsx','step8.高频治法矩阵YN.xlsx')
        extract_high_freq_columns('step3.1症状矩阵_10.xlsx', 'step7.高频症状统计.xlsx', 'step8.高频症状矩阵10.xlsx')
        extract_high_freq_columns('step3.2症状矩阵_YN.xlsx', 'step7.高频症状统计.xlsx', 'step8.高频症状矩阵YN.xlsx')

        # 连接高频药物和症状
        from d_connect_rect import connect_rect
        connect_rect('step8.高频药物矩阵10.xlsx','step8.高频症状矩阵10.xlsx','step13.药物-症状连接矩阵10.xlsx')
        connect_rect('step8.高频药物矩阵YN.xlsx','step8.高频症状矩阵YN.xlsx','step13.药物-症状连接矩阵YN.xlsx')
        from d_connect_columns import connect_columns
        connect_columns('step1.药物标准化后.xlsx','症状','处方S','症药', 'step14.药物-症状连接.xlsx')



        from d_cal_rules import calculate_rulues
        calculate_rulues('step1.药物标准化后.xlsx', 'step15.频繁项药物.xlsx', rules_file_path='step15.关联规则.xlsx',
                         min_support=0.05, min_confidence=0.8)
        # calculate_rulues('step14.药物-症状连接.xlsx', 'step15.频繁项症药.xlsx', rules_file_path='step15.关联规则症药.xlsx',
        #                  min_support=0.05, min_confidence=0.8)

        from hcin import draw_rule

        draw_rule('step15.关联规则_for_draw.xlsx', 'step15.关联规则图和弦图.png')
        # draw_rule('step15.关联规则症药_for_draw.xlsx', 'step15.关联规则图和弦图_症药.png')


        # 绘制四气饼图
        from hsqt import generat_pie_sqt

        generat_pie_sqt('step5.四气统计.xlsx', 'step13.四气饼图.png')

        from e_pca import pca_analysis

        pca_analysis('step8.高频药物矩阵10.xlsx', 'step9.药物PCA10.xlsx', 'step9.药物PCA.png',
                     'step9.药物PCA_upset.png',
                     'step9.药物PCA_per.png')

        temp1 = read_excel_to_dict_list('step7.高频药物统计.xlsx')
        high_times = 0
        for t1 in temp1:
            high_times = t1['times']
        from e_complex_network import plot_complex_network

        plot_complex_network('step6.药物连接度.xlsx', 'step7.高频药物统计.xlsx', 'step10.药物复杂网络.png', high_times)

        from e_fluster import class_z_final

        class_z_final('step8.高频药物矩阵10.xlsx', 'step11.聚类结果.xlsx', 'step11.聚类')

        # 绘制高频药物词云图
        from hcyt import generate_wordcloud_from_xlsx

        generate_wordcloud_from_xlsx('step7.高频药物统计.xlsx', 'step12.药物词云.png')
        generate_wordcloud_from_xlsx('step7.高频治法统计.xlsx', 'step12.治法词云.png')
        generate_wordcloud_from_xlsx('step5.症状统计.xlsx', 'step12.症状词云.png')
        # generate_wordcloud_from_xlsx('step5.')

        # 绘制归经雷达图1111111111111

        from hradar import generate_single_radar_chart

        generate_single_radar_chart('step5.五味统计.xlsx', 'step14.五味雷达图.png')
        generate_single_radar_chart('step5.归经统计.xlsx', 'step14.归经雷达图.png')

        from e_fisher import fisher
        src_file = r'step8.高频药物矩阵10.xlsx'
        dst_file = r'step16.显著性药对检验.xlsx'  # 指定输出文件路径
        fisher(src_file, 'step16.显著性药对检验.png', dst_file=dst_file)
        move_xlsx_to_result_folder(dst_folder=dst_folder)

        from _baselib import zip_dir, count_files_in_directory
        count_file = count_files_in_directory("D:\PhpProjects\SinoDigMed\dms")
        zip_dir(dst_folder, f'D:\PhpProjects\SinoDigMed\dms\\{count_file}.zip')
        return count_file

    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    dm1('data/xst.xlsx')
