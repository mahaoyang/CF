#!/usr/bin/python3
# -*- encoding: utf-8 -*-
import numpy as np
from tqdm import trange
import operator
import sys

sys.path.append('../util')
import util.reader as read


def lfm_train(train_data, F, alpha, beta, step):
    """

    :param train_data:
    :param F: user vector len, item vector len
    :param alpha: regularization factor
    :param beta: learning rate
    :param step: iteration rate
    :return: {itemid:[]},{userid:[]}
    """
    user_vec = {}
    item_vec = {}
    for step_index in trange(step):
        for data_instance in train_data:
            userid, itemid, label = data_instance
            if userid not in user_vec:
                user_vec[userid] = init_model(F)
            if itemid not in item_vec:
                item_vec[itemid] = init_model(F)

        delta = label - model_predict(user_vec[userid], item_vec[itemid])
        for index in range(F):
            user_vec[userid][index] += beta * (
                    delta * item_vec[itemid][index] - alpha *
                    user_vec[userid][index])
            item_vec[itemid][index] += beta * (
                    delta * user_vec[userid][index] - alpha *
                    item_vec[itemid][index])
        beta = beta * 0.9
    return user_vec, item_vec


def init_model(vector_len):
    """

    :param vector_len:
    :return:
    """
    return np.random.randn(vector_len)


def model_predict(user_vector, item_verctor):
    """
    获取用户向量和物品向量的cosine距离
    :param user_vector:
    :param item_verctor:
    :return: num
    """
    res = np.dot(user_vector, item_verctor) / (
            np.linalg.norm(user_vector) * np.linalg.norm(item_verctor))
    return res


def model_train_process():
    """

    :return:
    """
    train_data = read.get_train_data('../data/ratings.csv')
    user_vec, item_vec = lfm_train(train_data, 50, 0.01, 0.1, 100)
    print(user_vec['1'])
    print(item_vec['2455'])
    res = give_recom_result(user_vec, item_vec, '24')
    print(res)


def give_recom_result(user_vec, item_vec, userid):
    """

    :param user_vec:
    :param item_vec:
    :param userid:
    :return:
    """
    fix_num = 10
    if userid not in user_vec:
        return []
    record = dict()
    recom_list = []
    user_vector = user_vec[userid]
    for itemid in item_vec:
        item_vector = item_vec[itemid]
        res = np.dot(user_vector, item_vector) / (
                np.linalg.norm(user_vector) * np.linalg.norm(item_vector))
        record[itemid] = res
    for zuhe in sorted(record.items(), key=operator.itemgetter(1),
                       reverse=True)[:fix_num]:
        itemid = zuhe[0]
        score = round(zuhe[1], 3)
        recom_list.append((itemid, score))
    return recom_list


def ana_recom_result(train_data, userid, recom_list):
    """

    :param train_data:
    :param userid:
    :param recom_list:
    :return:
    """


if __name__ == '__main__':
    model_train_process()
