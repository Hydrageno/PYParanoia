# -*- coding: UTF-8 -*-
# AUTHOR NAME: Tsung YiLee
# AUTHOR EMAIL: свит_дрим@yandex.com
from flask import Flask, jsonify, send_file
from flask import request
from flask_cors import CORS
from pypinyin import pinyin
import json


app = Flask(__name__)
CORS(app)
'''
参数设置细节
cached_char：目标搜索字
cached_which：缓存大模式
cached_grade：缓存年级
cached_period：缓存时期
cached_hybrid_mode：缓存小模式
'''
cached_char = None
cached_which = None
cached_grade = None
cached_period = None
cached_hybrid_mode = None


@app.route('/')
def welcome():
    '''
    Hawaii: Aloha!!
    '''
    return jsonify({
        "message": "Aloha!!Hau oli kēia hui ana o kāua"
    })


@app.route('/set_target_character/<given_char>')
def set_target_character(given_char):
    '''
    功能：后台缓存搜索目标字
    '''
    global cached_char
    cached_char = given_char
    return jsonify({
        "message": "ok"
    })


@app.route('/search_character_info/<target_char>')
def search_character_info(target_char):
    '''
    功能：搜索目标字的相应信息
    '''
    from python.search_info import search_wordtextpair
    # 首先是搜索该字的拼音、词语、解释信息
    (wtp_cue, wtp_info) = search_wordtextpair(target_char)
    if wtp_cue == "FOUND":
        (word,word_pinyin, text, text_pinyin) = wtp_info
    else:
        [word, word_pinyin, text, text_pinyin] = ["NOINFO"] * 4
    # 其次是搜索该字的笔画
    from python.search_info import search_stroke
    (stroke_cue, stroke_info) = search_stroke(target_char)
    if stroke_cue != "FOUND":
        stroke_info = "NOINFO"
    # 再者是搜索该字的成语
    from python.search_info import search_idiom
    (idiom_cue, idiom_info) = search_idiom(target_char)
    if idiom_cue == "FOUND":
        (idiom, idiom_pinyin, explanation) = idiom_info
    else:
        [idiom, idiom_pinyin, explanation] = ["NOINFO"] * 3
    # 将搜索结果打包，返回回去
    result = {
        'char': target_char,
        'pinyin': ' '.join([''.join(p) for p in pinyin(target_char)]), 
        'wtp_status': wtp_cue,
        'wtp_info': {
            'word': word,
            'word_pinyin': word_pinyin,
            'text': text,
            'text_pinyin': text_pinyin
        },
        'stroke_status': stroke_cue,
        'stroke_info': stroke_info,
        'idiom_status': idiom_cue,
        'idiom_info': {
            'idiom': idiom,
            'idiom_pinyin': idiom_pinyin,
            'explanation': explanation 
        }
    }
    return jsonify(result)


@app.route('/add_to_wordbook/<target_char>')
def add_to_wordbook(target_char):
    '''
    功能：将生词添加到生词本中
    '''
    from python.add_newword import add_newword_to_wordbook
    add_newword_to_wordbook(target_char)
    return jsonify({
        "message": "ok"
    })


@app.route('/compose_allwordbook/')
def compse_allwordbook():
    '''
    功能：抽取所有的生词汇聚到一起
    '''
    from python.search_info import search_wordbook_composed
    (wordbook_cue, wordbook_composed) = search_wordbook_composed()
    from python.search_info import search_gradewordbook_composed
    (gradewordbook_cue, gradewordbook_composed) = search_gradewordbook_composed()
    return jsonify({
        "message": "ok",
        "wordbook": wordbook_composed,
        "gradewordbook": gradewordbook_composed
    })


@app.route('/search_ffp_info/<given_ff>')
def search_ffp_info(given_ff):
    '''
    功能：搜索固定格式词语的信息
    '''
    from python.search_info import search_fixedformat_phrase
    (ffp_cue, ffp_info) = search_fixedformat_phrase(given_ff)
    if ffp_cue == "FOUND":
        (words, words_pinyin, texts, texts_pinyin) = ffp_info
        return jsonify({
            "message": "ok",
            "words": words,
            "words_pinyin": words_pinyin,
            "texts": texts,
            "texts_pinyin": texts_pinyin
        })
    else:
        return jsonify({
            "message": "no"
        })
    

@app.route('/fetch_questions', methods=['POST'])
def fetch_questions():
    '''
    功能：获取年级生词本题目序列
    '''
    from python.auxiliary import regularize_questions
    data = request.json
    global cached_which
    cached_which = data['mode']
    if cached_which == 'gradewordbook':
        global cached_grade
        global cached_period
        global cached_hybrid_mode
        cached_grade = data['gradeperiod'][0]
        cached_period = data['gradeperiod'][1]
        cached_hybrid_mode = data['hybrid_mode']
        from python.select_questions import select_questions_by_gradewordbook
        select_questions_by_gradewordbook(cached_grade, cached_period, cached_hybrid_mode)
    else:
        from python.generate_questions import generate_questions_by_wordbook
        from python.select_questions import select_questions_by_wordbook
        generate_questions_by_wordbook(history_mode=False)
        select_questions_by_wordbook()
    regularize_questions(cached_which)
    with open(f'./database/regular/regularized_{cached_which}_questions.json', 'r', encoding='utf-8') as file:
        questions_json = json.load(file)
    return jsonify({
        "message": "ok",
        "questions": questions_json
    })


@app.route('/process_uanswer', methods=['POST'])
def process_uanswer():
    '''
    功能：获取年级生词本题目序列
    '''
    data = request.json
    uanswer_json = data['user_answers']
    with open('./database/process/user_cache_answer.json', 'w', encoding='utf-8') as file:
        json.dump(uanswer_json, file, indent=2, ensure_ascii=False)
    global cached_which
    if cached_which == 'gradewordbook':
        global cached_grade
        global cached_period
        global cached_hybrid_mode
        from python.process_answer import process_answer_by_gradewordbook
        process_answer_by_gradewordbook(cached_grade, cached_period, cached_hybrid_mode)
    else:
        from python.process_answer import process_answer_by_wordbook
        process_answer_by_wordbook()
    with open(f'./database/process/response_info.json', 'r', encoding='utf-8') as file:
        response_json = json.load(file)
    return jsonify(
        {
            "message": "ok",
            "response": response_json
        }
    )


@app.route('/download_figure')
def download_figure():
    '''
    功能：下载分析数据
    '''
    global cached_which
    if cached_which == 'gradewordbook':
        global cached_grade
        global cached_period
        global cached_hybrid_mode
        from python.pack_pdf import pack_pdf_by_gradewordbook
        pack_pdf_by_gradewordbook(cached_grade, cached_period, cached_hybrid_mode)
    else:
        from python.pack_pdf import pack_pdf_by_wordbook
        pack_pdf_by_wordbook()
    with open('./resource/figure/测试情况.pdf', 'rb') as file:
        pdf_content = file.read()
    import io
    blob_data = io.BytesIO()
    blob_data.write(pdf_content)
    blob_data.seek(0)
    return send_file(
        blob_data,
        mimetype='application/pdf',
        as_attachment=True,
        download_name='测试情况.pdf'
    )


@app.route('/machine_read/<content>')
def machine_read(content):
    '''
    功能：通过驱动ttx引擎
    '''
    from python.auxiliary import read_text_by_machine
    read_text_by_machine(content)
    return jsonify(
        {
            "message": "ok"
        }
    )


if __name__ == "__main__":
    app.run(host='127.0.0.1', port='5000')
