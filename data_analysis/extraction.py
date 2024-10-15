from typing import List, Tuple
from utils.common_ops import unix_to_iso_with_timezone, iso_to_unix
from datetime import datetime
import statistics
import ast
import pandas as pd
from collections import defaultdict


def get_time_data(ct_time, csv_file):
    try:
        ct = ct_time
        if isinstance(ct, str):
            iso_time = str(ct_time)
            ct = iso_to_unix(iso_time)
        else:
            iso_time = unix_to_iso_with_timezone(ct)

        iso_split = iso_time.split("T")
        iso_date = iso_split[0]
        iso_split_time = iso_split[1].split("+")
        iso_time = iso_split_time[0]
        swing_ISO_time = iso_date + " " + iso_time
        return swing_ISO_time
    except Exception as e:
        print(f"Unable to get the Time Data from {csv_file} file : {e}")


def get_coin_data(csv_file) -> List[str]:
    try:
        split_data = csv_file.split(".")
        coin_name = split_data[0][6:]
        tf_data_coma = split_data[1].split(",")
        tf_data_strip = tf_data_coma[1].strip()
        tf_data_under = tf_data_strip.split("_")
        # Modified the coin name with USDT.P
        coin_data = [coin_name + "." + "P", int(tf_data_under[0])]
        print("coin_data ==>", coin_data)
        print(f"Coin data extracted success full form {csv_file} file")
        return coin_data
    except Exception as e:
        print(f"Unable to get the Coin Data from {csv_file} file : {e}")


def get_swing_col(row_num, row):
    swing_col = "NA"
    if row["Higher High"] == 1:
        swing_col = "Higher High"
    elif row["Lower High"] == 1:
        swing_col = "Lower High"
    elif row["Higher Low"] == 1:
        swing_col = "Higher Low"
    elif row["Lower Low"] == 1:
        swing_col = "Lower Low"
    elif (row["Lower Low"] == 0) and (row["Higher High"] == 0) and (row["Lower High"] == 0) and (row["Higher Low"] == 0):
        swing_col = "NA"
    else:
        swing_col = "NaN"
    return [row_num, swing_col]


def get_swing_direction(swing_1_col, swing_2_col):
    if (swing_1_col == "Higher High" or swing_1_col == "Lower High") and (swing_2_col == "Lower Low" or swing_2_col == "Higher Low"):
        swing_direction = "down_swing"
    elif (swing_1_col == "Lower Low" or swing_1_col == "Higher Low") and (swing_2_col == "Higher High" or swing_2_col == "Lower High"):
        swing_direction = "up_swing"
    elif (swing_1_col == "Higher High" or swing_1_col == "Lower High") and (swing_2_col == "Higher High" or swing_2_col == "Lower High"):
        swing_direction = "up_swing"
    elif (swing_1_col == "Lower Low" or swing_1_col == "Higher Low") and (swing_2_col == "Lower Low" or swing_2_col == "Higher Low"):
        swing_direction = "down_swing"
    else:
        swing_direction = "NA"
    return swing_direction


def get_swing_percentage(swing_dir, row_1, row_2):
    if swing_dir == "up_swing":
        old_price = row_1["low"]
        new_price = row_2["high"]
        per_change = ((new_price-old_price)/old_price)*100
        per_change = round(per_change, 3)
    elif swing_dir == "down_swing":
        old_price = row_1["high"]
        new_price = row_2["low"]
        per_change = ((new_price-old_price)/old_price)*100
        per_change = round(per_change, 3)
    else:
        per_change = "NA"
    return per_change


def get_randomness_percentage(swing_dir, swing_1_row_num, swing_2_row_num, df):
    rand_per_lst = []
    if swing_dir == "down_swing":
        for i in range(swing_1_row_num, swing_2_row_num):
            current_val = df.iloc[i]["high"]
            next_val = df.iloc[i+1]["high"]
            if current_val > next_val:
                rand_per = 0
            else:
                old_price = current_val
                new_price = next_val
                rand_per = ((new_price-old_price)/old_price)*100
                rand_per = round(rand_per, 4)
            rand_per_lst.append(rand_per)
    if swing_dir == "up_swing":
        for i in range(swing_1_row_num, swing_2_row_num):
            current_val = df.iloc[i]["low"]
            next_val = df.iloc[i+1]["low"]
            if current_val < next_val:
                rand_per = 0
            else:
                old_price = current_val
                new_price = next_val
                rand_per = ((new_price-old_price)/old_price)*100
                rand_per = round(rand_per, 4)
            rand_per_lst.append(rand_per)
    swing_rand_per = sum(rand_per_lst)
    swing_rand_per = round(swing_rand_per, 3)
    return swing_rand_per


def get_high_FB(false_breakout_lst):
    high_fb = 0
    for swing in false_breakout_lst:
        if swing[1] == "Higher High" or swing[1] == "Lower High":
            high_fb += 1
    return high_fb


def get_low_FB(false_breakout_lst):
    low_fb = 0
    for swing in false_breakout_lst:
        if swing[1] == "Lower Low" or swing[1] == "Higher Low":
            low_fb += 1
    return low_fb


def get_last_FB(false_breakout_lst, df, csv_file):
    if (len(false_breakout_lst) > 0):
        last_fb = false_breakout_lst[-1]
        last_fb_record = last_fb[0]
        last_fb_unix_time = df.iloc[last_fb_record]["time"]
        last_fb_iso_time = get_time_data(last_fb_unix_time, csv_file)
        return last_fb_iso_time
    else:
        return "NA"


def get_fb_lst_with_time(false_breakout_lst, df, csv_file):
    fb_lst_with_time = []
    for swing in false_breakout_lst:
        fb_time = df.iloc[swing[2]]["time"]
        fb_time_iso = get_time_data(fb_time, csv_file)
        swing.append(fb_time_iso)
        fb_lst_with_time.append(swing)
    return fb_lst_with_time


def get_swing_time(swing_1_row_num, swing_2_row_num, df):
    timestamp1 = df.iloc[swing_1_row_num]["time"]
    timestamp2 = df.iloc[swing_2_row_num]["time"]

    # Convert timestamps to datetime objects
    dt1 = datetime.fromtimestamp(timestamp1)
    dt2 = datetime.fromtimestamp(timestamp2)

    # Calculate the difference in minutes
    difference_in_minutes = (dt2 - dt1).total_seconds() / 60
    difference_in_hours = round(difference_in_minutes/60, 2)

    return difference_in_hours


def get_swing_rsi_diff(swing_dir, swing_1_RSI, swing_2_RSI):
    swing_rsi_diff = 0
    if swing_dir == "up_swing":
        swing_rsi_diff = swing_2_RSI - swing_1_RSI
    if swing_dir == "down_swing":
        swing_rsi_diff = swing_1_RSI - swing_2_RSI
    swing_rsi_diff = round(swing_rsi_diff, 2)
    return swing_rsi_diff


def get_swing_per_info(coin_name, coin_time_tf, swing_per_lst, pstv_swing_per_lst, neg_swing_per_lst):
    if len(pstv_swing_per_lst) >= 10:
        t_10_lrg_pp_sp_lst = sorted(pstv_swing_per_lst, reverse=True)[:10]
        t_10_sml_pp_sp_lst = sorted(pstv_swing_per_lst, reverse=False)[:10]
        t_5_lrg_pp_sp_lst = str(sorted(pstv_swing_per_lst, reverse=True)[:5])
    elif len(pstv_swing_per_lst) > 0 and len(pstv_swing_per_lst) < 10:
        t_10_lrg_pp_sp_lst = sorted(pstv_swing_per_lst, reverse=True)[
            :len(pstv_swing_per_lst)]
        t_10_sml_pp_sp_lst = sorted(pstv_swing_per_lst, reverse=False)[
            :len(pstv_swing_per_lst)]
        t_5_lrg_pp_sp_lst = str(sorted(pstv_swing_per_lst, reverse=True)[:5])
    else:
        t_10_lrg_pp_sp_lst = [0]
        t_10_sml_pp_sp_lst = [0]
        t_5_lrg_pp_sp_lst = str([0])
    if len(neg_swing_per_lst) >= 10:
        t_10_lrg_np_sp_lst = sorted(neg_swing_per_lst, reverse=False)[:10]
        t_10_sml_np_sp_lst = sorted(neg_swing_per_lst, reverse=True)[:10]
        t_5_lrg_np_sp_lst = str(sorted(neg_swing_per_lst, reverse=False)[:5])
    elif len(neg_swing_per_lst) > 0 and len(neg_swing_per_lst) < 10:
        t_10_lrg_np_sp_lst = sorted(neg_swing_per_lst, reverse=True)[
            :len(neg_swing_per_lst)]
        t_10_sml_np_sp_lst = sorted(neg_swing_per_lst, reverse=False)[
            :len(neg_swing_per_lst)]
        t_5_lrg_np_sp_lst = str(sorted(neg_swing_per_lst, reverse=False)[:5])
    else:
        t_10_lrg_np_sp_lst = [0]
        t_10_sml_np_sp_lst = [0]
        t_5_lrg_np_sp_lst = str([0])
    # all swing info
    all_swing_count = len(swing_per_lst)
    all_swings_pp_count = len(pstv_swing_per_lst)
    all_swings_np_count = len(neg_swing_per_lst)
    all_swings_pp_sum = round((sum(pstv_swing_per_lst)), 2)
    all_swings_np_sum = round((sum(neg_swing_per_lst)), 2)
    all_swing_per_sum = round((all_swings_pp_sum + abs(all_swings_np_sum)), 2)
    all_swings_pp_avg = round((statistics.mean(pstv_swing_per_lst)), 2)
    all_swings_np_avg = round((statistics.mean(neg_swing_per_lst)), 2)
    all_swings_pp_med = round((statistics.median(pstv_swing_per_lst)), 2)
    all_swings_np_med = round((statistics.median(neg_swing_per_lst)), 2)

    # Top_10 Info
    t_10_lrg_pp_sp_sum = round((sum(t_10_lrg_pp_sp_lst)), 2)
    t_10_lrg_np_sp_sum = round((sum(t_10_lrg_np_sp_lst)), 2)
    t_10_lrg_pp_sp_avg = round((statistics.mean(t_10_lrg_pp_sp_lst)), 2)
    t_10_lrg_np_sp_avg = round((statistics.mean(t_10_lrg_np_sp_lst)), 2)
    t_10_lrg_pp_sp_med = round((statistics.median(t_10_lrg_pp_sp_lst)), 2)
    t_10_lrg_np_sp_med = round((statistics.median(t_10_lrg_np_sp_lst)), 2)

    t_10_sml_pp_sp_sum = round((sum(t_10_sml_pp_sp_lst)), 2)
    t_10_sml_np_sp_sum = round((sum(t_10_sml_np_sp_lst)), 2)
    t_10_sml_pp_sp_avg = round((statistics.mean(t_10_sml_pp_sp_lst)), 2)
    t_10_sml_np_sp_avg = round((statistics.mean(t_10_sml_np_sp_lst)), 2)
    t_10_sml_pp_sp_med = round((statistics.median(t_10_sml_pp_sp_lst)), 2)
    t_10_sml_np_sp_med = round((statistics.median(t_10_sml_np_sp_lst)), 2)

    swing_per_analysis_lst = [coin_name, coin_time_tf, all_swing_count, all_swings_pp_count, all_swings_np_count, all_swing_per_sum, all_swings_pp_sum, all_swings_np_sum, all_swings_pp_avg, all_swings_np_avg, all_swings_pp_med, all_swings_np_med, t_5_lrg_pp_sp_lst,
                              t_5_lrg_np_sp_lst, t_10_lrg_pp_sp_sum, t_10_lrg_np_sp_sum, t_10_lrg_pp_sp_avg, t_10_lrg_np_sp_avg, t_10_lrg_pp_sp_med, t_10_lrg_np_sp_med, t_10_sml_pp_sp_sum, t_10_sml_np_sp_sum, t_10_sml_pp_sp_avg, t_10_sml_np_sp_avg, t_10_sml_pp_sp_med, t_10_sml_np_sp_med]

    return swing_per_analysis_lst


def get_swing_pstv_per_range_info(coin_name, coin_time_tf, pstv_swing_per_lst):
    if len(pstv_swing_per_lst) > 0:
        range_1_pp_lst = [per for per in pstv_swing_per_lst if 0 < per <= 1]
        if len(range_1_pp_lst) > 0:
            sp_pp_cnt_0_1 = len(range_1_pp_lst)
            sp_pp_sum_0_1 = round(sum(range_1_pp_lst), 2)
            sp_pp_avg_0_1 = round(statistics.mean(range_1_pp_lst), 2)
        else:
            sp_pp_cnt_0_1 = 0
            sp_pp_sum_0_1 = 0
            sp_pp_avg_0_1 = 0
    else:
        range_1_pp_lst = []

    if len(pstv_swing_per_lst) > 0:
        range_2_pp_lst = [per for per in pstv_swing_per_lst if 1 < per <= 2]
        if len(range_2_pp_lst) > 0:
            sp_pp_cnt_1_2 = len(range_2_pp_lst)
            sp_pp_sum_1_2 = round(sum(range_2_pp_lst), 2)
            sp_pp_avg_1_2 = round(statistics.mean(range_2_pp_lst), 2)
        else:
            sp_pp_cnt_1_2 = 0
            sp_pp_sum_1_2 = 0
            sp_pp_avg_1_2 = 0
    else:
        range_2_pp_lst = []

    # small_range_pp_lst
    if len(pstv_swing_per_lst) > 0:
        small_range_pp_lst = [
            per for per in pstv_swing_per_lst if 0 < per <= 2]
        if len(small_range_pp_lst) > 0:
            sp_pp_cnt_0_2 = len(small_range_pp_lst)
            sp_pp_sum_0_2 = round(sum(small_range_pp_lst), 2)
            sp_pp_avg_0_2 = round(statistics.mean(small_range_pp_lst), 2)
        else:
            sp_pp_cnt_0_2 = 0
            sp_pp_sum_0_2 = 0
            sp_pp_avg_0_2 = 0
    else:
        small_range_pp_lst = []

    if len(pstv_swing_per_lst) > 0:
        range_3_pp_lst = [per for per in pstv_swing_per_lst if 2 < per <= 3]
        if len(range_3_pp_lst) > 0:
            sp_pp_cnt_2_3 = len(range_3_pp_lst)
            sp_pp_sum_2_3 = round(sum(range_3_pp_lst), 2)
            sp_pp_avg_2_3 = round(statistics.mean(range_3_pp_lst), 2)
        else:
            sp_pp_cnt_2_3 = 0
            sp_pp_sum_2_3 = 0
            sp_pp_avg_2_3 = 0
    else:
        range_3_pp_lst = []

    if len(pstv_swing_per_lst) > 0:
        range_4_pp_lst = [per for per in pstv_swing_per_lst if 3 < per <= 4]
        if len(range_4_pp_lst) > 0:
            sp_pp_cnt_3_4 = len(range_4_pp_lst)
            sp_pp_sum_3_4 = round(sum(range_4_pp_lst), 2)
            sp_pp_avg_3_4 = round(statistics.mean(range_4_pp_lst), 2)
        else:
            sp_pp_cnt_3_4 = 0
            sp_pp_sum_3_4 = 0
            sp_pp_avg_3_4 = 0
    else:
        range_4_pp_lst = []

    if len(pstv_swing_per_lst) > 0:
        medium_range_pp_lst = [
            per for per in pstv_swing_per_lst if 2 < per <= 4]
        if len(medium_range_pp_lst) > 0:
            sp_pp_cnt_2_4 = len(medium_range_pp_lst)
            sp_pp_sum_2_4 = round(sum(medium_range_pp_lst), 2)
            sp_pp_avg_2_4 = round(statistics.mean(medium_range_pp_lst), 2)
        else:
            sp_pp_cnt_2_4 = 0
            sp_pp_sum_2_4 = 0
            sp_pp_avg_2_4 = 0
    else:
        medium_range_pp_lst = []

    if len(pstv_swing_per_lst) > 0:
        range_5_pp_lst = [per for per in pstv_swing_per_lst if 4 < per <= 5]
        if len(range_5_pp_lst) > 0:
            sp_pp_cnt_4_5 = len(range_5_pp_lst)
            sp_pp_sum_4_5 = round(sum(range_5_pp_lst), 2)
            sp_pp_avg_4_5 = round(statistics.mean(range_5_pp_lst), 2)
        else:
            sp_pp_cnt_4_5 = 0
            sp_pp_sum_4_5 = 0
            sp_pp_avg_4_5 = 0
    else:
        range_5_pp_lst = []

    if len(pstv_swing_per_lst) > 0:
        range_6_pp_lst = [per for per in pstv_swing_per_lst if 5 < per <= 6]
        if len(range_6_pp_lst) > 0:
            sp_pp_cnt_5_6 = len(range_6_pp_lst)
            sp_pp_sum_5_6 = round(sum(range_6_pp_lst), 2)
            sp_pp_avg_5_6 = round(statistics.mean(range_6_pp_lst), 2)
        else:
            sp_pp_cnt_5_6 = 0
            sp_pp_sum_5_6 = 0
            sp_pp_avg_5_6 = 0
    else:
        range_6_pp_lst = []

    if len(pstv_swing_per_lst) > 0:
        range_7_pp_lst = [per for per in pstv_swing_per_lst if 6 < per <= 7]
        if len(range_7_pp_lst) > 0:
            sp_pp_cnt_6_7 = len(range_7_pp_lst)
            sp_pp_sum_6_7 = round(sum(range_7_pp_lst), 2)
            sp_pp_avg_6_7 = round(statistics.mean(range_7_pp_lst), 2)
        else:
            sp_pp_cnt_6_7 = 0
            sp_pp_sum_6_7 = 0
            sp_pp_avg_6_7 = 0
    else:
        range_7_pp_lst = []

    # large_range_pp_lst
    if len(pstv_swing_per_lst) > 0:
        large_range_pp_lst = [
            per for per in pstv_swing_per_lst if 4 < per <= 7]
        if len(large_range_pp_lst) > 0:
            sp_pp_cnt_4_7 = len(large_range_pp_lst)
            sp_pp_sum_4_7 = round(sum(large_range_pp_lst), 2)
            sp_pp_avg_4_7 = round(statistics.mean(large_range_pp_lst), 2)
        else:
            sp_pp_cnt_4_7 = 0
            sp_pp_sum_4_7 = 0
            sp_pp_avg_4_7 = 0
    else:
        large_range_pp_lst = []

    if len(pstv_swing_per_lst) > 0:
        range_8_pp_lst = [per for per in pstv_swing_per_lst if 7 < per <= 9]
        if len(range_8_pp_lst) > 0:
            sp_pp_cnt_7_9 = len(range_8_pp_lst)
            sp_pp_sum_7_9 = round(sum(range_8_pp_lst), 2)
            sp_pp_avg_7_9 = round(statistics.mean(range_8_pp_lst), 2)
        else:
            sp_pp_cnt_7_9 = 0
            sp_pp_sum_7_9 = 0
            sp_pp_avg_7_9 = 0
    else:
        range_8_pp_lst = []

    if len(pstv_swing_per_lst) > 0:
        range_9_pp_lst = [per for per in pstv_swing_per_lst if 9 < per <= 11]
        if len(range_9_pp_lst) > 0:
            sp_pp_cnt_9_11 = len(range_9_pp_lst)
            sp_pp_sum_9_11 = round(sum(range_9_pp_lst), 2)
            sp_pp_avg_9_11 = round(statistics.mean(range_9_pp_lst), 2)
        else:
            sp_pp_cnt_9_11 = 0
            sp_pp_sum_9_11 = 0
            sp_pp_avg_9_11 = 0
    else:
        range_9_pp_lst = []

    if len(pstv_swing_per_lst) > 0:
        range_10_pp_lst = [per for per in pstv_swing_per_lst if 11 < per <= 13]
        if len(range_10_pp_lst) > 0:
            sp_pp_cnt_11_13 = len(range_10_pp_lst)
            sp_pp_sum_11_13 = round(sum(range_10_pp_lst), 2)
            sp_pp_avg_11_13 = round(statistics.mean(range_10_pp_lst), 2)
        else:
            sp_pp_cnt_11_13 = 0
            sp_pp_sum_11_13 = 0
            sp_pp_avg_11_13 = 0
    else:
        range_10_pp_lst = []

    if len(pstv_swing_per_lst) > 0:
        range_11_pp_lst = [per for per in pstv_swing_per_lst if 13 < per <= 15]
        if len(range_11_pp_lst) > 0:
            sp_pp_cnt_13_15 = len(range_11_pp_lst)
            sp_pp_sum_13_15 = round(sum(range_11_pp_lst), 2)
            sp_pp_avg_13_15 = round(statistics.mean(range_11_pp_lst), 2)
        else:
            sp_pp_cnt_13_15 = 0
            sp_pp_sum_13_15 = 0
            sp_pp_avg_13_15 = 0
    else:
        range_11_pp_lst = []

    # extra_large_pp_lst
    if len(pstv_swing_per_lst) > 0:
        extra_large_range_pp_lst = [
            per for per in pstv_swing_per_lst if 7 < per <= 15]
        if len(extra_large_range_pp_lst) > 0:
            sp_pp_cnt_7_15 = len(extra_large_range_pp_lst)
            sp_pp_sum_7_15 = round(sum(extra_large_range_pp_lst), 2)
            sp_pp_avg_7_15 = round(
                statistics.mean(extra_large_range_pp_lst), 2)
        else:
            sp_pp_cnt_7_15 = 0
            sp_pp_sum_7_15 = 0
            sp_pp_avg_7_15 = 0
    else:
        extra_large_range_pp_lst = []

    if len(pstv_swing_per_lst) > 0:
        range_12_pp_lst = [per for per in pstv_swing_per_lst if 15 < per <= 18]
        if len(range_12_pp_lst) > 0:
            sp_pp_cnt_15_18 = len(range_12_pp_lst)
            sp_pp_sum_15_18 = round(sum(range_12_pp_lst), 2)
            sp_pp_avg_15_18 = round(statistics.mean(range_12_pp_lst), 2)
        else:
            sp_pp_cnt_15_18 = 0
            sp_pp_sum_15_18 = 0
            sp_pp_avg_15_18 = 0
    else:
        range_12_pp_lst = []

    if len(pstv_swing_per_lst) > 0:
        range_13_pp_lst = [per for per in pstv_swing_per_lst if 18 < per <= 22]
        if len(range_13_pp_lst) > 0:
            sp_pp_cnt_18_22 = len(range_13_pp_lst)
            sp_pp_sum_18_22 = round(sum(range_13_pp_lst), 2)
            sp_pp_avg_18_22 = round(statistics.mean(range_13_pp_lst), 2)
        else:
            sp_pp_cnt_18_22 = 0
            sp_pp_sum_18_22 = 0
            sp_pp_avg_18_22 = 0
    else:
        range_13_pp_lst = []

    if len(pstv_swing_per_lst) > 0:
        range_14_pp_lst = [per for per in pstv_swing_per_lst if 22 < per <= 25]
        if len(range_14_pp_lst) > 0:
            sp_pp_cnt_22_25 = len(range_14_pp_lst)
            sp_pp_sum_22_25 = round(sum(range_14_pp_lst), 2)
            sp_pp_avg_22_25 = round(statistics.mean(range_14_pp_lst), 2)
        else:
            sp_pp_cnt_22_25 = 0
            sp_pp_sum_22_25 = 0
            sp_pp_avg_22_25 = 0
    else:
        range_14_pp_lst = []

    if len(pstv_swing_per_lst) > 0:
        extreme_large_range_pp_lst = [
            per for per in pstv_swing_per_lst if 15 < per <= 25]
        if len(extreme_large_range_pp_lst) > 0:
            sp_pp_cnt_15_25 = len(extreme_large_range_pp_lst)
            sp_pp_sum_15_25 = round(sum(extreme_large_range_pp_lst), 2)
            sp_pp_avg_15_25 = round(statistics.mean(
                extreme_large_range_pp_lst), 2)
        else:
            sp_pp_cnt_15_25 = 0
            sp_pp_sum_15_25 = 0
            sp_pp_avg_15_25 = 0
    else:
        extreme_large_range_pp_lst = []

    if len(pstv_swing_per_lst) > 0:
        super_extreme_large_range_pp_lst = [
            per for per in pstv_swing_per_lst if per > 25]
        if len(super_extreme_large_range_pp_lst) > 0:
            sp_pp_cnt_25_plus = len(super_extreme_large_range_pp_lst)
            sp_pp_sum_25_plus = round(sum(super_extreme_large_range_pp_lst), 2)
            sp_pp_avg_25_plus = round(statistics.mean(
                super_extreme_large_range_pp_lst), 2)
        else:
            sp_pp_cnt_25_plus = 0
            sp_pp_sum_25_plus = 0
            sp_pp_avg_25_plus = 0
    else:
        super_extreme_large_range_pp_lst = []

    sp_pp_cnt_0_1_lst = str(
        ["sp_pp_0_1", sp_pp_cnt_0_1, sp_pp_sum_0_1, sp_pp_avg_0_1])
    sp_pp_cnt_1_2_lst = str(
        ["sp_pp_1_2", sp_pp_cnt_1_2, sp_pp_sum_1_2, sp_pp_avg_1_2])
    sp_pp_cnt_0_2_lst = str(
        ["sp_pp_0_2", sp_pp_cnt_0_2, sp_pp_sum_0_2, sp_pp_avg_0_2])
    sp_pp_cnt_2_3_lst = str(
        ["sp_pp_2_3", sp_pp_cnt_2_3, sp_pp_sum_2_3, sp_pp_avg_2_3])
    sp_pp_cnt_3_4_lst = str(
        ["sp_pp_3_4", sp_pp_cnt_3_4, sp_pp_sum_3_4, sp_pp_avg_3_4])
    sp_pp_cnt_2_4_lst = str(
        ["sp_pp_2_4", sp_pp_cnt_2_4, sp_pp_sum_2_4, sp_pp_avg_2_4])
    sp_pp_cnt_4_5_lst = str(
        ["sp_pp_4_5", sp_pp_cnt_4_5, sp_pp_sum_4_5, sp_pp_avg_4_5])
    sp_pp_cnt_5_6_lst = str(
        ["sp_pp_5_6", sp_pp_cnt_5_6, sp_pp_sum_5_6, sp_pp_avg_5_6])
    sp_pp_cnt_6_7_lst = str(
        ["sp_pp_6_7", sp_pp_cnt_6_7, sp_pp_sum_6_7, sp_pp_avg_6_7])
    sp_pp_cnt_4_7_lst = str(
        ["sp_pp_4_7", sp_pp_cnt_4_7, sp_pp_sum_4_7, sp_pp_avg_4_7])
    sp_pp_cnt_7_9_lst = str(
        ["sp_pp_7_9", sp_pp_cnt_7_9, sp_pp_sum_7_9, sp_pp_avg_7_9])
    sp_pp_cnt_9_11_lst = str(
        ["sp_pp_9_11", sp_pp_cnt_9_11, sp_pp_sum_9_11, sp_pp_avg_9_11])
    sp_pp_cnt_11_13_lst = str(
        ["sp_pp_11_13", sp_pp_cnt_11_13, sp_pp_sum_11_13, sp_pp_avg_11_13])
    sp_pp_cnt_13_15_lst = str(
        ["sp_pp_13_15", sp_pp_cnt_13_15, sp_pp_sum_13_15, sp_pp_avg_13_15])
    sp_pp_cnt_7_15_lst = str(
        ["sp_pp_7_15", sp_pp_cnt_7_15, sp_pp_sum_7_15, sp_pp_avg_7_15])
    sp_pp_cnt_15_18_lst = str(
        ["sp_pp_15_18", sp_pp_cnt_15_18, sp_pp_sum_15_18, sp_pp_avg_15_18])
    sp_pp_cnt_18_22_lst = str(
        ["sp_pp_18_22", sp_pp_cnt_18_22, sp_pp_sum_18_22, sp_pp_avg_18_22])
    sp_pp_cnt_22_25_lst = str(
        ["sp_pp_22_25", sp_pp_cnt_22_25, sp_pp_sum_22_25, sp_pp_avg_22_25])
    sp_pp_cnt_15_25_lst = str(
        ["sp_pp_15_25", sp_pp_cnt_15_25, sp_pp_sum_15_25, sp_pp_avg_15_25])
    sp_pp_cnt_25_plus_lst = str(
        ["sp_pp_25_plus", sp_pp_cnt_25_plus, sp_pp_sum_25_plus, sp_pp_avg_25_plus])

    swing_pstv_per_range_lst = [coin_name, coin_time_tf, sp_pp_cnt_0_1_lst, sp_pp_cnt_1_2_lst, sp_pp_cnt_0_2_lst, sp_pp_cnt_2_3_lst, sp_pp_cnt_3_4_lst, sp_pp_cnt_2_4_lst, sp_pp_cnt_4_5_lst, sp_pp_cnt_5_6_lst, sp_pp_cnt_6_7_lst,
                                sp_pp_cnt_4_7_lst, sp_pp_cnt_7_9_lst, sp_pp_cnt_9_11_lst, sp_pp_cnt_11_13_lst, sp_pp_cnt_13_15_lst, sp_pp_cnt_7_15_lst, sp_pp_cnt_15_18_lst, sp_pp_cnt_18_22_lst, sp_pp_cnt_22_25_lst, sp_pp_cnt_15_25_lst, sp_pp_cnt_25_plus_lst]

    swing_pstv_per_range_lst_conv = [
        eval(lst) for lst in swing_pstv_per_range_lst[2:]]
    skip_list = ['sp_pp_0_2', 'sp_pp_2_4',
                 'sp_pp_4_7', 'sp_pp_7_15', 'sp_pp_15_25']
    swing_pstv_per_range_lst_conv_with_out_large_range = [
        item for item in swing_pstv_per_range_lst_conv if item[0] not in skip_list]
    t_3_sp_pp_ranges = sorted(
        swing_pstv_per_range_lst_conv_with_out_large_range, key=lambda x: abs(x[2]), reverse=True)[:3]

    swing_pstv_per_range_lst.append(t_3_sp_pp_ranges)

    return swing_pstv_per_range_lst


