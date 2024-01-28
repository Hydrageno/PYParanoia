# -*- coding: UTF-8 -*-
# AUTHOR NAME: Tsung YiLee
# AUTHOR EMAIL: свит_дрим@yandex.com
import json
from pypinyin import pinyin, Style
from tqdm import trange


def generate_questions_by_gradewordbook(grade, period):
    '''
    功能：生成所有年级的题目
    '''
    with open('./database/data/gradewordbook.json', 'r', encoding='utf-8') as file:
        gradewordbook_json = json.load(file)
    with open('./database/data/idiom_indented.json', 'r', encoding='utf-8') as file:
        idioms_json = json.load(file)
    with open('./database/data/char_info.json', 'r', encoding='utf-8') as file:
        char_info_json = json.load(file)
    '''
        根据年级出题目
        一年级上仅会一年级上
        一年级下会一年级下同时还会一年级上，以此类推，
        直接生成大题库然后从里面抽题目就行
    '''
    # 记录所有年级的生词
    newword_list = []
    for gradewordbook_info in gradewordbook_json:
            newword_list += gradewordbook_info["newwords"]
    '''
        生成题库并且保存下来
    '''
    questions = []
    newword_list_num = len(newword_list)
    for i in trange(newword_list_num):
        # 获得这个生词
        newword = newword_list[i]
        # 先获得这个词在哪个年级上册还是下册
        newword_gradeperiodrank = None
        for gradewordbook_info in gradewordbook_json:
            if newword in gradewordbook_info["newwords"]:
                newword_gradeperiodrank = gradewordbook_info["gradeperiodrank"]
        # 拼音项、词语项和wtp_data关联
        matched_newword_info = [newword_info for newword_info in char_info_json if newword_info["char"] == newword][0]
        ## 先是拼音项
        question_type = 1
        question_desc = f"{newword}-?-1-2-3-4"
        answer = pinyin(newword, style=Style.TONE3)[0][0]
        matched_question = {
            "char": newword,
            "question_type": question_type,
            "question_desc": question_desc,
            "answer": answer,
            "gradeperiodrank": newword_gradeperiodrank,
            "bingo": False,
        }
        questions.append(matched_question)
        ## 再是词语项
        if "wordtextpairs" in matched_newword_info and len(matched_newword_info["wordtextpairs"]) != 0:
            matched_wordtextpairs = matched_newword_info["wordtextpairs"]
            for matched_wordtextpair in matched_wordtextpairs:
                word = matched_wordtextpair["word"]
                word = word.replace(newword, '？')
                word_pinyin = matched_wordtextpair["word_pinyin"]
                text = matched_wordtextpair["text"]
                text_pinyin = matched_wordtextpair["text_pinyin"]
                text = text.replace(newword, '？')
                question_type = 2
                question_desc = f"{word}-{word_pinyin}-{text}-{text_pinyin}"
                answer = newword
                matched_question = {
                    "char": newword,
                    "question_type": question_type,
                    "question_desc": question_desc,
                    "answer": answer,
                    "gradeperiodrank": newword_gradeperiodrank,
                    "bingo": False
                }
                questions.append(matched_question)
        # 最后成语项
        for idiom in idioms_json:
            if newword in idiom["word"]:
                word = idiom["word"]
                word = word.replace(newword, '？')
                word_pinyin = idiom["pinyin"]
                text = idiom["explanation"]
                text_pinyin = ' '.join([''.join(p) for p in pinyin(text)])
                text = text.replace(newword, '？')  # 先生成拼音然后再掩盖原词
                question_type = 3
                question_desc = f"{word}-{word_pinyin}-{text}-{text_pinyin}"
                answer = newword
                matched_question = {
                    "char": newword,
                    "question_type": question_type,
                    "question_desc": question_desc,
                    "answer": answer,
                    "gradeperiodrank": newword_gradeperiodrank,
                    "bingo": False
                }
                questions.append(matched_question)

    with open('./database/question/gradewordbook_questions.json', 'w', encoding='utf-8') as file:
        json.dump(questions, file, indent=2, ensure_ascii=False)


def generate_questions_by_wordbook(history_mode):
    with open('./database/data/wordbook.json', 'r', encoding='utf-8') as file:
        wordbook_json = json.load(file)
    with open('./database/data/idiom_indented.json', 'r', encoding='utf-8') as file:
        idioms_json = json.load(file)
    with open('./database/data/char_info.json', 'r', encoding='utf-8') as file:
        char_info_json = json.load(file)
    '''
        根据生词本出题，划分为是否启用历史模式，添加生词
    '''
    newword_list = []
    for each_wordbook in wordbook_json:
        if each_wordbook["weight"] <= 0:
            if history_mode is True:
                newword_list.append(each_wordbook["char"])
        else:
            newword_list.append(each_wordbook["char"])
    '''
        生成题库并且保存下来
    '''
    questions = []
    newword_list_num = len(newword_list)
    for i in trange(newword_list_num):
        newword = newword_list[i]
        # 拼音项、词语项和wtp_data关联
        matched_newword_info = [newword_info for newword_info in char_info_json if newword_info["char"] == newword][0]
        ## 先是拼音项
        question_type = 1
        question_desc = f"{newword}-?-1-2-3-4"
        answer = pinyin(newword, style=Style.TONE3)[0][0]
        matched_question = {
            "char": newword,
            "question_type": question_type,
            "question_desc": question_desc,
            "answer": answer,
        }
        questions.append(matched_question)
        ## 再是词语项
        if "wordtextpairs" in matched_newword_info and len(matched_newword_info["wordtextpairs"]) != 0:
            matched_wordtextpairs = matched_newword_info["wordtextpairs"]
            for matched_wordtextpair in matched_wordtextpairs:
                word = matched_wordtextpair["word"]
                word = word.replace(newword, '？')
                word_pinyin = matched_wordtextpair["word_pinyin"]
                text = matched_wordtextpair["text"]
                text_pinyin = matched_wordtextpair["text_pinyin"]
                text = text.replace(newword, '？')
                question_type = 2
                question_desc = f"{word}-{word_pinyin}-{text}-{text_pinyin}"
                answer = newword
                matched_question = {
                "char": newword,
                "question_type": question_type,
                "question_desc": question_desc,
                "answer": answer,
                }
                questions.append(matched_question)
        # 最后成语项
        for idiom in idioms_json:
            if newword in idiom["word"]:
                word = idiom["word"]
                word = word.replace(newword, '？')
                word_pinyin = idiom["pinyin"]
                text = idiom["explanation"]
                text_pinyin = ' '.join([''.join(p) for p in pinyin(text)])
                text = text.replace(newword, '？')
                question_type = 3
                question_desc = f"{word}-{word_pinyin}-{text}-{text_pinyin}"
                answer = newword
                matched_question = {
                    "char": newword,
                    "question_type": question_type,
                    "question_desc": question_desc,
                    "answer": answer,
                }
                questions.append(matched_question)

    with open('./database/question/wordbook_questions.json', 'w', encoding='utf-8') as file:
        json.dump(questions, file, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    generate_questions_by_wordbook()
    generate_questions_by_gradewordbook("六", "下")