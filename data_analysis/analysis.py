import itertools
import time

from utils.csv_ops import check_path_total_csv, read_validate_csv_file
from data_analysis.extraction import get_time_data, get_coin_data, get_swing_col, get_swing_direction, get_swing_percentage, get_randomness_percentage, get_high_FB, get_low_FB, get_last_FB, get_fb_lst_with_time, get_swing_time, get_swing_rsi_diff, get_swing_per_info, get_swing_pstv_per_range_info, get_swing_neg_per_range_info, get_swing_rand_per_info, get_swing_zero_rand_per_cluster_lst, get_swing_pstv_rand_per_cluster_lst, get_swing_neg_rand_per_cluster_lst, get_swing_time_and_rsi_diff_lst, get_swing_fb_info_lst, get_last_3_swings_info, get_s_per_analysis_2_info, get_s_pstv_per_rang_3_info, get_s_neg_per_rang_4_info, get_s_rand_per_analysis_5_info, get_s_zero_rand_cluster_6_info, get_s_pstv_rand_cluster_7_info, get_s_neg_rand_cluster_8_info, get_s_time_analysis_9_info, get_s_rsi_dif_10_info, get_s_fb_analysis_11_info, get_btc_last_3_swings_info, get_coin_dir_with_btc_dir, get_coin_rank_lst, get_final_coin_rank_lst, get_coin_rank_step_stop_info, add_stop_loss_to_rank_list, add_rank_to_coin_data


def layer_1_analysis(auto_download_excel_path):
    start_time = time.time()
    csv_files = check_path_total_csv(auto_download_excel_path)
    layer_1_data_lst = []
    fb_coin_wise_lst = []
    fb_excel_lst = []
    for csv_file in csv_files[0]:
        read_csv_status, df = read_validate_csv_file(
            auto_download_excel_path, csv_file)
        if read_csv_status == 1:
            coin_data = get_coin_data(csv_file)
            coin_name, coin_time_frame = coin_data[0], coin_data[1]
            swing_with_row_num_lst = []
            for row_num, row in df.iterrows():
                swing_with_row_num = get_swing_col(row_num, row)
                swing_with_row_num_lst.append(swing_with_row_num)

            swing_change_rows_lst = []
            for swing in swing_with_row_num_lst:
                if swing[1] == "Higher Low" or swing[1] == "Lower High" or swing[1] == "Higher High" or swing[1] == "Lower Low":
                    swing_change_rows_lst.append(swing)

            High_Col_lst = ["Higher High", "Lower High"]
            Low_Col_lst = ["Lower Low", "Higher Low"]
            current_lst = swing_change_rows_lst

            # Initialize the false breakout and swing lists
            false_breakout_lst = []
            for i in range(len(current_lst) - 1):
                current_value = current_lst[i][1]
                next_value = current_lst[i + 1][1]
                # Check if both current and next values are within the same type
                if (current_value in Low_Col_lst and next_value in Low_Col_lst) or (current_value in High_Col_lst and next_value in High_Col_lst):
                    false_breakout_lst.append(current_lst[i])

            fb_lst_with_coin = []
            for item in false_breakout_lst:
                new_item = [coin_name, coin_time_frame] + item
                fb_lst_with_coin.append(new_item)

            total_FB = len(false_breakout_lst)
            fb_lst_with_time = get_fb_lst_with_time(
                fb_lst_with_coin, df, csv_file)

            High_FB = get_high_FB(false_breakout_lst)
            Low_FB = get_low_FB(false_breakout_lst)
            last_FB = get_last_FB(false_breakout_lst, df, csv_file)

            # Total False Breakout Information
            fb_overall_info_lst = [coin_name, coin_time_frame,
                                   fb_lst_with_time, total_FB, High_FB, Low_FB, last_FB]
            swing_lst = [
                item for item in swing_change_rows_lst if item not in false_breakout_lst]

            swing_info_lst = []
            for i in range(len(swing_lst) - 1):
                # Swing_1 info
                row_1 = df.iloc[swing_lst[i][0]]
                swing_1_col = swing_lst[i][1]
                swing_1_ISO_time = get_time_data(row_1["time"], csv_file)
                swing_1_RSI = round(row_1["Plot"], 2)

                # Swing_2 info
                row_2 = df.iloc[swing_lst[i+1][0]]
                swing_2_col = swing_lst[i+1][1]
                swing_2_ISO_time = get_time_data(row_2["time"], csv_file)
                swing_2_RSI = round(row_2["Plot"], 2)

                # Swing Direction
                swing_dir = get_swing_direction(swing_1_col, swing_2_col)
                swing_rsi_diff = get_swing_rsi_diff(
                    swing_dir, swing_1_RSI, swing_2_RSI)
                # Swing Percentage Change
                swing_per = get_swing_percentage(swing_dir, row_1, row_2)

                # Calculate randomness Percentage in the swing
                swing_1_row_num = swing_lst[i][0]
                swing_2_row_num = swing_lst[i+1][0]
                swing_rand_per = get_randomness_percentage(
                    swing_dir, swing_1_row_num, swing_2_row_num, df)

                # Total Time Taken for swing
                swing_time = get_swing_time(
                    swing_1_row_num, swing_2_row_num, df)
                # Total Number of Candle in the swing
                swing_candles = swing_2_row_num - swing_1_row_num

                swing_info = [coin_name, coin_time_frame, swing_1_col, swing_2_col, swing_dir, swing_per, swing_rand_per,
                              swing_time, swing_candles, swing_1_RSI, swing_2_RSI, swing_rsi_diff, swing_1_ISO_time, swing_2_ISO_time]
                swing_info_lst.append(swing_info)
            layer_1_data_lst.append(swing_info_lst)
            fb_coin_wise_lst.append(fb_overall_info_lst)
            fb_excel_lst.append(fb_lst_with_time)
    end_time = time.time()
    total_time_for_analysis = round(((end_time - start_time)/60), 2)
    print(f"Total Time Taken for analysis is : {total_time_for_analysis} Min")
    print("========= Layer_1 Analysis Successful ==========")
    return layer_1_data_lst, fb_coin_wise_lst, fb_excel_lst


