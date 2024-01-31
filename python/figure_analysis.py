# -*- coding: UTF-8 -*-
# AUTHOR NAME: Tsung YiLee
# AUTHOR EMAIL: свит_дрим@yandex.com
import json
from tqdm import trange
import wordcloud
import numpy
from PIL import Image
import random


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
    

def analyze_ffphrase_category():
    '''
    功能：统计固定格式词语种类数量
    '''
    with open('./database/data/fixedformat_phrases_info.json', 'r', encoding='utf-8') as file:
        ffp_json = json.load(file)
    ffp_category = set()
    for ffp_info in ffp_json:
        ffp_category.add(ffp_info['format'])
    return ffp_category


def paint_wordcloud():
    '''
    功能：生成词云，但是推荐在年级生词本模式下使用，因为普通生词本可分析数据过少
    '''
    with open('./database/states/gradewordbook_char_distribution.json', 'r', encoding='utf-8') as file:
        char_distribution_json = json.load(file)
    word_count = 0
    composed = ''
    for char_distribution_info in char_distribution_json:
        composed = composed + char_distribution_info['char'] + ','
        word_count += 1
    while word_count < 100:
        random_one = random.choice(char_distribution_json)
        random_two = random.choice(char_distribution_json)
        composed = composed + random_one['char'] + random_two['char'] + ','
        word_count += 1
    img = Image.open('./resource/figure/wordcloud_background.png')
    mask = numpy.array(img)
    wc = wordcloud.WordCloud(font_path='./resource/figure/字魂白鸽天行体.ttf', collocations=True, mask=mask, width=852, height=640, background_color='white', min_font_size=32)
    wc.generate(composed)
    wc.to_file('result.png')


if __name__ == "__main__":
    switch_boom = 3
    if switch_boom == 1:
        init_gradewordbook_questions_progress()
    elif switch_boom == 2:
        print(analyze_ffphrase_category())
    elif switch_boom == 3:
        paint_wordcloud()