def get_swing_neg_per_range_info(coin_name, coin_time_tf, neg_swing_per_lst):
    if len(neg_swing_per_lst) > 0:
        range_1_np_lst = [
            per for per in neg_swing_per_lst if 0 < abs(per) <= 1]
        if len(range_1_np_lst) > 0:
            sp_np_cnt_0_1 = len(range_1_np_lst)
            sp_np_sum_0_1 = round(sum(range_1_np_lst), 2)
            sp_np_avg_0_1 = round(statistics.mean(range_1_np_lst), 2)
        else:
            sp_np_cnt_0_1 = 0
            sp_np_sum_0_1 = 0
            sp_np_avg_0_1 = 0
    else:
        range_1_np_lst = []

    if len(neg_swing_per_lst) > 0:
        range_2_np_lst = [
            per for per in neg_swing_per_lst if 1 < abs(per) <= 2]
        if len(range_2_np_lst) > 0:
            sp_np_cnt_1_2 = len(range_2_np_lst)
            sp_np_sum_1_2 = round(sum(range_2_np_lst), 2)
            sp_np_avg_1_2 = round(statistics.mean(range_2_np_lst), 2)
        else:
            sp_np_cnt_1_2 = 0
            sp_np_sum_1_2 = 0
            sp_np_avg_1_2 = 0
    else:
        range_2_np_lst = []

    # small_range_np_lst
    if len(neg_swing_per_lst) > 0:
        small_range_np_lst = [
            per for per in neg_swing_per_lst if 0 < abs(per) <= 2]
        if len(small_range_np_lst) > 0:
            sp_np_cnt_0_2 = len(small_range_np_lst)
            sp_np_sum_0_2 = round(sum(small_range_np_lst), 2)
            sp_np_avg_0_2 = round(statistics.mean(small_range_np_lst), 2)
        else:
            sp_np_cnt_0_2 = 0
            sp_np_sum_0_2 = 0
            sp_np_avg_0_2 = 0
    else:
        small_range_np_lst = []

    if len(neg_swing_per_lst) > 0:
        range_3_np_lst = [
            per for per in neg_swing_per_lst if 2 < abs(per) <= 3]
        if len(range_3_np_lst) > 0:
            sp_np_cnt_2_3 = len(range_3_np_lst)
            sp_np_sum_2_3 = round(sum(range_3_np_lst), 2)
            sp_np_avg_2_3 = round(statistics.mean(range_3_np_lst), 2)
        else:
            sp_np_cnt_2_3 = 0
            sp_np_sum_2_3 = 0
            sp_np_avg_2_3 = 0
    else:
        range_3_np_lst = []

    if len(neg_swing_per_lst) > 0:
        range_4_np_lst = [
            per for per in neg_swing_per_lst if 3 < abs(per) <= 4]
        if len(range_4_np_lst) > 0:
            sp_np_cnt_3_4 = len(range_4_np_lst)
            sp_np_sum_3_4 = round(sum(range_4_np_lst), 2)
            sp_np_avg_3_4 = round(statistics.mean(range_4_np_lst), 2)
        else:
            sp_np_cnt_3_4 = 0
            sp_np_sum_3_4 = 0
            sp_np_avg_3_4 = 0
    else:
        range_4_np_lst = []

    if len(neg_swing_per_lst) > 0:
        medium_range_np_lst = [
            per for per in neg_swing_per_lst if 2 < abs(per) <= 4]
        if len(medium_range_np_lst) > 0:
            sp_np_cnt_2_4 = len(medium_range_np_lst)
            sp_np_sum_2_4 = round(sum(medium_range_np_lst), 2)
            sp_np_avg_2_4 = round(statistics.mean(medium_range_np_lst), 2)
        else:
            sp_np_cnt_2_4 = 0
            sp_np_sum_2_4 = 0
            sp_np_avg_2_4 = 0
    else:
        medium_range_np_lst = []

    if len(neg_swing_per_lst) > 0:
        range_5_np_lst = [
            per for per in neg_swing_per_lst if 4 < abs(per) <= 5]
        if len(range_5_np_lst) > 0:
            sp_np_cnt_4_5 = len(range_5_np_lst)
            sp_np_sum_4_5 = round(sum(range_5_np_lst), 2)
            sp_np_avg_4_5 = round(statistics.mean(range_5_np_lst), 2)
        else:
            sp_np_cnt_4_5 = 0
            sp_np_sum_4_5 = 0
            sp_np_avg_4_5 = 0
    else:
        range_5_np_lst = []

    if len(neg_swing_per_lst) > 0:
        range_6_np_lst = [
            per for per in neg_swing_per_lst if 5 < abs(per) <= 6]
        if len(range_6_np_lst) > 0:
            sp_np_cnt_5_6 = len(range_6_np_lst)
            sp_np_sum_5_6 = round(sum(range_6_np_lst), 2)
            sp_np_avg_5_6 = round(statistics.mean(range_6_np_lst), 2)
        else:
            sp_np_cnt_5_6 = 0
            sp_np_sum_5_6 = 0
            sp_np_avg_5_6 = 0
    else:
        range_6_np_lst = []

    if len(neg_swing_per_lst) > 0:
        range_7_np_lst = [
            per for per in neg_swing_per_lst if 6 < abs(per) <= 7]
        if len(range_7_np_lst) > 0:
            sp_np_cnt_6_7 = len(range_7_np_lst)
            sp_np_sum_6_7 = round(sum(range_7_np_lst), 2)
            sp_np_avg_6_7 = round(statistics.mean(range_7_np_lst), 2)
        else:
            sp_np_cnt_6_7 = 0
            sp_np_sum_6_7 = 0
            sp_np_avg_6_7 = 0
    else:
        range_7_np_lst = []

    # large_range_np_lst
    if len(neg_swing_per_lst) > 0:
        large_range_np_lst = [
            per for per in neg_swing_per_lst if 4 < abs(per) <= 7]
        if len(large_range_np_lst) > 0:
            sp_np_cnt_4_7 = len(large_range_np_lst)
            sp_np_sum_4_7 = round(sum(large_range_np_lst), 2)
            sp_np_avg_4_7 = round(statistics.mean(large_range_np_lst), 2)
        else:
            sp_np_cnt_4_7 = 0
            sp_np_sum_4_7 = 0
            sp_np_avg_4_7 = 0
    else:
        large_range_np_lst = []

    if len(neg_swing_per_lst) > 0:
        range_8_np_lst = [
            per for per in neg_swing_per_lst if 7 < abs(per) <= 9]
        if len(range_8_np_lst) > 0:
            sp_np_cnt_7_9 = len(range_8_np_lst)
            sp_np_sum_7_9 = round(sum(range_8_np_lst), 2)
            sp_np_avg_7_9 = round(statistics.mean(range_8_np_lst), 2)
        else:
            sp_np_cnt_7_9 = 0
            sp_np_sum_7_9 = 0
            sp_np_avg_7_9 = 0
    else:
        range_8_np_lst = []

    if len(neg_swing_per_lst) > 0:
        range_9_np_lst = [
            per for per in neg_swing_per_lst if 9 < abs(per) <= 11]
        if len(range_9_np_lst) > 0:
            sp_np_cnt_9_11 = len(range_9_np_lst)
            sp_np_sum_9_11 = round(sum(range_9_np_lst), 2)
            sp_np_avg_9_11 = round(statistics.mean(range_9_np_lst), 2)
        else:
            sp_np_cnt_9_11 = 0
            sp_np_sum_9_11 = 0
            sp_np_avg_9_11 = 0
    else:
        range_9_np_lst = []

    if len(neg_swing_per_lst) > 0:
        range_10_np_lst = [
            per for per in neg_swing_per_lst if 11 < abs(per) <= 13]
        if len(range_10_np_lst) > 0:
            sp_np_cnt_11_13 = len(range_10_np_lst)
            sp_np_sum_11_13 = round(sum(range_10_np_lst), 2)
            sp_np_avg_11_13 = round(statistics.mean(range_10_np_lst), 2)
        else:
            sp_np_cnt_11_13 = 0
            sp_np_sum_11_13 = 0
            sp_np_avg_11_13 = 0
    else:
        range_10_np_lst = []

    if len(neg_swing_per_lst) > 0:
        range_11_np_lst = [
            per for per in neg_swing_per_lst if 13 < abs(per) <= 15]
        if len(range_11_np_lst) > 0:
            sp_np_cnt_13_15 = len(range_11_np_lst)
            sp_np_sum_13_15 = round(sum(range_11_np_lst), 2)
            sp_np_avg_13_15 = round(statistics.mean(range_11_np_lst), 2)
        else:
            sp_np_cnt_13_15 = 0
            sp_np_sum_13_15 = 0
            sp_np_avg_13_15 = 0
    else:
        range_11_np_lst = []

    # extra_large_np_lst
    if len(neg_swing_per_lst) > 0:
        extra_large_range_np_lst = [
            per for per in neg_swing_per_lst if 7 < abs(per) <= 15]
        if len(extra_large_range_np_lst) > 0:
            sp_np_cnt_7_15 = len(extra_large_range_np_lst)
            sp_np_sum_7_15 = round(sum(extra_large_range_np_lst), 2)
            sp_np_avg_7_15 = round(
                statistics.mean(extra_large_range_np_lst), 2)
        else:
            sp_np_cnt_7_15 = 0
            sp_np_sum_7_15 = 0
            sp_np_avg_7_15 = 0
    else:
        extra_large_range_np_lst = []

    if len(neg_swing_per_lst) > 0:
        range_12_np_lst = [
            per for per in neg_swing_per_lst if 15 < abs(per) <= 18]
        if len(range_12_np_lst) > 0:
            sp_np_cnt_15_18 = len(range_12_np_lst)
            sp_np_sum_15_18 = round(sum(range_12_np_lst), 2)
            sp_np_avg_15_18 = round(statistics.mean(range_12_np_lst), 2)
        else:
            sp_np_cnt_15_18 = 0
            sp_np_sum_15_18 = 0
            sp_np_avg_15_18 = 0
    else:
        range_12_np_lst = []

    if len(neg_swing_per_lst) > 0:
        range_13_np_lst = [
            per for per in neg_swing_per_lst if 18 < abs(per) <= 22]
        if len(range_13_np_lst) > 0:
            sp_np_cnt_18_22 = len(range_13_np_lst)
            sp_np_sum_18_22 = round(sum(range_13_np_lst), 2)
            sp_np_avg_18_22 = round(statistics.mean(range_13_np_lst), 2)
        else:
            sp_np_cnt_18_22 = 0
            sp_np_sum_18_22 = 0
            sp_np_avg_18_22 = 0
    else:
        range_13_np_lst = []

    if len(neg_swing_per_lst) > 0:
        range_14_np_lst = [
            per for per in neg_swing_per_lst if 22 < abs(per) <= 25]
        if len(range_14_np_lst) > 0:
            sp_np_cnt_22_25 = len(range_14_np_lst)
            sp_np_sum_22_25 = round(sum(range_14_np_lst), 2)
            sp_np_avg_22_25 = round(statistics.mean(range_14_np_lst), 2)
        else:
            sp_np_cnt_22_25 = 0
            sp_np_sum_22_25 = 0
            sp_np_avg_22_25 = 0
    else:
        range_14_np_lst = []

    if len(neg_swing_per_lst) > 0:
        extreme_large_range_np_lst = [
            per for per in neg_swing_per_lst if 15 < abs(per) <= 25]
        if len(extreme_large_range_np_lst) > 0:
            sp_np_cnt_15_25 = len(extreme_large_range_np_lst)
            sp_np_sum_15_25 = round(sum(extreme_large_range_np_lst), 2)
            sp_np_avg_15_25 = round(statistics.mean(
                extreme_large_range_np_lst), 2)
        else:
            sp_np_cnt_15_25 = 0
            sp_np_sum_15_25 = 0
            sp_np_avg_15_25 = 0
    else:
        extreme_large_range_np_lst = []

    if len(neg_swing_per_lst) > 0:
        super_extreme_large_range_np_lst = [
            per for per in neg_swing_per_lst if abs(per) > 25]
        if len(super_extreme_large_range_np_lst) > 0:
            sp_np_cnt_25_plus = len(super_extreme_large_range_np_lst)
            sp_np_sum_25_plus = round(sum(super_extreme_large_range_np_lst), 2)
            sp_np_avg_25_plus = round(statistics.mean(
                super_extreme_large_range_np_lst), 2)
        else:
            sp_np_cnt_25_plus = 0
            sp_np_sum_25_plus = 0
            sp_np_avg_25_plus = 0
    else:
        super_extreme_large_range_np_lst = []

    sp_np_cnt_0_1_lst = str(
        ["sp_np_0_1", sp_np_cnt_0_1, sp_np_sum_0_1, sp_np_avg_0_1])
    sp_np_cnt_1_2_lst = str(
        ["sp_np_1_2", sp_np_cnt_1_2, sp_np_sum_1_2, sp_np_avg_1_2])
    sp_np_cnt_0_2_lst = str(
        ["sp_np_0_2", sp_np_cnt_0_2, sp_np_sum_0_2, sp_np_avg_0_2])
    sp_np_cnt_2_3_lst = str(
        ["sp_np_2_3", sp_np_cnt_2_3, sp_np_sum_2_3, sp_np_avg_2_3])
    sp_np_cnt_3_4_lst = str(
        ["sp_np_3_4", sp_np_cnt_3_4, sp_np_sum_3_4, sp_np_avg_3_4])
    sp_np_cnt_2_4_lst = str(
        ["sp_np_2_4", sp_np_cnt_2_4, sp_np_sum_2_4, sp_np_avg_2_4])
    sp_np_cnt_4_5_lst = str(
        ["sp_np_4_5", sp_np_cnt_4_5, sp_np_sum_4_5, sp_np_avg_4_5])
    sp_np_cnt_5_6_lst = str(
        ["sp_np_5_6", sp_np_cnt_5_6, sp_np_sum_5_6, sp_np_avg_5_6])
    sp_np_cnt_6_7_lst = str(
        ["sp_np_6_7", sp_np_cnt_6_7, sp_np_sum_6_7, sp_np_avg_6_7])
    sp_np_cnt_4_7_lst = str(
        ["sp_np_4_7", sp_np_cnt_4_7, sp_np_sum_4_7, sp_np_avg_4_7])
    sp_np_cnt_7_9_lst = str(
        ["sp_np_7_9", sp_np_cnt_7_9, sp_np_sum_7_9, sp_np_avg_7_9])
    sp_np_cnt_9_11_lst = str(
        ["sp_np_9_11", sp_np_cnt_9_11, sp_np_sum_9_11, sp_np_avg_9_11])
    sp_np_cnt_11_13_lst = str(
        ["sp_np_11_13", sp_np_cnt_11_13, sp_np_sum_11_13, sp_np_avg_11_13])
    sp_np_cnt_13_15_lst = str(
        ["sp_np_13_15", sp_np_cnt_13_15, sp_np_sum_13_15, sp_np_avg_13_15])
    sp_np_cnt_7_15_lst = str(
        ["sp_np_7_15", sp_np_cnt_7_15, sp_np_sum_7_15, sp_np_avg_7_15])
    sp_np_cnt_15_18_lst = str(
        ["sp_np_15_18", sp_np_cnt_15_18, sp_np_sum_15_18, sp_np_avg_15_18])
    sp_np_cnt_18_22_lst = str(
        ["sp_np_18_22", sp_np_cnt_18_22, sp_np_sum_18_22, sp_np_avg_18_22])
    sp_np_cnt_22_25_lst = str(
        ["sp_np_22_25", sp_np_cnt_22_25, sp_np_sum_22_25, sp_np_avg_22_25])
    sp_np_cnt_15_25_lst = str(
        ["sp_np_15_25", sp_np_cnt_15_25, sp_np_sum_15_25, sp_np_avg_15_25])
    sp_np_cnt_25_plus_lst = str(
        ["sp_np_25_plus", sp_np_cnt_25_plus, sp_np_sum_25_plus, sp_np_avg_25_plus])

    swing_neg_per_range_lst = [coin_name, coin_time_tf, sp_np_cnt_0_1_lst, sp_np_cnt_1_2_lst, sp_np_cnt_0_2_lst, sp_np_cnt_2_3_lst, sp_np_cnt_3_4_lst, sp_np_cnt_2_4_lst, sp_np_cnt_4_5_lst, sp_np_cnt_5_6_lst, sp_np_cnt_6_7_lst,
                               sp_np_cnt_4_7_lst, sp_np_cnt_7_9_lst, sp_np_cnt_9_11_lst, sp_np_cnt_11_13_lst, sp_np_cnt_13_15_lst, sp_np_cnt_7_15_lst, sp_np_cnt_15_18_lst, sp_np_cnt_18_22_lst, sp_np_cnt_22_25_lst, sp_np_cnt_15_25_lst, sp_np_cnt_25_plus_lst]

    swing_neg_per_range_lst_conv = [eval(lst)
                                    for lst in swing_neg_per_range_lst[2:]]
    skip_list = ['sp_np_0_2', 'sp_np_2_4',
                 'sp_np_4_7', 'sp_np_7_15', 'sp_np_15_25']
    swing_neg_per_range_lst_conv_with_out_large_range = [
        item for item in swing_neg_per_range_lst_conv if item[0] not in skip_list]
    t_3_sp_np_ranges = sorted(
        swing_neg_per_range_lst_conv_with_out_large_range, key=lambda x: abs(x[2]), reverse=True)[:3]

    swing_neg_per_range_lst.append(t_3_sp_np_ranges)
    return swing_neg_per_range_lst