def layer_2_analysis(layer_1_data, fb_coin_lst):
    # swing percentage excel analysis
    swing_per_analysis_excel_lst = []
    swing_pstv_per_range_excel_lst = []
    swing_neg_per_range_excel_lst = []

    # swing rand per excel analysis
    swing_rand_per_analysis_excel_lst = []
    swing_zero_rand_per_cluster_excel_lst = []
    swing_pstv_rand_per_cluster_excel_lst = []
    swing_neg_rand_per_cluster_excel_lst = []

    # swing time and rsi analysis
    swing_time_analysis_excel_lst = []
    swing_rsi_diff_analysis_excel_lst = []

    # swing false breakout info
    swing_fb_analysis_excel_lst = []

    for coin in layer_1_data:
        # Coin Info
        coin_name = coin[0][0]
        coin_time_tf = coin[0][1]
        print("coin_name ==>", coin_name)
        print("coin_time_tf ==>", coin_time_tf)

        # Swing Percentage analysis
        swing_per_lst = [swing[5] for swing in coin]
        pstv_swing_per_lst = [
            swing_per for swing_per in swing_per_lst if swing_per >= 0]
        neg_swing_per_lst = [
            swing_per for swing_per in swing_per_lst if swing_per < 0]

        # Swing Percentage Info
        swing_per_analysis_lst = get_swing_per_info(
            coin_name, coin_time_tf, swing_per_lst, pstv_swing_per_lst, neg_swing_per_lst)

        # Swing Percentage ranges info
        swing_pstv_per_range_lst = get_swing_pstv_per_range_info(
            coin_name, coin_time_tf, pstv_swing_per_lst)
        swing_neg_per_range_lst = get_swing_neg_per_range_info(
            coin_name, coin_time_tf, neg_swing_per_lst)

        # Append swing percentage info to the excel lists
        swing_per_analysis_excel_lst.append(swing_per_analysis_lst)
        swing_pstv_per_range_excel_lst.append(swing_pstv_per_range_lst)
        swing_neg_per_range_excel_lst.append(swing_neg_per_range_lst)

        # Swing randomness analysis
        swing_rand_per_lst = [swing[6] for swing in coin]
        swing_zero_rand_and_swing_per_lst = [
            [swing[6], swing[5]] for swing in coin if swing[6] == 0]
        zero_rand_swing_per_lst = [
            swing_rand_per for swing_rand_per in swing_rand_per_lst if swing_rand_per == 0]
        pstv_rand_swing_per_lst = [
            swing_rand_per for swing_rand_per in swing_rand_per_lst if swing_rand_per > 0]
        neg_rand_swing_per_lst = [
            swing_rand_per for swing_rand_per in swing_rand_per_lst if swing_rand_per < 0]

        # swing randomness info
        swing_rand_per_analysis_lst = get_swing_rand_per_info(
            coin_name, coin_time_tf, swing_rand_per_lst, pstv_rand_swing_per_lst, neg_rand_swing_per_lst)

        # swing randomness clusters info
        swing_zero_rand_per_cluster_lst = get_swing_zero_rand_per_cluster_lst(
            coin_name, coin_time_tf, zero_rand_swing_per_lst, swing_zero_rand_and_swing_per_lst)
        swing_pstv_rand_per_cluster_lst = get_swing_pstv_rand_per_cluster_lst(
            coin_name, coin_time_tf, pstv_rand_swing_per_lst)
        swing_neg_rand_per_cluster_lst = get_swing_neg_rand_per_cluster_lst(
            coin_name, coin_time_tf, neg_rand_swing_per_lst)

        # Append swing rand info to the excel lists
        swing_rand_per_analysis_excel_lst.append(swing_rand_per_analysis_lst)
        swing_zero_rand_per_cluster_excel_lst.append(
            swing_zero_rand_per_cluster_lst)
        swing_pstv_rand_per_cluster_excel_lst.append(
            swing_pstv_rand_per_cluster_lst)
        swing_neg_rand_per_cluster_excel_lst.append(
            swing_neg_rand_per_cluster_lst)

        # Swing Time and RSI difference analysis
        all_swing_per_rand_time_rsi_diff_lst = [
            [swing[5], swing[6], swing[7], swing[11]] for swing in coin]

        pstv_swing_per_rand_time_rsi_diff_lst = [
            swing for swing in all_swing_per_rand_time_rsi_diff_lst if swing[0] > 0]
        neg_swing_per_rand_time_rsi_diff_lst = [
            swing for swing in all_swing_per_rand_time_rsi_diff_lst if swing[0] < 0]
        swing_per_zero_rand_time_rsi_diff_lst = [
            swing for swing in all_swing_per_rand_time_rsi_diff_lst if swing[1] == 0]
        pstv_swing_per_zero_rand_time_rsi_diff_lst = [
            swing for swing in swing_per_zero_rand_time_rsi_diff_lst if swing[0] > 0]
        neg_swing_per_zero_rand_time_rsi_diff_lst = [
            swing for swing in swing_per_zero_rand_time_rsi_diff_lst if swing[0] < 0]

        swing_time_analysis_lst, swing_rsi_diff_analysis_lst = get_swing_time_and_rsi_diff_lst(coin_name, coin_time_tf, all_swing_per_rand_time_rsi_diff_lst, pstv_swing_per_rand_time_rsi_diff_lst,
                                                                                               neg_swing_per_rand_time_rsi_diff_lst, swing_per_zero_rand_time_rsi_diff_lst, pstv_swing_per_zero_rand_time_rsi_diff_lst, neg_swing_per_zero_rand_time_rsi_diff_lst)

        # Swing Time and RSI difference analysis append excels
        swing_time_analysis_excel_lst.append(swing_time_analysis_lst)
        swing_rsi_diff_analysis_excel_lst.append(swing_rsi_diff_analysis_lst)

    for fb_coin in fb_coin_lst:
        # swing false breakout info
        coin_name = fb_coin[0]
        coin_time_tf = fb_coin[1]
        swing_fb_analysis_lst = get_swing_fb_info_lst(
            coin_name, coin_time_tf, fb_coin)
        swing_fb_analysis_excel_lst.append(swing_fb_analysis_lst)

    print("========= Layer_2 Analysis Successful ==========")
    return [swing_per_analysis_excel_lst, swing_pstv_per_range_excel_lst, swing_neg_per_range_excel_lst, swing_rand_per_analysis_excel_lst, swing_zero_rand_per_cluster_excel_lst, swing_pstv_rand_per_cluster_excel_lst, swing_neg_rand_per_cluster_excel_lst, swing_time_analysis_excel_lst, swing_rsi_diff_analysis_excel_lst, swing_fb_analysis_excel_lst]


