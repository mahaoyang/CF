import sys
import math
import operator

sys.path.append('../util')
from util import reader


def base_contribute_score():
    return 1  # 基础策略


def update_one_contribute_score(user_click_num):
    return 1 / math.log10(1 + user_click_num)  # 按用户活跃度惩罚活跃用户策略


def update_two_contribute_score(time_one, time_two):
    delata_time = abs(time_one - time_two)
    total_sec = 60 * 60 * 24
    delata_time /= total_sec
    return 1 / (1 + delata_time)


def cal_item_sim(user_click, user_click_time):
    co_appear = dict()
    item_user_click_time = dict()
    for user, itemlist in user_click.items():
        for index_i in range(0, len(itemlist)):
            itemid_i = itemlist[index_i]
            item_user_click_time.setdefault(itemid_i, 0)
            item_user_click_time[itemid_i] += 1
            for index_j in range(index_i + 1, len(itemlist)):
                itemid_j = itemlist[index_j]

                if user + '_' + itemid_i not in user_click_time:
                    click_time_one = 0
                else:
                    click_time_one = user_click_time[user + '_' + itemid_i]
                if user + '_' + itemid_j not in user_click_time:
                    click_time_two = 0
                else:
                    click_time_two = user_click_time[user + '_' + itemid_j]

                co_appear.setdefault(itemid_i, dict())
                co_appear[itemid_i].setdefault(itemid_j, 0)
                co_appear[itemid_i][itemid_j] += update_two_contribute_score(click_time_one, click_time_two)

                co_appear.setdefault(itemid_j, dict())
                co_appear[itemid_j].setdefault(itemid_i, 0)
                co_appear[itemid_j][itemid_i] += update_two_contribute_score(click_time_one, click_time_two)

    item_sim_score = dict()
    item_sim_score_sorted = dict()
    for itemid_i, relate_item in co_appear.items():
        for itemid_j, co_time in relate_item.items():
            sim_score = co_time / math.sqrt(item_user_click_time[itemid_i] * item_user_click_time[itemid_j])
            item_sim_score.setdefault(itemid_i, dict())
            item_sim_score[itemid_i].setdefault(itemid_j, 0)
            item_sim_score[itemid_i][itemid_j] = sim_score
    for itemid in item_sim_score:
        item_sim_score_sorted[itemid] = sorted(item_sim_score[itemid].items(), key=operator.itemgetter(1),
                                               reverse=True)
    return item_sim_score_sorted


def cal_recom_result(sim_info, user_click):
    recent_click_num = 3
    topk = 5
    recom_info = dict()
    for user in user_click:
        click_list = user_click[user]
        recom_info.setdefault(user, dict())
        for itemid in click_list[:recent_click_num]:
            if itemid not in sim_info:
                continue
            for itemsimzuhe in sim_info[itemid][:topk]:
                itemsimid = itemsimzuhe[0]
                itemsimscore = itemsimzuhe[1]
                recom_info[user][itemsimid] = itemsimscore
    return recom_info


def debug_itemsim(item_info, sim_info):
    fixed_itemid = '1'
    if fixed_itemid not in item_info:
        print('invalid itemid')
        return
    [title_fix, genres_fix] = item_info[fixed_itemid]
    for zuhe in sim_info[fixed_itemid][:5]:
        itemid_sim = zuhe[0]
        sim_score = zuhe[1]
        if itemid_sim not in item_info:
            continue
        [title, genres] = item_info[itemid_sim]
        print('%s\t%s\tsim:%s\t%s\t%s' % (title_fix, genres_fix, title, genres, sim_score))


def debug_recomresult(recom_result, item_info):
    user_id = '1'
    if user_id not in recom_result:
        print('invalid result')
        return
    for zuhe in sorted(recom_result[user_id].items(), key=operator.itemgetter(1), reverse=True):
        itemid, score = zuhe
        if itemid not in item_info:
            continue
        print(','.join(item_info[itemid]) + '\t%s' % score)


def main_flow():
    user_click, user_click_time = reader.get_user_click('../data/ratings.csv')
    item_info = reader.get_item_info('../data/movies.csv')
    sim_info = cal_item_sim(user_click, user_click_time)
    debug_itemsim(item_info, sim_info)
    # recom_results = cal_recom_result(sim_info, user_click)
    # debug_itemsim(recom_results, item_info)
    # return recom_results


if __name__ == '__main__':
    res = main_flow()
    # print(res['1'])