def get_swing_rand_per_info(coin_name, coin_time_tf, swing_rand_per_lst, pstv_rand_swing_per_lst, neg_rand_swing_per_lst):
    if len(pstv_rand_swing_per_lst) >= 10:
        t_10_lrg_pp_rand_sp_lst = sorted(
            pstv_rand_swing_per_lst, reverse=True)[:10]
        t_10_sml_pp_rand_sp_lst = sorted(
            pstv_rand_swing_per_lst, reverse=False)[:10]
        t_5_lrg_pp_rand_sp_lst = str(
            sorted(pstv_rand_swing_per_lst, reverse=True)[:5])
    elif len(pstv_rand_swing_per_lst) > 0 and len(pstv_rand_swing_per_lst) < 10:
        t_10_lrg_pp_rand_sp_lst = sorted(pstv_rand_swing_per_lst, reverse=True)[
            :len(pstv_rand_swing_per_lst)]
        t_10_sml_pp_rand_sp_lst = sorted(pstv_rand_swing_per_lst, reverse=False)[
            :len(pstv_rand_swing_per_lst)]
        t_5_lrg_pp_rand_sp_lst = str(
            sorted(pstv_rand_swing_per_lst, reverse=True)[:5])
    else:
        t_10_lrg_pp_rand_sp_lst = [0]
        t_10_sml_pp_rand_sp_lst = [0]
        t_5_lrg_pp_rand_sp_lst = str([0])
    if len(neg_rand_swing_per_lst) >= 10:
        t_10_lrg_np_rand_sp_lst = sorted(
            neg_rand_swing_per_lst, reverse=False)[:10]
        t_10_sml_np_rand_sp_lst = sorted(
            neg_rand_swing_per_lst, reverse=True)[:10]
        t_5_lrg_np_rand_sp_lst = str(
            sorted(neg_rand_swing_per_lst, reverse=False)[:5])
    elif len(neg_rand_swing_per_lst) > 0 and len(neg_rand_swing_per_lst) < 10:
        t_10_lrg_np_rand_sp_lst = sorted(neg_rand_swing_per_lst, reverse=True)[
            :len(neg_rand_swing_per_lst)]
        t_10_sml_np_rand_sp_lst = sorted(neg_rand_swing_per_lst, reverse=False)[
            :len(neg_rand_swing_per_lst)]
        t_5_lrg_np_rand_sp_lst = str(
            sorted(neg_rand_swing_per_lst, reverse=False)[:5])
    else:
        t_10_lrg_np_rand_sp_lst = [0]
        t_10_sml_np_rand_sp_lst = [0]
        t_5_lrg_np_rand_sp_lst = str([0])

    # all swing info
    all_swing_rand_count = len(swing_rand_per_lst)
    all_swings_rand_pp_count = len(pstv_rand_swing_per_lst)
    all_swings_rand_np_count = len(neg_rand_swing_per_lst)
    all_swings_rand_pp_sum = round((sum(pstv_rand_swing_per_lst)), 2)
    all_swings_rand_np_sum = round((sum(neg_rand_swing_per_lst)), 2)
    all_swing_rand_per_sum = round(
        (all_swings_rand_pp_sum + abs(all_swings_rand_np_sum)), 2)

    all_swings_rand_pp_avg = round(
        (statistics.mean(pstv_rand_swing_per_lst)), 2)
    all_swings_rand_np_avg = round(
        (statistics.mean(neg_rand_swing_per_lst)), 2)
    all_swings_rand_pp_med = round(
        (statistics.median(pstv_rand_swing_per_lst)), 2)
    all_swings_rand_np_med = round(
        (statistics.median(neg_rand_swing_per_lst)), 2)

    # Top_10 Info
    t_10_lrg_pp_rand_sp_sum = round((sum(t_10_lrg_pp_rand_sp_lst)), 2)
    t_10_lrg_np_rand_sp_sum = round((sum(t_10_lrg_np_rand_sp_lst)), 2)
    t_10_lrg_pp_rand_sp_avg = round(
        (statistics.mean(t_10_lrg_pp_rand_sp_lst)), 2)
    t_10_lrg_np_rand_sp_avg = round(
        (statistics.mean(t_10_lrg_np_rand_sp_lst)), 2)
    t_10_lrg_pp_rand_sp_med = round(
        (statistics.median(t_10_lrg_pp_rand_sp_lst)), 2)
    t_10_lrg_np_rand_sp_med = round(
        (statistics.median(t_10_lrg_np_rand_sp_lst)), 2)

    t_10_sml_pp_rand_sp_sum = round((sum(t_10_sml_pp_rand_sp_lst)), 2)
    t_10_sml_np_rand_sp_sum = round((sum(t_10_sml_np_rand_sp_lst)), 2)
    t_10_sml_pp_rand_sp_avg = round(
        (statistics.mean(t_10_sml_pp_rand_sp_lst)), 2)
    t_10_sml_np_rand_sp_avg = round(
        (statistics.mean(t_10_sml_np_rand_sp_lst)), 2)
    t_10_sml_pp_rand_sp_med = round(
        (statistics.median(t_10_sml_pp_rand_sp_lst)), 2)
    t_10_sml_np_rand_sp_med = round(
        (statistics.median(t_10_sml_np_rand_sp_lst)), 2)

    swing_rand_per_analysis_lst = [coin_name, coin_time_tf, all_swing_rand_count, all_swings_rand_pp_count, all_swings_rand_np_count, all_swing_rand_per_sum, all_swings_rand_pp_sum, all_swings_rand_np_sum, all_swings_rand_pp_avg, all_swings_rand_np_avg, all_swings_rand_pp_med, all_swings_rand_np_med, t_5_lrg_pp_rand_sp_lst,
                                   t_5_lrg_np_rand_sp_lst, t_10_lrg_pp_rand_sp_sum, t_10_lrg_np_rand_sp_sum, t_10_lrg_pp_rand_sp_avg, t_10_lrg_np_rand_sp_avg, t_10_lrg_pp_rand_sp_med, t_10_lrg_np_rand_sp_med, t_10_sml_pp_rand_sp_sum, t_10_sml_np_rand_sp_sum, t_10_sml_pp_rand_sp_avg, t_10_sml_np_rand_sp_avg, t_10_sml_pp_rand_sp_med, t_10_sml_np_rand_sp_med]

    return swing_rand_per_analysis_lst


def get_swing_zero_rand_per_cluster_lst(coin_name, coin_time_tf, zero_rand_swing_per_lst, swing_zero_rand_and_swing_per_lst):
    pstv_per_swing_zero_rand_lst = [
        swing for swing in swing_zero_rand_and_swing_per_lst if swing[1] > 0]
    neg_per_swing_zero_rand_lst = [
        swing for swing in swing_zero_rand_and_swing_per_lst if swing[1] < 0]

    if len(pstv_per_swing_zero_rand_lst) >= 10:
        t_10_lrg_pp_zero_rand_sp_lst = sorted(
            pstv_per_swing_zero_rand_lst, key=lambda x: x[1], reverse=True)[:10]
        t_10_sml_pp_zero_rand_sp_lst = sorted(
            pstv_per_swing_zero_rand_lst, key=lambda x: x[1], reverse=False)[:10]
        t_5_lrg_pp_zero_rand_sp_lst = str(
            sorted(pstv_per_swing_zero_rand_lst, key=lambda x: x[1], reverse=True)[:5])
    elif len(pstv_per_swing_zero_rand_lst) > 0 and len(pstv_per_swing_zero_rand_lst) < 10:
        t_10_lrg_pp_zero_rand_sp_lst = sorted(pstv_per_swing_zero_rand_lst, key=lambda x: x[1], reverse=True)[
            :len(pstv_per_swing_zero_rand_lst)]
        t_10_sml_pp_zero_rand_sp_lst = sorted(pstv_per_swing_zero_rand_lst, key=lambda x: x[1], reverse=False)[
            :len(pstv_per_swing_zero_rand_lst)]
        t_5_lrg_pp_zero_rand_sp_lst = str(
            sorted(pstv_per_swing_zero_rand_lst, key=lambda x: x[1], reverse=True)[:5])
    else:
        # Add the corner conditions
        t_10_lrg_pp_zero_rand_sp_lst = [[0, 0]]
        t_10_sml_pp_zero_rand_sp_lst = [[0, 0]]
        t_5_lrg_pp_zero_rand_sp_lst = str([0])
        pstv_per_swing_zero_rand_lst = [[0, 0]]

    if len(neg_per_swing_zero_rand_lst) >= 10:
        t_10_lrg_np_zero_rand_sp_lst = sorted(
            neg_per_swing_zero_rand_lst, key=lambda x: x[1], reverse=False)[:10]
        t_10_sml_np_zero_rand_sp_lst = sorted(
            neg_per_swing_zero_rand_lst, key=lambda x: x[1], reverse=True)[:10]
        t_5_lrg_np_zero_rand_sp_lst = str(
            sorted(neg_per_swing_zero_rand_lst, key=lambda x: x[1], reverse=False)[:5])
    elif len(neg_per_swing_zero_rand_lst) > 0 and len(neg_per_swing_zero_rand_lst) < 10:
        t_10_lrg_np_zero_rand_sp_lst = sorted(neg_per_swing_zero_rand_lst, key=lambda x: x[1], reverse=False)[
            :len(neg_per_swing_zero_rand_lst)]
        t_10_sml_np_zero_rand_sp_lst = sorted(neg_per_swing_zero_rand_lst, key=lambda x: x[1], reverse=True)[
            :len(neg_per_swing_zero_rand_lst)]
        t_5_lrg_np_zero_rand_sp_lst = str(
            sorted(neg_per_swing_zero_rand_lst, key=lambda x: x[1], reverse=False)[:5])
    else:
        # Add the corner conditions
        t_10_lrg_np_zero_rand_sp_lst = [[0, 0]]
        t_10_sml_np_zero_rand_sp_lst = [[0, 0]]
        t_5_lrg_np_zero_rand_sp_lst = str([0])
        neg_per_swing_zero_rand_lst = [[0, 0]]

    # Zero rand info
    all_swings_zero_rand_count = len(zero_rand_swing_per_lst)
    all_swings_zero_rand_pp_count = len(pstv_per_swing_zero_rand_lst)
    all_swings_zero_rand_np_count = len(neg_per_swing_zero_rand_lst)
    all_swings_zero_rand_pp_sum = round(
        (sum([swing[1] for swing in pstv_per_swing_zero_rand_lst])), 2)
    all_swings_zero_rand_np_sum = round(
        (sum([swing[1] for swing in neg_per_swing_zero_rand_lst])), 2)
    all_swing_zero_rand_per_sum = round(
        (all_swings_zero_rand_pp_sum + abs(all_swings_zero_rand_np_sum)), 2)

    all_swings_zero_rand_pp_mean = round(
        (statistics.mean([swing[1] for swing in pstv_per_swing_zero_rand_lst])), 2)
    all_swings_zero_rand_np_mean = round(
        (statistics.mean([swing[1] for swing in neg_per_swing_zero_rand_lst])), 2)
    all_swings_zero_rand_pp_med = round(
        (statistics.median([swing[1] for swing in pstv_per_swing_zero_rand_lst])), 2)
    all_swings_zero_rand_np_med = round(
        (statistics.median([swing[1] for swing in neg_per_swing_zero_rand_lst])), 2)

    # Top_10 Zero Rand Info
    t_10_lrg_pp_zero_rand_sp_sum = round(
        (sum([swing[1] for swing in t_10_lrg_pp_zero_rand_sp_lst])), 2)
    t_10_lrg_np_zero_rand_sp_sum = round(
        (sum([swing[1] for swing in t_10_lrg_np_zero_rand_sp_lst])), 2)
    t_10_lrg_pp_zero_rand_sp_avg = round(
        (statistics.mean([swing[1] for swing in t_10_lrg_pp_zero_rand_sp_lst])), 2)
    t_10_lrg_np_zero_rand_sp_avg = round(
        (statistics.mean([swing[1] for swing in t_10_lrg_np_zero_rand_sp_lst])), 2)
    t_10_lrg_pp_zero_rand_sp_med = round(
        (statistics.median([swing[1] for swing in t_10_lrg_pp_zero_rand_sp_lst])), 2)
    t_10_lrg_np_zero_rand_sp_med = round(
        (statistics.median([swing[1] for swing in t_10_lrg_np_zero_rand_sp_lst])), 2)

    t_10_sml_pp_zero_rand_sp_sum = round(
        (sum([swing[1] for swing in t_10_sml_pp_zero_rand_sp_lst])), 2)
    t_10_sml_np_zero_rand_sp_sum = round(
        (sum([swing[1] for swing in t_10_sml_np_zero_rand_sp_lst])), 2)
    t_10_sml_pp_zero_rand_sp_avg = round(
        (statistics.mean([swing[1] for swing in t_10_sml_pp_zero_rand_sp_lst])), 2)
    t_10_sml_np_zero_rand_sp_avg = round(
        (statistics.mean([swing[1] for swing in t_10_sml_np_zero_rand_sp_lst])), 2)
    t_10_sml_pp_zero_rand_sp_med = round(
        (statistics.median([swing[1] for swing in t_10_sml_pp_zero_rand_sp_lst])), 2)
    t_10_sml_np_zero_rand_sp_med = round(
        (statistics.median([swing[1] for swing in t_10_sml_np_zero_rand_sp_lst])), 2)

    swing_zero_rand_per_analysis_lst = [coin_name, coin_time_tf, all_swings_zero_rand_count, all_swings_zero_rand_pp_count, all_swings_zero_rand_np_count, all_swings_zero_rand_pp_sum, all_swings_zero_rand_np_sum, all_swing_zero_rand_per_sum, all_swings_zero_rand_pp_mean, all_swings_zero_rand_np_mean, all_swings_zero_rand_pp_med, all_swings_zero_rand_np_med, t_5_lrg_pp_zero_rand_sp_lst,
                                        t_5_lrg_np_zero_rand_sp_lst, t_10_lrg_pp_zero_rand_sp_sum, t_10_lrg_np_zero_rand_sp_sum, t_10_lrg_pp_zero_rand_sp_avg, t_10_lrg_np_zero_rand_sp_avg, t_10_lrg_pp_zero_rand_sp_med, t_10_lrg_np_zero_rand_sp_med, t_10_sml_pp_zero_rand_sp_sum, t_10_sml_np_zero_rand_sp_sum, t_10_sml_pp_zero_rand_sp_avg, t_10_sml_np_zero_rand_sp_avg, t_10_sml_pp_zero_rand_sp_med, t_10_sml_np_zero_rand_sp_med]

    return swing_zero_rand_per_analysis_lst


def get_swing_pstv_rand_per_cluster_lst(coin_name, coin_time_tf, pstv_rand_swing_per_lst):
    if len(pstv_rand_swing_per_lst) > 0:
        cluster_1_rand_pp_lst = [
            per for per in pstv_rand_swing_per_lst if 0 < per <= 0.25]
        if len(cluster_1_rand_pp_lst) > 0:
            rand_pp_cnt_0_to_0_25 = len(cluster_1_rand_pp_lst)
            rand_pp_sum_0_to_0_25 = round(sum(cluster_1_rand_pp_lst), 2)
            rand_pp_avg_0_to_0_25 = round(
                statistics.mean(cluster_1_rand_pp_lst), 2)
        else:
            rand_pp_cnt_0_to_0_25 = 0
            rand_pp_sum_0_to_0_25 = 0
            rand_pp_avg_0_to_0_25 = 0
    else:
        cluster_1_rand_pp_lst = []

    if len(pstv_rand_swing_per_lst) > 0:
        cluster_2_rand_pp_lst = [
            per for per in pstv_rand_swing_per_lst if 0.25 < per <= 0.5]
        if len(cluster_2_rand_pp_lst) > 0:
            rand_pp_cnt_0_25_to_0_5 = len(cluster_2_rand_pp_lst)
            rand_pp_sum_0_25_to_0_5 = round(sum(cluster_2_rand_pp_lst), 2)
            rand_pp_avg_0_25_to_0_5 = round(
                statistics.mean(cluster_2_rand_pp_lst), 2)
        else:
            rand_pp_cnt_0_25_to_0_5 = 0
            rand_pp_sum_0_25_to_0_5 = 0
            rand_pp_avg_0_25_to_0_5 = 0
    else:
        cluster_2_rand_pp_lst = []

    # small_cluster_pp_lst
    if len(pstv_rand_swing_per_lst) > 0:
        small_cluster_pp_lst = [
            per for per in pstv_rand_swing_per_lst if 0 < per <= 0.5]
        if len(small_cluster_pp_lst) > 0:
            rand_pp_cnt_0_to_0_5 = len(small_cluster_pp_lst)
            rand_pp_sum_0_to_0_5 = round(sum(small_cluster_pp_lst), 2)
            rand_pp_avg_0_to_0_5 = round(
                statistics.mean(small_cluster_pp_lst), 2)
        else:
            rand_pp_cnt_0_to_0_5 = 0
            rand_pp_sum_0_to_0_5 = 0
            rand_pp_avg_0_to_0_5 = 0
    else:
        small_cluster_pp_lst = []

    if len(pstv_rand_swing_per_lst) > 0:
        cluster_3_rand_pp_lst = [
            per for per in pstv_rand_swing_per_lst if 0.5 < per <= 1]
        if len(cluster_3_rand_pp_lst) > 0:
            rand_pp_cnt_0_5_to_1 = len(cluster_3_rand_pp_lst)
            rand_pp_sum_0_5_to_1 = round(sum(cluster_3_rand_pp_lst), 2)
            rand_pp_avg_0_5_to_1 = round(
                statistics.mean(cluster_3_rand_pp_lst), 2)
        else:
            rand_pp_cnt_0_5_to_1 = 0
            rand_pp_sum_0_5_to_1 = 0
            rand_pp_avg_0_5_to_1 = 0
    else:
        cluster_3_rand_pp_lst = []

    if len(pstv_rand_swing_per_lst) > 0:
        cluster_4_rand_pp_lst = [
            per for per in pstv_rand_swing_per_lst if 1 < per <= 1.5]
        if len(cluster_4_rand_pp_lst) > 0:
            rand_pp_cnt_1_to_1_5 = len(cluster_4_rand_pp_lst)
            rand_pp_sum_1_to_1_5 = round(sum(cluster_4_rand_pp_lst), 2)
            rand_pp_avg_1_to_1_5 = round(
                statistics.mean(cluster_4_rand_pp_lst), 2)
        else:
            rand_pp_cnt_1_to_1_5 = 0
            rand_pp_sum_1_to_1_5 = 0
            rand_pp_avg_1_to_1_5 = 0
    else:
        cluster_4_rand_pp_lst = []

    # medium_cluster_pp_lst
    if len(pstv_rand_swing_per_lst) > 0:
        medium_cluster_pp_lst = [
            per for per in pstv_rand_swing_per_lst if 0.5 < per <= 1.5]
        if len(medium_cluster_pp_lst) > 0:
            rand_pp_cnt_0_5_to_1_5 = len(medium_cluster_pp_lst)
            rand_pp_sum_0_5_to_1_5 = round(sum(medium_cluster_pp_lst), 2)
            rand_pp_avg_0_5_to_1_5 = round(
                statistics.mean(medium_cluster_pp_lst), 2)
        else:
            rand_pp_cnt_0_5_to_1_5 = 0
            rand_pp_sum_0_5_to_1_5 = 0
            rand_pp_avg_0_5_to_1_5 = 0
    else:
        medium_cluster_pp_lst = []

    if len(pstv_rand_swing_per_lst) > 0:
        cluster_5_rand_pp_lst = [
            per for per in pstv_rand_swing_per_lst if 1.5 < per <= 2]
        if len(cluster_5_rand_pp_lst) > 0:
            rand_pp_cnt_1_5_to_2 = len(cluster_5_rand_pp_lst)
            rand_pp_sum_1_5_to_2 = round(sum(cluster_5_rand_pp_lst), 2)
            rand_pp_avg_1_5_to_2 = round(
                statistics.mean(cluster_5_rand_pp_lst), 2)
        else:
            rand_pp_cnt_1_5_to_2 = 0
            rand_pp_sum_1_5_to_2 = 0
            rand_pp_avg_1_5_to_2 = 0
    else:
        cluster_5_rand_pp_lst = []

    if len(pstv_rand_swing_per_lst) > 0:
        cluster_6_rand_pp_lst = [
            per for per in pstv_rand_swing_per_lst if 2 < per <= 2.5]
        if len(cluster_6_rand_pp_lst) > 0:
            rand_pp_cnt_2_to_2_5 = len(cluster_6_rand_pp_lst)
            rand_pp_sum_2_to_2_5 = round(sum(cluster_6_rand_pp_lst), 2)
            rand_pp_avg_2_to_2_5 = round(
                statistics.mean(cluster_6_rand_pp_lst), 2)
        else:
            rand_pp_cnt_2_to_2_5 = 0
            rand_pp_sum_2_to_2_5 = 0
            rand_pp_avg_2_to_2_5 = 0
    else:
        cluster_6_rand_pp_lst = []

    if len(pstv_rand_swing_per_lst) > 0:
        cluster_7_rand_pp_lst = [
            per for per in pstv_rand_swing_per_lst if 2.5 < per <= 3.5]
        if len(cluster_7_rand_pp_lst) > 0:
            rand_pp_cnt_2_5_to_3_5 = len(cluster_7_rand_pp_lst)
            rand_pp_sum_2_5_to_3_5 = round(sum(cluster_7_rand_pp_lst), 2)
            rand_pp_avg_2_5_to_3_5 = round(
                statistics.mean(cluster_7_rand_pp_lst), 2)
        else:
            rand_pp_cnt_2_5_to_3_5 = 0
            rand_pp_sum_2_5_to_3_5 = 0
            rand_pp_avg_2_5_to_3_5 = 0
    else:
        cluster_7_rand_pp_lst = []

    # large_cluster_pp_lst
    if len(pstv_rand_swing_per_lst) > 0:
        large_cluster_pp_lst = [
            per for per in pstv_rand_swing_per_lst if 1.5 < per <= 3.5]
        if len(large_cluster_pp_lst) > 0:
            rand_pp_cnt_1_5_to_3_5 = len(large_cluster_pp_lst)
            rand_pp_sum_1_5_to_3_5 = round(sum(large_cluster_pp_lst), 2)
            rand_pp_avg_1_5_to_3_5 = round(
                statistics.mean(large_cluster_pp_lst), 2)
        else:
            rand_pp_cnt_1_5_to_3_5 = 0
            rand_pp_sum_1_5_to_3_5 = 0
            rand_pp_avg_1_5_to_3_5 = 0
    else:
        large_cluster_pp_lst = []

    if len(pstv_rand_swing_per_lst) > 0:
        cluster_8_rand_pp_lst = [
            per for per in pstv_rand_swing_per_lst if 3.5 < per <= 4.5]
        if len(cluster_8_rand_pp_lst) > 0:
            rand_pp_cnt_3_5_to_4_5 = len(cluster_8_rand_pp_lst)
            rand_pp_sum_3_5_to_4_5 = round(sum(cluster_8_rand_pp_lst), 2)
            rand_pp_avg_3_5_to_4_5 = round(
                statistics.mean(cluster_8_rand_pp_lst), 2)
        else:
            rand_pp_cnt_3_5_to_4_5 = 0
            rand_pp_sum_3_5_to_4_5 = 0
            rand_pp_avg_3_5_to_4_5 = 0
    else:
        cluster_8_rand_pp_lst = []

    if len(pstv_rand_swing_per_lst) > 0:
        cluster_9_rand_pp_lst = [
            per for per in pstv_rand_swing_per_lst if 4.5 < per <= 5.5]
        if len(cluster_9_rand_pp_lst) > 0:
            rand_pp_cnt_4_5_to_5_5 = len(cluster_9_rand_pp_lst)
            rand_pp_sum_4_5_to_5_5 = round(sum(cluster_9_rand_pp_lst), 2)
            rand_pp_avg_4_5_to_5_5 = round(
                statistics.mean(cluster_9_rand_pp_lst), 2)
        else:
            rand_pp_cnt_4_5_to_5_5 = 0
            rand_pp_sum_4_5_to_5_5 = 0
            rand_pp_avg_4_5_to_5_5 = 0
    else:
        cluster_9_rand_pp_lst = []

    if len(pstv_rand_swing_per_lst) > 0:
        cluster_10_rand_pp_lst = [
            per for per in pstv_rand_swing_per_lst if 5.5 < per <= 7]
        if len(cluster_10_rand_pp_lst) > 0:
            rand_pp_cnt_5_5_to_7 = len(cluster_10_rand_pp_lst)
            rand_pp_sum_5_5_to_7 = round(sum(cluster_10_rand_pp_lst), 2)
            rand_pp_avg_5_5_to_7 = round(
                statistics.mean(cluster_10_rand_pp_lst), 2)
        else:
            rand_pp_cnt_5_5_to_7 = 0
            rand_pp_sum_5_5_to_7 = 0
            rand_pp_avg_5_5_to_7 = 0
    else:
        cluster_10_rand_pp_lst = []

    # extra_large_cluster_pp_lst
    if len(pstv_rand_swing_per_lst) > 0:
        extra_large_cluster_pp_lst = [
            per for per in pstv_rand_swing_per_lst if 3.5 < per <= 7]
        if len(extra_large_cluster_pp_lst) > 0:
            rand_pp_cnt_3_5_to_7 = len(extra_large_cluster_pp_lst)
            rand_pp_sum_3_5_to_7 = round(sum(extra_large_cluster_pp_lst), 2)
            rand_pp_avg_3_5_to_7 = round(
                statistics.mean(extra_large_cluster_pp_lst), 2)
        else:
            rand_pp_cnt_3_5_to_7 = 0
            rand_pp_sum_3_5_to_7 = 0
            rand_pp_avg_3_5_to_7 = 0
    else:
        extra_large_cluster_pp_lst = []

    if len(pstv_rand_swing_per_lst) > 0:
        cluster_11_rand_pp_lst = [
            per for per in pstv_rand_swing_per_lst if 7 < per <= 9]
        if len(cluster_11_rand_pp_lst) > 0:
            rand_pp_cnt_7_to_9 = len(cluster_11_rand_pp_lst)
            rand_pp_sum_7_to_9 = round(sum(cluster_11_rand_pp_lst), 2)
            rand_pp_avg_7_to_9 = round(
                statistics.mean(cluster_11_rand_pp_lst), 2)
        else:
            rand_pp_cnt_7_to_9 = 0
            rand_pp_sum_7_to_9 = 0
            rand_pp_avg_7_to_9 = 0
    else:
        cluster_11_rand_pp_lst = []

    if len(pstv_rand_swing_per_lst) > 0:
        cluster_12_rand_pp_lst = [
            per for per in pstv_rand_swing_per_lst if 9 < per <= 12]
        if len(cluster_12_rand_pp_lst) > 0:
            rand_pp_cnt_9_to_12 = len(cluster_12_rand_pp_lst)
            rand_pp_sum_9_to_12 = round(sum(cluster_12_rand_pp_lst), 2)
            rand_pp_avg_9_to_12 = round(
                statistics.mean(cluster_12_rand_pp_lst), 2)
        else:
            rand_pp_cnt_9_to_12 = 0
            rand_pp_sum_9_to_12 = 0
            rand_pp_avg_9_to_12 = 0
    else:
        cluster_12_rand_pp_lst = []

    if len(pstv_rand_swing_per_lst) > 0:
        cluster_13_rand_pp_lst = [
            per for per in pstv_rand_swing_per_lst if 12 < per <= 15]
        if len(cluster_13_rand_pp_lst) > 0:
            rand_pp_cnt_12_to_15 = len(cluster_13_rand_pp_lst)
            rand_pp_sum_12_to_15 = round(sum(cluster_13_rand_pp_lst), 2)
            rand_pp_avg_12_to_15 = round(
                statistics.mean(cluster_13_rand_pp_lst), 2)
        else:
            rand_pp_cnt_12_to_15 = 0
            rand_pp_sum_12_to_15 = 0
            rand_pp_avg_12_to_15 = 0
    else:
        cluster_13_rand_pp_lst = []

    # extrema_large_cluster_pp_lst
    if len(pstv_rand_swing_per_lst) > 0:
        extreme_large_cluster_pp_lst = [
            per for per in pstv_rand_swing_per_lst if 7 < per <= 15]
        if len(extreme_large_cluster_pp_lst) > 0:
            rand_pp_cnt_7_to_15 = len(extreme_large_cluster_pp_lst)
            rand_pp_sum_7_to_15 = round(sum(extreme_large_cluster_pp_lst), 2)
            rand_pp_avg_7_to_15 = round(
                statistics.mean(extreme_large_cluster_pp_lst), 2)
        else:
            rand_pp_cnt_7_to_15 = 0
            rand_pp_sum_7_to_15 = 0
            rand_pp_avg_7_to_15 = 0
    else:
        extreme_large_cluster_pp_lst = []

    # Super Extreme large cluster
    if len(pstv_rand_swing_per_lst) > 0:
        super_extreme_large_cluster_pp_lst = [
            per for per in pstv_rand_swing_per_lst if per > 15]
        if len(super_extreme_large_cluster_pp_lst) > 0:
            rand_pp_cnt_15_plus = len(super_extreme_large_cluster_pp_lst)
            rand_pp_sum_15_plus = round(
                sum(super_extreme_large_cluster_pp_lst), 2)
            rand_pp_avg_15_plus = round(statistics.mean(
                super_extreme_large_cluster_pp_lst), 2)
        else:
            rand_pp_cnt_15_plus = 0
            rand_pp_sum_15_plus = 0
            rand_pp_avg_15_plus = 0
    else:
        super_extreme_large_range_pp_lst = []

    rand_pp_cnt_0_to_0_25_lst = str(
        ["rand_pp_0_to_0_25", rand_pp_cnt_0_to_0_25, rand_pp_sum_0_to_0_25, rand_pp_avg_0_to_0_25])
    rand_pp_cnt_0_25_to_0_5_lst = str(
        ["rand_pp_0_25_to_0_5", rand_pp_cnt_0_25_to_0_5, rand_pp_sum_0_25_to_0_5, rand_pp_avg_0_25_to_0_5])
    rand_pp_cnt_0_to_0_5_lst = str(
        ["rand_pp_0_to_0_5", rand_pp_cnt_0_to_0_5, rand_pp_sum_0_to_0_5, rand_pp_avg_0_to_0_5])
    rand_pp_cnt_0_5_to_1_lst = str(
        ["rand_pp_0_5_to_1", rand_pp_cnt_0_5_to_1, rand_pp_sum_0_5_to_1, rand_pp_avg_0_5_to_1])
    rand_pp_cnt_1_to_1_5_lst = str(
        ["rand_pp_1_to_1_5", rand_pp_cnt_1_to_1_5, rand_pp_sum_1_to_1_5, rand_pp_avg_1_to_1_5])
    rand_pp_cnt_0_5_to_1_5_lst = str(
        ["rand_pp_0_5_to_1_5", rand_pp_cnt_0_5_to_1_5, rand_pp_sum_0_5_to_1_5, rand_pp_avg_0_5_to_1_5])
    rand_pp_cnt_1_5_to_2_lst = str(
        ["rand_pp_1_5_to_2", rand_pp_cnt_1_5_to_2, rand_pp_sum_1_5_to_2, rand_pp_avg_1_5_to_2])
    rand_pp_cnt_2_to_2_5_lst = str(
        ["rand_pp_2_to_2_5", rand_pp_cnt_2_to_2_5, rand_pp_sum_2_to_2_5, rand_pp_avg_2_to_2_5])
    rand_pp_cnt_2_5_to_3_5_lst = str(
        ["rand_pp_2_5_to_3_5", rand_pp_cnt_2_5_to_3_5, rand_pp_sum_2_5_to_3_5, rand_pp_avg_2_5_to_3_5])
    rand_pp_cnt_1_5_to_3_5_lst = str(
        ["rand_pp_1_5_to_3_5", rand_pp_cnt_1_5_to_3_5, rand_pp_sum_1_5_to_3_5, rand_pp_avg_1_5_to_3_5])
    rand_pp_cnt_3_5_to_4_5_lst = str(
        ["rand_pp_3_5_to_4_5", rand_pp_cnt_3_5_to_4_5, rand_pp_sum_3_5_to_4_5, rand_pp_avg_3_5_to_4_5])
    rand_pp_cnt_4_5_to_5_5_lst = str(
        ["rand_pp_4_5_to_5_5", rand_pp_cnt_4_5_to_5_5, rand_pp_sum_4_5_to_5_5, rand_pp_avg_4_5_to_5_5])
    rand_pp_cnt_5_5_to_7_lst = str(
        ["rand_pp_5_5_to_7", rand_pp_cnt_5_5_to_7, rand_pp_sum_5_5_to_7, rand_pp_avg_5_5_to_7])
    rand_pp_cnt_3_5_to_7_lst = str(
        ["rand_pp_3_5_to_7", rand_pp_cnt_3_5_to_7, rand_pp_sum_3_5_to_7, rand_pp_avg_3_5_to_7])
    rand_pp_cnt_7_to_9_lst = str(
        ["rand_pp_7_to_9", rand_pp_cnt_7_to_9, rand_pp_sum_7_to_9, rand_pp_avg_7_to_9])
    rand_pp_cnt_9_to_12_lst = str(
        ["rand_pp_9_to_12", rand_pp_cnt_9_to_12, rand_pp_sum_9_to_12, rand_pp_avg_9_to_12])
    rand_pp_cnt_12_to_15_lst = str(
        ["rand_pp_12_to_15", rand_pp_cnt_12_to_15, rand_pp_sum_12_to_15, rand_pp_avg_12_to_15])
    rand_pp_cnt_7_to_15_lst = str(
        ["rand_pp_7_to_15", rand_pp_cnt_7_to_15, rand_pp_sum_7_to_15, rand_pp_avg_7_to_15])
    rand_pp_cnt_15_plus_lst = str(
        ["rand_pp_15_plus", rand_pp_cnt_15_plus, rand_pp_sum_15_plus, rand_pp_avg_15_plus])

    swing_rand_pstv_per_range_lst = [coin_name, coin_time_tf, rand_pp_cnt_0_to_0_25_lst, rand_pp_cnt_0_25_to_0_5_lst, rand_pp_cnt_0_to_0_5_lst, rand_pp_cnt_0_5_to_1_lst, rand_pp_cnt_1_to_1_5_lst, rand_pp_cnt_0_5_to_1_5_lst, rand_pp_cnt_1_5_to_2_lst, rand_pp_cnt_2_to_2_5_lst,
                                     rand_pp_cnt_2_5_to_3_5_lst, rand_pp_cnt_1_5_to_3_5_lst, rand_pp_cnt_3_5_to_4_5_lst, rand_pp_cnt_4_5_to_5_5_lst, rand_pp_cnt_5_5_to_7_lst, rand_pp_cnt_3_5_to_7_lst, rand_pp_cnt_7_to_9_lst, rand_pp_cnt_9_to_12_lst, rand_pp_cnt_12_to_15_lst, rand_pp_cnt_7_to_15_lst, rand_pp_cnt_15_plus_lst]

    swing_rand_pstv_per_range_lst_conv = [
        eval(lst) for lst in swing_rand_pstv_per_range_lst[2:]]
    skip_list = ['rand_pp_0_to_0_5', 'rand_pp_0_5_to_1_5',
                 'rand_pp_1_5_to_3_5', 'rand_pp_3_5_to_7', 'rand_pp_7_to_15']

    swing_rand_pstv_per_range_lst_conv_with_out_large_range = [
        item for item in swing_rand_pstv_per_range_lst_conv if item[0] not in skip_list]
    t_3_rand_pp_ranges = sorted(
        swing_rand_pstv_per_range_lst_conv_with_out_large_range, key=lambda x: abs(x[2]), reverse=True)[:3]
    swing_rand_pstv_per_range_lst.append(t_3_rand_pp_ranges)

    return swing_rand_pstv_per_range_lst


