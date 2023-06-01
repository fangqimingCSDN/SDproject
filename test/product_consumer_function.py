# -*- coding: utf-8 -*-


"""
@File    : product_consumer_function.py
@Author  : xiaoming
@Time    : 2023-5-24 14:39
"""
from translate import Translator
import jieba
import re
from collections import Counter
from logger import logger



def translate_txt(translator_list):

    #在任何两种语言之间，中文翻译成英文
    translator=Translator(to_lang="en",from_lang="zh")
    # translation = translator.translate("你好")
    # logger.info(translation)
    # translator_list = [translator.translate(x) for x in q_cut_list]
    translator_list = translator.translate(','.join(translator_list))
    prompt = translator_list
    logger.info(f"The translated content is:{prompt}")
    return prompt


def jieba_deal(strs, prompt_weight=[], no_prompt_weight=[], other_list=[[], []]):
    #     jieba.enable_paddle()
    seg_list_gen = jieba.cut(strs, use_paddle=True)  # 使用paddle模式
    seg_list = list(seg_list_gen)
    logger.info("Paddle Mode: " + ','.join(list(seg_list)))

    # 加载停用词表
    stopwords_file = 'stopwords.txt'
    # stopwords_file = 'cn_stopwords.txt'  哈工大停用词表  https://github.com/goto456/stopwords
    with open(stopwords_file, "r") as words:  # ,encoding='utf-8'
        stopwords = [i.strip() for i in words]
    stopwords.extend(['.', '（', '）', '-', '——', '(', ')', ' ', '，'])  # 此处可以添加一些停用词表中没有的停用词

    q_cut_list = [i for i in seg_list if not i.strip() in stopwords]  # 去除停用词
    if prompt_weight:
        q_cut_list_str = str(q_cut_list)
        for word in prompt_weight:
            if word:
                num = 1
                if other_list:
                    word_list = [x for x in other_list[0] if word in x[0]]
                    if word_list:
                        num = word_list[0][1]
                q_cut_list_str = q_cut_list_str.replace(word, "{" * num + word + "}" * num)
        q_cut_list = eval(q_cut_list_str)
    if no_prompt_weight:
        q_cut_list_str = str(q_cut_list)
        for word in no_prompt_weight:
            if word:
                num = 1
                if other_list:
                    word_list = [x for x in other_list[1] if word in x[0]]
                    if word_list:
                        num = word_list[0][1]
                q_cut_list_str = q_cut_list_str.replace(word, "[" * num + word + "]" * num)
        q_cut_list = eval(q_cut_list_str)
    logger.info(f"After you stop using words:{q_cut_list}")
    return q_cut_list


def return_weight(strings):

    #     string = "Hello, （在路上）（车）(天津)![公交车]"
    pattern = r"\(.*?\)|\[.*?\]|\（.*?\）|\【.*?\】"
    result = re.findall(pattern, strings)
    prompt = [x.strip()[1:-1] for x in result if '[' not in x]
    no_prompt = [x.strip()[1:-1] for x in result if '[' in x]

    weight_list = get_weight_num(prompt, no_prompt)

    prompt_weight = [x[0] for x in [jieba_deal(x) for x in prompt] if x != []]
    no_prompt_weight = [x[0] for x in [jieba_deal(x) for x in no_prompt] if x != []]
    return prompt_weight, no_prompt_weight, weight_list


def get_weight_num(prompt, no_prompt):
    prompt_list = []
    for word in prompt:
        weight_i = 1
        if "（" in word or "(" in word:
            for bye in word:
                #             logger.info(bye)
                if "（" == bye or "(" == bye:
                    weight_i += 1
        #                 logger.info(weight_i)
        prompt_list.append((word.replace("（", "").replace("(", "").replace(")", "").replace("）", ""), weight_i))

    no_prompt_list = []
    for word in no_prompt:
        weight_i = 1
        if "[" in word or "【" in word:
            for bye in word:
                #             logger.info(bye)
                if "[" == bye or "【" == bye:
                    weight_i += 1
        #                 logger.info(weight_i)
        no_prompt_list.append((word.replace("[", "").replace("【", "").replace("]", "").replace("】", ""), weight_i))
    return [prompt_list, no_prompt_list]



