# -*- coding: UTF-8 -*-
# AUTHOR NAME: Tsung YiLee
# AUTHOR EMAIL: свит_дрим@yandex.com
import json
import random


def search_fixedformat_phrase(given_fixedformat):
    '''
    功能：查找对应固定格式的对应词语
    '''
    with open('./database/data/fixedformat_phrases_info.json', 'r', encoding='utf-8') as file:
        # ffp指代fixedformatphrase
        ffp_json = json.load(file)
    found_ffps = []
    for ffp_info in ffp_json:
        # 支持大小写不敏感
        if ffp_info["format"].lower() == given_fixedformat.lower():
            found_ffps.append(ffp_info)
    # 随机5个充字数
    if len(found_ffps) != 0:
        random_ffps = random.sample(found_ffps, 5)
        random_words = [item["word"] for item in random_ffps]
        random_words_pinyin = [item["word_pinyin"] for item in random_ffps]
        random_texts = [item["text"] for item in random_ffps]
        random_texts_pinyin = [item["text_pinyin"] for item in random_ffps]
        return ("FOUND", (random_words, random_words_pinyin, random_texts, random_texts_pinyin))
    else:
        return ("NOINFO", "NOINFO")


def search_idiom(given_char):
    '''
    功能：从成语库中找出包含该字的成语
    '''
    with open('./database/data/idiom_indented.json', 'r', encoding='utf-8') as file:
        idioms_json = json.load(file)
    # 先找到这个char对应的一堆items
    found_idioms = []
    for idiom_info in idioms_json:
        if given_char in idiom_info["word"]:
            found_idioms.append(idiom_info)
    if len(found_idioms) != 0:
        random_idiom_info = random.choice(found_idioms)
        random_word = random_idiom_info["word"]
        random_pinyin = random_idiom_info["pinyin"]
        random_explanation = random_idiom_info["explanation"]
        return ("FOUND", (random_word, random_pinyin, random_explanation))
    else:
        return ("NOINFO", "NOINFO")   


def search_stroke(given_char):
    '''
    功能：找出某个字的笔画
    '''
    stroke_dict = {
            "点": "㇔",
            "横": "㇐",
            "横钩": "㇖",
            "横撇": "㇇",
            "横撇弯钩": "㇌",
            "横斜钩": "⺄",
            "横折": "㇕",
            "横折竖钩": "㇆",
            "横折提": "㇊",
            "横折弯": "㇍",
            "横折弯钩": "㇈",
            "横折折": "㇅",
            "横折折撇": "㇋",
            "横折折折": "㇎",
            "横折折折钩": "㇡",
            "捺": "㇏",
            "撇": "㇓",
            "撇点": "㇛",
            "撇折": "㇜",
            "竖": "㇑",
            "竖钩": "㇚",
            "竖提": "㇙",
            "竖弯": "㇄",
            "竖弯横钩": "㇟",
            "竖折": "㇗",
            "竖折撇": "ㄣ",
            "竖折折": "㇞",
            "竖折折钩": "㇉",
            "提": "㇀",
            "弯钩": "㇁",
            "卧钩": "㇃",
            "斜钩": "㇂",
    }
    with open('./database/data/strokes.txt', 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(':')
            char, strokes = parts[0], parts[1]
            if char == given_char:
                stroke_list = strokes.split(',')
                convert_stroke_list = []
                for single_stroke in stroke_list:
                    convert_stroke_list.append(stroke_dict[single_stroke])
                return ("FOUND", convert_stroke_list)
    return ("NOINFO", "NOINFO")


def search_wordtextpair(given_char):
    '''
    功能：找出某个字的词语、解释及其对应的拼音
    '''
    with open('./database/data/char_info.json', 'r', encoding='utf-8') as file:
        char_info_json = json.load(file)
    for char_info in char_info_json:
        # 先找到这个char对应的信息
        if char_info["char"] == given_char:
            if "wordtextpairs" in char_info and len(char_info["wordtextpairs"]) != 0:
                char_info_nums = len(char_info["wordtextpairs"])
                while char_info_nums != 0:
                    # 这是因为可能有一个字对应多个wordtextpair项，所以得先随机一个。
                    random_wordtextpair = random.choice(char_info["wordtextpairs"])
                    if "word" in random_wordtextpair:
                        random_word = random_wordtextpair["word"]
                        random_word_pinyin = random_wordtextpair["word_pinyin"]
                        random_text = random_wordtextpair["text"]
                        random_text_pinyin = random_wordtextpair["text_pinyin"]
                        return ("FOUND", (random_word, random_word_pinyin, random_text, random_text_pinyin))
                    char_info_nums -= 1
            # 找了一圈也没找到，说明就是没有
            return ("NOINFO", "NOINFO")


def search_wordbook_composed():
    '''
    功能：将所有积累的所有生词返回
    '''
    with open('./database/data/wordbook.json', 'r', encoding='utf-8') as file:
        wordbook_json = json.load(file)
    # 将所有的结果拼成一个长串
    long_result = ''
    for wordbook_info in wordbook_json:
        long_result += wordbook_info['char'] + '(' + wordbook_info['pinyin'] + ') '
    if long_result == '':
        return ("NOINFO", "你尚未添加任何生词哦~")
    else:
        return ("FOUND", long_result)
    

def search_gradewordbook_composed():
    '''
    功能：将不同年级不同时期的生词拼凑返回
    '''
    with open('./database/data/gradewordbook.json', 'r', encoding='utf-8') as file:
        gradewordbook_json = json.load(file)
    compose_dict = {}
    # 将所有不同年级的结果拼成一个超级长串！
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
    for j in range(0, len(gradewordbook_json)):
        gradewordbook_info = gradewordbook_json[j]
        compose = ''
        for i in range(0, len(gradewordbook_info['newwords'])):
            compose = compose + gradewordbook_info['newwords'][i] + '    '# +'(' +  gradewordbook_info['pinyin'][i] + ') '
        compose_dict[j] = compose
    return ("FOUND", compose_dict)
        


if __name__ == "__main__":
    switch_boom = 6
    if switch_boom == 1:
        (cue, result) = search_fixedformat_phrase("AAbb")
        if cue == "FOUND":
            (random_words, random_words_pinyin, random_texts, random_texts_pinyin) = result
            print(random_words)
    elif switch_boom == 2:
        (cue, result) = search_idiom("六")
        if cue == "FOUND":
            (word, pinyin, explanation) = result
            print(word)
    elif switch_boom == 3:
        (cue, convert_stroke_list) = search_stroke("贵")
        if cue == "FOUND":
            print(convert_stroke_list)
    elif switch_boom == 4:
        (cue, (random_word, random_word_pinyin, random_text, random_text_pinyin)) = search_wordtextpair("心")
        print((random_word, random_word_pinyin, random_text, random_text_pinyin))
    elif switch_boom == 5:
        (cue, long_result) = search_wordbook_composed()
        print(long_result)
    elif switch_boom == 6:
        (cue, long_result) = search_gradewordbook_composed()
        print(long_result)