def get_swing_neg_rand_per_cluster_lst(coin_name, coin_time_tf, neg_rand_swing_per_lst):
    if len(neg_rand_swing_per_lst) > 0:
        cluster_1_rand_np_lst = [
            per for per in neg_rand_swing_per_lst if 0 < abs(per) <= 0.25]
        if len(cluster_1_rand_np_lst) > 0:
            rand_np_cnt_0_to_0_25 = len(cluster_1_rand_np_lst)
            rand_np_sum_0_to_0_25 = round(sum(cluster_1_rand_np_lst), 2)
            rand_np_avg_0_to_0_25 = round(
                statistics.mean(cluster_1_rand_np_lst), 2)
        else:
            rand_np_cnt_0_to_0_25 = 0
            rand_np_sum_0_to_0_25 = 0
            rand_np_avg_0_to_0_25 = 0
    else:
        cluster_1_rand_np_lst = []

    if len(neg_rand_swing_per_lst) > 0:
        cluster_2_rand_np_lst = [
            per for per in neg_rand_swing_per_lst if 0.25 < abs(per) <= 0.5]
        if len(cluster_2_rand_np_lst) > 0:
            rand_np_cnt_0_25_to_0_5 = len(cluster_2_rand_np_lst)
            rand_np_sum_0_25_to_0_5 = round(sum(cluster_2_rand_np_lst), 2)
            rand_np_avg_0_25_to_0_5 = round(
                statistics.mean(cluster_2_rand_np_lst), 2)
        else:
            rand_np_cnt_0_25_to_0_5 = 0
            rand_np_sum_0_25_to_0_5 = 0
            rand_np_avg_0_25_to_0_5 = 0
    else:
        cluster_2_rand_np_lst = []

    # small_cluster_np_lst
    if len(neg_rand_swing_per_lst) > 0:
        small_cluster_np_lst = [
            per for per in neg_rand_swing_per_lst if 0 < abs(per) <= 0.5]
        if len(small_cluster_np_lst) > 0:
            rand_np_cnt_0_to_0_5 = len(small_cluster_np_lst)
            rand_np_sum_0_to_0_5 = round(sum(small_cluster_np_lst), 2)
            rand_np_avg_0_to_0_5 = round(
                statistics.mean(small_cluster_np_lst), 2)
        else:
            rand_np_cnt_0_to_0_5 = 0
            rand_np_sum_0_to_0_5 = 0
            rand_np_avg_0_to_0_5 = 0
    else:
        small_cluster_np_lst = []

    if len(neg_rand_swing_per_lst) > 0:
        cluster_3_rand_np_lst = [
            per for per in neg_rand_swing_per_lst if 0.5 < abs(per) <= 1]
        if len(cluster_3_rand_np_lst) > 0:
            rand_np_cnt_0_5_to_1 = len(cluster_3_rand_np_lst)
            rand_np_sum_0_5_to_1 = round(sum(cluster_3_rand_np_lst), 2)
            rand_np_avg_0_5_to_1 = round(
                statistics.mean(cluster_3_rand_np_lst), 2)
        else:
            rand_np_cnt_0_5_to_1 = 0
            rand_np_sum_0_5_to_1 = 0
            rand_np_avg_0_5_to_1 = 0
    else:
        cluster_3_rand_np_lst = []

    if len(neg_rand_swing_per_lst) > 0:
        cluster_4_rand_np_lst = [
            per for per in neg_rand_swing_per_lst if 1 < abs(per) <= 1.5]
        if len(cluster_4_rand_np_lst) > 0:
            rand_np_cnt_1_to_1_5 = len(cluster_4_rand_np_lst)
            rand_np_sum_1_to_1_5 = round(sum(cluster_4_rand_np_lst), 2)
            rand_np_avg_1_to_1_5 = round(
                statistics.mean(cluster_4_rand_np_lst), 2)
        else:
            rand_np_cnt_1_to_1_5 = 0
            rand_np_sum_1_to_1_5 = 0
            rand_np_avg_1_to_1_5 = 0
    else:
        cluster_4_rand_np_lst = []

    # medium_cluster_np_lst
    if len(neg_rand_swing_per_lst) > 0:
        medium_cluster_np_lst = [
            per for per in neg_rand_swing_per_lst if 0.5 < abs(per) <= 1.5]
        if len(medium_cluster_np_lst) > 0:
            rand_np_cnt_0_5_to_1_5 = len(medium_cluster_np_lst)
            rand_np_sum_0_5_to_1_5 = round(sum(medium_cluster_np_lst), 2)
            rand_np_avg_0_5_to_1_5 = round(
                statistics.mean(medium_cluster_np_lst), 2)
        else:
            rand_np_cnt_0_5_to_1_5 = 0
            rand_np_sum_0_5_to_1_5 = 0
            rand_np_avg_0_5_to_1_5 = 0
    else:
        medium_cluster_np_lst = []

    if len(neg_rand_swing_per_lst) > 0:
        cluster_5_rand_np_lst = [
            per for per in neg_rand_swing_per_lst if 1.5 < abs(per) <= 2]
        if len(cluster_5_rand_np_lst) > 0:
            rand_np_cnt_1_5_to_2 = len(cluster_5_rand_np_lst)
            rand_np_sum_1_5_to_2 = round(sum(cluster_5_rand_np_lst), 2)
            rand_np_avg_1_5_to_2 = round(
                statistics.mean(cluster_5_rand_np_lst), 2)
        else:
            rand_np_cnt_1_5_to_2 = 0
            rand_np_sum_1_5_to_2 = 0
            rand_np_avg_1_5_to_2 = 0
    else:
        cluster_5_rand_np_lst = []

    if len(neg_rand_swing_per_lst) > 0:
        cluster_6_rand_np_lst = [
            per for per in neg_rand_swing_per_lst if 2 < abs(per) <= 2.5]
        if len(cluster_6_rand_np_lst) > 0:
            rand_np_cnt_2_to_2_5 = len(cluster_6_rand_np_lst)
            rand_np_sum_2_to_2_5 = round(sum(cluster_6_rand_np_lst), 2)
            rand_np_avg_2_to_2_5 = round(
                statistics.mean(cluster_6_rand_np_lst), 2)
        else:
            rand_np_cnt_2_to_2_5 = 0
            rand_np_sum_2_to_2_5 = 0
            rand_np_avg_2_to_2_5 = 0
    else:
        cluster_6_rand_np_lst = []

    if len(neg_rand_swing_per_lst) > 0:
        cluster_7_rand_np_lst = [
            per for per in neg_rand_swing_per_lst if 2.5 < abs(per) <= 3.5]
        if len(cluster_7_rand_np_lst) > 0:
            rand_np_cnt_2_5_to_3_5 = len(cluster_7_rand_np_lst)
            rand_np_sum_2_5_to_3_5 = round(sum(cluster_7_rand_np_lst), 2)
            rand_np_avg_2_5_to_3_5 = round(
                statistics.mean(cluster_7_rand_np_lst), 2)
        else:
            rand_np_cnt_2_5_to_3_5 = 0
            rand_np_sum_2_5_to_3_5 = 0
            rand_np_avg_2_5_to_3_5 = 0
    else:
        cluster_7_rand_np_lst = []

    # large_cluster_np_lst
    if len(neg_rand_swing_per_lst) > 0:
        large_cluster_np_lst = [
            per for per in neg_rand_swing_per_lst if 1.5 < abs(per) <= 3.5]
        if len(large_cluster_np_lst) > 0:
            rand_np_cnt_1_5_to_3_5 = len(large_cluster_np_lst)
            rand_np_sum_1_5_to_3_5 = round(sum(large_cluster_np_lst), 2)
            rand_np_avg_1_5_to_3_5 = round(
                statistics.mean(large_cluster_np_lst), 2)
        else:
            rand_np_cnt_1_5_to_3_5 = 0
            rand_np_sum_1_5_to_3_5 = 0
            rand_np_avg_1_5_to_3_5 = 0
    else:
        large_cluster_np_lst = []

    if len(neg_rand_swing_per_lst) > 0:
        cluster_8_rand_np_lst = [
            per for per in neg_rand_swing_per_lst if 3.5 < abs(per) <= 4.5]
        if len(cluster_8_rand_np_lst) > 0:
            rand_np_cnt_3_5_to_4_5 = len(cluster_8_rand_np_lst)
            rand_np_sum_3_5_to_4_5 = round(sum(cluster_8_rand_np_lst), 2)
            rand_np_avg_3_5_to_4_5 = round(
                statistics.mean(cluster_8_rand_np_lst), 2)
        else:
            rand_np_cnt_3_5_to_4_5 = 0
            rand_np_sum_3_5_to_4_5 = 0
            rand_np_avg_3_5_to_4_5 = 0
    else:
        cluster_8_rand_np_lst = []

    if len(neg_rand_swing_per_lst) > 0:
        cluster_9_rand_np_lst = [
            per for per in neg_rand_swing_per_lst if 4.5 < abs(per) <= 5.5]
        if len(cluster_9_rand_np_lst) > 0:
            rand_np_cnt_4_5_to_5_5 = len(cluster_9_rand_np_lst)
            rand_np_sum_4_5_to_5_5 = round(sum(cluster_9_rand_np_lst), 2)
            rand_np_avg_4_5_to_5_5 = round(
                statistics.mean(cluster_9_rand_np_lst), 2)
        else:
            rand_np_cnt_4_5_to_5_5 = 0
            rand_np_sum_4_5_to_5_5 = 0
            rand_np_avg_4_5_to_5_5 = 0
    else:
        cluster_9_rand_np_lst = []

    if len(neg_rand_swing_per_lst) > 0:
        cluster_10_rand_np_lst = [
            per for per in neg_rand_swing_per_lst if 5.5 < abs(per) <= 7]
        if len(cluster_10_rand_np_lst) > 0:
            rand_np_cnt_5_5_to_7 = len(cluster_10_rand_np_lst)
            rand_np_sum_5_5_to_7 = round(sum(cluster_10_rand_np_lst), 2)
            rand_np_avg_5_5_to_7 = round(
                statistics.mean(cluster_10_rand_np_lst), 2)
        else:
            rand_np_cnt_5_5_to_7 = 0
            rand_np_sum_5_5_to_7 = 0
            rand_np_avg_5_5_to_7 = 0
    else:
        cluster_10_rand_np_lst = []

    # extra_large_cluster_np_lst
    if len(neg_rand_swing_per_lst) > 0:
        extra_large_cluster_np_lst = [
            per for per in neg_rand_swing_per_lst if 3.5 < abs(per) <= 7]
        if len(extra_large_cluster_np_lst) > 0:
            rand_np_cnt_3_5_to_7 = len(extra_large_cluster_np_lst)
            rand_np_sum_3_5_to_7 = round(sum(extra_large_cluster_np_lst), 2)
            rand_np_avg_3_5_to_7 = round(
                statistics.mean(extra_large_cluster_np_lst), 2)
        else:
            rand_np_cnt_3_5_to_7 = 0
            rand_np_sum_3_5_to_7 = 0
            rand_np_avg_3_5_to_7 = 0
    else:
        extra_large_cluster_np_lst = []

    if len(neg_rand_swing_per_lst) > 0:
        cluster_11_rand_np_lst = [
            per for per in neg_rand_swing_per_lst if 7 < abs(per) <= 9]
        if len(cluster_11_rand_np_lst) > 0:
            rand_np_cnt_7_to_9 = len(cluster_11_rand_np_lst)
            rand_np_sum_7_to_9 = round(sum(cluster_11_rand_np_lst), 2)
            rand_np_avg_7_to_9 = round(
                statistics.mean(cluster_11_rand_np_lst), 2)
        else:
            rand_np_cnt_7_to_9 = 0
            rand_np_sum_7_to_9 = 0
            rand_np_avg_7_to_9 = 0
    else:
        cluster_11_rand_np_lst = []

    if len(neg_rand_swing_per_lst) > 0:
        cluster_12_rand_np_lst = [
            per for per in neg_rand_swing_per_lst if 9 < abs(per) <= 12]
        if len(cluster_12_rand_np_lst) > 0:
            rand_np_cnt_9_to_12 = len(cluster_12_rand_np_lst)
            rand_np_sum_9_to_12 = round(sum(cluster_12_rand_np_lst), 2)
            rand_np_avg_9_to_12 = round(
                statistics.mean(cluster_12_rand_np_lst), 2)
        else:
            rand_np_cnt_9_to_12 = 0
            rand_np_sum_9_to_12 = 0
            rand_np_avg_9_to_12 = 0
    else:
        cluster_12_rand_np_lst = []

    if len(neg_rand_swing_per_lst) > 0:
        cluster_13_rand_np_lst = [
            per for per in neg_rand_swing_per_lst if 12 < abs(per) <= 15]
        if len(cluster_13_rand_np_lst) > 0:
            rand_np_cnt_12_to_15 = len(cluster_13_rand_np_lst)
            rand_np_sum_12_to_15 = round(sum(cluster_13_rand_np_lst), 2)
            rand_np_avg_12_to_15 = round(
                statistics.mean(cluster_13_rand_np_lst), 2)
        else:
            rand_np_cnt_12_to_15 = 0
            rand_np_sum_12_to_15 = 0
            rand_np_avg_12_to_15 = 0
    else:
        cluster_13_rand_np_lst = []

    # extrema_large_cluster_np_lst
    if len(neg_rand_swing_per_lst) > 0:
        extreme_large_cluster_np_lst = [
            per for per in neg_rand_swing_per_lst if 7 < abs(per) <= 15]
        if len(extreme_large_cluster_np_lst) > 0:
            rand_np_cnt_7_to_15 = len(extreme_large_cluster_np_lst)
            rand_np_sum_7_to_15 = round(sum(extreme_large_cluster_np_lst), 2)
            rand_np_avg_7_to_15 = round(
                statistics.mean(extreme_large_cluster_np_lst), 2)
        else:
            rand_np_cnt_7_to_15 = 0
            rand_np_sum_7_to_15 = 0
            rand_np_avg_7_to_15 = 0
    else:
        extreme_large_cluster_np_lst = []

    # Super Extreme large cluster
    if len(neg_rand_swing_per_lst) > 0:
        super_extreme_large_cluster_np_lst = [
            per for per in neg_rand_swing_per_lst if abs(per) > 15]
        if len(super_extreme_large_cluster_np_lst) > 0:
            rand_np_cnt_15_plus = len(super_extreme_large_cluster_np_lst)
            rand_np_sum_15_plus = round(
                sum(super_extreme_large_cluster_np_lst), 2)
            rand_np_avg_15_plus = round(statistics.mean(
                super_extreme_large_cluster_np_lst), 2)
        else:
            rand_np_cnt_15_plus = 0
            rand_np_sum_15_plus = 0
            rand_np_avg_15_plus = 0
    else:
        super_extreme_large_range_np_lst = []

    rand_np_cnt_0_to_0_25_lst = str(
        ["rand_np_0_to_0_25", rand_np_cnt_0_to_0_25, rand_np_sum_0_to_0_25, rand_np_avg_0_to_0_25])
    rand_np_cnt_0_25_to_0_5_lst = str(
        ["rand_np_0_25_to_0_5", rand_np_cnt_0_25_to_0_5, rand_np_sum_0_25_to_0_5, rand_np_avg_0_25_to_0_5])
    rand_np_cnt_0_to_0_5_lst = str(
        ["rand_np_0_to_0_5", rand_np_cnt_0_to_0_5, rand_np_sum_0_to_0_5, rand_np_avg_0_to_0_5])
    rand_np_cnt_0_5_to_1_lst = str(
        ["rand_np_0_5_to_1", rand_np_cnt_0_5_to_1, rand_np_sum_0_5_to_1, rand_np_avg_0_5_to_1])
    rand_np_cnt_1_to_1_5_lst = str(
        ["rand_np_1_to_1_5", rand_np_cnt_1_to_1_5, rand_np_sum_1_to_1_5, rand_np_avg_1_to_1_5])
    rand_np_cnt_0_5_to_1_5_lst = str(
        ["rand_np_0_5_to_1_5", rand_np_cnt_0_5_to_1_5, rand_np_sum_0_5_to_1_5, rand_np_avg_0_5_to_1_5])
    rand_np_cnt_1_5_to_2_lst = str(
        ["rand_np_1_5_to_2", rand_np_cnt_1_5_to_2, rand_np_sum_1_5_to_2, rand_np_avg_1_5_to_2])
    rand_np_cnt_2_to_2_5_lst = str(
        ["rand_np_2_to_2_5", rand_np_cnt_2_to_2_5, rand_np_sum_2_to_2_5, rand_np_avg_2_to_2_5])
    rand_np_cnt_2_5_to_3_5_lst = str(
        ["rand_np_2_5_to_3_5", rand_np_cnt_2_5_to_3_5, rand_np_sum_2_5_to_3_5, rand_np_avg_2_5_to_3_5])
    rand_np_cnt_1_5_to_3_5_lst = str(
        ["rand_np_1_5_to_3_5", rand_np_cnt_1_5_to_3_5, rand_np_sum_1_5_to_3_5, rand_np_avg_1_5_to_3_5])
    rand_np_cnt_3_5_to_4_5_lst = str(
        ["rand_np_3_5_to_4_5", rand_np_cnt_3_5_to_4_5, rand_np_sum_3_5_to_4_5, rand_np_avg_3_5_to_4_5])
    rand_np_cnt_4_5_to_5_5_lst = str(
        ["rand_np_4_5_to_5_5", rand_np_cnt_4_5_to_5_5, rand_np_sum_4_5_to_5_5, rand_np_avg_4_5_to_5_5])
    rand_np_cnt_5_5_to_7_lst = str(
        ["rand_np_5_5_to_7", rand_np_cnt_5_5_to_7, rand_np_sum_5_5_to_7, rand_np_avg_5_5_to_7])
    rand_np_cnt_3_5_to_7_lst = str(
        ["rand_np_3_5_to_7", rand_np_cnt_3_5_to_7, rand_np_sum_3_5_to_7, rand_np_avg_3_5_to_7])
    rand_np_cnt_7_to_9_lst = str(
        ["rand_np_7_to_9", rand_np_cnt_7_to_9, rand_np_sum_7_to_9, rand_np_avg_7_to_9])
    rand_np_cnt_9_to_12_lst = str(
        ["rand_np_9_to_12", rand_np_cnt_9_to_12, rand_np_sum_9_to_12, rand_np_avg_9_to_12])
    rand_np_cnt_12_to_15_lst = str(
        ["rand_np_12_to_15", rand_np_cnt_12_to_15, rand_np_sum_12_to_15, rand_np_avg_12_to_15])
    rand_np_cnt_7_to_15_lst = str(
        ["rand_np_7_to_15", rand_np_cnt_7_to_15, rand_np_sum_7_to_15, rand_np_avg_7_to_15])
    rand_np_cnt_15_plus_lst = str(
        ["rand_np_15_plus", rand_np_cnt_15_plus, rand_np_sum_15_plus, rand_np_avg_15_plus])

    swing_rand_neg_per_range_lst = [coin_name, coin_time_tf, rand_np_cnt_0_to_0_25_lst, rand_np_cnt_0_25_to_0_5_lst, rand_np_cnt_0_to_0_5_lst, rand_np_cnt_0_5_to_1_lst, rand_np_cnt_1_to_1_5_lst, rand_np_cnt_0_5_to_1_5_lst, rand_np_cnt_1_5_to_2_lst, rand_np_cnt_2_to_2_5_lst,
                                    rand_np_cnt_2_5_to_3_5_lst, rand_np_cnt_1_5_to_3_5_lst, rand_np_cnt_3_5_to_4_5_lst, rand_np_cnt_4_5_to_5_5_lst, rand_np_cnt_5_5_to_7_lst, rand_np_cnt_3_5_to_7_lst, rand_np_cnt_7_to_9_lst, rand_np_cnt_9_to_12_lst, rand_np_cnt_12_to_15_lst, rand_np_cnt_7_to_15_lst, rand_np_cnt_15_plus_lst]

    swing_rand_neg_per_range_lst_conv = [
        eval(lst) for lst in swing_rand_neg_per_range_lst[2:]]
    skip_list = ['rand_np_0_to_0_5', 'rand_np_0_5_to_1_5',
                 'rand_np_1_5_to_3_5', 'rand_np_3_5_to_7', 'rand_np_7_to_15']

    swing_rand_neg_per_range_lst_conv_with_out_large_range = [
        item for item in swing_rand_neg_per_range_lst_conv if item[0] not in skip_list]
    t_3_rand_np_ranges = sorted(
        swing_rand_neg_per_range_lst_conv_with_out_large_range, key=lambda x: abs(x[2]), reverse=True)[:3]
    swing_rand_neg_per_range_lst.append(t_3_rand_np_ranges)

    return swing_rand_neg_per_range_lst


