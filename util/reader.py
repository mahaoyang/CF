import os


def get_user_click(rating_file):
    if not os.path.exists(rating_file):
        return dict(), dict()
    with open(rating_file, 'r') as fp:
        num = 0
        user_click = dict()
        user_click_time = dict()
        for line in fp:
            if num == 0:
                num += 1
                continue
            item = line.strip().split(',')
            if len(item) < 4:
                continue
            [userid, itemid, rating, timestamp] = item
            if userid + '_' + itemid not in user_click_time:
                user_click_time[userid + '_' + itemid] = int(timestamp)
            if float(rating) < 3.0:
                continue
            if userid not in user_click:
                user_click[userid] = []
            user_click[userid].append(itemid)
    return user_click, user_click_time


def get_item_info(item_file):
    if not os.path.exists(item_file):
        return dict()
    with open(item_file, 'r') as fp:
        num = 0
        item_info = dict()
        for line in fp:
            if num == 0:
                num += 1
                continue
            item = line.strip().split(',')
            if len(item) < 3:
                continue
            if len(item) == 3:
                [itemid, title, generes] = item
            elif len(item) > 3:
                itemid = item[0]
                generes = item[-1]
                title = ','.join(item[1:-1])
            if itemid not in item_info:
                item_info[itemid] = [title, generes]
    return item_info


def get_ave_score(input_file):
    """
    获取每个item相对于用户的平均分
    :param input_file:
    :return:
    """
    if not os.path.exists(input_file):
        return dict()
    num = 0
    record_dict = dict()
    score_dict = dict()
    with open(input_file, 'r') as fp:
        for line in fp:
            if num == 0:
                num += 1
                continue
            item = line.strip().split(',')
            if len(item) < 4:
                continue
            userid, itemid, rating = item[0], item[1], float(item[2])
            if itemid not in record_dict:
                record_dict[itemid] = [0, 0]
            record_dict[itemid][0] += 1
            record_dict[itemid][1] += rating
    for itemid in record_dict:
        score_dict[itemid] = round(
            record_dict[itemid][1] / record_dict[itemid][0], 3)
    return score_dict


def get_train_data(input_file):
    """
    获取user-item-pos/neg 三元组，即用户对item喜好的正负偏向
    :param input_file:
    :return:
    """
    if not os.path.exists(input_file):
        return list()
    score_dict = get_ave_score(input_file)
    neg_dict = dict()
    pos_dict = dict()
    train_data = list()
    score_thr = 4.0
    num = 0
    with open(input_file, 'r') as fp:
        for line in fp:
            if num == 0:
                num += 1
                continue
            item = line.strip().split(',')
            if len(item) < 4:
                continue
            userid, itemid, rating = item[0], item[1], float(item[2])
            if userid not in pos_dict:
                pos_dict[userid] = []
            if userid not in neg_dict:
                neg_dict[userid] = []
            if rating >= score_thr:
                pos_dict[userid].append((itemid, 1))
            else:
                score = score_dict.get(itemid, 0)
                neg_dict[userid].append((itemid, score))
    for userid in pos_dict:
        data_num = min(len(pos_dict[userid]), len(neg_dict.get(userid, [])))
        if data_num > 0:
            train_data += [(userid, zuhe[0], zuhe[1]) for zuhe in
                           pos_dict[userid]]
        else:
            continue
        sorted_neg_list = sorted(neg_dict[userid],
                                 key=lambda element: element[1],
                                 reverse=True)[:data_num]
        train_data += [(userid, zuhe[0], 0) for zuhe in sorted_neg_list]
    return train_data


if __name__ == '__main__':
    # user_click = get_user_click('../data/ratings.csv')
    # print(len(user_click))
    # print(user_click.get('1'))
    # item_info = get_item_info('../data/movies.csv')
    # print(len(item_info))
    # print(item_info.get('1'))
    # score_dict = get_ave_score('../data/ratings.csv')
    # print(len(score_dict))
    # print(score_dict['31'])
    train_data = get_train_data('../data/ratings.csv')
    print(len(train_data))
    print(train_data[:40])