def layer_3_analysis(layer_1_data, swing_per_analysis_excel_lst, swing_pstv_per_range_excel_lst, swing_neg_per_range_excel_lst, swing_rand_per_analysis_excel_lst, swing_zero_rand_per_cluster_excel_lst, swing_pstv_rand_per_cluster_excel_lst, swing_neg_rand_per_cluster_excel_lst, swing_time_analysis_excel_lst, swing_rsi_diff_analysis_excel_lst, swing_fb_analysis_excel_lst):

    # Get the last 3 swings info from the coin
    last_three_swing_excel_lst = []
    for coin in layer_1_data:
        coin_name = coin[0][0]
        coin_time_tf = coin[0][1]
        last_three_swings = [coin_name, coin_time_tf, coin[-3:]]
        last_three_swing_excel_lst.append(last_three_swings)

    layer_1_data_len = len(layer_1_data)
    # Check the record lengths
    if layer_1_data_len == len(last_three_swing_excel_lst) == len(swing_per_analysis_excel_lst) == len(swing_pstv_per_range_excel_lst) == len(swing_neg_per_range_excel_lst) == len(swing_rand_per_analysis_excel_lst) == len(swing_zero_rand_per_cluster_excel_lst) == len(swing_pstv_rand_per_cluster_excel_lst) == len(swing_neg_rand_per_cluster_excel_lst) == len(swing_time_analysis_excel_lst) == len(swing_rsi_diff_analysis_excel_lst) == len(swing_fb_analysis_excel_lst):
        # Loop over all the excels
        layer_3_str_info_excel_lst = []
        layer_3_rank_1_excel_lst = []
        layer_3_rank_2_excel_lst = []
        layer_3_rank_3_excel_lst = []
        layer_3_rank_4_excel_lst = []
        layer_3_rank_5_excel_lst = []
        layer_3_rank_6_excel_lst = []

        for last_3_swings_1, s_per_analysis_2, s_pstv_per_rang_3, s_neg_per_rang_4, s_rand_per_analysis_5, s_zero_rand_cluster_6, s_pstv_rand_cluster_7, s_neg_rand_cluster_8, s_time_analysis_9, s_rsi_dif_10, s_fb_analysis_11 in zip(last_three_swing_excel_lst, swing_per_analysis_excel_lst, swing_pstv_per_range_excel_lst, swing_neg_per_range_excel_lst, swing_rand_per_analysis_excel_lst, swing_zero_rand_per_cluster_excel_lst, swing_pstv_rand_per_cluster_excel_lst, swing_neg_rand_per_cluster_excel_lst, swing_time_analysis_excel_lst, swing_rsi_diff_analysis_excel_lst, swing_fb_analysis_excel_lst):
            # Check the coin name in all the records
            if last_3_swings_1[0] == s_per_analysis_2[0] == s_pstv_per_rang_3[0] == s_neg_per_rang_4[0] == s_rand_per_analysis_5[0] == s_zero_rand_cluster_6[0] == s_pstv_rand_cluster_7[0] == s_neg_rand_cluster_8[0] == s_time_analysis_9[0] == s_rsi_dif_10[0] == s_fb_analysis_11[0]:
                coin_name = last_3_swings_1[0]
                coin_time_tf = last_3_swings_1[1]

                # last_3_swings_1 data extraction
                str_info_1, get_last_3_swings_rank_1, get_last_3_swings_rank_2, get_last_3_swings_rank_3, get_last_3_swings_rank_4, get_last_3_swings_rank_5, get_last_3_swings_rank_6 = get_last_3_swings_info(
                    last_3_swings_1)

                # s_per_analysis_2 data extraction
                str_info_2, s_per_analysis_rank_1, s_per_analysis_rank_2, s_per_analysis_rank_3, s_per_analysis_rank_4, s_per_analysis_rank_5, s_per_analysis_rank_6 = get_s_per_analysis_2_info(
                    s_per_analysis_2)

                # s_pstv_per_rang_3 data extraction
                str_info_3, s_pstv_per_rang_rank_1, s_pstv_per_rang_rank_2, s_pstv_per_rang_rank_3, s_pstv_per_rang_rank_4, s_pstv_per_rang_rank_5, s_pstv_per_rang_rank_6 = get_s_pstv_per_rang_3_info(
                    s_pstv_per_rang_3)

                # s_neg_per_rang_4 data extraction
                str_info_4, s_neg_per_rang_rank_1, s_neg_per_rang_rank_2, s_neg_per_rang_rank_3, s_neg_per_rang_rank_4, s_neg_per_rang_rank_5, s_neg_per_rang_rank_6 = get_s_neg_per_rang_4_info(
                    s_neg_per_rang_4)

                # s_rand_per_analysis_5 data extraction
                str_info_5, s_rand_per_analysis_rank_1, s_rand_per_analysis_rank_2, s_rand_per_analysis_rank_3, s_rand_per_analysis_rank_4, s_rand_per_analysis_rank_5, s_rand_per_analysis_rank_6 = get_s_rand_per_analysis_5_info(
                    s_rand_per_analysis_5)

                # s_zero_rand_cluster_6
                str_info_6, s_zero_rand_cluster_rank_1, s_zero_rand_cluster_rank_2, s_zero_rand_cluster_rank_3, s_zero_rand_cluster_rank_4, s_zero_rand_cluster_rank_5, s_zero_rand_cluster_rank_6 = get_s_zero_rand_cluster_6_info(
                    s_zero_rand_cluster_6)

                # s_pstv_rand_cluster_7
                str_info_7, s_pstv_rand_cluster_rank_1, s_pstv_rand_cluster_rank_2, s_pstv_rand_cluster_rank_3, s_pstv_rand_cluster_rank_4, s_pstv_rand_cluster_rank_5, s_pstv_rand_cluster_rank_6 = get_s_pstv_rand_cluster_7_info(
                    s_pstv_rand_cluster_7)

                # s_neg_rand_cluster_8
                str_info_8, s_neg_rand_cluster_rank_1, s_neg_rand_cluster_rank_2, s_neg_rand_cluster_rank_3, s_neg_rand_cluster_rank_4, s_neg_rand_cluster_rank_5, s_neg_rand_cluster_rank_6 = get_s_neg_rand_cluster_8_info(
                    s_neg_rand_cluster_8)

                # s_time_analysis_9
                s_time_analysis_rank_1, s_time_analysis_rank_2, s_time_analysis_rank_3, s_time_analysis_rank_4, s_time_analysis_rank_5, s_time_analysis_rank_6 = get_s_time_analysis_9_info(
                    s_time_analysis_9)

                # s_rsi_dif_10
                s_rsi_dif_rank_1, s_rsi_dif_rank_2, s_rsi_dif_rank_3, s_rsi_dif_rank_4, s_rsi_dif_rank_5, s_rsi_dif_rank_6 = get_s_rsi_dif_10_info(
                    s_rsi_dif_10)

                # s_fb_analysis_11
                str_info_11, s_fb_analysis_rank_1, s_fb_analysis_rank_2, s_fb_analysis_rank_3, s_fb_analysis_rank_4, s_fb_analysis_rank_5, s_fb_analysis_rank_6 = get_s_fb_analysis_11_info(
                    s_fb_analysis_11)

                coin_info = [coin_name, coin_time_tf]

                layer_3_str_info_lst = [coin_info, str_info_1, str_info_2, str_info_3,
                                        str_info_4, str_info_5, str_info_6, str_info_7, str_info_8, str_info_11]
                layer_3_str_info_lst = list(
                    itertools.chain.from_iterable(layer_3_str_info_lst))

                layer_3_rank_1_lst = [coin_info, get_last_3_swings_rank_1, s_per_analysis_rank_1, s_pstv_per_rang_rank_1, s_neg_per_rang_rank_1, s_rand_per_analysis_rank_1,
                                      s_zero_rand_cluster_rank_1, s_pstv_rand_cluster_rank_1, s_neg_rand_cluster_rank_1, s_time_analysis_rank_1, s_rsi_dif_rank_1, s_fb_analysis_rank_1]
                layer_3_rank_1_lst = list(
                    itertools.chain.from_iterable(layer_3_rank_1_lst))

                layer_3_rank_2_lst = [coin_info, get_last_3_swings_rank_2, s_per_analysis_rank_2, s_pstv_per_rang_rank_2, s_neg_per_rang_rank_2, s_rand_per_analysis_rank_2,
                                      s_zero_rand_cluster_rank_2, s_pstv_rand_cluster_rank_2, s_neg_rand_cluster_rank_2, s_time_analysis_rank_2, s_rsi_dif_rank_2, s_fb_analysis_rank_2]
                layer_3_rank_2_lst = list(
                    itertools.chain.from_iterable(layer_3_rank_2_lst))

                layer_3_rank_3_lst = [coin_info, get_last_3_swings_rank_3, s_per_analysis_rank_3, s_pstv_per_rang_rank_3, s_neg_per_rang_rank_3, s_rand_per_analysis_rank_3,
                                      s_zero_rand_cluster_rank_3, s_pstv_rand_cluster_rank_3, s_neg_rand_cluster_rank_3, s_time_analysis_rank_3, s_rsi_dif_rank_3, s_fb_analysis_rank_3]
                layer_3_rank_3_lst = list(
                    itertools.chain.from_iterable(layer_3_rank_3_lst))

                layer_3_rank_4_lst = [coin_info, get_last_3_swings_rank_4, s_per_analysis_rank_4, s_pstv_per_rang_rank_4, s_neg_per_rang_rank_4, s_rand_per_analysis_rank_4,
                                      s_zero_rand_cluster_rank_4, s_pstv_rand_cluster_rank_4, s_neg_rand_cluster_rank_4, s_time_analysis_rank_4, s_rsi_dif_rank_4, s_fb_analysis_rank_4]
                layer_3_rank_4_lst = list(
                    itertools.chain.from_iterable(layer_3_rank_4_lst))

                layer_3_rank_5_lst = [coin_info, get_last_3_swings_rank_5, s_per_analysis_rank_5, s_pstv_per_rang_rank_5, s_neg_per_rang_rank_5, s_rand_per_analysis_rank_5,
                                      s_zero_rand_cluster_rank_5, s_pstv_rand_cluster_rank_5, s_neg_rand_cluster_rank_5, s_time_analysis_rank_5, s_rsi_dif_rank_5, s_fb_analysis_rank_5]
                layer_3_rank_5_lst = list(
                    itertools.chain.from_iterable(layer_3_rank_5_lst))

                layer_3_rank_6_lst = [coin_info, get_last_3_swings_rank_6, s_per_analysis_rank_6, s_pstv_per_rang_rank_6, s_neg_per_rang_rank_6, s_rand_per_analysis_rank_6,
                                      s_zero_rand_cluster_rank_6, s_pstv_rand_cluster_rank_6, s_neg_rand_cluster_rank_6, s_time_analysis_rank_6, s_rsi_dif_rank_6, s_fb_analysis_rank_6]
                layer_3_rank_6_lst = list(
                    itertools.chain.from_iterable(layer_3_rank_6_lst))

                layer_3_str_info_excel_lst.append(layer_3_str_info_lst)
                layer_3_rank_1_excel_lst.append(layer_3_rank_1_lst)
                layer_3_rank_2_excel_lst.append(layer_3_rank_2_lst)
                layer_3_rank_3_excel_lst.append(layer_3_rank_3_lst)
                layer_3_rank_4_excel_lst.append(layer_3_rank_4_lst)
                layer_3_rank_5_excel_lst.append(layer_3_rank_5_lst)
                layer_3_rank_6_excel_lst.append(layer_3_rank_6_lst)

            else:
                print(f"{last_3_swings_1[0]} coin name is mis matched !!!!")
        print("========= Layer_3 Analysis Successful ==========")
        return [layer_3_str_info_excel_lst, layer_3_rank_1_excel_lst, layer_3_rank_2_excel_lst, layer_3_rank_3_excel_lst, layer_3_rank_4_excel_lst, layer_3_rank_5_excel_lst, layer_3_rank_6_excel_lst]
    else:
        print(" Record lengths are not Matched !!! ")
        return [0, 0, 0, 0, 0, 0, 0]


