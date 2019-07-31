#-*- coding:utf-8 _*-
"""
@author:charlesXu
@file: Utils.py
@desc: 实体提取预处理工具类
@time: 2018/08/08
"""

import logging, sys, argparse, re

from functools import reduce

import proprecess_money


def str2bool(v):
    # copy from StackOverflow
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def get_entity(tag_seq, char_seq):
    PER = get_PER_entity(tag_seq, char_seq)
    # LOC = get_LOC_entity(tag_seq, char_seq)
    LOC = get_LOC_entitys(tag_seq, char_seq)
    ORG = get_ORG_entity(tag_seq, char_seq)
    # TIM = get_TIM_entity(tag_seq, char_seq)
    return PER, LOC, ORG


def get_PER_entity(tag_seq, char_seq):
    length = len(char_seq)
    PER = []
    try:
        for i, (char, tag) in enumerate(zip(char_seq, tag_seq)):
            if tag == 'B-PER':
                if 'per' in locals().keys():
                    PER.append(per)
                    del per
                per = char
                if i+1 == length:
                    PER.append(per)
            if tag == 'I-PER':
                per += char
                if i+1 == length:
                    PER.append(per)
            if tag not in ['I-PER', 'B-PER']:
                if 'per' in locals().keys():
                    PER.append(per)
                    del per
                continue
    except Exception as e:
        print("Error is ", e)
    PER = list(set(PER))     #  去重
    return PER


def get_LOC_entity(tag_seq, char_seq):
    '''
    这里需要对输出序列进行判断，对连续序列进行拼接
    :param tag_seq:
    :param char_seq:
    :return:
    '''
    length = len(char_seq)
    LOC = []
    location = []
    for i, (char, tag) in enumerate(zip(char_seq, tag_seq)):
        if tag == 'B-LOC':
            if 'loc' in locals().keys():
                LOC.append(loc)
                del loc
            loc = char
            if i+1 == length:
                LOC.append(loc)
        if tag == 'I-LOC':
            loc += char
            if i+1 == length:
                LOC.append(loc)
        if tag not in ['I-LOC', 'B-LOC']:
            if 'loc' in locals().keys():
                LOC.append(loc)
                del loc
            continue
    return LOC

def get_LOC_entitys(tag_seq, char_seq):
    length = len(char_seq)
    location = []
    LOC = []
    try:
        for i, (char, tag) in enumerate(zip(char_seq, tag_seq)):
            if tag == 'B-LOC' or tag == 'I-LOC':
                # tags = tag.strip().split('-')[1]
                # loc = char
                location.append(char)
            if tag_seq[i] == 0 and tag_seq[i - 1 ] == 'I-LOC':
                t = reduce(lambda x, y: str(x) + str(y), location)
                LOC.append(t)
                location = []
        LOC = list(set(LOC))  # 去重
        for i in range(len(LOC)):
            strs = '中华人民共和国'
            txt = LOC[i]
            if strs in txt:
                LOC.remove(txt)
    except Exception as e:
        print("Error is ", e)
    return LOC

def get_ORG_entity(tag_seq, char_seq):
    length = len(char_seq)
    ORG = []
    try:
        for i, (char, tag) in enumerate(zip(char_seq, tag_seq)):
            if tag == 'B-ORG':
                if 'org' in locals().keys():
                    ORG.append(org)
                    del org
                org = char
                if i+1 == length:
                    ORG.append(org)
            if tag == 'I-ORG':
                org += char
                if i+1 == length:
                    ORG.append(org)
            if tag not in ['I-ORG', 'B-ORG']:
                if 'org' in locals().keys():
                    ORG.append(org)
                    del org
                continue

        ORG = list(set(ORG))  # 去重
        for i in range(len(ORG)):
            # rem = re.compile(r'.*(.*法院).*?')
            str = '法院'
            txt = ORG[i]
            if str in txt:
                ORG.remove(txt)
    except Exception as e:
        print("Error is ", e)
    return ORG

def get_TIM_entity(tag_seq, char_seq):
    '''
    获取时间实体
    :param tag_seq:
    :param char_seq:
    :return:
    '''
    length = len(char_seq)
    TIM = []
    try:
        for i, (char, tag) in enumerate(zip(char_seq, tag_seq)):
            if tag == 'B-TIM':
                if 'tim' in locals().keys():
                    TIM.append(org)
                    del org
                org = char
                if i + 1 == length:
                    TIM.append(org)
            if tag == 'I-TIM':
                org += char
                if i + 1 == length:
                    TIM.append(org)
            if tag not in ['I-TIM', 'B-TIM']:
                if 'tim' in locals().keys():
                    TIM.append(org)
                    del org
                continue

        TIM = list(set(TIM))  # 去重

    except Exception as e:
        print('error is ', e)
    return TIM


def get_MON_entity(text):
    '''
    获取金额实体
    :param text:
    :return:
    '''
    M = []
    MON = []
    tr = proprecess_money.wash_data(text)
    sent = proprecess_money.split_sentence(tr)
    for sentence in sent:
        money = proprecess_money.get_properties_and_values(sentence)
        M.append(money)
        for i in range(len(M)):
            if M[i]:
                MON.append(M[i])
    dup = lambda x, y: x if y in x else x + [y]  # 去重
    MON = reduce(dup, [[], ] + MON)
    return MON

def get_logger(filename):
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)
    handler = logging.FileHandler(filename)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s: %(message)s'))
    logging.getLogger().addHandler(handler)
    return logger
