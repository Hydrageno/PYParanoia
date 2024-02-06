# -*- coding: UTF-8 -*-
# AUTHOR NAME: Tsung YiLee
# AUTHOR EMAIL: свит_дрим@yandex.com
import json
import pyttsx3
import time

'''
涉及函数：
    check_wordbook_empty
        本质：检查生词本是否空，辅助抽题功能
    clear_gradewordbook_questions_bingolabel
        本质：根据需求清空不同年级不同时期题目的bingo标志，初始化使用
    reindent_json
        本质：规范格式化json文件
    read_text_by_machine
        本质：让电脑读出拼音
    init_database
        本质：初始化项目数据，涵盖生词本
    regularize_questions
        本质：规范化题目描述文本信息
'''

def check_wordbook_empty():
    '''
    功能：检查生词本是否空，如若空则不允许从生词本中抽题目！
    '''
    with open('./database/data/wordbook.json', 'r', encoding='utf-8') as file:
        wordbook_json = json.load(file)
    if len(wordbook_json) == 0:
        return True
    else:
        return False


def clear_gradewordbook_questions_bingolabel(grade, period, all_mode):
    '''
    功能：根据需求清空不同年级不同时期题目的bingo标志
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

    if all_mode is True:
        # 清洗所有的bingo标志不论年级时期
        for gradewordbook_questions_info in gradewordbook_questions_json:
            gradewordbook_questions_info['bingo'] = False
    else:
        # 按年级时期清洗bingo标志
        gradeperiodrank = gradeperiodrank_dict[grade + period]
        for gradewordbook_questions_info in gradewordbook_questions_json:
            if gradewordbook_questions_info['gradeperiodrank'] == gradeperiodrank:
                gradewordbook_questions_info['bingo'] = False
    # 将数据存放回原位置
    with open('./database/question/gradewordbook_questions.json', 'w', encoding='utf-8') as file:
        json.dump(gradewordbook_questions_json, file, indent=2, ensure_ascii=False)


def reindent_json(source_filepath, target_filepath):
    '''
    功能：更正json缩进格式
    '''
    with open(source_filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    with open(target_filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def read_text_by_machine(text):
    '''
    功能：让机器读出语音
    '''
    engine = pyttsx3.init()
    # 设置语速
    engine.setProperty('rate', 120)
    # 将文本转换为语音
    engine.say(text)
    # 等待语音输出完成
    engine.runAndWait()


def init_database():
    '''
    功能：初始化项目数据
    '''
    filepath_list = ['./database/data/wordbook.json']
    # 初始化生词本
    for filepath in filepath_list:
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump([], file, ensure_ascii=False, indent=2)
    # 初始化所有年级标志
    clear_gradewordbook_questions_bingolabel('六', '下', True)
    # 初始化年级所有题目缓存题数
    from figure_analysis import init_gradewordbook_questions_progress
    init_gradewordbook_questions_progress()


def regularize_questions(filename):
    '''
    功能：规范化题目内容
    '''
    with open(f'./database/selected/selected_{filename}_questions.json', 'r', encoding='utf-8') as file:
        select_questions_json = json.load(file)
    process_questions = []
    selected_num = len(select_questions_json)
    for i in range(0, selected_num):
        select_question_info = select_questions_json[i]
        current_question_id = str(i + 1)
        if select_question_info["question_type"] == 1:
            current_question_maintext = f"请为“{select_question_info['char']}”找出拼音哦~"
            current_question_desc = "龍的拼音：lóng第2声，所以填入long2"
        else:
            source_question_desc = select_question_info["question_desc"].split('-')
            current_question_maintext = f"请为“{source_question_desc[0]}”（{source_question_desc[1]}）补充字"
            current_question_desc = f"{source_question_desc[2]}（{source_question_desc[3]}）"
        process_questions.append({
            "question_id": current_question_id,
            "question_maintext": current_question_maintext,
            "question_desc": current_question_desc
        }) 
    with open(f'./database/regular/regularized_{filename}_questions.json', 'w', encoding='utf-8') as file:
        json.dump(process_questions, file, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    switch_boom = 1
    if switch_boom == 1:
        init_database()
    elif switch_boom == 2:
        regularize_questions('gradewordbook')
    elif switch_boom == 3:
        reindent_json('source.json', 'target.json')
    elif switch_boom == 4:
        read_text_by_machine('你好')
    elif switch_boom == 5:
        init_database()
    elif switch_boom == 6:
        regularize_questions('gradewordbook')