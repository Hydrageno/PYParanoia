# -*- coding: UTF-8 -*-
# AUTHOR NAME: Tsung YiLee
# AUTHOR EMAIL: свит_дрим@yandex.com
import json
import numpy as np


def process_answer_by_gradewordbook(grade, period, hybrid_mode):
    '''
    功能：处理前端返回的用户填写结果
    参数：
        grade：年级
        period：上下册
        hybrid_mode：混合模式标志
    '''
    # 读取题库以及用户答案缓存文件
    with open('./database/selected/selected_gradewordbook_questions.json', 'r', encoding='utf-8') as file:
        questions_json = json.load(file)
    with open('./database/process/user_cache_answer.json', 'r', encoding='utf-8') as file:
        uanswer_json = json.load(file)
    '''
    基本参数设置
    '''
    # 年级时期映射表
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
    # 用户当前年级时期值
    user_gradeperiodrank = gradeperiodrank_dict[grade + period]
    # 当前选中题目数量 & 用户回答正确数量
    questions_num = len(questions_json)
    user_rightnum = 0.0
    # char_weight内容是：{char:[pinyin_times, word_times, idiom_times, py_errors, word_errors, idiom_errors, gp_rank]}
    char_weight = {}
    # 混合模式下，记录用户每个年级题目数量、回答正确数量并计算每个年级权重
    # 内容是：{gradeperiodrank:[times, erros]}
    gradeperiodrank_weight = {}
    # 纯净模式下，记录用户当前年级时期回答正确题目，用于标记题目已正确作答。
    user_rightquestions = []
    # 返还作答情况
    response_info = []
    '''
    遍历每一题以及用户对应的回答
    '''
    for i in range(0, questions_num):
        question_info = questions_json[i]  # 获取第i条问题信息
        question_char = question_info['char']  # 获取第i题考察的字
        question_type = question_info['question_type']  # 获取第i题考察类型：1为拼音，2为词语，3为成语
        question_answer = question_info['answer']  # 获取第i题的答案
        question_gradeperiodrank = question_info['gradeperiodrank']  # 获取第i题的归属年级
        uanswer_info = uanswer_json[i]  # 获取用户对应的回答
        if question_char not in char_weight:
            # 如果当前字不在，初始化对应权重参数
            char_weight[question_char] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, question_gradeperiodrank]
        if question_gradeperiodrank not in gradeperiodrank_weight:
            # 如果当前年级不在，初始化对应权重参数
            gradeperiodrank_weight[question_gradeperiodrank] = [0.0, 0.0]
        # 统计一下当前年级题目出现次数
        gradeperiodrank_weight[question_gradeperiodrank][0] += 1.0
        # 统计一下当前字各种题型出现次数
        char_weight[question_char][question_type - 1] += 1.0
        if uanswer_info != question_answer:
            # 用户回答错误
            gradeperiodrank_weight[question_gradeperiodrank][1] += 1.0
            char_weight[question_char][question_type - 1 + 3] += 1.0
            response_info.append(
                {
                    "message": "回答错误",
                    "answer": question_answer
                }
            )
        else:
            # 用户回答正确
            user_rightnum += 1.0
            if hybrid_mode is False:
                # 纯净模式下，登记该题目
                user_rightquestions.append(question_info)
            response_info.append(
                {
                    "message": "回答正确",
                    "answer": question_answer
                }
            )
    '''
    统计状态，统计每个字的情况
    '''
    states = []
    for char, weights in char_weight.items():
        times = np.array(weights[0:3])  # 获取当前字各种题型出现次数
        errors = np.array(weights[3:6])  # 获取当前字各种题型错误次数
        times = times + 1e-5  # 预防除零异常
        prev_softmax_weights = errors / times  # 计算各种题型占比
        softmax_weights = np.exp(prev_softmax_weights) / (np.exp(prev_softmax_weights)).sum(axis=0)
        sum_weights = (softmax_weights * times).sum(axis=0)
        states.append({
            "char": char,
            "times": times.tolist(),
            "errors": errors.tolist(),
            "softmax_weights": softmax_weights.tolist(),
            "weights": sum_weights,
            "gradeperiodrank": weights[6]
        })
    '''
    记录封存
    '''
    # 排序各个字的答题情况
    sorted_states = sorted(states, key=lambda x: x["weights"], reverse=True)
    with open('./database/states/gradewordbook_char_distribution.json', 'w', encoding='utf-8') as file:
        json.dump(sorted_states, file, indent=2, ensure_ascii=False)
    # 记录用户本次作答情况
    with open('./database/states/response_info.json', 'w', encoding='utf-8') as file:
        json.dump(response_info, file, indent=2, ensure_ascii=False)    
    if hybrid_mode is True:
        # 如果是混合答题模式需要按年级划分答题情况
        question_distribution = []
        for gradeperiodrank, weights in gradeperiodrank_weight.items():
            question_distribution.append({
                "gradeperiodrank": gradeperiodrank,
                "times": weights[0],
                "errors": weights[1],
                "weights": weights[1] / weights[0]
            })
        sorted_question_distribution = sorted(question_distribution, key=lambda x: (x["weights"], x["errors"], x["gradeperiodrank"]), reverse=True)
        with open('./database/states/gradewordbook_question_distribution.json', 'w', encoding='utf-8') as file:
            json.dump(sorted_question_distribution, file, indent=2, ensure_ascii=False)
    else:
        # 混合模式，更新本年级本时期进度
        with open('./database/states/gradewordbook_question_progress.json', 'r', encoding='utf-8') as file:
            gradewordbook_question_progress_json = json.load(file)
        for gradewordbook_question_progress_info in gradewordbook_question_progress_json:
            if gradewordbook_question_progress_info["gradeperiodrank"] == user_gradeperiodrank:
                gradewordbook_question_progress_info["grade_dynamic_right_nums"].append(user_rightnum)
                gradewordbook_question_progress_info['grade_dynamic_picked_nums'].append(questions_num)
        with open('./database/states/gradewordbook_question_progress.json', 'w', encoding='utf-8') as file:
            json.dump(gradewordbook_question_progress_json, file, indent=2, ensure_ascii=False)
        # 另外对题库数据进行标记
        with open('./database/question/gradewordbook_questions.json', 'r', encoding='utf-8') as file:
            gradewordbook_questions_json = json.load(file)
        for gradeperiod_rightquestions in user_rightquestions:
            for gradewordbook_questions_info in gradewordbook_questions_json:
                if gradewordbook_questions_info["question_desc"] == gradeperiod_rightquestions["question_desc"]:
                    gradewordbook_questions_info["bingo"] = True
        with open('./database/question/gradewordbook_questions.json', 'w', encoding='utf-8') as file:
            json.dump(gradewordbook_questions_json, file, indent=2, ensure_ascii=False)


