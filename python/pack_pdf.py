# -*- coding: UTF-8 -*-
# AUTHOR NAME: Tsung YiLee
# AUTHOR EMAIL: свит_дрим@yandex.com
import json
import random
import wordcloud
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


'''
涉及函数
    paint_wordcloud
        本质：绘画词云
    paint_char_distribution
        本质：绘制字的分布情况，不同字的权重，采用直方图展示
    paint_question_gradeperiod_distribution
        本质：年级生字本+混合模式，绘制题目的不同年级分布
    paint_question_progress
        本质：年级生字本+纯净模式，绘制当前题目当前时期的年级进度图
'''


def paint_wordcloud(which):
    '''
    功能：生成词云，但是推荐在年级生词本模式下使用，因为普通生词本可分析数据过少
    '''
    with open(f'./database/states/{which}_char_distribution.json', 'r', encoding='utf-8') as file:
        char_distribution_json = json.load(file)
    word_count = 0
    composed = ''
    for char_distribution_info in char_distribution_json:
        composed = composed + char_distribution_info['char'] + ','
        word_count += 1
    while word_count < 50:
        random_one = random.choice(char_distribution_json)
        random_two = random.choice(char_distribution_json)
        composed = composed + random_one['char'] + random_two['char'] + ','
        word_count += 1
    wc = wordcloud.WordCloud(font_path='./resource/figure/字魂白鸽天行体.ttf', collocations=True, width=480, height=300, background_color='white', min_font_size=32)
    wc.generate(composed)
    wc.to_file('./resource/figure/wordcloud.png')


def paint_char_distribution(which):
    '''
    功能：绘制字的分布情况，不同字的权重
    '''
    with open(f'./database/states/{which}_char_distribution.json', 'r', encoding='utf-8') as file:
        char_distribution_json = json.load(file)
    char_sequence = []
    external_weight_sequence = []  # 每个字之间的总权重
    for char_distribution_info in char_distribution_json:
        char_sequence.append(char_distribution_info['char'])
        external_weight_sequence.append(char_distribution_info['weights'])
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(4.8, 3))
    plt.bar(char_sequence, external_weight_sequence)
    plt.ylabel('权重')
    plt.title('生字权重分布直方图')
    plt.savefig('./resource/figure/char_distribution.png')


def paint_question_gradeperiod_distribution():
    '''
    功能：混合模式，绘制题目的不同年级分布
    '''
    with open(f'./database/states/gradewordbook_question_distribution.json', 'r', encoding='utf-8') as file:
        question_distribution_json = json.load(file)
    gradeperiodrank_dict = {
        1: "一上",
        2: "一下",
        3: "二上",
        4: "二下",
        5: "三上",
        6: "三下",
        7: "四上",
        8: "四下",
        9: "五上",
        10: "五下",
        11: "六上",
        12: "六下"
    }
    gradeperiod_sequence = []
    external_weight_sequence = []  # 每个字之间的总权重
    for question_distribution_info in question_distribution_json:
        gradeperiod_sequence.append(gradeperiodrank_dict[question_distribution_info['gradeperiodrank']])
        external_weight_sequence.append(question_distribution_info['weights'])
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(4.8, 3))
    plt.barh(gradeperiod_sequence, external_weight_sequence, color='lightgreen')
    plt.ylabel('权重')
    plt.title('题目年级时期分布直方图')
    plt.savefig('./resource/figure/question_gradeperiod_distribution.png')


def paint_question_progress(grade, period):
    '''
    功能：纯净模式，绘制当前题目当前时期的年级进度图
    '''
    with open(f'./database/states/gradewordbook_question_progress.json', 'r', encoding='utf-8') as file:
        question_progress_json = json.load(file)
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
    right_progress = []
    picked_progress = []  
    accumulate_picked = 0
    accumulate_right = 0
    whole_num = None
    for question_progress_info in question_progress_json:
        if question_progress_info['gradeperiodrank'] == gradeperiodrank_dict[grade + period]:
            for i in range(0, len(question_progress_info['grade_dynamic_right_nums'])):
                accumulate_right += question_progress_info['grade_dynamic_right_nums'][i]
                stage_right = float(question_progress_info['grade_dynamic_right_nums'][i])
                stage_picked = float(question_progress_info['grade_dynamic_picked_nums'][i])
                accumulate_picked += question_progress_info['grade_dynamic_picked_nums'][i]
                right_progress.append(stage_right / stage_picked)
                picked_progress.append(accumulate_picked)
            whole_num = question_progress_info['grade_question_nums']
            break
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(4.8, 3))
    x_major_locator=MultipleLocator(20)
    ax=plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    plt.plot(picked_progress, right_progress)
    plt.title('本年级题目正确率走势')
    plt.savefig('./resource/figure/question_progress.png')
    return (accumulate_right, whole_num)



