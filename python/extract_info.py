# -*- coding: UTF-8 -*-
# AUTHOR NAME: Tsung YiLee
# AUTHOR EMAIL: свит_дрим@yandex.com
import json
from pypinyin import pinyin
from tqdm import trange


def extract_wordtextpairs():
    '''
    从char_detail中提取词
    从文件中读取JSON数据
    '''
    with open('./database/prevdata/char_detail_indented.json', 'r', encoding='utf-8') as file:
        char_info_json = json.load(file)  
    convert_char_info = []  
    # 遍历所有的char_info用于提取信息
    for i in trange(0, len(char_info_json)):
        char_info = char_info_json[i]
        char = char_info["char"]
        # 若pronunciations不存在说明当前字价值不大跳过
        if "pronunciations" not in char_info:
            continue
        pronunciations = char_info["pronunciations"]
        # 同理，跳过无用地方
        if "explanations" not in pronunciations[0]:
            continue
        # 先获取explanation处信息
        char_explanations = pronunciations[0]["explanations"]
        # 整合当前“字”对应的“词语”和对应的“解释”
        char_word_list = []
        char_text_list = []   
        # 遍历explanations中每条信息用于提取“词语”和“解释”
        for char_explanation in char_explanations:
            # 首先需要判断当前“字”是否有words信息
            if "words" in char_explanation:     
                # 遍历当前“字”的每条信息
                for char_word in char_explanation["words"]:
                    # 可能出现当前“字”的某条信息没有word信息，我们认定该处数据非法，跳过即可
                    if "word" not in char_word:
                        continue
                    # 要命的事情是，可能一个“字”当前的word中有多个“词语”
                    if ";" in char_word["word"]:
                        # 分割当前“字”当前word的多个“词语”
                        char_dumplicate_words = char_word["word"].split(";")
                        repeat_times = len(char_dumplicate_words)
                        if "text" in char_word:
                            # 首先确保这个text在里面
                            char_dumplicate_text = [char_word["text"]] * repeat_times
                        else:
                            # 不在的话，那也就只能把word重复N遍了
                            # 即对应的“词语”没有“解释”，那只能拷贝“词语”
                            char_dumplicate_text = [char_dumplicate_words[0]] * repeat_times
                        # 拓展当前“字”的“词语”和“解释”
                        char_word_list.extend(char_dumplicate_words)
                        char_text_list.extend(char_dumplicate_text)
                    else:
                        # 当前“字”仅有个一个“词语”
                        char_word_list.append(char_word["word"])
                        if "text" in char_word:
                            char_text_list.append(char_word["text"])
                        else:
                            char_text_list.append(char_word["word"])

        # 对先前提取的每个“词语”和“解释”添加拼音
        char_word_pinyin_list = []
        char_text_pinyin_list = []
        for i in range(0, len(char_word_list)):
            char_word = char_word_list[i]
            char_text = char_text_list[i]
            # 转换成拼音并添加到对应的序列中，结果是nǐ hǎo
            char_word_pinyin = ' '.join([''.join(p) for p in pinyin(char_word)])
            char_word_pinyin_list.append(char_word_pinyin)
            char_text_pinyin = ' '.join([''.join(p) for p in pinyin(char_text)])
            char_text_pinyin_list.append(char_text_pinyin)

        # 将该字的拼音、词语保存下来构建wordtextpairs
        char_wordtextpairs = []
        for i in range(0, len(char_word_list)):
            char_word = char_word_list[i]
            char_text = char_text_list[i]
            char_word_pinyin = char_word_pinyin_list[i]
            char_text_pinyin = char_text_pinyin_list[i]

            # 构建 wordtextpair字典
            char_wordtextpairs.append(
                {
                    "word": char_word,
                    "word_pinyin": char_word_pinyin,
                    "text": char_text,
                    "text_pinyin": char_text_pinyin
                }
            )
        
        # 添加该字的诸多细节
        convert_char_info.append(
            {
                "char": char,
                "pinyin": ' '.join([''.join(p) for p in pinyin(char)]),
                "wordtextpairs": char_wordtextpairs
            }
        )
    output_filename = "./database/data/char_info.json"
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        json.dump(convert_char_info, output_file, ensure_ascii=False, indent=2)


def extract_fixedformat_phrases():
    with open('./database/prevdata/fixedformat_phrases.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    convert_fixedformat_pharases = []
    # 读取每一行的内容
    for i in trange(len(lines)):
        line = lines[i]
        # 将每一行内容按照空格分割
        split_parts = line.strip().split()
        fixedformat, fixedformat_phrase, explanation = split_parts
        fixedformat_phrase_pinyin = ' '.join([''.join(p) for p in pinyin(fixedformat_phrase)])
        explanation_pinyin = ' '.join([''.join(p) for p in pinyin(explanation)])
        convert_fixedformat_pharases.append(
            {
                "format": fixedformat,
                "word": fixedformat_phrase,
                "word_pinyin": fixedformat_phrase_pinyin,
                "text": explanation,
                "text_pinyin": explanation_pinyin
            }
        )
    output_filename = "./database/data/fixedformat_phrases_info.json"
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        json.dump(convert_fixedformat_pharases, output_file, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    extract_fixedformat_phrases()

