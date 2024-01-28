# -*- coding: UTF-8 -*-
# AUTHOR NAME: Tsung YiLee
# AUTHOR EMAIL: свит_дрим@yandex.com
import json
import random


def select_questions_by_gradewordbook(grade, period, hybrid_mode:False):
    '''
    功能：从生词题库中直接抽一定数量题目，然后再random数量的题目
    '''
    with open('./database/question/gradewordbook_questions.json', 'r', encoding='utf-8') as file:
        gradewordbook_questions_json = json.load(file)
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
    gradeperiodrank = gradeperiodrank_dict[grade + period]
    pick_questions = []
    for gradewordbook_questions_info in gradewordbook_questions_json:
        if hybrid_mode is True:
            # 混用模式不用统计每个年级的进展，只需要单次正确率即可
            if gradeperiodrank >= gradewordbook_questions_info["gradeperiodrank"]:
                pick_questions.append(gradewordbook_questions_info)
        else:
            # 单个年级，需要统计正确率和覆盖率，所以需要挑选出没做正确的
            if gradeperiodrank == gradewordbook_questions_info["gradeperiodrank"] and gradewordbook_questions_info["bingo"] is False:
                pick_questions.append(gradewordbook_questions_info)
    random_pick_questions = random.sample(pick_questions, 20)
    random.shuffle(random_pick_questions)
    with open('./database/selected/selected_gradewordbook_questions.json', 'w', encoding='utf-8') as file:
        json.dump(random_pick_questions, file, indent=2, ensure_ascii=False)


def select_questions_by_wordbook():
    '''
    从生词题库中直接抽固定数量题目，然后再random数量的题目
    '''
    with open('./database/question/wordbook_questions.json', 'r', encoding='utf-8') as file:
        wordbook_questions_json = json.load(file)
    random_pick_questions = random.sample(wordbook_questions_json, 20)
    random.shuffle(random_pick_questions)
    with open('./database/selected/selected_wordbook_questions.json', 'w', encoding='utf-8') as file:
        json.dump(random_pick_questions, file, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    switch_boom = 2
    if switch_boom == 1:
        select_questions_by_gradewordbook("四", "上", hybrid_mode=True)
    else:
        select_questions_by_wordbook()