def get_swing_time_and_rsi_diff_lst(coin_name, coin_time_tf, all_swing_per_rand_time_rsi_diff_lst, pstv_swing_per_rand_time_rsi_diff_lst, neg_swing_per_rand_time_rsi_diff_lst, swing_per_zero_rand_time_rsi_diff_lst, pstv_swing_per_zero_rand_time_rsi_diff_lst, neg_swing_per_zero_rand_time_rsi_diff_lst):
    # Overall swing time info
    sum_all_swings_time = round(
        sum([swing[2] for swing in all_swing_per_rand_time_rsi_diff_lst]), 2)
    all_swing_max_time = round(
        max([swing[2] for swing in all_swing_per_rand_time_rsi_diff_lst]), 2)
    all_swing_min_time = round(
        min([swing[2] for swing in all_swing_per_rand_time_rsi_diff_lst]), 2)
    all_swing_avg_time = round(statistics.mean(
        [swing[2] for swing in all_swing_per_rand_time_rsi_diff_lst]), 2)
    all_swing_median_time = round(statistics.median(
        [swing[2] for swing in all_swing_per_rand_time_rsi_diff_lst]), 2)

    # Positive Swing Percentage
    total_pstv_swings_time = round(
        sum([swing[2] for swing in pstv_swing_per_rand_time_rsi_diff_lst]), 2)
    pstv_swing_max_time = round(
        max([swing[2] for swing in pstv_swing_per_rand_time_rsi_diff_lst]), 2)
    pstv_swing_min_time = round(
        min([swing[2] for swing in pstv_swing_per_rand_time_rsi_diff_lst]), 2)
    pstv_swing_avg_time = round(statistics.mean(
        [swing[2] for swing in pstv_swing_per_rand_time_rsi_diff_lst]), 2)
    pstv_swing_median_time = round(statistics.median(
        [swing[2] for swing in pstv_swing_per_rand_time_rsi_diff_lst]), 2)

    # Negative Swing Percentage
    total_neg_swings_time = round(
        sum([swing[2] for swing in neg_swing_per_rand_time_rsi_diff_lst]), 2)
    neg_swing_max_time = round(
        max([swing[2] for swing in neg_swing_per_rand_time_rsi_diff_lst]), 2)
    neg_swing_min_time = round(
        min([swing[2] for swing in neg_swing_per_rand_time_rsi_diff_lst]), 2)
    neg_swing_avg_time = round(statistics.mean(
        [swing[2] for swing in neg_swing_per_rand_time_rsi_diff_lst]), 2)
    neg_swing_median_time = round(statistics.median(
        [swing[2] for swing in neg_swing_per_rand_time_rsi_diff_lst]), 2)

    # top_10 Positive Swing Percentage
    if len(pstv_swing_per_rand_time_rsi_diff_lst) >= 10:
        t_10_lrg_pp_sp_time_lst = sorted(
            pstv_swing_per_rand_time_rsi_diff_lst, key=lambda x: x[0], reverse=True)[:10]
        t_10_sml_pp_sp_time_lst = sorted(
            pstv_swing_per_rand_time_rsi_diff_lst, key=lambda x: x[0], reverse=False)[:10]
        t_5_lrg_pp_sp_time_lst = str(sorted(
            pstv_swing_per_rand_time_rsi_diff_lst, key=lambda x: x[0], reverse=True)[:5])
    elif len(pstv_swing_per_rand_time_rsi_diff_lst) > 0 and len(pstv_swing_per_rand_time_rsi_diff_lst) < 10:
        t_10_lrg_pp_sp_time_lst = sorted(pstv_swing_per_rand_time_rsi_diff_lst, key=lambda x: x[0], reverse=True)[
            :len(pstv_swing_per_rand_time_rsi_diff_lst)]
        t_10_sml_pp_sp_time_lst = sorted(pstv_swing_per_rand_time_rsi_diff_lst, key=lambda x: x[0], reverse=False)[
            :len(pstv_swing_per_rand_time_rsi_diff_lst)]
        t_5_lrg_pp_sp_time_lst = str(sorted(sorted(
            pstv_swing_per_rand_time_rsi_diff_lst, key=lambda x: x[0], reverse=True)[:5]))
    else:
        t_10_lrg_pp_sp_time_lst = [0]
        t_10_sml_pp_sp_time_lst = [0]
        t_5_lrg_pp_sp_time_lst = str([0])

    # top_10 Negative Swing Percentage
    if len(neg_swing_per_rand_time_rsi_diff_lst) >= 10:
        t_10_lrg_np_sp_time_lst = sorted(
            neg_swing_per_rand_time_rsi_diff_lst, key=lambda x: x[0], reverse=False)[:10]
        t_10_sml_np_sp_time_lst = sorted(
            neg_swing_per_rand_time_rsi_diff_lst, key=lambda x: x[0], reverse=True)[:10]
        t_5_lrg_np_sp_time_lst = str(sorted(
            neg_swing_per_rand_time_rsi_diff_lst, key=lambda x: x[0], reverse=False)[:5])
    elif len(neg_swing_per_rand_time_rsi_diff_lst) > 0 and len(neg_swing_per_rand_time_rsi_diff_lst) < 10:
        t_10_lrg_np_sp_time_lst = sorted(neg_swing_per_rand_time_rsi_diff_lst, key=lambda x: x[0], reverse=False)[
            :len(neg_swing_per_rand_time_rsi_diff_lst)]
        t_10_sml_np_sp_time_lst = sorted(neg_swing_per_rand_time_rsi_diff_lst, key=lambda x: x[0], reverse=True)[
            :len(neg_swing_per_rand_time_rsi_diff_lst)]
        t_5_lrg_np_sp_time_lst = str(sorted(sorted(
            neg_swing_per_rand_time_rsi_diff_lst, key=lambda x: x[0], reverse=False)[:5]))
    else:
        t_10_lrg_np_sp_time_lst = [0]
        t_10_sml_np_sp_time_lst = [0]
        t_5_lrg_np_sp_time_lst = str([0])

    # top_10 pstv and neg swing per with time info
    top_10_lrg_pstv_total_per_change = round(
        sum([swing[0] for swing in t_10_lrg_pp_sp_time_lst]), 2)
    top_10_lrg_pstv_total_rand_per_change = round(
        sum([swing[1] for swing in t_10_lrg_pp_sp_time_lst]), 2)
    top_10_lrg_pstv_total_swings_time = round(
        sum([swing[2] for swing in t_10_lrg_pp_sp_time_lst]), 2)
    top_10_lrg_pstv_max_time = round(
        max([swing[2] for swing in t_10_lrg_pp_sp_time_lst]), 2)
    top_10_lrg_pstv_min_time = round(
        min([swing[2] for swing in t_10_lrg_pp_sp_time_lst]), 2)
    top_10_lrg_pstv_avg_time = round(statistics.mean(
        [swing[2] for swing in t_10_lrg_pp_sp_time_lst]), 2)
    top_10_lrg_pstv_median_time = round(statistics.median(
        [swing[2] for swing in t_10_lrg_pp_sp_time_lst]), 2)
    t_5_lrg_pstv_sp_time = t_5_lrg_pp_sp_time_lst

    top_10_sml_pstv_total_per_change = round(
        sum([swing[0] for swing in t_10_sml_pp_sp_time_lst]), 2)
    top_10_sml_pstv_total_rand_per_change = round(
        sum([swing[1] for swing in t_10_sml_pp_sp_time_lst]), 2)
    top_10_sml_pstv_total_swings_time = round(
        sum([swing[2] for swing in t_10_sml_pp_sp_time_lst]), 2)
    top_10_sml_pstv_max_time = round(
        max([swing[2] for swing in t_10_sml_pp_sp_time_lst]), 2)
    top_10_sml_pstv_min_time = round(
        min([swing[2] for swing in t_10_sml_pp_sp_time_lst]), 2)
    top_10_sml_pstv_avg_time = round(statistics.mean(
        [swing[2] for swing in t_10_sml_pp_sp_time_lst]), 2)
    top_10_sml_pstv_median_time = round(statistics.median(
        [swing[2] for swing in t_10_sml_pp_sp_time_lst]), 2)

    top_10_lrg_neg_total_per_change = round(
        sum([swing[0] for swing in t_10_lrg_np_sp_time_lst]), 2)
    top_10_lrg_neg_total_rand_per_change = round(
        sum([swing[1] for swing in t_10_lrg_np_sp_time_lst]), 2)
    top_10_lrg_neg_total_swings_time = round(
        sum([swing[2] for swing in t_10_lrg_np_sp_time_lst]), 2)
    top_10_lrg_neg_max_time = round(
        max([swing[2] for swing in t_10_lrg_np_sp_time_lst]), 2)
    top_10_lrg_neg_min_time = round(
        min([swing[2] for swing in t_10_lrg_np_sp_time_lst]), 2)
    top_10_lrg_neg_avg_time = round(statistics.mean(
        [swing[2] for swing in t_10_lrg_np_sp_time_lst]), 2)
    top_10_lrg_neg_median_time = round(statistics.median(
        [swing[2] for swing in t_10_lrg_np_sp_time_lst]), 2)
    t_5_lrg_neg_sp_time = t_5_lrg_np_sp_time_lst

    top_10_sml_neg_total_per_change = round(
        sum([swing[0] for swing in t_10_sml_np_sp_time_lst]), 2)
    top_10_sml_neg_total_rand_per_change = round(
        sum([swing[1] for swing in t_10_sml_np_sp_time_lst]), 2)
    top_10_sml_neg_total_swings_time = round(
        sum([swing[2] for swing in t_10_sml_np_sp_time_lst]), 2)
    top_10_sml_neg_max_time = round(
        max([swing[2] for swing in t_10_sml_np_sp_time_lst]), 2)
    top_10_sml_neg_min_time = round(
        min([swing[2] for swing in t_10_sml_np_sp_time_lst]), 2)
    top_10_sml_neg_avg_time = round(statistics.mean(
        [swing[2] for swing in t_10_sml_np_sp_time_lst]), 2)
    top_10_sml_neg_median_time = round(statistics.median(
        [swing[2] for swing in t_10_sml_np_sp_time_lst]), 2)

    # Zero rand swing time info
    if len(swing_per_zero_rand_time_rsi_diff_lst) == 0:
        swing_per_zero_rand_time_rsi_diff_lst = [[0, 0, 0, 0]]
    zero_rand_total_swings_time = round(
        sum([swing[2] for swing in swing_per_zero_rand_time_rsi_diff_lst]), 2)
    zero_rand_max_swings_time = round(
        max([swing[2] for swing in swing_per_zero_rand_time_rsi_diff_lst]), 2)
    zero_rand_min_swings_time = round(
        min([swing[2] for swing in swing_per_zero_rand_time_rsi_diff_lst]), 2)
    zero_rand_avg_swings_time = round(statistics.mean(
        [swing[2] for swing in swing_per_zero_rand_time_rsi_diff_lst]), 2)
    zero_rand_med_swings_time = round(statistics.median(
        [swing[2] for swing in swing_per_zero_rand_time_rsi_diff_lst]), 2)

    # Positive Zero rand swing time info
    if len(pstv_swing_per_zero_rand_time_rsi_diff_lst) == 0:
        pstv_swing_per_zero_rand_time_rsi_diff_lst = [[0, 0, 0, 0]]
    zero_rand_pstv_sp_total_swings_time = round(
        sum([swing[2] for swing in pstv_swing_per_zero_rand_time_rsi_diff_lst]), 2)
    zero_rand_pstv_sp_total_swings_per_change = round(
        sum([swing[0] for swing in pstv_swing_per_zero_rand_time_rsi_diff_lst]), 2)
    zero_rand_pstv_sp_max_swings_time = round(
        max([swing[2] for swing in pstv_swing_per_zero_rand_time_rsi_diff_lst]), 2)
    zero_rand_pstv_sp_min_swings_time = round(
        min([swing[2] for swing in pstv_swing_per_zero_rand_time_rsi_diff_lst]), 2)
    zero_rand_pstv_sp_avg_swings_time = round(statistics.mean(
        [swing[2] for swing in pstv_swing_per_zero_rand_time_rsi_diff_lst]), 2)
    zero_rand_pstv_sp_med_swings_time = round(statistics.median(
        [swing[2] for swing in pstv_swing_per_zero_rand_time_rsi_diff_lst]), 2)

    # Negative Zero rand swing time info
    if len(neg_swing_per_zero_rand_time_rsi_diff_lst) == 0:
        neg_swing_per_zero_rand_time_rsi_diff_lst = [[0, 0, 0, 0]]
    zero_rand_neg_sp_total_swings_time = round(
        sum([swing[2] for swing in neg_swing_per_zero_rand_time_rsi_diff_lst]), 2)
    zero_rand_neg_sp_total_swings_per_change = round(
        sum([swing[0] for swing in neg_swing_per_zero_rand_time_rsi_diff_lst]), 2)
    zero_rand_neg_sp_max_swings_time = round(
        max([swing[2] for swing in neg_swing_per_zero_rand_time_rsi_diff_lst]), 2)
    zero_rand_neg_sp_min_swings_time = round(
        min([swing[2] for swing in neg_swing_per_zero_rand_time_rsi_diff_lst]), 2)
    zero_rand_neg_sp_avg_swings_time = round(statistics.mean(
        [swing[2] for swing in neg_swing_per_zero_rand_time_rsi_diff_lst]), 2)
    zero_rand_neg_sp_med_swings_time = round(statistics.median(
        [swing[2] for swing in neg_swing_per_zero_rand_time_rsi_diff_lst]), 2)

    swing_time_analysis_lst = [coin_name, coin_time_tf, sum_all_swings_time, all_swing_max_time, all_swing_min_time, all_swing_avg_time, all_swing_median_time, total_pstv_swings_time, pstv_swing_max_time, pstv_swing_min_time, pstv_swing_avg_time, pstv_swing_median_time, total_neg_swings_time, neg_swing_max_time, neg_swing_min_time, neg_swing_avg_time, neg_swing_median_time, top_10_lrg_pstv_total_per_change, top_10_lrg_pstv_total_rand_per_change, top_10_lrg_pstv_total_swings_time, top_10_lrg_pstv_max_time, top_10_lrg_pstv_min_time, top_10_lrg_pstv_avg_time, top_10_lrg_pstv_median_time, t_5_lrg_pstv_sp_time, top_10_sml_pstv_total_per_change, top_10_sml_pstv_total_rand_per_change, top_10_sml_pstv_total_swings_time, top_10_sml_pstv_max_time, top_10_sml_pstv_min_time, top_10_sml_pstv_avg_time, top_10_sml_pstv_median_time, top_10_lrg_neg_total_per_change, top_10_lrg_neg_total_rand_per_change, top_10_lrg_neg_total_swings_time,
                               top_10_lrg_neg_max_time, top_10_lrg_neg_min_time, top_10_lrg_neg_avg_time, top_10_lrg_neg_median_time, t_5_lrg_neg_sp_time, top_10_sml_neg_total_per_change, top_10_sml_neg_total_rand_per_change, top_10_sml_neg_total_swings_time, top_10_sml_neg_max_time, top_10_sml_neg_min_time, top_10_sml_neg_avg_time, top_10_sml_neg_median_time, zero_rand_total_swings_time, zero_rand_max_swings_time, zero_rand_min_swings_time, zero_rand_avg_swings_time, zero_rand_med_swings_time, zero_rand_pstv_sp_total_swings_time, zero_rand_pstv_sp_total_swings_per_change, zero_rand_pstv_sp_max_swings_time, zero_rand_pstv_sp_min_swings_time, zero_rand_pstv_sp_avg_swings_time, zero_rand_pstv_sp_med_swings_time, zero_rand_neg_sp_total_swings_time, zero_rand_neg_sp_total_swings_per_change, zero_rand_neg_sp_max_swings_time, zero_rand_neg_sp_min_swings_time, zero_rand_neg_sp_avg_swings_time, zero_rand_neg_sp_med_swings_time]

    # Swing RSI Difference Analysis

    # Overall swing rsi difference info
    sum_all_swings_rsi_diff = round(
        sum([swing[3] for swing in all_swing_per_rand_time_rsi_diff_lst]), 2)
    all_swing_max_rsi_diff = round(
        max([swing[3] for swing in all_swing_per_rand_time_rsi_diff_lst]), 2)
    all_swing_min_rsi_diff = round(
        min([swing[3] for swing in all_swing_per_rand_time_rsi_diff_lst]), 2)
    all_swing_avg_rsi_diff = round(statistics.mean(
        [swing[3] for swing in all_swing_per_rand_time_rsi_diff_lst]), 2)
    all_swing_median_rsi_diff = round(statistics.median(
        [swing[3] for swing in all_swing_per_rand_time_rsi_diff_lst]), 2)

    # Positive Swing Percentage
    total_pstv_swings_rsi_diff = round(
        sum([swing[3] for swing in pstv_swing_per_rand_time_rsi_diff_lst]), 2)
    pstv_swing_max_rsi_diff = round(
        max([swing[3] for swing in pstv_swing_per_rand_time_rsi_diff_lst]), 2)
    pstv_swing_min_rsi_diff = round(
        min([swing[3] for swing in pstv_swing_per_rand_time_rsi_diff_lst]), 2)
    pstv_swing_avg_rsi_diff = round(statistics.mean(
        [swing[3] for swing in pstv_swing_per_rand_time_rsi_diff_lst]), 2)
    pstv_swing_median_rsi_diff = round(statistics.median(
        [swing[3] for swing in pstv_swing_per_rand_time_rsi_diff_lst]), 2)

    # Negative Swing Percentage
    total_neg_swings_rsi_diff = round(
        sum([swing[3] for swing in neg_swing_per_rand_time_rsi_diff_lst]), 2)
    neg_swing_max_rsi_diff = round(
        max([swing[3] for swing in neg_swing_per_rand_time_rsi_diff_lst]), 2)
    neg_swing_min_rsi_diff = round(
        min([swing[3] for swing in neg_swing_per_rand_time_rsi_diff_lst]), 2)
    neg_swing_avg_rsi_diff = round(statistics.mean(
        [swing[3] for swing in neg_swing_per_rand_time_rsi_diff_lst]), 2)
    neg_swing_median_rsi_diff = round(statistics.median(
        [swing[3] for swing in neg_swing_per_rand_time_rsi_diff_lst]), 2)

    # top_10 pstv and neg swing per with rsi difference info
    top_10_lrg_pstv_total_per_change = round(
        sum([swing[0] for swing in t_10_lrg_pp_sp_time_lst]), 2)
    top_10_lrg_pstv_total_rand_per_change = round(
        sum([swing[1] for swing in t_10_lrg_pp_sp_time_lst]), 2)
    top_10_lrg_pstv_total_swings_rsi_diff = round(
        sum([swing[3] for swing in t_10_lrg_pp_sp_time_lst]), 2)
    top_10_lrg_pstv_max_rsi_diff = round(
        max([swing[3] for swing in t_10_lrg_pp_sp_time_lst]), 2)
    top_10_lrg_pstv_min_rsi_diff = round(
        min([swing[3] for swing in t_10_lrg_pp_sp_time_lst]), 2)
    top_10_lrg_pstv_avg_rsi_diff = round(statistics.mean(
        [swing[3] for swing in t_10_lrg_pp_sp_time_lst]), 2)
    top_10_lrg_pstv_median_rsi_diff = round(statistics.median(
        [swing[3] for swing in t_10_lrg_pp_sp_time_lst]), 2)
    t_5_lrg_pstv_sp_rsi_diff = t_5_lrg_pp_sp_time_lst

    top_10_sml_pstv_total_per_change = round(
        sum([swing[0] for swing in t_10_sml_pp_sp_time_lst]), 2)
    top_10_sml_pstv_total_rand_per_change = round(
        sum([swing[1] for swing in t_10_sml_pp_sp_time_lst]), 2)
    top_10_sml_pstv_total_swings_rsi_diff = round(
        sum([swing[3] for swing in t_10_sml_pp_sp_time_lst]), 2)
    top_10_sml_pstv_max_rsi_diff = round(
        max([swing[3] for swing in t_10_sml_pp_sp_time_lst]), 2)
    top_10_sml_pstv_min_rsi_diff = round(
        min([swing[3] for swing in t_10_sml_pp_sp_time_lst]), 2)
    top_10_sml_pstv_avg_rsi_diff = round(statistics.mean(
        [swing[3] for swing in t_10_sml_pp_sp_time_lst]), 2)
    top_10_sml_pstv_median_rsi_diff = round(statistics.median(
        [swing[3] for swing in t_10_sml_pp_sp_time_lst]), 2)

    top_10_lrg_neg_total_per_change = round(
        sum([swing[0] for swing in t_10_lrg_np_sp_time_lst]), 2)
    top_10_lrg_neg_total_rand_per_change = round(
        sum([swing[1] for swing in t_10_lrg_np_sp_time_lst]), 2)
    top_10_lrg_neg_total_swings_rsi_diff = round(
        sum([swing[3] for swing in t_10_lrg_np_sp_time_lst]), 2)
    top_10_lrg_neg_max_rsi_diff = round(
        max([swing[3] for swing in t_10_lrg_np_sp_time_lst]), 2)
    top_10_lrg_neg_min_rsi_diff = round(
        min([swing[3] for swing in t_10_lrg_np_sp_time_lst]), 2)
    top_10_lrg_neg_avg_rsi_diff = round(statistics.mean(
        [swing[3] for swing in t_10_lrg_np_sp_time_lst]), 2)
    top_10_lrg_neg_median_rsi_diff = round(statistics.median(
        [swing[3] for swing in t_10_lrg_np_sp_time_lst]), 2)
    t_5_lrg_neg_sp_rsi_diff = t_5_lrg_np_sp_time_lst

    top_10_sml_neg_total_per_change = round(
        sum([swing[0] for swing in t_10_sml_np_sp_time_lst]), 2)
    top_10_sml_neg_total_rand_per_change = round(
        sum([swing[1] for swing in t_10_sml_np_sp_time_lst]), 2)
    top_10_sml_neg_total_swings_rsi_diff = round(
        sum([swing[3] for swing in t_10_sml_np_sp_time_lst]), 2)
    top_10_sml_neg_max_rsi_diff = round(
        max([swing[3] for swing in t_10_sml_np_sp_time_lst]), 2)
    top_10_sml_neg_min_rsi_diff = round(
        min([swing[3] for swing in t_10_sml_np_sp_time_lst]), 2)
    top_10_sml_neg_avg_rsi_diff = round(statistics.mean(
        [swing[3] for swing in t_10_sml_np_sp_time_lst]), 2)
    top_10_sml_neg_median_rsi_diff = round(statistics.median(
        [swing[3] for swing in t_10_sml_np_sp_time_lst]), 2)

    # Zero rand swing rsi diff info
    zero_rand_total_swings_rsi_diff = round(
        sum([swing[3] for swing in swing_per_zero_rand_time_rsi_diff_lst]), 2)
    zero_rand_max_swings_rsi_diff = round(
        max([swing[3] for swing in swing_per_zero_rand_time_rsi_diff_lst]), 2)
    zero_rand_min_swings_rsi_diff = round(
        min([swing[3] for swing in swing_per_zero_rand_time_rsi_diff_lst]), 2)
    zero_rand_avg_swings_rsi_diff = round(statistics.mean(
        [swing[3] for swing in swing_per_zero_rand_time_rsi_diff_lst]), 2)
    zero_rand_med_swings_rsi_diff = round(statistics.median(
        [swing[3] for swing in swing_per_zero_rand_time_rsi_diff_lst]), 2)

    # Positive Zero rand swing rsi diff info
    zero_rand_pstv_sp_total_swings_rsi_diff = round(
        sum([swing[3] for swing in pstv_swing_per_zero_rand_time_rsi_diff_lst]), 2)
    zero_rand_pstv_sp_total_swings_per_change = round(
        sum([swing[0] for swing in pstv_swing_per_zero_rand_time_rsi_diff_lst]), 2)
    zero_rand_pstv_sp_max_swings_rsi_diff = round(
        max([swing[3] for swing in pstv_swing_per_zero_rand_time_rsi_diff_lst]), 2)
    zero_rand_pstv_sp_min_swings_rsi_diff = round(
        min([swing[3] for swing in pstv_swing_per_zero_rand_time_rsi_diff_lst]), 2)
    zero_rand_pstv_sp_avg_swings_rsi_diff = round(statistics.mean(
        [swing[3] for swing in pstv_swing_per_zero_rand_time_rsi_diff_lst]), 2)
    zero_rand_pstv_sp_med_swings_rsi_diff = round(statistics.median(
        [swing[3] for swing in pstv_swing_per_zero_rand_time_rsi_diff_lst]), 2)

    # Negative Zero rand swing rsi diff info
    zero_rand_neg_sp_total_swings_rsi_diff = round(
        sum([swing[3] for swing in neg_swing_per_zero_rand_time_rsi_diff_lst]), 2)
    zero_rand_neg_sp_total_swings_per_change = round(
        sum([swing[0] for swing in neg_swing_per_zero_rand_time_rsi_diff_lst]), 2)
    zero_rand_neg_sp_max_swings_rsi_diff = round(
        max([swing[3] for swing in neg_swing_per_zero_rand_time_rsi_diff_lst]), 2)
    zero_rand_neg_sp_min_swings_rsi_diff = round(
        min([swing[3] for swing in neg_swing_per_zero_rand_time_rsi_diff_lst]), 2)
    zero_rand_neg_sp_avg_swings_rsi_diff = round(statistics.mean(
        [swing[3] for swing in neg_swing_per_zero_rand_time_rsi_diff_lst]), 2)
    zero_rand_neg_sp_med_swings_rsi_diff = round(statistics.median(
        [swing[3] for swing in neg_swing_per_zero_rand_time_rsi_diff_lst]), 2)

    swing_rsi_diff_analysis_lst = [coin_name, coin_time_tf, sum_all_swings_rsi_diff, all_swing_max_rsi_diff, all_swing_min_rsi_diff, all_swing_avg_rsi_diff, all_swing_median_rsi_diff, total_pstv_swings_rsi_diff, pstv_swing_max_rsi_diff, pstv_swing_min_rsi_diff, pstv_swing_avg_rsi_diff, pstv_swing_median_rsi_diff, total_neg_swings_rsi_diff, neg_swing_max_rsi_diff, neg_swing_min_rsi_diff, neg_swing_avg_rsi_diff, neg_swing_median_rsi_diff, top_10_lrg_pstv_total_per_change, top_10_lrg_pstv_total_rand_per_change, top_10_lrg_pstv_total_swings_rsi_diff, top_10_lrg_pstv_max_rsi_diff, top_10_lrg_pstv_min_rsi_diff, top_10_lrg_pstv_avg_rsi_diff, top_10_lrg_pstv_median_rsi_diff, t_5_lrg_pstv_sp_rsi_diff, top_10_sml_pstv_total_per_change, top_10_sml_pstv_total_rand_per_change, top_10_sml_pstv_total_swings_rsi_diff, top_10_sml_pstv_max_rsi_diff, top_10_sml_pstv_min_rsi_diff, top_10_sml_pstv_avg_rsi_diff, top_10_sml_pstv_median_rsi_diff, top_10_lrg_neg_total_per_change, top_10_lrg_neg_total_rand_per_change, top_10_lrg_neg_total_swings_rsi_diff,
                                   top_10_lrg_neg_max_rsi_diff, top_10_lrg_neg_min_rsi_diff, top_10_lrg_neg_avg_rsi_diff, top_10_lrg_neg_median_rsi_diff, t_5_lrg_neg_sp_rsi_diff, top_10_sml_neg_total_per_change, top_10_sml_neg_total_rand_per_change, top_10_sml_neg_total_swings_rsi_diff, top_10_sml_neg_max_rsi_diff, top_10_sml_neg_min_rsi_diff, top_10_sml_neg_avg_rsi_diff, top_10_sml_neg_median_rsi_diff, zero_rand_total_swings_rsi_diff, zero_rand_max_swings_rsi_diff, zero_rand_min_swings_rsi_diff, zero_rand_avg_swings_rsi_diff, zero_rand_med_swings_rsi_diff, zero_rand_pstv_sp_total_swings_rsi_diff, zero_rand_pstv_sp_total_swings_per_change, zero_rand_pstv_sp_max_swings_rsi_diff, zero_rand_pstv_sp_min_swings_rsi_diff, zero_rand_pstv_sp_avg_swings_rsi_diff, zero_rand_pstv_sp_med_swings_rsi_diff, zero_rand_neg_sp_total_swings_rsi_diff, zero_rand_neg_sp_total_swings_per_change, zero_rand_neg_sp_max_swings_rsi_diff, zero_rand_neg_sp_min_swings_rsi_diff, zero_rand_neg_sp_avg_swings_rsi_diff, zero_rand_neg_sp_med_swings_rsi_diff]

    return [swing_time_analysis_lst, swing_rsi_diff_analysis_lst]


