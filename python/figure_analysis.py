# -*- coding: UTF-8 -*-
# AUTHOR NAME: Tsung YiLee
# AUTHOR EMAIL: свит_дрим@yandex.com
import json
from tqdm import trange


def init_gradewordbook_questions_progress():
    '''
    功能：初次统计不同年级题目的分布进度，注意这是初始化，会清空数据！
    '''
    with open('./database/question/gradewordbook_questions.json', 'r', encoding='utf-8') as file:
        gradewordbook_questions_json = json.load(file)
    gradewordbook_questions_distrbution = [0.0] * 12
    gradewordbook_questions_nums = len(gradewordbook_questions_json)
    # 遍历所有的类型题目，统计不同年级不同时期的题目数量
    for i in trange(gradewordbook_questions_nums):
        gradewordbook_questions_info = gradewordbook_questions_json[i]
        gradeperiodrank = gradewordbook_questions_info["gradeperiodrank"]
        gradewordbook_questions_distrbution[gradeperiodrank - 1] += 1.0
    gradewordbook_question_progress = []
    for i in range(0, 12):
        gradewordbook_question_progress.append(
            {
                "gradeperiodrank": i + 1,
                "grade_question_nums": gradewordbook_questions_distrbution[i],
                "grade_dynamic_right_nums": [],
                "grade_dynamic_picked_nums": []
            }
        )
    with open('./database/states/gradewordbook_question_progress.json', 'w', encoding='utf-8') as file:
        json.dump(gradewordbook_question_progress, file, indent=2, ensure_ascii=False)


def analyze_gradewordbook_question_coverage(grade, period, all_mode):
    '''
    功能：统计已经做过的题目占比，注意纯净模式才会触发bingo标志置True
    '''
    with open('./database/question/gradewordbook_question_progress.json', 'r', encoding='utf-8') as file:
        progress_json = json.load(file)
    # 开始计算每个年级的覆盖率
    gradeperiodrank_dict = {
        "一上": 1,
        "一下": 2,
        "二上": 3,
        "二下": 4,
        "三上": 5,
        "三下": 6,
        "四上": 7,
        "四下": 8,
        "五上": 9,
        "五下": 10,
        "六上": 11,
        "六下": 12,
    }
    coverage_list = []
    for progress_info in progress_json:
        # 当前年级累计的正确题数
        accumulate_rightnum = 0.0
        for i in progress_info['grade_dynamic_right_nums']:
            accumulate_rightnum += float(i)
        # 计算当前年级的覆盖率
        coverage = accumulate_rightnum / progress_info["grade_question_nums"] * 100
        # 将当前年级的覆盖率存储下来
        coverage_list.append("{:.5}".format(coverage))
    if all_mode is False:
        user_gradeperiodrank = gradeperiodrank_dict[grade + period]  # 获得用户的年级时期映射值
        return ("FOUND", coverage_list[user_gradeperiodrank - 1])
    else:
        return ("FOUND", coverage_list)



if __name__ == "__main__":
    switch_boom = 1
    if switch_boom == 1:
        init_gradewordbook_questions_progress()