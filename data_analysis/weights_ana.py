# Define the weight list
weight_lst = [
    ["last_swing_rand_per", 1, 1], ["last_swing_per", 1, 2], [
        "coin_dir_with_btc_dir", 1, 2], ["last_swing_time", 1, 3],
    ["last_swing_rsi_dif", 1, 4], ["last_3_s_rand_avg", 2, 1], [
        "last_3_s_rand_sum", 2, 1], ["last_3_s_per_avg", 2, 2],
    ["last_3_s_per_sum", 2, 2], ["last_3_s_avg_time", 2, 3], [
        "last_3_s_total_time", 2, 3], ["last_3_s_rsi_diff_avg", 2, 3],
    ["all_swings_zero_rand_count", 3, 1], ["all_swings_zero_rand_pp_count",
                                           3, 1], ["all_swings_zero_rand_np_count", 3, 1],
    ["all_swings_zero_rand_pp_med", 3, 1], ["all_swings_zero_rand_np_med", 3, 1], [
        "all_swings_zero_rand_pp_sum", 3, 2],
    ["all_swings_zero_rand_np_sum", 3, 2], ["all_swing_zero_rand_per_sum", 3, 2], [
        "t_10_sml_pp_zero_rand_sp_med", 3, 3],
    ["t_10_sml_np_zero_rand_sp_med", 3, 3], [
        "t_10_lrg_pp_zero_rand_sp_med", 3, 3], ["t_10_lrg_np_zero_rand_sp_med", 3, 3],
    ["t_10_sml_pp_zero_rand_sp_sum", 3, 4], [
        "t_10_sml_np_zero_rand_sp_sum", 3, 4], ["t_10_lrg_pp_zero_rand_sp_sum", 3, 4],
    ["t_10_lrg_np_zero_rand_sp_sum", 3, 4], [
        "all_swings_rand_pp_med", 3, 5], ["all_swings_rand_np_med", 3, 5],
    ["t_10_sml_pp_rand_sp_med", 3, 5], ["t_10_sml_np_rand_sp_med", 3, 5], [
        "t_10_lrg_pp_rand_sp_med", 3, 5],
    ["t_10_lrg_np_rand_sp_med", 3, 5], [
        "all_swing_rand_per_sum", 3, 6], ["all_swings_rand_pp_sum", 3, 6],
    ["all_swings_rand_np_sum", 3, 6], ["t_10_sml_pp_rand_sp_sum", 3, 6], [
        "t_10_sml_np_rand_sp_sum", 3, 6],
    ["t_10_lrg_pp_rand_sp_sum", 3, 6], ["t_10_lrg_np_rand_sp_sum", 3, 6], [
        "all_swing_count", 4, 1], ["all_swings_pp_med", 4, 1],
    ["all_swings_np_med", 4, 1], ["t_10_sml_pp_sp_med", 4, 1], [
        "t_10_sml_np_sp_med", 4, 1], ["t_10_lrg_pp_sp_med", 4, 1],
    ["t_10_lrg_np_sp_med", 4, 1], ["all_swing_per_sum", 4, 2], [
        "all_swings_pp_sum", 4, 2], ["all_swings_np_sum", 4, 2],
    ["t_10_sml_pp_sp_sum", 4, 2], ["t_10_sml_np_sp_sum", 4, 2], [
        "t_10_lrg_pp_sp_sum", 4, 2], ["t_10_lrg_np_sp_sum", 4, 2],
    ["sp_pp_cnt_0_2_lst", 4, 3], ["sp_np_cnt_0_2_lst", 4, 3], [
        "sp_pp_cnt_2_4_lst", 4, 3], ["sp_np_cnt_2_4_lst", 4, 3],
    ["sp_pp_cnt_4_7_lst", 4, 3], ["sp_np_cnt_4_7_lst", 4, 3], [
        "sp_pp_cnt_7_15_lst", 4, 3], ["sp_np_cnt_7_15_lst", 4, 3],
    ["sp_pp_cnt_15_25_lst", 4, 3], ["sp_np_cnt_15_25_lst", 4, 3], [
        "rand_pp_cnt_0_to_0_25_lst", 4, 4], ["rand_np_cnt_0_to_0_25_lst", 4, 4],
    ["rand_pp_cnt_0_25_to_0_5_lst", 4, 4], [
        "rand_np_cnt_0_25_to_0_5_lst", 4, 4], ["rand_pp_cnt_0_to_0_5_lst", 4, 4],
    ["rand_np_cnt_0_to_0_5_lst", 4, 4], ["rand_pp_cnt_0_5_to_1_lst", 4, 4], [
        "rand_np_cnt_0_5_to_1_lst", 4, 4],
    ["rand_pp_cnt_1_to_1_5_lst", 4, 4], ["rand_np_cnt_1_to_1_5_lst", 4, 4], [
        "rand_pp_cnt_0_5_to_1_5_lst", 4, 4],
    ["rand_np_cnt_0_5_to_1_5_lst", 4, 4], ["rand_pp_cnt_1_5_to_3_5_lst", 4, 4], [
        "rand_np_cnt_1_5_to_3_5_lst", 4, 4],
    ["rand_pp_cnt_3_5_to_7_lst", 4, 4], [
        "rand_np_cnt_3_5_to_7_lst", 4, 4], ["rand_pp_cnt_7_to_15_lst", 4, 4],
    ["rand_np_cnt_7_to_15_lst", 4, 4], ["all_swing_median_time", 5, 1], [
        "zero_rand_med_s_time", 5, 1], ["zero_rand_pstv_sp_med_s_time", 5, 1],
    ["zero_rand_neg_sp_med_s_time", 5, 1], [
        "top_10_sml_pstv_median_time", 5, 1], ["top_10_sml_neg_median_time", 5, 1],
    ["top_10_lrg_pstv_median_time", 5, 1], ["top_10_lrg_neg_median_time", 5, 1], [
        "sum_all_s_time", 5, 2], ["zero_rand_total_s_time", 5, 2],
    ["top_10_sml_pstv_total_rand_per", 5, 2], [
        "top_10_sml_neg_total_rand_per", 5, 2], ["top_10_sml_pstv_total_per", 5, 2],
    ["top_10_sml_neg_total_per", 5, 2], ["top_10_lrg_pstv_total_rand_per", 5, 2], [
        "top_10_lrg_neg_total_rand_per", 5, 2],
    ["top_10_lrg_pstv_total_per", 5, 2], [
        "top_10_lrg_neg_total_per", 5, 2], ["all_swing_median_rsi_df", 5, 3],
    ["pstv_swing_median_rsi_df", 5, 3], ["neg_swing_median_rsi_df", 5, 3], [
        "zero_rand_pstv_sp_med_s_rsi_df", 5, 3],
    ["zero_rand_neg_sp_med_s_rsi_df", 5, 3], [
        "top_10_sml_pstv_median_rsi_df", 5, 3], ["top_10_sml_neg_median_rsi_df", 5, 3],
    ["top_10_lrg_pstv_median_rsi_df", 5, 3], [
        "top_10_lrg_neg_median_rsi_df", 5, 3], ["sum_all_s_rsi_df", 5, 4],
    ["zero_rand_med_s_rsi_df", 5, 4], ["zero_rand_total_s_rsi_df", 5, 4], [
        "total_fb", 5, 5], ["total_pstv_fb", 5, 5],
    ["total_neg_fb", 5, 5]
]

# Initialize total score and parameters
total_score = 1000
main_group_score_reduction = 0.9  # 10% reduction for moving to next main group
sub_group_score_reduction = 0.95  # 5% reduction for moving to next sub group

# Initialize variables to track the current scores and the previous main/sub groups
current_score = total_score
prev_main_group = weight_lst[0][1]
prev_sub_group = weight_lst[0][2]

# List to store the final weighted list with scores added
weighted_lst_with_scores = []

# Iterate through the weight list
for item in weight_lst:
    main_group, sub_group = item[1], item[2]

    # Check if we moved to the next main group
    if main_group != prev_main_group:
        current_score *= main_group_score_reduction  # Reduce score by 10%
        prev_main_group = main_group  # Update the main group
        prev_sub_group = sub_group  # Reset the sub group

    # Check if we moved to the next sub group
    elif sub_group != prev_sub_group:
        current_score *= sub_group_score_reduction  # Reduce score by 5%
        prev_sub_group = sub_group  # Update the sub group

    # Append the item with the current score
    weighted_lst_with_scores.append(item + [round(current_score/10, 2)])

# Print the final list with the scores
for item in weighted_lst_with_scores:
    print(item)