def get_swing_fb_info_lst(coin_name, coin_time_tf, fb_coin):
    if (len(fb_coin) > 0):
        total_fb = fb_coin[-4]
        total_pstv_fb = fb_coin[-3]
        total_neg_fb = fb_coin[-2]
        last_fb_time = fb_coin[-1]
        swing_fb_analysis_lst = [coin_name, coin_time_tf,
                                 total_fb, total_pstv_fb, total_neg_fb, last_fb_time]
    else:
        swing_fb_analysis_lst = [coin_name,
                                 coin_time_tf, "NA", "NA", "NA", "NA"]

    return swing_fb_analysis_lst


def get_last_3_swings_info(last_3_swings_info):
    if (len(last_3_swings_info[2]) == 3):
        swing_1_info = [last_3_swings_info[2]
                        [0][2], last_3_swings_info[2][0][3]]
        swing_2_info = [last_3_swings_info[2]
                        [1][2], last_3_swings_info[2][1][3]]
        swing_3_info = [last_3_swings_info[2]
                        [2][2], last_3_swings_info[2][2][3]]
        swing_1_dir = last_3_swings_info[2][0][4]
        swing_2_dir = last_3_swings_info[2][1][4]
        swing_3_dir = last_3_swings_info[2][2][4]
        last_3_s_per_sum = round((abs(last_3_swings_info[2][0][5]) + abs(
            last_3_swings_info[2][1][5]) + abs(last_3_swings_info[2][2][5])), 2)
        last_3_s_per_avg = round((last_3_s_per_sum/3), 2)
        last_3_s_rand_sum = round((abs(last_3_swings_info[2][0][6]) + abs(
            last_3_swings_info[2][1][6]) + abs(last_3_swings_info[2][2][6])), 2)
        last_3_s_rand_avg = round((last_3_s_rand_sum/3), 2)
        last_3_s_total_time = round((abs(last_3_swings_info[2][0][7]) + abs(
            last_3_swings_info[2][1][7]) + abs(last_3_swings_info[2][2][7])), 2)
        last_3_s_avg_time = round((last_3_s_total_time/3), 2)
        last_3_s_rsi_diff_sum = round((abs(last_3_swings_info[2][0][11]) + abs(
            last_3_swings_info[2][1][11]) + abs(last_3_swings_info[2][2][11])), 2)
        last_3_s_rsi_diff_avg = round((last_3_s_rsi_diff_sum/3), 2)
        last_swing_per = round(abs(last_3_swings_info[2][2][5]), 2)
        last_swing_rand_per = round(abs(last_3_swings_info[2][2][6]), 2)
        last_swing_time = round(abs(last_3_swings_info[2][2][7]), 2)
        last_swing_rsi_dif = round(abs(last_3_swings_info[2][2][11])/10, 2)

        str_info_1 = [swing_1_info, swing_2_info, swing_3_info,
                      swing_1_dir, swing_2_dir, swing_3_dir]

        get_last_3_swings_rank_1 = [last_swing_per, last_swing_rand_per, last_swing_time, last_swing_rsi_dif,
                                    last_3_s_per_sum, last_3_s_per_avg, last_3_s_rand_sum, last_3_s_rand_avg, last_3_s_avg_time, last_3_s_rsi_diff_avg]

        get_last_3_swings_rank_2 = [last_swing_per, last_swing_rand_per, last_swing_time,
                                    last_swing_rsi_dif, last_3_s_per_sum, last_3_s_rand_sum, last_3_s_avg_time, last_3_s_rsi_diff_avg]

        get_last_3_swings_rank_3 = [last_swing_per, last_swing_rand_per, last_swing_time,
                                    last_swing_rsi_dif, last_3_s_per_sum, last_3_s_rand_avg, last_3_s_avg_time, last_3_s_rsi_diff_avg]

        get_last_3_swings_rank_4 = [last_swing_per, last_swing_rand_per, last_swing_time,
                                    last_swing_rsi_dif, last_3_s_per_avg, last_3_s_rand_sum, last_3_s_avg_time, last_3_s_rsi_diff_avg]

        get_last_3_swings_rank_5 = [last_swing_per, last_swing_rand_per, last_swing_time,
                                    last_swing_rsi_dif, last_3_s_per_avg, last_3_s_rand_avg, last_3_s_avg_time, last_3_s_rsi_diff_avg]

        get_last_3_swings_rank_6 = [last_swing_per, last_swing_rand_per, last_swing_time,
                                    last_swing_rsi_dif, last_3_s_per_avg, last_3_s_rand_avg, last_3_s_avg_time, last_3_s_rsi_diff_avg]

        return [str_info_1, get_last_3_swings_rank_1, get_last_3_swings_rank_2, get_last_3_swings_rank_3, get_last_3_swings_rank_4, get_last_3_swings_rank_5, get_last_3_swings_rank_6]

    else:
        print("Not getting the last 3 swings")
        return [0, 0, 0, 0, 0, 0, 0]


def get_s_per_analysis_2_info(s_per_analysis_data):
    if len(s_per_analysis_data) > 0:
        all_swing_count = round(abs(s_per_analysis_data[2])/100, 2)
        all_swings_pp_count = round(abs(s_per_analysis_data[3])/100, 2)
        all_swings_np_count = round(abs(s_per_analysis_data[4])/100, 2)
        all_swing_per_sum = abs(s_per_analysis_data[5])
        all_swings_pp_sum = abs(s_per_analysis_data[6])
        all_swings_np_sum = abs(s_per_analysis_data[7])
        all_swings_pp_avg = abs(s_per_analysis_data[8])
        all_swings_np_avg = abs(s_per_analysis_data[9])
        all_swings_pp_med = abs(s_per_analysis_data[10])
        all_swings_np_med = abs(s_per_analysis_data[11])
        t_5_lrg_pp_sp_lst = s_per_analysis_data[12]
        t_5_lrg_np_sp_lst = s_per_analysis_data[13]
        t_10_lrg_pp_sp_sum = abs(s_per_analysis_data[14])
        t_10_lrg_np_sp_sum = abs(s_per_analysis_data[15])
        t_10_lrg_pp_sp_avg = abs(s_per_analysis_data[16])
        t_10_lrg_np_sp_avg = abs(s_per_analysis_data[17])
        t_10_lrg_pp_sp_med = abs(s_per_analysis_data[18])
        t_10_lrg_np_sp_med = abs(s_per_analysis_data[19])
        t_10_sml_pp_sp_sum = abs(s_per_analysis_data[20])
        t_10_sml_np_sp_sum = abs(s_per_analysis_data[21])
        t_10_sml_pp_sp_avg = abs(s_per_analysis_data[22])
        t_10_sml_np_sp_avg = abs(s_per_analysis_data[23])
        t_10_sml_pp_sp_med = abs(s_per_analysis_data[24])
        t_10_sml_np_sp_med = abs(s_per_analysis_data[25])

        str_info_2 = [t_5_lrg_pp_sp_lst, t_5_lrg_np_sp_lst]
        s_per_analysis_rank_1 = [all_swing_count, all_swings_pp_count, all_swings_np_count, all_swing_per_sum, all_swings_pp_sum, all_swings_np_sum, all_swings_pp_avg, all_swings_np_avg, all_swings_pp_med, all_swings_np_med, t_10_lrg_pp_sp_sum,
                                 t_10_lrg_np_sp_sum, t_10_lrg_pp_sp_avg, t_10_lrg_np_sp_avg, t_10_lrg_pp_sp_med, t_10_lrg_np_sp_med, t_10_sml_pp_sp_sum, t_10_sml_np_sp_sum, t_10_sml_pp_sp_avg, t_10_sml_np_sp_avg, t_10_sml_pp_sp_med, t_10_sml_np_sp_med]

        s_per_analysis_rank_2 = [all_swing_count, all_swings_pp_count, all_swings_np_count, all_swing_per_sum,
                                 all_swings_pp_sum, all_swings_np_sum, t_10_lrg_pp_sp_sum, t_10_lrg_np_sp_sum, t_10_sml_pp_sp_sum, t_10_sml_np_sp_sum]

        s_per_analysis_rank_3 = [all_swing_count, all_swings_pp_count, all_swings_np_count, all_swing_per_sum,
                                 all_swings_pp_sum, all_swings_np_sum, t_10_lrg_pp_sp_sum, t_10_lrg_np_sp_sum, t_10_sml_pp_sp_sum, t_10_sml_np_sp_sum]

        s_per_analysis_rank_4 = [all_swing_count, all_swings_pp_count, all_swings_np_count, all_swings_pp_avg,
                                 all_swings_np_avg, t_10_lrg_pp_sp_avg, t_10_lrg_np_sp_avg, t_10_sml_pp_sp_avg, t_10_sml_np_sp_avg]

        s_per_analysis_rank_5 = [all_swing_count, all_swings_pp_count, all_swings_np_count, all_swings_pp_avg,
                                 all_swings_np_avg, t_10_lrg_pp_sp_avg, t_10_lrg_np_sp_avg, t_10_sml_pp_sp_avg, t_10_sml_np_sp_avg]

        s_per_analysis_rank_6 = [all_swing_count, all_swings_pp_count, all_swings_np_count, all_swings_pp_med,
                                 all_swings_np_med, t_10_lrg_pp_sp_med, t_10_lrg_np_sp_med, t_10_sml_pp_sp_med, t_10_sml_np_sp_med]

        return [str_info_2, s_per_analysis_rank_1, s_per_analysis_rank_2, s_per_analysis_rank_3, s_per_analysis_rank_4, s_per_analysis_rank_5, s_per_analysis_rank_6]
    else:
        print("No data available in s_per_analysis_2_info")
        return [0, 0, 0, 0, 0, 0, 0]


def get_s_pstv_per_rang_3_info(s_pstv_per_rang_data):
    if len(s_pstv_per_rang_data) > 0:
        sp_pp_cnt_0_2_lst = round(ast.literal_eval(
            s_pstv_per_rang_data[4])[1]/10, 2)
        sp_pp_cnt_2_4_lst = round(ast.literal_eval(
            s_pstv_per_rang_data[7])[1]/10, 2)
        sp_pp_cnt_4_7_lst = round(ast.literal_eval(
            s_pstv_per_rang_data[11])[1]/10, 2)
        sp_pp_cnt_7_15_lst = round(ast.literal_eval(
            s_pstv_per_rang_data[16])[1]/10, 2)
        sp_pp_cnt_15_25_lst = round(ast.literal_eval(
            s_pstv_per_rang_data[20])[1]/10, 2)
        t_3_sp_pp_ranges = s_pstv_per_rang_data[22]

        str_info_3 = [t_3_sp_pp_ranges]
        s_pstv_per_rang_rank_1 = s_pstv_per_rang_rank_2 = s_pstv_per_rang_rank_3 = s_pstv_per_rang_rank_4 = s_pstv_per_rang_rank_5 = s_pstv_per_rang_rank_6 = [
            sp_pp_cnt_0_2_lst, sp_pp_cnt_2_4_lst, sp_pp_cnt_4_7_lst, sp_pp_cnt_7_15_lst, sp_pp_cnt_15_25_lst]

        return [str_info_3, s_pstv_per_rang_rank_1, s_pstv_per_rang_rank_2, s_pstv_per_rang_rank_3, s_pstv_per_rang_rank_4, s_pstv_per_rang_rank_5, s_pstv_per_rang_rank_6]

    else:
        print("No records present in the s_pstv_per_rang_data")
        return [0, 0, 0, 0, 0, 0, 0]


def get_s_neg_per_rang_4_info(s_neg_per_rang_data):
    if len(s_neg_per_rang_data) > 0:
        sp_np_cnt_0_2_lst = round(ast.literal_eval(
            s_neg_per_rang_data[4])[1]/10, 2)
        sp_np_cnt_2_4_lst = round(ast.literal_eval(
            s_neg_per_rang_data[7])[1]/10, 2)
        sp_np_cnt_4_7_lst = round(ast.literal_eval(
            s_neg_per_rang_data[11])[1]/10, 2)
        sp_np_cnt_7_15_lst = round(ast.literal_eval(
            s_neg_per_rang_data[16])[1]/10, 2)
        sp_np_cnt_15_25_lst = round(
            ast.literal_eval(s_neg_per_rang_data[20])[1]/10, 2)
        t_3_sp_np_ranges = s_neg_per_rang_data[22]

        str_info_4 = [t_3_sp_np_ranges]
        s_neg_per_rang_rank_1 = s_neg_per_rang_rank_2 = s_neg_per_rang_rank_3 = s_neg_per_rang_rank_4 = s_neg_per_rang_rank_5 = s_neg_per_rang_rank_6 = [
            sp_np_cnt_0_2_lst, sp_np_cnt_2_4_lst, sp_np_cnt_4_7_lst, sp_np_cnt_7_15_lst, sp_np_cnt_15_25_lst]

        return [str_info_4, s_neg_per_rang_rank_1, s_neg_per_rang_rank_2, s_neg_per_rang_rank_3, s_neg_per_rang_rank_4, s_neg_per_rang_rank_5, s_neg_per_rang_rank_6]

    else:
        print("No records present in the s_neg_per_rang_data")
        return [0, 0, 0, 0, 0, 0, 0]


