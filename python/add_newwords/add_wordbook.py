# -*- coding: UTF-8 -*-
# AUTHOR NAME: Tsung YiLee
# AUTHOR EMAIL: свит_дрим@yandex.com
import json
from datetime import datetime
from pypinyin import pinyin
import os


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
    add_newword_to_wordbook('牛')

    

