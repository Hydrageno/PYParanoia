# -*- coding: UTF-8 -*-
# AUTHOR NAME: Tsung YiLee
# AUTHOR EMAIL: свит_дрим@yandex.com
import re
import json
from pypinyin import pinyin
import os
from datetime import datetime


def add_newword_to_gradewordbook():
    '''
    功能：生成各个年级的生词
    参数：无
    返回：无
    '''
    grade = None
    period = None
    newword_gradeperiod = {}
    newword_pinyin_gradeperiod = {}
    with open('./database/prevdata/gradewordbook.txt', 'r', encoding='utf-8') as file:
        for line in file:
            # 匹配每行是否是某个年级范围的开头
            pattern = re.compile(r'\S年级\S册生字')
            if bool(pattern.search(line)):
                # 比如'一年级上册生字'
                grade = line[0]
                period = line[3]
                gradeperiod = grade + period
                # 如果当前字典里面没有当前年级的生字
                if gradeperiod not in newword_gradeperiod:
                    newword_gradeperiod[gradeperiod] = []
                    newword_pinyin_gradeperiod[gradeperiod] = []
            else:
                # 否则就是普通生词一行
                # 去除末尾的回车，然后再根据空格分割
                line_newwords = line[:-1].split()
                for newword in line_newwords:
                    # 通过观察规律可以得知，生字都是以：字(zi) 的形式存在
                    newword_pattern = re.compile(r'\S+\(\S+\)')
                    if bool(newword_pattern.search(newword)):
                        gradeperiod = grade + period
                        # 但存在部分特殊开头，比如“1、与()”
                        newword_pattern = re.compile(r'\d、\S+\(\S+\)')
                        idx = 0
                        if bool(newword_pattern.search(newword)):
                            # 如果当前的模式匹配的话，那么可以根据(的位置定位汉字
                            idx = newword.index('(') - 1
                        if '\u4e00' <= newword[idx] <= '\u9fff':
                            # 部分里面会出现非汉字字符，因此需要额外判断
                            newword_gradeperiod[gradeperiod].append(newword[idx])
                            newword_pinyin_gradeperiod[gradeperiod].append(' '.join([''.join(p) for p in pinyin(newword[idx])]))
    convert_gradewordbook_json = []
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
    for key, value in newword_gradeperiod.items():
        gradeperiodrank = gradeperiodrank_dict[key]
        convert_gradewordbook_json.append(
            {
                "gradeperiod": key,
                "gradeperiodrank": gradeperiodrank,
                "newwords": value,
                "pinyin": newword_pinyin_gradeperiod[key]
            }
        )
    with open('./database/data/gradewordbook.json', 'w', encoding='utf-8') as file:
        json.dump(convert_gradewordbook_json, file, ensure_ascii=False, indent=2)            


def add_newword_to_wordbook(given_char):
    '''
    功能：将当前某个字添加到生词本
    参数：单个汉字
    返回：无
    '''
    if not os.path.exists('./database/data/wordbook.json'):
        # 检查文件存在性，创建该文件
        with open('./database/data/wordbook.json', 'w') as file:
            json.dump([], file, ensure_ascii=False, indent=2)
    with open('./database/data/wordbook.json', 'r', encoding='utf-8') as file:
        wordbook_json = json.load(file)
    # 再将该字添加到生字本前，需要检查一下是否生词本中有记录过这个字
    char_exists = False
    for wordbook_info in wordbook_json:
        if wordbook_info['char'] == given_char:
            if wordbook_info['weight'] <= 0:
                wordbook_info['weight'] = 1
            else:
                wordbook_info['weight'] += 1
            wordbook_info['act_time'] = str(datetime.now())
            char_exists = True
            break
    # 对于当前给定的字确实不存在，那么添加新的记录
    if not char_exists:
        newchar_info = {
                        "char": given_char, 
                        "pinyin": ' '.join([''.join(p) for p in pinyin(given_char)]),
                        "weight": 1, 
                        "add_time": str(datetime.now().strftime("%Y-%m-%d")), 
                        "act_time": str(datetime.now().strftime("%Y-%m-%d"))
                    }
        wordbook_json.append(newchar_info)
    # 再按照每个生词的weight对wordbook_json进行排序
    sorted_wordbook_json = sorted(wordbook_json, key=lambda x: x["weight"], reverse=True)
    # 更新wordbook.json文件
    with open("./database/data/wordbook.json", "w", encoding="utf-8") as file:
        json.dump(sorted_wordbook_json, file, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    add_newword_to_wordbook()