def pack_pdf_by_gradewordbook(grade, period, hybrid_mode):
    '''
    功能：打包中文内容
    '''
    # 创建PDF文档
    doc = SimpleDocTemplate("./resource/figure/测试情况.pdf")
    # 注册字体
    pdfmetrics.registerFont(TTFont('zh', './resource/figure/字魂白鸽天行体.ttf'))
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(fontName='zh', name='zh', leading=20, fontSize=12, leftIndet=2))
    story = []

    # 写入内容区域
    # 写入词云部分
    paint_wordcloud('gradewordbook')
    story.append(Paragraph(f"本次测试涉及以{grade}{period}为目标，主要涉及以下生字：", styles['zh']))
    image_path = './resource/figure/wordcloud.png'
    image = Image(image_path, width=240, height=150)
    story.append(image)
    # 写入生字权重直方图
    paint_char_distribution('gradewordbook')
    story.append(Paragraph(f"上述生字权重如下所示，越高说明掌握程度较低", styles['zh']))
    image_path = './resource/figure/char_distribution.png'
    image = Image(image_path, width=240, height=150)
    story.append(image)
    # 分为混合模式和纯净模式
    if hybrid_mode is True:
        # 混合模式：绘制年级题目时期分布图
        paint_question_gradeperiod_distribution()
        story.append(Paragraph(f"本次题目年级时期分布如下所示，越长说明掌握程度较低", styles['zh']))
        image_path = './resource/figure/question_gradeperiod_distribution.png'
        image = Image(image_path, width=240, height=150)
        story.append(image)
    else:
        # 纯净模式：绘制当前年级进展图
        (right_num, whole_num) = paint_question_progress(grade, period)
        story.append(Paragraph(f"近期本年级题目正确率走势如下所示，已攻略{right_num}道，剩余{whole_num - right_num}道", styles['zh']))
        image_path = './resource/figure/question_progress.png'
        image = Image(image_path, width=240, height=150)
        story.append(image)
    # 创建PDF文件
    doc.build(story)


def pack_pdf_by_wordbook():
    '''
    功能：打包中文内容
    '''
    # 创建PDF文档
    doc = SimpleDocTemplate("./resource/figure/测试情况.pdf")
    # 注册字体
    pdfmetrics.registerFont(TTFont('zh', './resource/figure/字魂白鸽天行体.ttf'))
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(fontName='zh', name='zh', leading=20, fontSize=12, leftIndet=2))
    story = []
    # 写入内容区域
    # 写入词云部分
    paint_wordcloud('wordbook')
    story.append(Paragraph(f"本次测试涉及以生字本为目标，主要涉及以下生字：", styles['zh']))
    image_path = './resource/figure/wordcloud.png'
    image = Image(image_path, width=240, height=150)
    story.append(image)
    # 写入生字权重直方图
    paint_char_distribution('wordbook')
    story.append(Paragraph(f"上述生字权重如下所示，越高说明掌握程度较低", styles['zh']))
    image_path = './resource/figure/char_distribution.png'
    image = Image(image_path, width=240, height=150)
    story.append(image)
    # 创建PDF文件
    doc.build(story)



if __name__ == "__main__":
    switch_boom = 4
    if switch_boom == 1:
        paint_wordcloud('gradewordbook') 
    elif switch_boom == 2:
        paint_char_distribution('gradewordbook') 
    elif switch_boom == 3:
        pack_pdf_by_wordbook()
    elif switch_boom == 4:
        pack_pdf_by_gradewordbook('四', '下', False) 