def get_s_rand_per_analysis_5_info(s_rand_per_analysis_data):
    if len(s_rand_per_analysis_data) > 0:
        all_swing_rand_per_sum = abs(s_rand_per_analysis_data[5])
        all_swings_rand_pp_sum = abs(s_rand_per_analysis_data[6])
        all_swings_rand_np_sum = abs(s_rand_per_analysis_data[7])
        all_swings_rand_pp_avg = abs(s_rand_per_analysis_data[8])
        all_swings_rand_np_avg = abs(s_rand_per_analysis_data[9])
        all_swings_rand_pp_med = abs(s_rand_per_analysis_data[10])
        all_swings_rand_np_med = abs(s_rand_per_analysis_data[11])
        t_5_lrg_pp_rand_sp_lst = s_rand_per_analysis_data[12]
        t_5_lrg_np_rand_sp_lst = s_rand_per_analysis_data[13]
        t_10_lrg_pp_rand_sp_sum = abs(s_rand_per_analysis_data[14])
        t_10_lrg_np_rand_sp_sum = abs(s_rand_per_analysis_data[15])
        t_10_lrg_pp_rand_sp_avg = abs(s_rand_per_analysis_data[16])
        t_10_lrg_np_rand_sp_avg = abs(s_rand_per_analysis_data[17])
        t_10_lrg_pp_rand_sp_med = abs(s_rand_per_analysis_data[18])
        t_10_lrg_np_rand_sp_med = abs(s_rand_per_analysis_data[19])
        t_10_sml_pp_rand_sp_sum = abs(s_rand_per_analysis_data[20])
        t_10_sml_np_rand_sp_sum = abs(s_rand_per_analysis_data[21])
        t_10_sml_pp_rand_sp_avg = abs(s_rand_per_analysis_data[22])
        t_10_sml_np_rand_sp_avg = abs(s_rand_per_analysis_data[23])
        t_10_sml_pp_rand_sp_med = abs(s_rand_per_analysis_data[24])
        t_10_sml_np_rand_sp_med = abs(s_rand_per_analysis_data[25])

        str_info_5 = [t_5_lrg_pp_rand_sp_lst, t_5_lrg_np_rand_sp_lst]

        s_rand_per_analysis_rank_1 = [all_swing_rand_per_sum, all_swings_rand_pp_sum, all_swings_rand_np_sum, all_swings_rand_pp_avg, all_swings_rand_np_avg, all_swings_rand_pp_med, all_swings_rand_np_med, t_10_lrg_pp_rand_sp_sum, t_10_lrg_np_rand_sp_sum,
                                      t_10_lrg_pp_rand_sp_avg, t_10_lrg_np_rand_sp_avg, t_10_lrg_pp_rand_sp_med, t_10_lrg_np_rand_sp_med, t_10_sml_pp_rand_sp_sum, t_10_sml_np_rand_sp_sum, t_10_sml_pp_rand_sp_avg, t_10_sml_np_rand_sp_avg, t_10_sml_pp_rand_sp_med, t_10_sml_np_rand_sp_med]

        s_rand_per_analysis_rank_2 = [all_swing_rand_per_sum, all_swings_rand_pp_sum, all_swings_rand_np_sum,
                                      t_10_lrg_pp_rand_sp_sum, t_10_lrg_np_rand_sp_sum, t_10_sml_pp_rand_sp_sum, t_10_sml_np_rand_sp_sum]

        s_rand_per_analysis_rank_3 = [all_swings_rand_pp_avg, all_swings_rand_np_avg,
                                      t_10_lrg_pp_rand_sp_avg, t_10_lrg_np_rand_sp_avg, t_10_sml_pp_rand_sp_avg, t_10_sml_np_rand_sp_avg]

        s_rand_per_analysis_rank_4 = [all_swing_rand_per_sum, all_swings_rand_pp_sum, all_swings_rand_np_sum,
                                      t_10_lrg_pp_rand_sp_sum, t_10_lrg_np_rand_sp_sum, t_10_sml_pp_rand_sp_sum, t_10_sml_np_rand_sp_sum]

        s_rand_per_analysis_rank_5 = [all_swings_rand_pp_avg, all_swings_rand_np_avg,
                                      t_10_lrg_pp_rand_sp_avg, t_10_lrg_np_rand_sp_avg, t_10_sml_pp_rand_sp_avg, t_10_sml_np_rand_sp_avg]

        s_rand_per_analysis_rank_6 = [all_swings_rand_pp_med, all_swings_rand_np_med,
                                      t_10_lrg_pp_rand_sp_med, t_10_lrg_np_rand_sp_med, t_10_sml_pp_rand_sp_med, t_10_sml_np_rand_sp_med]

        return [str_info_5, s_rand_per_analysis_rank_1, s_rand_per_analysis_rank_2, s_rand_per_analysis_rank_3, s_rand_per_analysis_rank_4, s_rand_per_analysis_rank_5, s_rand_per_analysis_rank_6]
    else:
        print("No records found in s_rand_per_analysis_data")
        return [0, 0, 0, 0, 0, 0, 0]


def get_s_zero_rand_cluster_6_info(s_zero_rand_cluster_data):
    if len(s_zero_rand_cluster_data) > 0:
        all_swings_zero_rand_count = round(
            abs(s_zero_rand_cluster_data[2])/10, 2)
        all_swings_zero_rand_pp_count = round(
            abs(s_zero_rand_cluster_data[3])/10, 2)
        all_swings_zero_rand_np_count = round(
            abs(s_zero_rand_cluster_data[4])/10, 2)
        all_swings_zero_rand_pp_sum = abs(s_zero_rand_cluster_data[5])
        all_swings_zero_rand_np_sum = abs(s_zero_rand_cluster_data[6])
        all_swing_zero_rand_per_sum = abs(s_zero_rand_cluster_data[7])
        all_swings_zero_rand_pp_mean = abs(s_zero_rand_cluster_data[8])
        all_swings_zero_rand_np_mean = abs(s_zero_rand_cluster_data[9])
        all_swings_zero_rand_pp_med = abs(s_zero_rand_cluster_data[10])
        all_swings_zero_rand_np_med = abs(s_zero_rand_cluster_data[11])
        t_5_lrg_pp_zero_rand_sp_lst = s_zero_rand_cluster_data[12]
        t_5_lrg_np_zero_rand_sp_lst = s_zero_rand_cluster_data[13]
        t_10_lrg_pp_zero_rand_sp_sum = abs(s_zero_rand_cluster_data[14])
        t_10_lrg_np_zero_rand_sp_sum = abs(s_zero_rand_cluster_data[15])
        t_10_lrg_pp_zero_rand_sp_avg = abs(s_zero_rand_cluster_data[16])
        t_10_lrg_np_zero_rand_sp_avg = abs(s_zero_rand_cluster_data[17])
        t_10_lrg_pp_zero_rand_sp_med = abs(s_zero_rand_cluster_data[18])
        t_10_lrg_np_zero_rand_sp_med = abs(s_zero_rand_cluster_data[19])
        t_10_sml_pp_zero_rand_sp_sum = abs(s_zero_rand_cluster_data[20])
        t_10_sml_np_zero_rand_sp_sum = abs(s_zero_rand_cluster_data[21])
        t_10_sml_pp_zero_rand_sp_avg = abs(s_zero_rand_cluster_data[22])
        t_10_sml_np_zero_rand_sp_avg = abs(s_zero_rand_cluster_data[23])
        t_10_sml_pp_zero_rand_sp_med = abs(s_zero_rand_cluster_data[24])
        t_10_sml_np_zero_rand_sp_med = abs(s_zero_rand_cluster_data[25])

        str_info_6 = [t_5_lrg_pp_zero_rand_sp_lst, t_5_lrg_np_zero_rand_sp_lst]

        s_zero_rand_cluster_rank_1 = [all_swings_zero_rand_count, all_swings_zero_rand_pp_count, all_swings_zero_rand_np_count, all_swings_zero_rand_pp_sum, all_swings_zero_rand_np_sum, all_swing_zero_rand_per_sum, all_swings_zero_rand_pp_mean, all_swings_zero_rand_np_mean, all_swings_zero_rand_pp_med, all_swings_zero_rand_np_med, t_10_lrg_pp_zero_rand_sp_sum,
                                      t_10_lrg_np_zero_rand_sp_sum, t_10_lrg_pp_zero_rand_sp_avg, t_10_lrg_np_zero_rand_sp_avg, t_10_lrg_pp_zero_rand_sp_med, t_10_lrg_np_zero_rand_sp_med, t_10_sml_pp_zero_rand_sp_sum, t_10_sml_np_zero_rand_sp_sum, t_10_sml_pp_zero_rand_sp_avg, t_10_sml_np_zero_rand_sp_avg, t_10_sml_pp_zero_rand_sp_med, t_10_sml_np_zero_rand_sp_med]

        s_zero_rand_cluster_rank_2 = [all_swings_zero_rand_count, all_swings_zero_rand_pp_count, all_swings_zero_rand_np_count, all_swings_zero_rand_pp_sum, all_swings_zero_rand_np_sum,
                                      all_swing_zero_rand_per_sum, t_10_lrg_pp_zero_rand_sp_sum, t_10_lrg_np_zero_rand_sp_sum, t_10_sml_pp_zero_rand_sp_sum, t_10_sml_np_zero_rand_sp_sum]

        s_zero_rand_cluster_rank_3 = [all_swings_zero_rand_count, all_swings_zero_rand_pp_count, all_swings_zero_rand_np_count, all_swings_zero_rand_pp_mean,
                                      all_swings_zero_rand_np_mean, t_10_lrg_pp_zero_rand_sp_avg, t_10_lrg_np_zero_rand_sp_avg, t_10_sml_pp_zero_rand_sp_avg, t_10_sml_np_zero_rand_sp_avg]

        s_zero_rand_cluster_rank_4 = [all_swings_zero_rand_count, all_swings_zero_rand_pp_count, all_swings_zero_rand_np_count, all_swings_zero_rand_pp_sum, all_swings_zero_rand_np_sum,
                                      all_swing_zero_rand_per_sum, t_10_lrg_pp_zero_rand_sp_sum, t_10_lrg_np_zero_rand_sp_sum, t_10_sml_pp_zero_rand_sp_sum, t_10_sml_np_zero_rand_sp_sum]

        s_zero_rand_cluster_rank_5 = [all_swings_zero_rand_count, all_swings_zero_rand_pp_count, all_swings_zero_rand_np_count, all_swings_zero_rand_pp_mean,
                                      all_swings_zero_rand_np_mean, t_10_lrg_pp_zero_rand_sp_avg, t_10_lrg_np_zero_rand_sp_avg, t_10_sml_pp_zero_rand_sp_avg, t_10_sml_np_zero_rand_sp_avg]

        s_zero_rand_cluster_rank_6 = [all_swings_zero_rand_count, all_swings_zero_rand_pp_count, all_swings_zero_rand_np_count, all_swings_zero_rand_pp_med,
                                      all_swings_zero_rand_np_med, t_10_lrg_pp_zero_rand_sp_med, t_10_lrg_np_zero_rand_sp_med, t_10_sml_pp_zero_rand_sp_med, t_10_sml_np_zero_rand_sp_med]

        return [str_info_6, s_zero_rand_cluster_rank_1, s_zero_rand_cluster_rank_2, s_zero_rand_cluster_rank_3, s_zero_rand_cluster_rank_4, s_zero_rand_cluster_rank_5, s_zero_rand_cluster_rank_6]

    else:
        print("No records found in s_zero_rand_cluster_data")
        return [0, 0, 0, 0, 0, 0, 0]


def get_s_pstv_rand_cluster_7_info(s_pstv_rand_cluster_data):
    if len(s_pstv_rand_cluster_data) > 0:
        rand_pp_cnt_0_to_0_25_lst = round(
            ast.literal_eval(s_pstv_rand_cluster_data[2])[1]/10, 2)
        rand_pp_cnt_0_25_to_0_5_lst = round(
            ast.literal_eval(s_pstv_rand_cluster_data[3])[1]/10, 2)
        rand_pp_cnt_0_to_0_5_lst = round(
            ast.literal_eval(s_pstv_rand_cluster_data[4])[1]/10, 2)
        rand_pp_cnt_0_5_to_1_lst = round(
            ast.literal_eval(s_pstv_rand_cluster_data[5])[1]/10, 2)
        rand_pp_cnt_1_to_1_5_lst = round(
            ast.literal_eval(s_pstv_rand_cluster_data[6])[1]/10, 2)
        rand_pp_cnt_0_5_to_1_5_lst = round(
            ast.literal_eval(s_pstv_rand_cluster_data[7])[1]/10, 2)
        rand_pp_cnt_1_5_to_3_5_lst = round(
            ast.literal_eval(s_pstv_rand_cluster_data[11])[1]/10, 2)
        rand_pp_cnt_3_5_to_7_lst = round(
            ast.literal_eval(s_pstv_rand_cluster_data[15])[1]/10, 2)
        rand_pp_cnt_7_to_15_lst = round(ast.literal_eval(
            s_pstv_rand_cluster_data[19])[1]/10, 2)
        t_3_rand_pp_ranges = s_pstv_rand_cluster_data[21]

        str_info_7 = [t_3_rand_pp_ranges]
        s_pstv_rand_cluster_rank_1 = s_pstv_rand_cluster_rank_2 = s_pstv_rand_cluster_rank_3 = s_pstv_rand_cluster_rank_4 = s_pstv_rand_cluster_rank_5 = s_pstv_rand_cluster_rank_6 = [
            rand_pp_cnt_0_to_0_25_lst, rand_pp_cnt_0_25_to_0_5_lst, rand_pp_cnt_0_to_0_5_lst, rand_pp_cnt_0_5_to_1_lst, rand_pp_cnt_1_to_1_5_lst, rand_pp_cnt_0_5_to_1_5_lst, rand_pp_cnt_1_5_to_3_5_lst, rand_pp_cnt_3_5_to_7_lst, rand_pp_cnt_7_to_15_lst]

        return [str_info_7, s_pstv_rand_cluster_rank_1, s_pstv_rand_cluster_rank_2, s_pstv_rand_cluster_rank_3, s_pstv_rand_cluster_rank_4, s_pstv_rand_cluster_rank_5, s_pstv_rand_cluster_rank_6]
    else:
        print("No records found in s_pstv_rand_cluster_data")
        return [0, 0, 0, 0, 0, 0, 0]


def get_s_neg_rand_cluster_8_info(s_neg_rand_cluster_data):
    print("s_neg_rand_cluster_data  ==>", s_neg_rand_cluster_data)
    if len(s_neg_rand_cluster_data) > 0:
        rand_np_cnt_0_to_0_25_lst = round(
            ast.literal_eval(s_neg_rand_cluster_data[2])[1]/10, 2)
        rand_np_cnt_0_25_to_0_5_lst = round(
            ast.literal_eval(s_neg_rand_cluster_data[3])[1]/10, 2)
        rand_np_cnt_0_to_0_5_lst = round(
            ast.literal_eval(s_neg_rand_cluster_data[4])[1]/10, 2)
        rand_np_cnt_0_5_to_1_lst = round(
            ast.literal_eval(s_neg_rand_cluster_data[5])[1]/10, 2)
        rand_np_cnt_1_to_1_5_lst = round(
            ast.literal_eval(s_neg_rand_cluster_data[6])[1]/10, 2)
        rand_np_cnt_0_5_to_1_5_lst = round(
            ast.literal_eval(s_neg_rand_cluster_data[7])[1]/10, 2)
        rand_np_cnt_1_5_to_3_5_lst = round(
            ast.literal_eval(s_neg_rand_cluster_data[11])[1]/10, 2)
        rand_np_cnt_3_5_to_7_lst = round(
            ast.literal_eval(s_neg_rand_cluster_data[15])[1]/10, 2)
        rand_np_cnt_7_to_15_lst = round(
            ast.literal_eval(s_neg_rand_cluster_data[19])[1]/10, 2)
        t_3_rand_np_ranges = s_neg_rand_cluster_data[21]

        str_info_8 = [t_3_rand_np_ranges]
        s_neg_rand_cluster_rank_1 = s_neg_rand_cluster_rank_2 = s_neg_rand_cluster_rank_3 = s_neg_rand_cluster_rank_4 = s_neg_rand_cluster_rank_5 = s_neg_rand_cluster_rank_6 = [
            rand_np_cnt_0_to_0_25_lst, rand_np_cnt_0_25_to_0_5_lst, rand_np_cnt_0_to_0_5_lst, rand_np_cnt_0_5_to_1_lst, rand_np_cnt_1_to_1_5_lst, rand_np_cnt_0_5_to_1_5_lst, rand_np_cnt_1_5_to_3_5_lst, rand_np_cnt_3_5_to_7_lst, rand_np_cnt_7_to_15_lst]

        return [str_info_8, s_neg_rand_cluster_rank_1, s_neg_rand_cluster_rank_2, s_neg_rand_cluster_rank_3, s_neg_rand_cluster_rank_4, s_neg_rand_cluster_rank_5, s_neg_rand_cluster_rank_6]
    else:
        print("No records found in s_neg_rand_cluster_data")
        return [0, 0, 0, 0, 0, 0, 0]


def get_s_time_analysis_9_info(s_time_analysis_data):
    if len(s_time_analysis_data) > 0:
        all_swing_max_time = abs(s_time_analysis_data[3])
        all_swing_avg_time = abs(s_time_analysis_data[5])
        all_swing_median_time = abs(s_time_analysis_data[6])
        pstv_swing_max_time = abs(s_time_analysis_data[8])
        pstv_swing_avg_time = abs(s_time_analysis_data[10])
        pstv_swing_median_time = abs(s_time_analysis_data[11])
        neg_swing_max_time = abs(s_time_analysis_data[13])
        neg_swing_avg_time = abs(s_time_analysis_data[15])
        neg_swing_median_time = abs(s_time_analysis_data[16])
        top_10_lrg_pstv_total_rand_per_change = round(
            abs(s_time_analysis_data[18])/10, 2)
        top_10_lrg_pstv_max_time = abs(s_time_analysis_data[20])
        top_10_lrg_pstv_avg_time = abs(s_time_analysis_data[22])
        top_10_lrg_pstv_median_time = abs(s_time_analysis_data[23])
        top_10_sml_pstv_total_rand_per_change = round(
            abs(s_time_analysis_data[26])/10, 2)
        top_10_sml_pstv_max_time = abs(s_time_analysis_data[28])
        top_10_sml_pstv_avg_time = abs(s_time_analysis_data[30])
        top_10_sml_pstv_median_time = abs(s_time_analysis_data[31])
        top_10_lrg_neg_total_rand_per_change = round(
            abs(s_time_analysis_data[33])/10, 2)
        top_10_lrg_neg_max_time = abs(s_time_analysis_data[35])
        top_10_lrg_neg_avg_time = abs(s_time_analysis_data[37])
        top_10_lrg_neg_median_time = abs(s_time_analysis_data[38])
        top_10_sml_neg_total_rand_per_change = round(
            abs(s_time_analysis_data[41])/10, 2)
        top_10_sml_neg_max_time = abs(s_time_analysis_data[43])
        top_10_sml_neg_avg_time = abs(s_time_analysis_data[45])
        top_10_sml_neg_median_time = abs(s_time_analysis_data[46])
        zero_rand_max_swings_time = abs(s_time_analysis_data[48])
        zero_rand_avg_swings_time = abs(s_time_analysis_data[50])
        zero_rand_med_swings_time = abs(s_time_analysis_data[51])
        zero_rand_pstv_sp_max_swings_time = abs(s_time_analysis_data[54])
        zero_rand_pstv_sp_avg_swings_time = abs(s_time_analysis_data[56])
        zero_rand_pstv_sp_med_swings_time = abs(s_time_analysis_data[57])
        zero_rand_neg_sp_max_swings_time = abs(s_time_analysis_data[60])
        zero_rand_neg_sp_avg_swings_time = abs(s_time_analysis_data[62])
        zero_rand_neg_sp_med_swings_time = abs(s_time_analysis_data[63])

        s_time_analysis_rank_1 = [all_swing_max_time, all_swing_avg_time, all_swing_median_time, pstv_swing_max_time, pstv_swing_avg_time, pstv_swing_median_time, neg_swing_max_time, neg_swing_avg_time, neg_swing_median_time, top_10_lrg_pstv_total_rand_per_change, top_10_lrg_pstv_max_time, top_10_lrg_pstv_avg_time, top_10_lrg_pstv_median_time, top_10_sml_pstv_total_rand_per_change, top_10_sml_pstv_max_time, top_10_sml_pstv_avg_time, top_10_sml_pstv_median_time, top_10_lrg_neg_total_rand_per_change,
                                  top_10_lrg_neg_max_time, top_10_lrg_neg_avg_time, top_10_lrg_neg_median_time, top_10_sml_neg_total_rand_per_change, top_10_sml_neg_max_time, top_10_sml_neg_avg_time, top_10_sml_neg_median_time, zero_rand_max_swings_time, zero_rand_avg_swings_time, zero_rand_med_swings_time, zero_rand_pstv_sp_max_swings_time, zero_rand_pstv_sp_avg_swings_time, zero_rand_pstv_sp_med_swings_time, zero_rand_neg_sp_max_swings_time, zero_rand_neg_sp_avg_swings_time, zero_rand_neg_sp_med_swings_time]

        s_time_analysis_rank_2 = [all_swing_avg_time, pstv_swing_avg_time, neg_swing_avg_time, top_10_lrg_pstv_total_rand_per_change, top_10_lrg_pstv_avg_time, top_10_sml_pstv_total_rand_per_change,
                                  top_10_sml_pstv_avg_time, top_10_lrg_neg_avg_time, top_10_sml_neg_avg_time, zero_rand_avg_swings_time, zero_rand_pstv_sp_avg_swings_time, zero_rand_neg_sp_avg_swings_time]

        s_time_analysis_rank_3 = [all_swing_avg_time, pstv_swing_avg_time, neg_swing_avg_time, top_10_lrg_pstv_total_rand_per_change, top_10_lrg_pstv_avg_time, top_10_sml_pstv_total_rand_per_change,
                                  top_10_sml_pstv_avg_time, top_10_lrg_neg_avg_time, top_10_sml_neg_avg_time, zero_rand_avg_swings_time, zero_rand_pstv_sp_avg_swings_time, zero_rand_neg_sp_avg_swings_time]

        s_time_analysis_rank_4 = [all_swing_avg_time, pstv_swing_avg_time, neg_swing_avg_time, top_10_lrg_pstv_total_rand_per_change, top_10_lrg_pstv_avg_time, top_10_sml_pstv_total_rand_per_change,
                                  top_10_sml_pstv_avg_time, top_10_lrg_neg_avg_time, top_10_sml_neg_avg_time, zero_rand_avg_swings_time, zero_rand_pstv_sp_avg_swings_time, zero_rand_neg_sp_avg_swings_time]

        s_time_analysis_rank_5 = [all_swing_avg_time, pstv_swing_avg_time, neg_swing_avg_time, top_10_lrg_pstv_total_rand_per_change, top_10_lrg_pstv_avg_time, top_10_sml_pstv_total_rand_per_change,
                                  top_10_sml_pstv_avg_time, top_10_lrg_neg_avg_time, top_10_sml_neg_avg_time, zero_rand_avg_swings_time, zero_rand_pstv_sp_avg_swings_time, zero_rand_neg_sp_avg_swings_time]

        s_time_analysis_rank_6 = [all_swing_median_time, pstv_swing_median_time, neg_swing_median_time, top_10_lrg_pstv_total_rand_per_change, top_10_lrg_pstv_median_time, top_10_sml_pstv_total_rand_per_change,
                                  top_10_sml_pstv_median_time, top_10_lrg_neg_median_time, top_10_sml_neg_median_time, zero_rand_med_swings_time, zero_rand_pstv_sp_med_swings_time, zero_rand_neg_sp_med_swings_time]

        return [s_time_analysis_rank_1, s_time_analysis_rank_2, s_time_analysis_rank_3, s_time_analysis_rank_4, s_time_analysis_rank_5, s_time_analysis_rank_6]

    else:
        print("No records found in s_time_analysis_data")
        return [0, 0, 0, 0, 0, 0, 0]