def process_answer_by_wordbook():
    '''
    功能：处理前端返回的用户填写结果
    '''
    with open('./database/selected/selected_wordbook_questions.json', 'r', encoding='utf-8') as file:
        questions_json = json.load(file)
    with open('./database/process/user_cache_answer.json', 'r', encoding='utf-8') as file:
        uanswer_json = json.load(file)
    '''
    基本参数设置
    '''
    # char_weight内容是：{char:[pinyin_times, word_times, idiom_times, py_errors, word_errors, idiom_errors, gp_rank]}
    char_weight = {}
    # 当前选中题目数量 & 用户回答正确数量
    questions_num = len(questions_json)
    user_rightnum = 0.0
    # 返还作答情况
    response_info = []
    for i in range(0, questions_num):
        question_info = questions_json[i]  # 获取第i条问题信息
        question_char = question_info['char']  # 获取第i题考察的字
        question_type = question_info['question_type']  # 获取第i题考察类型：1为拼音，2为词语，3为成语
        question_answer = question_info['answer']  # 获取第i题的答案
        uanswer_info = uanswer_json[i]  # 获取用户对应的回答
        if question_char not in char_weight:
            char_weight[question_char] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        # 统计一下当前字各种题型出现次数
        char_weight[question_char][question_type - 1] += 1.0
        if uanswer_info != question_answer:
            # 用户回答错误
            char_weight[question_char][question_type - 1 + 3] += 1.0
            response_info.append(
                {
                    "message": "回答错误",
                    "answer": question_answer
                }
            )
        else:
            # 用户回答正确
            user_rightnum += 1.0
            response_info.append(
                {
                    "message": "回答正确",
                    "answer": question_answer
                }
            )
    
    # 更新一下生词本各词权重
    with open('./database/data/wordbook.json', 'r', encoding='utf-8') as file:
        wordbook_json = json.load(file)

    states = []
    for char, weights in char_weight.items():
        times = np.array(weights[0:3])  # 获取当前字各种题型出现次数
        errors = np.array(weights[3:6])  # 获取当前字各种题型错误次数
        times = times + 1e-5  # 预防除零异常
        prev_softmax_weights = errors / times  # 计算各种题型占比
        softmax_weights = np.exp(prev_softmax_weights) / (np.exp(prev_softmax_weights)).sum(axis=0)
        sum_weights = (softmax_weights * times).sum(axis=0)
        states.append({
            "char": char,
            "times": times.tolist(),
            "errors": errors.tolist(),
            "softmax_weights": softmax_weights.tolist(),
            "weights": sum_weights,
        })
        # 对每个词语更新权重
        for wordbook_info in wordbook_json:
            if char == wordbook_info["char"]:
                if sum_weights > times.sum(axis=0) / 2.0:
                    wordbook_info["weight"] += 1
                else:
                    wordbook_info["weight"] -= 1
    # 排序各个字的答题情况
    sorted_states = sorted(states, key=lambda x: x["weights"], reverse=True)
    with open('./database/states/wordbook_char_distribution.json', 'w', encoding='utf-8') as file:
        json.dump(sorted_states, file, indent=2, ensure_ascii=False)
    # 记录用户本次作答情况
    with open('./database/states/response_info.json', 'w', encoding='utf-8') as file:
        json.dump(response_info, file, indent=2, ensure_ascii=False) 
    # 排序生词本情况
    sorted_wordbook_json = sorted(wordbook_json, key=lambda x: x["weight"], reverse=True)
    with open('./database/data/wordbook.json', 'w', encoding='utf-8') as file:
        json.dump(sorted_wordbook_json, file, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    process_answer_by_wordbook()




    