def get_coin_rank_analysis(layer_3_rank_1_col_weights, layer_3_rank_2_col_weights, layer_3_rank_3_col_weights, layer_3_rank_4_col_weights, layer_3_rank_5_col_weights, layer_3_rank_6_col_weights, layer_3_rank_1_col_names, layer_3_rank_2_col_names, layer_3_rank_3_col_names, layer_3_rank_4_col_names, layer_3_rank_5_col_names, layer_3_rank_6_col_names, layer_3_rank_1_excel_lst, layer_3_rank_2_excel_lst, layer_3_rank_3_excel_lst, layer_3_rank_4_excel_lst, layer_3_rank_5_excel_lst, layer_3_rank_6_excel_lst):

    layer_3_rank_1_lst = get_coin_rank_lst(
        layer_3_rank_1_col_weights, layer_3_rank_1_col_names, layer_3_rank_1_excel_lst)
    layer_3_rank_2_lst = get_coin_rank_lst(
        layer_3_rank_2_col_weights, layer_3_rank_2_col_names, layer_3_rank_2_excel_lst)
    layer_3_rank_3_lst = get_coin_rank_lst(
        layer_3_rank_3_col_weights, layer_3_rank_3_col_names, layer_3_rank_3_excel_lst)
    layer_3_rank_4_lst = get_coin_rank_lst(
        layer_3_rank_4_col_weights, layer_3_rank_4_col_names, layer_3_rank_4_excel_lst)
    layer_3_rank_5_lst = get_coin_rank_lst(
        layer_3_rank_5_col_weights, layer_3_rank_5_col_names, layer_3_rank_5_excel_lst)
    layer_3_rank_6_lst = get_coin_rank_lst(
        layer_3_rank_6_col_weights, layer_3_rank_6_col_names, layer_3_rank_6_excel_lst)
    layer_3_rank_7_lst = get_final_coin_rank_lst(
        layer_3_rank_2_lst, layer_3_rank_3_lst, layer_3_rank_4_lst, layer_3_rank_5_lst, layer_3_rank_6_lst)

    coin_step_stop_loss_lst = []
    for coin in layer_3_rank_1_excel_lst:
        coin_step_stop_loss = get_coin_rank_step_stop_info(coin)
        coin_step_stop_loss_lst.append(coin_step_stop_loss)

    stop_loss_dict = {item[0]: item[2:] for item in coin_step_stop_loss_lst}

    # After adding stop loss and step values
    layer_3_rank_1_lst = add_stop_loss_to_rank_list(
        layer_3_rank_1_lst, stop_loss_dict)
    layer_3_rank_2_lst = add_stop_loss_to_rank_list(
        layer_3_rank_2_lst, stop_loss_dict)
    layer_3_rank_3_lst = add_stop_loss_to_rank_list(
        layer_3_rank_3_lst, stop_loss_dict)
    layer_3_rank_4_lst = add_stop_loss_to_rank_list(
        layer_3_rank_4_lst, stop_loss_dict)
    layer_3_rank_5_lst = add_stop_loss_to_rank_list(
        layer_3_rank_5_lst, stop_loss_dict)
    layer_3_rank_6_lst = add_stop_loss_to_rank_list(
        layer_3_rank_6_lst, stop_loss_dict)
    layer_3_rank_7_lst = add_stop_loss_to_rank_list(
        layer_3_rank_7_lst, stop_loss_dict)

    layer_3_rank_1_excel_lst_rank = add_rank_to_coin_data(
        layer_3_rank_1_excel_lst, layer_3_rank_1_lst)
    layer_3_rank_2_excel_lst_rank = add_rank_to_coin_data(
        layer_3_rank_2_excel_lst, layer_3_rank_2_lst)
    layer_3_rank_3_excel_lst_rank = add_rank_to_coin_data(
        layer_3_rank_3_excel_lst, layer_3_rank_3_lst)
    layer_3_rank_4_excel_lst_rank = add_rank_to_coin_data(
        layer_3_rank_4_excel_lst, layer_3_rank_4_lst)
    layer_3_rank_5_excel_lst_rank = add_rank_to_coin_data(
        layer_3_rank_5_excel_lst, layer_3_rank_5_lst)
    layer_3_rank_6_excel_lst_rank = add_rank_to_coin_data(
        layer_3_rank_6_excel_lst, layer_3_rank_6_lst)
    print("========= coin_rank_analysis Analysis Successful ==========")
    return [layer_3_rank_1_lst, layer_3_rank_2_lst, layer_3_rank_3_lst, layer_3_rank_4_lst, layer_3_rank_5_lst, layer_3_rank_6_lst, layer_3_rank_7_lst, layer_3_rank_1_excel_lst_rank, layer_3_rank_2_excel_lst_rank, layer_3_rank_3_excel_lst_rank, layer_3_rank_4_excel_lst_rank, layer_3_rank_5_excel_lst_rank, layer_3_rank_6_excel_lst_rank]