def is_chinese(word):
    for ch in word:
        if ord(ch) > 255:
            return True
    return False

def get_weight_set_en(strs, weight_list=[(),()]):
    strs = strs.replace("（","").replace("(","").replace(")","").replace("）","").replace("[","").replace("【","").replace("]","").replace("】","")
    q_cut_list_str = str(strs)
    if weight_list[0]:
        repeat = []
        for word in weight_list[0]:
            if word:
                if word not in repeat:
                    repeat.append(word)
                elif word in repeat:
                    continue
                num = word[1]
                q_cut_list_str=q_cut_list_str.replace(word[0],"{"*num+word[0]+"}"*num)
    if weight_list[1]:
        repeat = []
        for word in weight_list[1]:
            if word:
                if word not in repeat:
                    repeat.append(word)
                elif word in repeat:
                    continue
                num = word[1]
                q_cut_list_str=q_cut_list_str.replace(word[0],"["*num+word[0]+"]"*num)
    return q_cut_list_str

def schedule_tag_del(strs):
    # strs = 'Sun Youhai, 你好, Professor, and Ph.D. Supervisor of the Law School of Tianjin University, Participation, Hello, Wedding, On the bus., Outside, Hei, one spot, flourishing, On the road, Walk'
    # strs = "我在天津， 参加同学（婚礼），在公交车上，人很少， 外面很【[黑]】， 在一处不是很繁华的路上行走"
    prompt_weight, no_prompt_weight, weight_list = return_weight(strs)
    logger.info(f"权重文件：重要：{prompt_weight}， 非重要：{no_prompt_weight}")
    aList = [is_chinese(word) for word in strs.split(',')]
    counter = Counter(aList)
    max_item = max(counter.items(), key=lambda x: x[1])
    if max_item[0]:  # 中文处理
        logger.info(f"中文处理过程....")
        cn_list = jieba_deal(strs=strs, prompt_weight=prompt_weight, no_prompt_weight=no_prompt_weight,
                             other_list=weight_list)
        sn_txt = translate_txt(cn_list)
        # logger.info(sn_txt)
        return sn_txt
    else:  # 英文处理
        logger.info(f"英文处理过程....")
        sn_txt = get_weight_set_en(strs, weight_list)
        logger.info(sn_txt)
        return sn_txt



if __name__ == '__main__':
    a = 'Sun Youhai, 你好, Professor, and Ph.D. Supervisor of the Law School of Tianjin University, Participation, Hello, Wedding, On the bus., Outside, Hei, one spot, flourishing, On the road, Walk'
    a = "我在天津， 参加同学（婚礼），在公交车上，人很少， 外面很【[黑]】， 在一处不是很繁华的路上行走"
    a = "tianjin, attending, classmate, (wedding), bus, outside, [[black]], one place, bustling, on the road, walking,tianjin, attending, classmate, {wedding}, bus, outside, [[black]], one place, bustling, on the road, walking"

    logger.info(schedule_tag_del(a))

    # prompt_weight, no_prompt_weight, weight_list = return_weight(a)
    # logger.info(f"权重文件：重要：{prompt_weight}， 非重要：{no_prompt_weight}")
    # aList = [is_chinese(word) for word in a.split(',')]
    # counter = Counter(aList)
    # max_item = max(counter.items(), key=lambda x: x[1])
    # if max_item[0]:  # 中文处理
    #     logger.info(f"中文处理过程....")
    #     cn_list = jieba_deal(strs=a, prompt_weight=prompt_weight, no_prompt_weight=no_prompt_weight,
    #                          other_list=weight_list)
    #     sn_txt = translate_txt(cn_list)
    #     logger.info(sn_txt)
    # else:  # 英文处理
    #     logger.info(f"英文处理过程....")
    #     sn_txt = get_weight_set_en(a, weight_list)
    #     logger.info(sn_txt)
