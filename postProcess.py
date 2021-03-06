# -*- coding: utf-8 -*-
"""
Created on Tue May 24 10:41:50 2016

@author: dahoiv
"""

# import os
import util

exclude_pid = [1307, 1461]


def process(folder, glioma_grades):
    """ Post process data """
    print(folder)
    util.setup(folder)
    params = ['Index_value', 'Global_index', 'Mobility', 'Selfcare', 'Activity', 'Pain', 'Anxiety', 'karnofsky']
    (image_ids, qol) = util.get_image_id_and_qol(None, exclude_pid, glioma_grades=glioma_grades)
    print(len(image_ids))
    result = util.post_calculations(image_ids)
    print(len(result['all']))
    util.avg_calculation(result['all'], 'all', None, True, folder, save_sum=True)
    util.avg_calculation(result['img'], 'img', None, True, folder)

    # (image_ids, qol) = util.get_image_id_and_qol('Index_value', exclude_pid, glioma_grades=glioma_grades)
    # result = util.post_calculations(image_ids)
    # util.calculate_t_test(result['all'], 1)

    for qol_param in params:
        (image_ids, qol) = util.get_image_id_and_qol(qol_param, exclude_pid)
        if not qol_param == "karnofsky":
            qol = [_temp * 100 for _temp in qol]
        if not qol_param == "Index_value":
            default_value = -100
        else:
            default_value = 0
        print(image_ids)
        result = util.post_calculations(image_ids)
        for label in result:
            print(label)
            if label == 'img':
                continue
            util.avg_calculation(result[label], label + '_' + qol_param, qol, True, folder, default_value=default_value)
            util.std_calculation(result[label], label + '_' + qol_param, qol, True, folder)


def process_vlsm(folder, glioma_grades):
    """ Post process vlsm data """
    print(folder)
    util.setup(folder)
    params = ['Index_value', 'Mobility', 'Selfcare', 'Activity', 'Pain', 'Anxiety', 'karnofsky']
    stat_func = [util.brunner_munzel_test, [util.mannwhitneyu_test]*6]
    for (qol_param, stat_func_i) in zip(params, stat_func):
        (image_ids, qol) = util.get_image_id_and_qol(qol_param, exclude_pid)
        print(image_ids)
        result = util.post_calculations(image_ids)
        for label in result:
            print(label)
            if label == 'img':
                continue
            util.vlsm(result[label], label + '_' + qol_param, stat_func_i, qol, folder, n_permutations=100)


if __name__ == "__main__":
    import datetime
#    folder = "RES_1/"
#    glioma_grades = [2, 3, 4]
#    start_time = datetime.datetime.now()
#    process_vlsm(folder, glioma_grades)
#    print("Total runtime")
#    print(datetime.datetime.now() - start_time)
#
#    folder = "RES_2/"
#    glioma_grades = [4]
#    process(folder, glioma_grades)
#    process_vlsm(folder, glioma_grades)

    folder = "RES/"
    glioma_grades = [3, 4]
    process(folder, glioma_grades)
    start_time = datetime.datetime.now()
    process_vlsm(folder, glioma_grades)
    print("Total runtime")
    print(datetime.datetime.now() - start_time)