def get_s_rsi_dif_10_info(s_rsi_dif_data):
    if len(s_rsi_dif_data) > 0:
        all_swing_max_rsi_diff = round(abs(s_rsi_dif_data[3])/10, 2)
        all_swing_avg_rsi_diff = round(abs(s_rsi_dif_data[5])/10, 2)
        all_swing_median_rsi_diff = round(abs(s_rsi_dif_data[6])/10, 2)
        pstv_swing_max_rsi_diff = round(abs(s_rsi_dif_data[8])/10, 2)
        pstv_swing_avg_rsi_diff = round(abs(s_rsi_dif_data[10])/10, 2)
        pstv_swing_median_rsi_diff = round(abs(s_rsi_dif_data[11])/10, 2)
        neg_swing_max_rsi_diff = round(abs(s_rsi_dif_data[13])/10, 2)
        neg_swing_avg_rsi_diff = round(abs(s_rsi_dif_data[15])/10, 2)
        neg_swing_median_rsi_diff = round(abs(s_rsi_dif_data[16])/10, 2)
        top_10_lrg_pstv_max_rsi_diff = round(abs(s_rsi_dif_data[20])/10, 2)
        top_10_lrg_pstv_avg_rsi_diff = round(abs(s_rsi_dif_data[22])/10, 2)
        top_10_lrg_pstv_median_rsi_diff = round(abs(s_rsi_dif_data[23])/10, 2)
        top_10_sml_pstv_max_rsi_diff = round(abs(s_rsi_dif_data[28])/10, 2)
        top_10_sml_pstv_avg_rsi_diff = round(abs(s_rsi_dif_data[30])/10, 2)
        top_10_sml_pstv_median_rsi_diff = round(abs(s_rsi_dif_data[31])/10, 2)
        top_10_lrg_neg_max_rsi_diff = round(abs(s_rsi_dif_data[35])/10, 2)
        top_10_lrg_neg_avg_rsi_diff = round(abs(s_rsi_dif_data[37])/10, 2)
        top_10_lrg_neg_median_rsi_diff = round(abs(s_rsi_dif_data[38])/10, 2)
        top_10_sml_neg_max_rsi_diff = round(abs(s_rsi_dif_data[43])/10, 2)
        top_10_sml_neg_avg_rsi_diff = round(abs(s_rsi_dif_data[45])/10, 2)
        top_10_sml_neg_median_rsi_diff = round(abs(s_rsi_dif_data[46])/10, 2)
        zero_rand_max_swings_rsi_diff = round(abs(s_rsi_dif_data[48])/10, 2)
        zero_rand_avg_swings_rsi_diff = round(abs(s_rsi_dif_data[50])/10, 2)
        zero_rand_med_swings_rsi_diff = round(abs(s_rsi_dif_data[51])/10, 2)
        zero_rand_pstv_sp_max_swings_rsi_diff = round(
            abs(s_rsi_dif_data[54])/10, 2)
        zero_rand_pstv_sp_avg_swings_rsi_diff = round(
            abs(s_rsi_dif_data[56])/10, 2)
        zero_rand_pstv_sp_med_swings_rsi_diff = round(
            abs(s_rsi_dif_data[57])/10, 2)
        zero_rand_neg_sp_max_swings_rsi_diff = round(
            abs(s_rsi_dif_data[60])/10, 2)
        zero_rand_neg_sp_avg_swings_rsi_diff = round(
            abs(s_rsi_dif_data[62])/10, 2)
        zero_rand_neg_sp_med_swings_rsi_diff = round(
            abs(s_rsi_dif_data[63])/10, 2)

        s_rsi_dif_rank_1 = [all_swing_max_rsi_diff, all_swing_avg_rsi_diff, all_swing_median_rsi_diff, pstv_swing_max_rsi_diff, pstv_swing_avg_rsi_diff, pstv_swing_median_rsi_diff, neg_swing_max_rsi_diff, neg_swing_avg_rsi_diff, neg_swing_median_rsi_diff, top_10_lrg_pstv_max_rsi_diff, top_10_lrg_pstv_avg_rsi_diff, top_10_lrg_pstv_median_rsi_diff, top_10_sml_pstv_max_rsi_diff, top_10_sml_pstv_avg_rsi_diff, top_10_sml_pstv_median_rsi_diff, top_10_lrg_neg_max_rsi_diff,
                            top_10_lrg_neg_avg_rsi_diff, top_10_lrg_neg_median_rsi_diff, top_10_sml_neg_max_rsi_diff, top_10_sml_neg_avg_rsi_diff, top_10_sml_neg_median_rsi_diff, zero_rand_max_swings_rsi_diff, zero_rand_avg_swings_rsi_diff, zero_rand_med_swings_rsi_diff, zero_rand_pstv_sp_max_swings_rsi_diff, zero_rand_pstv_sp_avg_swings_rsi_diff, zero_rand_pstv_sp_med_swings_rsi_diff, zero_rand_neg_sp_max_swings_rsi_diff, zero_rand_neg_sp_avg_swings_rsi_diff, zero_rand_neg_sp_med_swings_rsi_diff]

        s_rsi_dif_rank_2 = [all_swing_avg_rsi_diff, pstv_swing_avg_rsi_diff, neg_swing_avg_rsi_diff, top_10_lrg_pstv_avg_rsi_diff, top_10_sml_pstv_avg_rsi_diff,
                            top_10_lrg_neg_avg_rsi_diff, top_10_sml_neg_avg_rsi_diff, zero_rand_avg_swings_rsi_diff, zero_rand_pstv_sp_avg_swings_rsi_diff, zero_rand_neg_sp_avg_swings_rsi_diff]

        s_rsi_dif_rank_3 = [all_swing_avg_rsi_diff, pstv_swing_avg_rsi_diff, neg_swing_avg_rsi_diff, top_10_lrg_pstv_avg_rsi_diff, top_10_sml_pstv_avg_rsi_diff,
                            top_10_lrg_neg_avg_rsi_diff, top_10_sml_neg_avg_rsi_diff, zero_rand_avg_swings_rsi_diff, zero_rand_pstv_sp_avg_swings_rsi_diff, zero_rand_neg_sp_avg_swings_rsi_diff]

        s_rsi_dif_rank_4 = [all_swing_avg_rsi_diff, pstv_swing_avg_rsi_diff, neg_swing_avg_rsi_diff, top_10_lrg_pstv_avg_rsi_diff, top_10_sml_pstv_avg_rsi_diff,
                            top_10_lrg_neg_avg_rsi_diff, top_10_sml_neg_avg_rsi_diff, zero_rand_avg_swings_rsi_diff, zero_rand_pstv_sp_avg_swings_rsi_diff, zero_rand_neg_sp_avg_swings_rsi_diff]

        s_rsi_dif_rank_5 = [all_swing_avg_rsi_diff, pstv_swing_avg_rsi_diff, neg_swing_avg_rsi_diff, top_10_lrg_pstv_avg_rsi_diff, top_10_sml_pstv_avg_rsi_diff,
                            top_10_lrg_neg_avg_rsi_diff, top_10_sml_neg_avg_rsi_diff, zero_rand_avg_swings_rsi_diff, zero_rand_pstv_sp_avg_swings_rsi_diff, zero_rand_neg_sp_avg_swings_rsi_diff]

        s_rsi_dif_rank_6 = [all_swing_median_rsi_diff, pstv_swing_median_rsi_diff, neg_swing_median_rsi_diff, top_10_sml_pstv_median_rsi_diff, top_10_lrg_neg_median_rsi_diff,
                            top_10_sml_neg_median_rsi_diff, zero_rand_med_swings_rsi_diff, zero_rand_pstv_sp_med_swings_rsi_diff, zero_rand_neg_sp_med_swings_rsi_diff]

        return [s_rsi_dif_rank_1, s_rsi_dif_rank_2, s_rsi_dif_rank_3, s_rsi_dif_rank_4, s_rsi_dif_rank_5, s_rsi_dif_rank_6]

    else:
        print("No records found in s_rsi_dif_data")

        return [0, 0, 0, 0, 0, 0, 0]


def get_s_fb_analysis_11_info(s_fb_analysis_data):
    if len(s_fb_analysis_data) > 0:
        total_fb = round(s_fb_analysis_data[2]/5, 2)
        total_pstv_fb = round(s_fb_analysis_data[3]/5, 2)
        total_neg_fb = round(s_fb_analysis_data[4]/5, 2)
        last_fb_time = s_fb_analysis_data[5]

        str_info_11 = [last_fb_time]
        s_fb_analysis_rank_1 = s_fb_analysis_rank_2 = s_fb_analysis_rank_3 = s_fb_analysis_rank_4 = s_fb_analysis_rank_5 = s_fb_analysis_rank_6 = [
            total_fb, total_pstv_fb, total_neg_fb]

        return [str_info_11, s_fb_analysis_rank_1, s_fb_analysis_rank_2, s_fb_analysis_rank_3, s_fb_analysis_rank_4, s_fb_analysis_rank_5, s_fb_analysis_rank_6]
    else:
        print("No records found in s_fb_analysis_data")
        return [0, 0, 0, 0, 0, 0, 0]


def get_btc_last_3_swings_info(btc_last_three_swing_excel_lst):
    btc_last_three_swing_excel_lst = btc_last_three_swing_excel_lst[0]
    if (len(btc_last_three_swing_excel_lst[2]) == 3):
        btc_swing_1_info = [btc_last_three_swing_excel_lst[2]
                            [0][2], btc_last_three_swing_excel_lst[2][0][3]]
        btc_swing_2_info = [btc_last_three_swing_excel_lst[2]
                            [1][2], btc_last_three_swing_excel_lst[2][1][3]]
        btc_swing_3_info = [btc_last_three_swing_excel_lst[2]
                            [2][2], btc_last_three_swing_excel_lst[2][2][3]]
        btc_swing_1_dir = btc_last_three_swing_excel_lst[2][0][4]
        btc_swing_2_dir = btc_last_three_swing_excel_lst[2][1][4]
        btc_swing_3_dir = btc_last_three_swing_excel_lst[2][2][4]
        btc_last_3_s_per_sum = round((abs(btc_last_three_swing_excel_lst[2][0][5]) + abs(
            btc_last_three_swing_excel_lst[2][1][5]) + abs(btc_last_three_swing_excel_lst[2][2][5])), 2)
        btc_last_3_s_per_avg = round((btc_last_3_s_per_sum/3), 2)
        btc_last_3_s_rand_sum = round((abs(btc_last_three_swing_excel_lst[2][0][6]) + abs(
            btc_last_three_swing_excel_lst[2][1][6]) + abs(btc_last_three_swing_excel_lst[2][2][6])), 2)
        btc_last_3_s_rand_avg = round((btc_last_3_s_rand_sum/3), 2)
        btc_last_3_s_total_time = round((abs(btc_last_three_swing_excel_lst[2][0][7]) + abs(
            btc_last_three_swing_excel_lst[2][1][7]) + abs(btc_last_three_swing_excel_lst[2][2][7])), 2)
        btc_last_3_s_avg_time = round((btc_last_3_s_total_time/3), 2)
        btc_last_3_s_rsi_diff_sum = round((abs(btc_last_three_swing_excel_lst[2][0][11]) + abs(
            btc_last_three_swing_excel_lst[2][1][11]) + abs(btc_last_three_swing_excel_lst[2][2][11])), 2)
        btc_last_3_s_rsi_diff_avg = round((btc_last_3_s_rsi_diff_sum/3), 2)
        btc_last_swing_per = round(
            abs(btc_last_three_swing_excel_lst[2][2][5]), 2)
        btc_last_swing_rand_per = round(
            abs(btc_last_three_swing_excel_lst[2][2][6]), 2)
        btc_last_swing_time = round(
            abs(btc_last_three_swing_excel_lst[2][2][7]), 2)
        btc_last_swing_rsi_dif = round(
            abs(btc_last_three_swing_excel_lst[2][2][11]), 2)

        return [{"btc_last_swing_per": btc_last_swing_per, "btc_last_swing_rand_per": btc_last_swing_rand_per, "btc_last_swing_time": btc_last_swing_time, "btc_last_swing_rsi_dif": btc_last_swing_rsi_dif, "btc_swing_1_info": btc_swing_1_info, "btc_swing_1_dir": btc_swing_1_dir, "btc_swing_2_info": btc_swing_2_info, "btc_swing_2_dir": btc_swing_2_dir, "btc_swing_3_info": btc_swing_3_info, "btc_swing_3_dir": btc_swing_3_dir, "btc_last_3_s_per_sum": btc_last_3_s_per_sum, "btc_last_3_s_per_avg": btc_last_3_s_per_avg, "btc_last_3_s_rand_sum": btc_last_3_s_rand_sum, "btc_last_3_s_rand_avg": btc_last_3_s_rand_avg, "btc_last_3_s_avg_time": btc_last_3_s_avg_time, "btc_last_3_s_rsi_diff_avg": btc_last_3_s_rsi_diff_avg}]

    else:
        print("Not getting the last 3 swings")
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def get_coin_dir_with_btc_dir(btc_swing_3_dir, swing_3_dir):
    if swing_3_dir == btc_swing_3_dir:
        return 1
    else:
        return 0


def get_coin_rank_lst(layer_3_rank_1_col_weights, layer_3_rank_col_names, layer_3_rank_excel_lst):
    df = pd.DataFrame(layer_3_rank_excel_lst, columns=layer_3_rank_col_names)
    ranking_columns = [col for col in layer_3_rank_1_col_weights.keys()]
    for col in ranking_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=ranking_columns)
    df['composite_score'] = df.apply(lambda row: round(sum(
        row[col] * layer_3_rank_1_col_weights[col] for col in ranking_columns), 2), axis=1)
    df['rank'] = df['composite_score'].rank(method='min', ascending=False)
    df = df.sort_values(by='rank')
    coin_rank_lst = df[['rank', 'coin_name', 'coin_time_tf',
                        'composite_score', ]].values.tolist()
    return coin_rank_lst


def get_final_coin_rank_lst(layer_3_rank_2_lst, layer_3_rank_3_lst, layer_3_rank_4_lst, layer_3_rank_5_lst, layer_3_rank_6_lst):
    sum_dict = defaultdict(float)

    # for sublist in layer_3_rank_1_lst:
    #     sum_dict[sublist[1]] += sublist[3]

    for sublist in layer_3_rank_2_lst:
        sum_dict[sublist[1]] += sublist[3]

    for sublist in layer_3_rank_3_lst:
        sum_dict[sublist[1]] += sublist[3]

    for sublist in layer_3_rank_4_lst:
        sum_dict[sublist[1]] += sublist[3]

    for sublist in layer_3_rank_5_lst:
        sum_dict[sublist[1]] += sublist[3]

    for sublist in layer_3_rank_6_lst:
        sum_dict[sublist[1]] += sublist[3]

    layer_3_rank_7_lst = sorted(
        [(rank, coin, 15, total)
         for rank, (coin, total) in enumerate(sum_dict.items(), start=1)],
        key=lambda x: x[3],
        reverse=True
    )
    rounded_layer_3_rank_7_lst = [
        [item[0], item[1], item[2], round(item[3], 2)] for item in layer_3_rank_7_lst]

    rounded_layer_3_rank_7_lst = [coin[1:]
                                  for coin in rounded_layer_3_rank_7_lst]
    for index, coin in enumerate(rounded_layer_3_rank_7_lst):
        coin.insert(0, index+1)

    return rounded_layer_3_rank_7_lst


def get_coin_rank_step_stop_info(coin):
    coin_name = coin[0]
    coin_time_tf = coin[1]
    last_swing_rand_per = coin[3]
    last_3_s_rand_avg = coin[9]
    all_swings_rand_pp_med = coin[49]
    all_swings_rand_np_med = coin[50]
    t_10_lrg_pp_rand_sp_med = coin[55]
    t_10_lrg_np_rand_sp_med = coin[56]
    t_10_sml_pp_rand_sp_med = coin[61]
    t_10_sml_np_rand_sp_med = coin[62]

    last_s_rank_rand_per = round((last_swing_rand_per+last_3_s_rand_avg)/2, 2)
    total_s_rank_rand_per = round((all_swings_rand_pp_med+all_swings_rand_np_med+t_10_lrg_pp_rand_sp_med +
                                  t_10_lrg_np_rand_sp_med+t_10_sml_pp_rand_sp_med+t_10_sml_np_rand_sp_med)/6, 2)

    if last_s_rank_rand_per <= 0.5:
        if total_s_rank_rand_per <= 0.5:
            coin_stop_loss = 0.85
        elif 0.5 < total_s_rank_rand_per <= 0.75:
            coin_stop_loss = 0.85
        elif 0.75 < total_s_rank_rand_per <= 1:
            coin_stop_loss = 0.9
        elif 1 < total_s_rank_rand_per <= 1.5:
            coin_stop_loss = 1
        else:
            coin_stop_loss = 1
    elif 0.5 < last_s_rank_rand_per <= 1:
        if 0.5 < total_s_rank_rand_per <= 1:
            coin_stop_loss = 1.25
        elif total_s_rank_rand_per <= 0.5:
            coin_stop_loss = 1.25
        elif 1 < total_s_rank_rand_per <= 1.5:
            coin_stop_loss = 1.5
        elif 1.5 < total_s_rank_rand_per <= 2:
            coin_stop_loss = 1.5
        elif 2 < total_s_rank_rand_per <= 2.5:
            coin_stop_loss = 1.5
        else:
            coin_stop_loss = 1.5
    elif 1 < last_s_rank_rand_per <= 1.5:
        if 1 < total_s_rank_rand_per <= 1.5:
            coin_stop_loss = 1.65
        elif total_s_rank_rand_per <= 1:
            coin_stop_loss = 1.65
        elif 1.5 < total_s_rank_rand_per <= 2:
            coin_stop_loss = 1.75
        elif 2 < total_s_rank_rand_per <= 2.5:
            coin_stop_loss = 1.75
        elif 2.5 < total_s_rank_rand_per <= 3:
            coin_stop_loss = 1.85
        else:
            coin_stop_loss = 1.85
    elif 1.5 < last_s_rank_rand_per <= 2:
        if 1.5 < total_s_rank_rand_per <= 2:
            coin_stop_loss = 1.85
        elif total_s_rank_rand_per <= 1.5:
            coin_stop_loss = 1.85
        elif 2 < total_s_rank_rand_per <= 2.5:
            coin_stop_loss = 2
        elif 2.5 < total_s_rank_rand_per <= 3:
            coin_stop_loss = 2
        elif 3 < total_s_rank_rand_per <= 3.5:
            coin_stop_loss = 2
        else:
            coin_stop_loss = 2
    elif 2 < last_s_rank_rand_per <= 2.5:
        if 2 < total_s_rank_rand_per <= 2.5:
            coin_stop_loss = 2.25
        elif total_s_rank_rand_per <= 2:
            coin_stop_loss = 2.15
        elif 2.5 < total_s_rank_rand_per <= 3:
            coin_stop_loss = 2.25
        elif 3 < total_s_rank_rand_per <= 3.5:
            coin_stop_loss = 2.25
        elif 3.5 < total_s_rank_rand_per <= 4:
            coin_stop_loss = 2.25
        else:
            coin_stop_loss = 2.5
    else:
        coin_stop_loss = 2.5
    # We can modify the values
    coin_step = 0.25
    coin_step_stop_loss = [coin_name, coin_time_tf, coin_stop_loss, coin_step]
    return coin_step_stop_loss


def add_stop_loss_to_rank_list(rank_list, stop_loss_dict):
    for sublist in rank_list:
        coin_name = sublist[1]
        if coin_name in stop_loss_dict:
            sublist.extend(stop_loss_dict[coin_name])
    return rank_list


def add_rank_to_coin_data(layer_3_rank_excel_lst, layer_3_rank_lst):
    rank_map = {item[1]: item[0] for item in layer_3_rank_lst}

    for sublist in layer_3_rank_excel_lst:
        coin_name = sublist[0]
        if coin_name in rank_map:
            sublist.insert(0, rank_map[coin_name])
    layer_3_rank_excel_lst.sort(key=lambda x: x[0])

    return layer_3_rank_excel_lst


def btc_last_swing_info(btc_layer_1_data):
    btc_last_three_swing_excel_lst = []
    for record in btc_layer_1_data:
        coin_name = record[0][0]
        coin_time_tf = record[0][1]
        btc_last_three_swings = [coin_name, coin_time_tf, record[-3:]]
        btc_last_three_swing_excel_lst.append(btc_last_three_swings)
    return btc_last_three_swing_excel_lst


def get_last_3_swings_info_rankings(last_3_swings_info):
    if (len(last_3_swings_info[2]) == 3):
        coin_name = last_3_swings_info[0]
        coin_tf = last_3_swings_info[1]
        swing_3_info = [last_3_swings_info[2]
                        [2][2], last_3_swings_info[2][2][3]]

        swing_1_dir = last_3_swings_info[2][0][4]
        swing_2_dir = last_3_swings_info[2][1][4]
        swing_3_dir = last_3_swings_info[2][2][4]

        swing_1_per = round(abs(last_3_swings_info[2][0][5]), 2)
        swing_2_per = round(abs(last_3_swings_info[2][1][5]), 2)
        swing_3_per = round(abs(last_3_swings_info[2][2][5]), 2)

        swing_1_rand_per = round(abs(last_3_swings_info[2][0][6]), 2)
        swing_2_rand_per = round(abs(last_3_swings_info[2][1][6]), 2)
        swing_3_rand_per = round(abs(last_3_swings_info[2][2][6]), 2)

        swing_1_time = last_3_swings_info[2][0][7]
        swing_2_time = last_3_swings_info[2][1][7]
        swing_3_time = last_3_swings_info[2][2][7]

        last_3_s_per_sum = round((abs(last_3_swings_info[2][0][5]) + abs(
            last_3_swings_info[2][1][5]) + abs(last_3_swings_info[2][2][5])), 2)
        last_3_s_per_avg = round((last_3_s_per_sum/3), 2)

        last_3_s_rand_sum = round((abs(last_3_swings_info[2][0][6]) + abs(
            last_3_swings_info[2][1][6]) + abs(last_3_swings_info[2][2][6])), 2)
        last_3_s_rand_avg = round((last_3_s_rand_sum/3), 2)

        last_3_swing_score = round(abs(last_3_s_per_sum + last_3_s_per_avg), 2)

        last_swing_info = [coin_name, coin_tf, swing_3_info,
                           swing_3_dir, swing_3_per, swing_3_rand_per, swing_3_time]

        last_3_swings_info = [coin_name, coin_tf, last_3_swing_score, last_3_s_per_sum, last_3_s_per_avg, [swing_3_dir, swing_3_per, swing_3_rand_per, swing_3_time], [
            swing_2_dir, swing_2_per, swing_2_rand_per, swing_2_time], [swing_1_dir, swing_1_per, swing_1_rand_per, swing_1_time], last_3_s_rand_sum, last_3_s_rand_avg]

        return [last_swing_info, last_3_swings_info]

    else:
        print("Not getting the last 3 swings")
        return [0, 0]


def best_swing_per_rankings(layer_1_data):
    # Get the last 3 swings info from the coin
    last_three_swing_excel_lst = []
    for coin in layer_1_data:
        coin_name = coin[0][0]
        coin_time_tf = coin[0][1]
        last_three_swings = [coin_name, coin_time_tf, coin[-3:]]
        last_three_swing_excel_lst.append(last_three_swings)

    last_swing_info_excel_ranks = []
    last_3_swing_excel_ranks = []
    for coin in last_three_swing_excel_lst:
        last_swing_info, last_3_swings_info = get_last_3_swings_info_rankings(
            coin)
        last_swing_info_excel_ranks.append(last_swing_info)
        last_3_swing_excel_ranks.append(last_3_swings_info)

    sort_last_s_excel_lst = sorted(
        last_swing_info_excel_ranks, key=lambda x: x[4], reverse=True)
    for index, coin in enumerate(sort_last_s_excel_lst):
        coin.insert(0, index+1)
    print("sort_last_s_excel_lst ==>", sort_last_s_excel_lst)

    sort_last_3_s_excel_lst = sorted(
        last_3_swing_excel_ranks, key=lambda x: x[2], reverse=True)
    for index, coin in enumerate(sort_last_3_s_excel_lst):
        coin.insert(0, index+1)
    print("sort_last_3_s_excel_lst ==>", sort_last_3_s_excel_lst)

    return [sort_last_s_excel_lst, sort_last_3_s_excel_lst]
