from utils.json_ops import load_json_from_file
default_values_file_path = 'default_values\default_values.json'
# Read the Json File
stored_default_value_dict = load_json_from_file(default_values_file_path)


if not stored_default_value_dict:
    pass
else:
    # Software folder path
    vts_software_folder_path = stored_default_value_dict["set_software_path"]
    output_excel_folder_path = stored_default_value_dict["output_excel_folder_path"]
    btc_excel_folder_path = stored_default_value_dict["btc_excel_folder_path"] 
    # cursor wait time
    wait_time_sec = stored_default_value_dict["wait_time_sec"]
    # calender x & y positions
    calender_1_tf = stored_default_value_dict["set_calender_x_y_position"][0]
    calender_2_tf = stored_default_value_dict["set_calender_x_y_position"][1]
    calender_5_tf = stored_default_value_dict["set_calender_x_y_position"][2]
    go_to_calender = stored_default_value_dict["set_calender_x_y_position"][3]
    choose_date = stored_default_value_dict["set_calender_x_y_position"][4]
    go_to_button = stored_default_value_dict["set_calender_x_y_position"][5]
    # chart x & y positions
    arrow_button = stored_default_value_dict["set_chart_x_y_positions"][0]
    export_chart = stored_default_value_dict["set_chart_x_y_positions"][1]
    chart_button = stored_default_value_dict["set_chart_x_y_positions"][2]
    one_TF_chart = stored_default_value_dict["set_chart_x_y_positions"][3]
    two_TF_chart = stored_default_value_dict["set_chart_x_y_positions"][4]
    five_TF_chart = stored_default_value_dict["set_chart_x_y_positions"][5]
    export_button = stored_default_value_dict["set_chart_x_y_positions"][6]
    # Auto Alert x & y positions
    initial_click = stored_default_value_dict["auto_alert_positions"][0]
    indicator_click = stored_default_value_dict["auto_alert_positions"][1]
    dots_click = stored_default_value_dict["auto_alert_positions"][2]
    add_alert = stored_default_value_dict["auto_alert_positions"][3]
    nh_create_button = stored_default_value_dict["auto_alert_positions"][4]
    click_condition = stored_default_value_dict["auto_alert_positions"][5]
    choose_low = stored_default_value_dict["auto_alert_positions"][6]
    nl_create_button = stored_default_value_dict["auto_alert_positions"][4]

layer_3_rank_1_col_weights = {
    "last_swing_per": 0.95,
    "last_swing_rand_per": -1,
    "last_swing_time": 0.9,
    "last_swing_rsi_dif": 0.86,
    "last_3_s_per_sum": 0.73,
    "last_3_s_per_avg": 0.73,
    "last_3_s_rand_sum": -0.77,
    "last_3_s_rand_avg": -0.77,
    "last_3_s_avg_time": 0.7,
    "last_3_s_rsi_diff_avg": 0.7,
    "all_swing_count": -0.44,
    "all_swings_pp_count": -0.44,
    "all_swings_np_count": -0.44,
    "all_swing_per_sum": 0.41,
    "all_swings_pp_sum": 0.41,
    "all_swings_np_sum": 0.41,
    "all_swings_pp_avg": 0.44,
    "all_swings_np_avg": 0.44,
    "all_swings_pp_med": 0.44,
    "all_swings_np_med": 0.44,
    "t_10_lrg_pp_sp_sum": 0.41,
    "t_10_lrg_np_sp_sum": 0.41,
    "t_10_lrg_pp_sp_avg": 0.44,
    "t_10_lrg_np_sp_avg": 0.44,
    "t_10_lrg_pp_sp_med": 0.44,
    "t_10_lrg_np_sp_med": 0.44,
    "t_10_sml_pp_sp_sum": 0.41,
    "t_10_sml_np_sp_sum": 0.41,
    "t_10_sml_pp_sp_avg": 0.44,
    "t_10_sml_np_sp_avg": 0.44,
    "t_10_sml_pp_sp_med": 0.44,
    "t_10_sml_np_sp_med": 0.44,
    "sp_pp_cnt_0_2_lst": -0.39,
    "sp_pp_cnt_2_4_lst": -0.39,
    "sp_pp_cnt_4_7_lst": 0.39,
    "sp_pp_cnt_7_15_lst": 0.39,
    "sp_pp_cnt_15_25_lst": 0.39,
    "sp_np_cnt_0_2_lst": -0.39,
    "sp_np_cnt_2_4_lst": -0.39,
    "sp_np_cnt_4_7_lst": 0.39,
    "sp_np_cnt_7_15_lst": 0.39,
    "sp_np_cnt_15_25_lst": 0.39,
    "all_swing_rand_per_sum": -0.48,
    "all_swings_rand_pp_sum": -0.48,
    "all_swings_rand_np_sum": -0.48,
    "all_swings_rand_pp_avg": -0.51,
    "all_swings_rand_np_avg": -0.51,
    "all_swings_rand_pp_med": -0.51,
    "all_swings_rand_np_med": -0.51,
    "t_10_lrg_pp_rand_sp_sum": -0.48,
    "t_10_lrg_np_rand_sp_sum": -0.48,
    "t_10_lrg_pp_rand_sp_avg": -0.51,
    "t_10_lrg_np_rand_sp_avg": -0.51,
    "t_10_lrg_pp_rand_sp_med": -0.51,
    "t_10_lrg_np_rand_sp_med": -0.51,
    "t_10_sml_pp_rand_sp_sum": -0.48,
    "t_10_sml_np_rand_sp_sum": -0.48,
    "t_10_sml_pp_rand_sp_avg": -0.51,
    "t_10_sml_np_rand_sp_avg": -0.51,
    "t_10_sml_pp_rand_sp_med": -0.51,
    "t_10_sml_np_rand_sp_med": -0.51,
    "all_swings_zero_rand_count": 0.63,
    "all_swings_zero_rand_pp_count": 0.63,
    "all_swings_zero_rand_np_count": 0.63,
    "all_swings_zero_rand_pp_sum": 0.6,
    "all_swings_zero_rand_np_sum": 0.6,
    "all_swing_zero_rand_per_sum": 0.6,
    "all_swings_zero_rand_pp_mean": 0.63,
    "all_swings_zero_rand_np_mean": 0.63,
    "all_swings_zero_rand_pp_med": 0.63,
    "all_swings_zero_rand_np_med": 0.63,
    "t_10_lrg_pp_zero_rand_sp_sum": 0.54,
    "t_10_lrg_np_zero_rand_sp_sum": 0.54,
    "t_10_lrg_pp_zero_rand_sp_avg": 0.57,
    "t_10_lrg_np_zero_rand_sp_avg": 0.57,
    "t_10_lrg_pp_zero_rand_sp_med": 0.57,
    "t_10_lrg_np_zero_rand_sp_med": 0.57,
    "t_10_sml_pp_zero_rand_sp_sum": 0.54,
    "t_10_sml_np_zero_rand_sp_sum": 0.54,
    "t_10_sml_pp_zero_rand_sp_avg": 0.57,
    "t_10_sml_np_zero_rand_sp_avg": 0.57,
    "t_10_sml_pp_zero_rand_sp_med": 0.57,
    "t_10_sml_np_zero_rand_sp_med": 0.57,
    "rand_pp_cnt_0_to_0_25_lst": 0.37,
    "rand_pp_cnt_0_25_to_0_5_lst": 0.37,
    "rand_pp_cnt_0_to_0_5_lst": 0.37,
    "rand_pp_cnt_0_5_to_1_lst": 0.37,
    "rand_pp_cnt_1_to_1_5_lst": 0.37,
    "rand_pp_cnt_0_5_to_1_5_lst": 0.37,
    "rand_pp_cnt_1_5_to_3_5_lst": -0.37,
    "rand_pp_cnt_3_5_to_7_lst": -0.37,
    "rand_pp_cnt_7_to_15_lst": -0.37,
    "rand_np_cnt_0_to_0_25_lst": 0.37,
    "rand_np_cnt_0_25_to_0_5_lst": 0.37,
    "rand_np_cnt_0_to_0_5_lst": 0.37,
    "rand_np_cnt_0_5_to_1_lst": 0.37,
    "rand_np_cnt_1_to_1_5_lst": 0.37,
    "rand_np_cnt_0_5_to_1_5_lst": 0.37,
    "rand_np_cnt_1_5_to_3_5_lst": -0.37,
    "rand_np_cnt_3_5_to_7_lst": -0.37,
    "rand_np_cnt_7_to_15_lst": -0.37,
    "all_swing_max_time": 0.34,
    "all_swing_avg_time": 0.34,
    "all_swing_median_time": 0.34,
    "pstv_swing_max_time": 0.34,
    "pstv_swing_avg_time": 0.34,
    "pstv_swing_median_time": 0.34,
    "neg_swing_max_time": 0.34,
    "neg_swing_avg_time": 0.34,
    "neg_swing_median_time": 0.34,
    "top_10_lrg_pstv_total_rand_per_change": 0.34,
    "top_10_lrg_pstv_max_time": 0.34,
    "top_10_lrg_pstv_avg_time": 0.34,
    "top_10_lrg_pstv_median_time": 0.34,
    "top_10_sml_pstv_total_rand_per_change": 0.34,
    "top_10_sml_pstv_max_time": 0.34,
    "top_10_sml_pstv_avg_time": 0.34,
    "top_10_sml_pstv_median_time": 0.34,
    "top_10_lrg_neg_total_rand_per_change": 0.34,
    "top_10_lrg_neg_max_time": 0.34,
    "top_10_lrg_neg_avg_time": 0.34,
    "top_10_lrg_neg_median_time": 0.34,
    "top_10_sml_neg_total_rand_per_change": 0.34,
    "top_10_sml_neg_max_time": 0.34,
    "top_10_sml_neg_avg_time": 0.34,
    "top_10_sml_neg_median_time": 0.34,
    "zero_rand_max_swings_time": 0.34,
    "zero_rand_avg_swings_time": 0.34,
    "zero_rand_med_swings_time": 0.34,
    "zero_rand_pstv_sp_max_swings_time": 0.34,
    "zero_rand_pstv_sp_avg_swings_time": 0.34,
    "zero_rand_pstv_sp_med_swings_time": 0.34,
    "zero_rand_neg_sp_max_swings_time": 0.34,
    "zero_rand_neg_sp_avg_swings_time": 0.34,
    "zero_rand_neg_sp_med_swings_time": 0.34,
    "all_swing_max_rsi_diff": 0.3,
    "all_swing_avg_rsi_diff": 0.3,
    "all_swing_median_rsi_diff": 0.3,
    "pstv_swing_max_rsi_diff": 0.3,
    "pstv_swing_avg_rsi_diff": 0.3,
    "pstv_swing_median_rsi_diff": 0.3,
    "neg_swing_max_rsi_diff": 0.3,
    "neg_swing_avg_rsi_diff": 0.3,
    "neg_swing_median_rsi_diff": 0.3,
    "top_10_lrg_pstv_max_rsi_diff": 0.3,
    "top_10_lrg_pstv_avg_rsi_diff": 0.3,
    "top_10_lrg_pstv_median_rsi_diff": 0.3,
    "top_10_sml_pstv_max_rsi_diff": 0.3,
    "top_10_sml_pstv_avg_rsi_diff": 0.3,
    "top_10_sml_pstv_median_rsi_diff": 0.3,
    "top_10_lrg_neg_max_rsi_diff": 0.3,
    "top_10_lrg_neg_avg_rsi_diff": 0.3,
    "top_10_lrg_neg_median_rsi_diff": 0.3,
    "top_10_sml_neg_max_rsi_diff": 0.3,
    "top_10_sml_neg_avg_rsi_diff": 0.3,
    "top_10_sml_neg_median_rsi_diff": 0.3,
    "zero_rand_max_swings_rsi_diff": 0.3,
    "zero_rand_avg_swings_rsi_diff": 0.3,
    "zero_rand_med_swings_rsi_diff": 0.3,
    "zero_rand_pstv_sp_max_swings_rsi_diff": 0.3,
    "zero_rand_pstv_sp_avg_swings_rsi_diff": 0.3,
    "zero_rand_pstv_sp_med_swings_rsi_diff": 0.3,
    "zero_rand_neg_sp_max_swings_rsi_diff": 0.3,
    "zero_rand_neg_sp_avg_swings_rsi_diff": 0.3,
    "zero_rand_neg_sp_med_swings_rsi_diff": 0.3,
    "total_fb": -0.27,
    "total_pstv_fb": -0.27,
    "total_neg_fb": -0.27
}

layer_3_rank_2_col_weights = {
    'last_swing_per': 0.95, 'last_swing_rand_per': -1, 'last_swing_time': 0.9, 'last_swing_rsi_dif': 0.86, 'last_3_s_per_sum': 0.73, 'last_3_s_rand_sum': -0.77, 'last_3_s_avg_time': 0.7, 'last_3_s_rsi_diff_avg': 0.7, 'all_swing_count': -0.44, 'all_swings_pp_count': -0.44, 'all_swings_np_count': -0.44, 'all_swing_per_sum': 0.41, 'all_swings_pp_sum': 0.41, 'all_swings_np_sum': 0.41, 't_10_lrg_pp_sp_sum': 0.41, 't_10_lrg_np_sp_sum': 0.41, 't_10_sml_pp_sp_sum': 0.41, 't_10_sml_np_sp_sum': 0.41, 'sp_pp_cnt_0_2_lst': -0.39, 'sp_pp_cnt_2_4_lst': -0.39, 'sp_pp_cnt_4_7_lst': 0.39, 'sp_pp_cnt_7_15_lst': 0.39, 'sp_pp_cnt_15_25_lst': 0.39, 'sp_np_cnt_0_2_lst': -0.39, 'sp_np_cnt_2_4_lst': -0.39, 'sp_np_cnt_4_7_lst': 0.39, 'sp_np_cnt_7_15_lst': 0.39, 'sp_np_cnt_15_25_lst': 0.39, 'all_swing_rand_per_sum': -0.48, 'all_swings_rand_pp_sum': -0.48, 'all_swings_rand_np_sum': -0.48, 't_10_lrg_pp_rand_sp_sum': -0.48, 't_10_lrg_np_rand_sp_sum': -0.48, 't_10_sml_pp_rand_sp_sum': -0.48, 't_10_sml_np_rand_sp_sum': -0.48, 'all_swings_zero_rand_count': 0.63, 'all_swings_zero_rand_pp_count': 0.63, 'all_swings_zero_rand_np_count': 0.63, 'all_swings_zero_rand_pp_sum': 0.6, 'all_swings_zero_rand_np_sum': 0.6, 'all_swing_zero_rand_per_sum': 0.6, 't_10_lrg_pp_zero_rand_sp_sum': 0.54, 't_10_lrg_np_zero_rand_sp_sum': 0.54, 't_10_sml_pp_zero_rand_sp_sum': 0.54, 't_10_sml_np_zero_rand_sp_sum': 0.54, 'rand_pp_cnt_0_to_0_25_lst': 0.37, 'rand_pp_cnt_0_25_to_0_5_lst': 0.37, 'rand_pp_cnt_0_to_0_5_lst': 0.37, 'rand_pp_cnt_0_5_to_1_lst': 0.37, 'rand_pp_cnt_1_to_1_5_lst': 0.37, 'rand_pp_cnt_0_5_to_1_5_lst': 0.37, 'rand_pp_cnt_1_5_to_3_5_lst': -0.37, 'rand_pp_cnt_3_5_to_7_lst': -0.37, 'rand_pp_cnt_7_to_15_lst': -0.37, 'rand_np_cnt_0_to_0_25_lst': 0.37, 'rand_np_cnt_0_25_to_0_5_lst': 0.37, 'rand_np_cnt_0_to_0_5_lst': 0.37, 'rand_np_cnt_0_5_to_1_lst': 0.37, 'rand_np_cnt_1_to_1_5_lst': 0.37, 'rand_np_cnt_0_5_to_1_5_lst': 0.37, 'rand_np_cnt_1_5_to_3_5_lst': -0.37, 'rand_np_cnt_3_5_to_7_lst': -0.37, 'rand_np_cnt_7_to_15_lst': -0.37, 'all_swing_avg_time': 0.34, 'pstv_swing_avg_time': 0.34, 'neg_swing_avg_time': 0.34, 'top_10_lrg_pstv_total_rand_per_change': 0.34, 'top_10_lrg_pstv_avg_time': 0.34, 'top_10_sml_pstv_total_rand_per_change': 0.34, 'top_10_sml_pstv_avg_time': 0.34, 'top_10_lrg_neg_avg_time': 0.34, 'top_10_sml_neg_avg_time': 0.34, 'zero_rand_avg_swings_time': 0.34, 'zero_rand_pstv_sp_avg_swings_time': 0.34, 'zero_rand_neg_sp_avg_swings_time': 0.34, 'all_swing_avg_rsi_diff': 0.3, 'pstv_swing_avg_rsi_diff': 0.3, 'neg_swing_avg_rsi_diff': 0.3, 'top_10_lrg_pstv_avg_rsi_diff': 0.3, 'top_10_sml_pstv_avg_rsi_diff': 0.3, 'top_10_lrg_neg_avg_rsi_diff': 0.3, 'top_10_sml_neg_avg_rsi_diff': 0.3, 'zero_rand_avg_swings_rsi_diff': 0.3, 'zero_rand_pstv_sp_avg_swings_rsi_diff': 0.3, 'zero_rand_neg_sp_avg_swings_rsi_diff': 0.3, 'total_fb': -0.27, 'total_pstv_fb': -0.27, 'total_neg_fb': -0.27}

layer_3_rank_3_col_weights = {
    'last_swing_per': 0.95, 'last_swing_rand_per': -1, 'last_swing_time': 0.9, 'last_swing_rsi_dif': 0.86, 'last_3_s_per_sum': 0.73, 'last_3_s_rand_avg': -0.77, 'last_3_s_avg_time': 0.7, 'last_3_s_rsi_diff_avg': 0.7, 'all_swing_count': -0.44, 'all_swings_pp_count': -0.44, 'all_swings_np_count': -0.44, 'all_swing_per_sum': 0.41, 'all_swings_pp_sum': 0.41, 'all_swings_np_sum': 0.41, 't_10_lrg_pp_sp_sum': 0.41, 't_10_lrg_np_sp_sum': 0.41, 't_10_sml_pp_sp_sum': 0.41, 't_10_sml_np_sp_sum': 0.41, 'sp_pp_cnt_0_2_lst': -0.39, 'sp_pp_cnt_2_4_lst': -0.39, 'sp_pp_cnt_4_7_lst': 0.39, 'sp_pp_cnt_7_15_lst': 0.39, 'sp_pp_cnt_15_25_lst': 0.39, 'sp_np_cnt_0_2_lst': -0.39, 'sp_np_cnt_2_4_lst': -0.39, 'sp_np_cnt_4_7_lst': 0.39, 'sp_np_cnt_7_15_lst': 0.39, 'sp_np_cnt_15_25_lst': 0.39, 'all_swings_rand_pp_avg': -0.51, 'all_swings_rand_np_avg': -0.51, 't_10_lrg_pp_rand_sp_avg': -0.51, 't_10_lrg_np_rand_sp_avg': -0.51, 't_10_sml_pp_rand_sp_avg': -0.51, 't_10_sml_np_rand_sp_avg': -0.51, 'all_swings_zero_rand_count': 0.63, 'all_swings_zero_rand_pp_count': 0.63, 'all_swings_zero_rand_np_count': 0.63, 'all_swings_zero_rand_pp_mean': 0.63, 'all_swings_zero_rand_np_mean': 0.63, 't_10_lrg_pp_zero_rand_sp_avg': 0.57, 't_10_lrg_np_zero_rand_sp_avg': 0.57, 't_10_sml_pp_zero_rand_sp_avg': 0.57, 't_10_sml_np_zero_rand_sp_avg': 0.57, 'rand_pp_cnt_0_to_0_25_lst': 0.37, 'rand_pp_cnt_0_25_to_0_5_lst': 0.37, 'rand_pp_cnt_0_to_0_5_lst': 0.37, 'rand_pp_cnt_0_5_to_1_lst': 0.37, 'rand_pp_cnt_1_to_1_5_lst': 0.37, 'rand_pp_cnt_0_5_to_1_5_lst': 0.37, 'rand_pp_cnt_1_5_to_3_5_lst': -0.37, 'rand_pp_cnt_3_5_to_7_lst': -0.37, 'rand_pp_cnt_7_to_15_lst': -0.37, 'rand_np_cnt_0_to_0_25_lst': 0.37, 'rand_np_cnt_0_25_to_0_5_lst': 0.37, 'rand_np_cnt_0_to_0_5_lst': 0.37, 'rand_np_cnt_0_5_to_1_lst': 0.37, 'rand_np_cnt_1_to_1_5_lst': 0.37, 'rand_np_cnt_0_5_to_1_5_lst': 0.37, 'rand_np_cnt_1_5_to_3_5_lst': -0.37, 'rand_np_cnt_3_5_to_7_lst': -0.37, 'rand_np_cnt_7_to_15_lst': -0.37, 'all_swing_avg_time': 0.34, 'pstv_swing_avg_time': 0.34, 'neg_swing_avg_time': 0.34, 'top_10_lrg_pstv_total_rand_per_change': 0.34, 'top_10_lrg_pstv_avg_time': 0.34, 'top_10_sml_pstv_total_rand_per_change': 0.34, 'top_10_sml_pstv_avg_time': 0.34, 'top_10_lrg_neg_avg_time': 0.34, 'top_10_sml_neg_avg_time': 0.34, 'zero_rand_avg_swings_time': 0.34, 'zero_rand_pstv_sp_avg_swings_time': 0.34, 'zero_rand_neg_sp_avg_swings_time': 0.34, 'all_swing_avg_rsi_diff': 0.3, 'pstv_swing_avg_rsi_diff': 0.3, 'neg_swing_avg_rsi_diff': 0.3, 'top_10_lrg_pstv_avg_rsi_diff': 0.3, 'top_10_sml_pstv_avg_rsi_diff': 0.3, 'top_10_lrg_neg_avg_rsi_diff': 0.3, 'top_10_sml_neg_avg_rsi_diff': 0.3, 'zero_rand_avg_swings_rsi_diff': 0.3, 'zero_rand_pstv_sp_avg_swings_rsi_diff': 0.3, 'zero_rand_neg_sp_avg_swings_rsi_diff': 0.3, 'total_fb': -0.27, 'total_pstv_fb': -0.27, 'total_neg_fb': -0.27}

layer_3_rank_4_col_weights = {
    'last_swing_per': 0.95, 'last_swing_rand_per': -1, 'last_swing_time': 0.9, 'last_swing_rsi_dif': 0.86, 'last_3_s_per_avg': 0.73, 'last_3_s_rand_avg': -0.77, 'last_3_s_avg_time': 0.7, 'last_3_s_rsi_diff_avg': 0.7, 'all_swing_count': -0.44, 'all_swings_pp_count': -0.44, 'all_swings_np_count': -0.44, 'all_swings_pp_avg': 0.44, 'all_swings_np_avg': 0.44, 't_10_lrg_pp_sp_avg': 0.44, 't_10_lrg_np_sp_avg': 0.44, 't_10_sml_pp_sp_avg': 0.44, 't_10_sml_np_sp_avg': 0.44, 'sp_pp_cnt_0_2_lst': -0.39, 'sp_pp_cnt_2_4_lst': -0.39, 'sp_pp_cnt_4_7_lst': 0.39, 'sp_pp_cnt_7_15_lst': 0.39, 'sp_pp_cnt_15_25_lst': 0.39, 'sp_np_cnt_0_2_lst': -0.39, 'sp_np_cnt_2_4_lst': -0.39, 'sp_np_cnt_4_7_lst': 0.39, 'sp_np_cnt_7_15_lst': 0.39, 'sp_np_cnt_15_25_lst': 0.39, 'all_swing_rand_per_sum': -0.48, 'all_swings_rand_pp_sum': -0.48, 'all_swings_rand_np_sum': -0.48, 't_10_lrg_pp_rand_sp_sum': -0.48, 't_10_lrg_np_rand_sp_sum': -0.48, 't_10_sml_pp_rand_sp_sum': -0.48, 't_10_sml_np_rand_sp_sum': -0.48, 'all_swings_zero_rand_count': 0.63, 'all_swings_zero_rand_pp_count': 0.63, 'all_swings_zero_rand_np_count': 0.63, 'all_swings_zero_rand_pp_sum': 0.6, 'all_swings_zero_rand_np_sum': 0.6, 'all_swing_zero_rand_per_sum': 0.6, 't_10_lrg_pp_zero_rand_sp_sum': 0.54, 't_10_lrg_np_zero_rand_sp_sum': 0.54, 't_10_sml_pp_zero_rand_sp_sum': 0.54, 't_10_sml_np_zero_rand_sp_sum': 0.54, 'rand_pp_cnt_0_to_0_25_lst': 0.37, 'rand_pp_cnt_0_25_to_0_5_lst': 0.37, 'rand_pp_cnt_0_to_0_5_lst': 0.37, 'rand_pp_cnt_0_5_to_1_lst': 0.37, 'rand_pp_cnt_1_to_1_5_lst': 0.37, 'rand_pp_cnt_0_5_to_1_5_lst': 0.37, 'rand_pp_cnt_1_5_to_3_5_lst': -0.37, 'rand_pp_cnt_3_5_to_7_lst': -0.37, 'rand_pp_cnt_7_to_15_lst': -0.37, 'rand_np_cnt_0_to_0_25_lst': 0.37, 'rand_np_cnt_0_25_to_0_5_lst': 0.37, 'rand_np_cnt_0_to_0_5_lst': 0.37, 'rand_np_cnt_0_5_to_1_lst': 0.37, 'rand_np_cnt_1_to_1_5_lst': 0.37, 'rand_np_cnt_0_5_to_1_5_lst': 0.37, 'rand_np_cnt_1_5_to_3_5_lst': -0.37, 'rand_np_cnt_3_5_to_7_lst': -0.37, 'rand_np_cnt_7_to_15_lst': -0.37, 'all_swing_avg_time': 0.34, 'pstv_swing_avg_time': 0.34, 'neg_swing_avg_time': 0.34, 'top_10_lrg_pstv_total_rand_per_change': 0.34, 'top_10_lrg_pstv_avg_time': 0.34, 'top_10_sml_pstv_total_rand_per_change': 0.34, 'top_10_sml_pstv_avg_time': 0.34, 'top_10_lrg_neg_avg_time': 0.34, 'top_10_sml_neg_avg_time': 0.34, 'zero_rand_avg_swings_time': 0.34, 'zero_rand_pstv_sp_avg_swings_time': 0.34, 'zero_rand_neg_sp_avg_swings_time': 0.34, 'all_swing_avg_rsi_diff': 0.3, 'pstv_swing_avg_rsi_diff': 0.3, 'neg_swing_avg_rsi_diff': 0.3, 'top_10_lrg_pstv_avg_rsi_diff': 0.3, 'top_10_sml_pstv_avg_rsi_diff': 0.3, 'top_10_lrg_neg_avg_rsi_diff': 0.3, 'top_10_sml_neg_avg_rsi_diff': 0.3, 'zero_rand_avg_swings_rsi_diff': 0.3, 'zero_rand_neg_sp_avg_swings_rsi_diff': 0.3, 'total_fb': -0.27, 'total_pstv_fb': -0.27, 'total_neg_fb': -0.27}

layer_3_rank_5_col_weights = {
    'last_swing_per': 0.95, 'last_swing_rand_per': -1, 'last_swing_time': 0.9, 'last_swing_rsi_dif': 0.86, 'last_3_s_per_avg': 0.73, 'last_3_s_rand_avg': -0.77, 'last_3_s_avg_time': 0.7, 'last_3_s_rsi_diff_avg': 0.7, 'all_swing_count': -0.44, 'all_swings_pp_count': -0.44, 'all_swings_np_count': -0.44, 'all_swings_pp_avg': 0.44, 'all_swings_np_avg': 0.44, 't_10_lrg_pp_sp_avg': 0.44, 't_10_lrg_np_sp_avg': 0.44, 't_10_sml_pp_sp_avg': 0.44, 't_10_sml_np_sp_avg': 0.44, 'sp_pp_cnt_0_2_lst': -0.39, 'sp_pp_cnt_2_4_lst': -0.39, 'sp_pp_cnt_4_7_lst': 0.39, 'sp_pp_cnt_7_15_lst': 0.39, 'sp_pp_cnt_15_25_lst': 0.39, 'sp_np_cnt_0_2_lst': -0.39, 'sp_np_cnt_2_4_lst': -0.39, 'sp_np_cnt_4_7_lst': 0.39, 'sp_np_cnt_7_15_lst': 0.39, 'sp_np_cnt_15_25_lst': 0.39, 'all_swings_rand_pp_avg': -0.51, 'all_swings_rand_np_avg': -0.51, 't_10_lrg_pp_rand_sp_avg': -0.51, 't_10_lrg_np_rand_sp_avg': -0.51, 't_10_sml_pp_rand_sp_avg': -0.51, 't_10_sml_np_rand_sp_avg': -0.51, 'all_swings_zero_rand_count': 0.63, 'all_swings_zero_rand_pp_count': 0.63, 'all_swings_zero_rand_np_count': 0.63, 'all_swings_zero_rand_pp_mean': 0.63, 'all_swings_zero_rand_np_mean': 0.63, 't_10_lrg_pp_zero_rand_sp_avg': 0.57, 't_10_lrg_np_zero_rand_sp_avg': 0.57, 't_10_sml_pp_zero_rand_sp_avg': 0.57, 't_10_sml_np_zero_rand_sp_avg': 0.57, 'rand_pp_cnt_0_to_0_25_lst': 0.37, 'rand_pp_cnt_0_25_to_0_5_lst': 0.37, 'rand_pp_cnt_0_to_0_5_lst': 0.37, 'rand_pp_cnt_0_5_to_1_lst': 0.37, 'rand_pp_cnt_1_to_1_5_lst': 0.37, 'rand_pp_cnt_0_5_to_1_5_lst': 0.37, 'rand_pp_cnt_1_5_to_3_5_lst': -0.37, 'rand_pp_cnt_3_5_to_7_lst': -0.37, 'rand_pp_cnt_7_to_15_lst': -0.37, 'rand_np_cnt_0_to_0_25_lst': 0.37, 'rand_np_cnt_0_25_to_0_5_lst': 0.37, 'rand_np_cnt_0_to_0_5_lst': 0.37, 'rand_np_cnt_0_5_to_1_lst': 0.37, 'rand_np_cnt_1_to_1_5_lst': 0.37, 'rand_np_cnt_0_5_to_1_5_lst': 0.37, 'rand_np_cnt_1_5_to_3_5_lst': -0.37, 'rand_np_cnt_3_5_to_7_lst': -0.37, 'rand_np_cnt_7_to_15_lst': -0.37, 'all_swing_avg_time': 0.34, 'pstv_swing_avg_time': 0.34, 'neg_swing_avg_time': 0.34, 'top_10_lrg_pstv_total_rand_per_change': 0.34, 'top_10_lrg_pstv_avg_time': 0.34, 'top_10_sml_pstv_total_rand_per_change': 0.34, 'top_10_sml_pstv_avg_time': 0.34, 'top_10_lrg_neg_avg_time': 0.34, 'top_10_sml_neg_avg_time': 0.34, 'zero_rand_avg_swings_time': 0.34, 'zero_rand_pstv_sp_avg_swings_time': 0.34, 'zero_rand_neg_sp_avg_swings_time': 0.34, 'all_swing_avg_rsi_diff': 0.3, 'pstv_swing_avg_rsi_diff': 0.3, 'neg_swing_avg_rsi_diff': 0.3, 'top_10_lrg_pstv_avg_rsi_diff': 0.3, 'top_10_sml_pstv_avg_rsi_diff': 0.3, 'top_10_lrg_neg_avg_rsi_diff': 0.3, 'top_10_sml_neg_avg_rsi_diff': 0.3, 'zero_rand_avg_swings_rsi_diff': 0.3, 'zero_rand_neg_sp_avg_swings_rsi_diff': 0.3, 'total_fb': -0.27, 'total_pstv_fb': -0.27, 'total_neg_fb': -0.27}

layer_3_rank_6_col_weights = {
    'last_swing_per': 0.95, 'last_swing_rand_per': -1, 'last_swing_time': 0.9, 'last_swing_rsi_dif': 0.86, 'last_3_s_per_avg': 0.73, 'last_3_s_rand_avg': -0.77, 'last_3_s_avg_time': 0.7, 'last_3_s_rsi_diff_avg': 0.7, 'all_swing_count': -0.44, 'all_swings_pp_count': -0.44, 'all_swings_np_count': -0.44, 'all_swings_pp_med': 0.44, 'all_swings_np_med': 0.44, 't_10_lrg_pp_sp_med': 0.44, 't_10_lrg_np_sp_med': 0.44, 't_10_sml_pp_sp_med': 0.44, 't_10_sml_np_sp_med': 0.44, 'sp_pp_cnt_0_2_lst': -0.39, 'sp_pp_cnt_2_4_lst': -0.39, 'sp_pp_cnt_4_7_lst': 0.39, 'sp_pp_cnt_7_15_lst': 0.39, 'sp_pp_cnt_15_25_lst': 0.39, 'sp_np_cnt_0_2_lst': -0.39, 'sp_np_cnt_2_4_lst': -0.39, 'sp_np_cnt_4_7_lst': 0.39, 'sp_np_cnt_7_15_lst': 0.39, 'sp_np_cnt_15_25_lst': 0.39, 'all_swings_rand_pp_med': -0.51, 'all_swings_rand_np_med': -0.51, 't_10_lrg_pp_rand_sp_med': -0.51, 't_10_lrg_np_rand_sp_med': -0.51, 't_10_sml_pp_rand_sp_med': -0.51, 't_10_sml_np_rand_sp_med': -0.51, 'all_swings_zero_rand_count': 0.63, 'all_swings_zero_rand_pp_count': 0.63, 'all_swings_zero_rand_np_count': 0.63, 'all_swings_zero_rand_pp_med': 0.63, 'all_swings_zero_rand_np_med': 0.63, 't_10_lrg_pp_zero_rand_sp_med': 0.57, 't_10_lrg_np_zero_rand_sp_med': 0.57, 't_10_sml_pp_zero_rand_sp_med': 0.57, 't_10_sml_np_zero_rand_sp_med': 0.57, 'rand_pp_cnt_0_to_0_25_lst': 0.37, 'rand_pp_cnt_0_25_to_0_5_lst': 0.37, 'rand_pp_cnt_0_to_0_5_lst': 0.37, 'rand_pp_cnt_0_5_to_1_lst': 0.37, 'rand_pp_cnt_1_to_1_5_lst': 0.37, 'rand_pp_cnt_0_5_to_1_5_lst': 0.37, 'rand_pp_cnt_1_5_to_3_5_lst': -0.37, 'rand_pp_cnt_3_5_to_7_lst': -0.37, 'rand_pp_cnt_7_to_15_lst': -0.37, 'rand_np_cnt_0_to_0_25_lst': 0.37, 'rand_np_cnt_0_25_to_0_5_lst': 0.37, 'rand_np_cnt_0_to_0_5_lst': 0.37, 'rand_np_cnt_0_5_to_1_lst': 0.37, 'rand_np_cnt_1_to_1_5_lst': 0.37, 'rand_np_cnt_0_5_to_1_5_lst': 0.37, 'rand_np_cnt_1_5_to_3_5_lst': -0.37, 'rand_np_cnt_3_5_to_7_lst': -0.37, 'rand_np_cnt_7_to_15_lst': -0.37, 'all_swing_median_time': 0.34, 'pstv_swing_median_time': 0.34, 'neg_swing_median_time': 0.34, 'top_10_lrg_pstv_total_rand_per_change': 0.34, 'top_10_lrg_pstv_median_time': 0.34, 'top_10_sml_pstv_total_rand_per_change': 0.34, 'top_10_sml_pstv_median_time': 0.34, 'top_10_lrg_neg_median_time': 0.34, 'top_10_sml_neg_median_time': 0.34, 'zero_rand_med_swings_time': 0.34, 'zero_rand_pstv_sp_med_swings_time': 0.34, 'zero_rand_neg_sp_med_swings_time': 0.34, 'all_swing_median_rsi_diff': 0.3, 'pstv_swing_median_rsi_diff': 0.3, 'neg_swing_median_rsi_diff': 0.3, 'top_10_sml_pstv_median_rsi_diff': 0.3, 'top_10_lrg_neg_median_rsi_diff': 0.3, 'top_10_sml_neg_median_rsi_diff': 0.3, 'zero_rand_med_swings_rsi_diff': 0.3, 'zero_rand_pstv_sp_med_swings_rsi_diff': 0.3, 'zero_rand_neg_sp_med_swings_rsi_diff': 0.3, 'total_fb': -0.27, 'total_pstv_fb': -0.27, 'total_neg_fb': -0.27}

layer_3_str_info_col_names = [
    'coin_name', 'coin_time_tf', 'swing_1_info', 'swing_2_info', 'swing_3_info', 'swing_1_dir', 'swing_2_dir', 'swing_3_dir', 't_5_lrg_pp_sp_lst', 't_5_lrg_np_sp_lst', 't_3_sp_pp_ranges', 't_3_sp_np_ranges', 't_5_lrg_pp_rand_sp_lst', 't_5_lrg_np_rand_sp_lst', 't_5_lrg_pp_zero_rand_sp_lst', 't_5_lrg_np_zero_rand_sp_lst', 't_3_rand_pp_ranges', 't_3_rand_np_ranges', 'last_fb_time']

layer_3_rank_1_col_names = [
    "coin_name","coin_time_tf","last_swing_per","last_swing_rand_per","last_swing_time","last_swing_rsi_dif","last_3_s_per_sum","last_3_s_per_avg","last_3_s_rand_sum","last_3_s_rand_avg","last_3_s_avg_time","last_3_s_rsi_diff_avg","all_swing_count","all_swings_pp_count","all_swings_np_count","all_swing_per_sum","all_swings_pp_sum","all_swings_np_sum","all_swings_pp_avg","all_swings_np_avg","all_swings_pp_med","all_swings_np_med","t_10_lrg_pp_sp_sum","t_10_lrg_np_sp_sum","t_10_lrg_pp_sp_avg","t_10_lrg_np_sp_avg","t_10_lrg_pp_sp_med","t_10_lrg_np_sp_med","t_10_sml_pp_sp_sum","t_10_sml_np_sp_sum","t_10_sml_pp_sp_avg","t_10_sml_np_sp_avg","t_10_sml_pp_sp_med","t_10_sml_np_sp_med","sp_pp_cnt_0_2_lst","sp_pp_cnt_2_4_lst","sp_pp_cnt_4_7_lst","sp_pp_cnt_7_15_lst","sp_pp_cnt_15_25_lst","sp_np_cnt_0_2_lst","sp_np_cnt_2_4_lst","sp_np_cnt_4_7_lst","sp_np_cnt_7_15_lst","sp_np_cnt_15_25_lst","all_swing_rand_per_sum","all_swings_rand_pp_sum","all_swings_rand_np_sum","all_swings_rand_pp_avg","all_swings_rand_np_avg","all_swings_rand_pp_med","all_swings_rand_np_med","t_10_lrg_pp_rand_sp_sum","t_10_lrg_np_rand_sp_sum","t_10_lrg_pp_rand_sp_avg","t_10_lrg_np_rand_sp_avg","t_10_lrg_pp_rand_sp_med","t_10_lrg_np_rand_sp_med","t_10_sml_pp_rand_sp_sum","t_10_sml_np_rand_sp_sum","t_10_sml_pp_rand_sp_avg","t_10_sml_np_rand_sp_avg","t_10_sml_pp_rand_sp_med","t_10_sml_np_rand_sp_med","all_swings_zero_rand_count","all_swings_zero_rand_pp_count","all_swings_zero_rand_np_count","all_swings_zero_rand_pp_sum","all_swings_zero_rand_np_sum","all_swing_zero_rand_per_sum","all_swings_zero_rand_pp_mean","all_swings_zero_rand_np_mean","all_swings_zero_rand_pp_med","all_swings_zero_rand_np_med","t_10_lrg_pp_zero_rand_sp_sum","t_10_lrg_np_zero_rand_sp_sum","t_10_lrg_pp_zero_rand_sp_avg","t_10_lrg_np_zero_rand_sp_avg","t_10_lrg_pp_zero_rand_sp_med","t_10_lrg_np_zero_rand_sp_med","t_10_sml_pp_zero_rand_sp_sum","t_10_sml_np_zero_rand_sp_sum","t_10_sml_pp_zero_rand_sp_avg","t_10_sml_np_zero_rand_sp_avg","t_10_sml_pp_zero_rand_sp_med","t_10_sml_np_zero_rand_sp_med","rand_pp_cnt_0_to_0_25_lst","rand_pp_cnt_0_25_to_0_5_lst","rand_pp_cnt_0_to_0_5_lst","rand_pp_cnt_0_5_to_1_lst","rand_pp_cnt_1_to_1_5_lst","rand_pp_cnt_0_5_to_1_5_lst","rand_pp_cnt_1_5_to_3_5_lst","rand_pp_cnt_3_5_to_7_lst","rand_pp_cnt_7_to_15_lst","rand_np_cnt_0_to_0_25_lst","rand_np_cnt_0_25_to_0_5_lst","rand_np_cnt_0_to_0_5_lst","rand_np_cnt_0_5_to_1_lst","rand_np_cnt_1_to_1_5_lst","rand_np_cnt_0_5_to_1_5_lst","rand_np_cnt_1_5_to_3_5_lst","rand_np_cnt_3_5_to_7_lst","rand_np_cnt_7_to_15_lst","all_swing_max_time","all_swing_avg_time","all_swing_median_time","pstv_swing_max_time","pstv_swing_avg_time","pstv_swing_median_time","neg_swing_max_time","neg_swing_avg_time","neg_swing_median_time","top_10_lrg_pstv_total_rand_per_change","top_10_lrg_pstv_max_time","top_10_lrg_pstv_avg_time","top_10_lrg_pstv_median_time","top_10_sml_pstv_total_rand_per_change","top_10_sml_pstv_max_time","top_10_sml_pstv_avg_time","top_10_sml_pstv_median_time","top_10_lrg_neg_total_rand_per_change","top_10_lrg_neg_max_time","top_10_lrg_neg_avg_time","top_10_lrg_neg_median_time","top_10_sml_neg_total_rand_per_change","top_10_sml_neg_max_time","top_10_sml_neg_avg_time","top_10_sml_neg_median_time","zero_rand_max_swings_time","zero_rand_avg_swings_time","zero_rand_med_swings_time","zero_rand_pstv_sp_max_swings_time","zero_rand_pstv_sp_avg_swings_time","zero_rand_pstv_sp_med_swings_time","zero_rand_neg_sp_max_swings_time","zero_rand_neg_sp_avg_swings_time","zero_rand_neg_sp_med_swings_time","all_swing_max_rsi_diff","all_swing_avg_rsi_diff","all_swing_median_rsi_diff","pstv_swing_max_rsi_diff","pstv_swing_avg_rsi_diff","pstv_swing_median_rsi_diff","neg_swing_max_rsi_diff","neg_swing_avg_rsi_diff","neg_swing_median_rsi_diff","top_10_lrg_pstv_max_rsi_diff","top_10_lrg_pstv_avg_rsi_diff","top_10_lrg_pstv_median_rsi_diff","top_10_sml_pstv_max_rsi_diff","top_10_sml_pstv_avg_rsi_diff","top_10_sml_pstv_median_rsi_diff","top_10_lrg_neg_max_rsi_diff","top_10_lrg_neg_avg_rsi_diff","top_10_lrg_neg_median_rsi_diff","top_10_sml_neg_max_rsi_diff","top_10_sml_neg_avg_rsi_diff","top_10_sml_neg_median_rsi_diff","zero_rand_max_swings_rsi_diff","zero_rand_avg_swings_rsi_diff","zero_rand_med_swings_rsi_diff","zero_rand_pstv_sp_max_swings_rsi_diff","zero_rand_pstv_sp_avg_swings_rsi_diff","zero_rand_pstv_sp_med_swings_rsi_diff","zero_rand_neg_sp_max_swings_rsi_diff","zero_rand_neg_sp_avg_swings_rsi_diff","zero_rand_neg_sp_med_swings_rsi_diff","total_fb","total_pstv_fb","total_neg_fb"] 

layer_3_rank_2_col_names = [
    "coin_name", "coin_time_tf", "last_swing_per", "last_swing_rand_per", "last_swing_time",
    "last_swing_rsi_dif", "last_3_s_per_sum", "last_3_s_rand_sum", "last_3_s_avg_time",
    "last_3_s_rsi_diff_avg", "all_swing_count", "all_swings_pp_count", "all_swings_np_count",
    "all_swing_per_sum", "all_swings_pp_sum", "all_swings_np_sum", "t_10_lrg_pp_sp_sum",
    "t_10_lrg_np_sp_sum", "t_10_sml_pp_sp_sum", "t_10_sml_np_sp_sum", "sp_pp_cnt_0_2_lst",
    "sp_pp_cnt_2_4_lst", "sp_pp_cnt_4_7_lst", "sp_pp_cnt_7_15_lst", "sp_pp_cnt_15_25_lst",
    "sp_np_cnt_0_2_lst", "sp_np_cnt_2_4_lst", "sp_np_cnt_4_7_lst", "sp_np_cnt_7_15_lst",
    "sp_np_cnt_15_25_lst", "all_swing_rand_per_sum", "all_swings_rand_pp_sum",
    "all_swings_rand_np_sum", "t_10_lrg_pp_rand_sp_sum", "t_10_lrg_np_rand_sp_sum",
    "t_10_sml_pp_rand_sp_sum", "t_10_sml_np_rand_sp_sum", "all_swings_zero_rand_count",
    "all_swings_zero_rand_pp_count", "all_swings_zero_rand_np_count",
    "all_swings_zero_rand_pp_sum", "all_swings_zero_rand_np_sum", "all_swing_zero_rand_per_sum",
    "t_10_lrg_pp_zero_rand_sp_sum", "t_10_lrg_np_zero_rand_sp_sum",
    "t_10_sml_pp_zero_rand_sp_sum", "t_10_sml_np_zero_rand_sp_sum", "rand_pp_cnt_0_to_0_25_lst",
    "rand_pp_cnt_0_25_to_0_5_lst", "rand_pp_cnt_0_to_0_5_lst", "rand_pp_cnt_0_5_to_1_lst",
    "rand_pp_cnt_1_to_1_5_lst", "rand_pp_cnt_0_5_to_1_5_lst", "rand_pp_cnt_1_5_to_3_5_lst",
    "rand_pp_cnt_3_5_to_7_lst", "rand_pp_cnt_7_to_15_lst", "rand_np_cnt_0_to_0_25_lst",
    "rand_np_cnt_0_25_to_0_5_lst", "rand_np_cnt_0_to_0_5_lst", "rand_np_cnt_0_5_to_1_lst",
    "rand_np_cnt_1_to_1_5_lst", "rand_np_cnt_0_5_to_1_5_lst", "rand_np_cnt_1_5_to_3_5_lst",
    "rand_np_cnt_3_5_to_7_lst", "rand_np_cnt_7_to_15_lst", "all_swing_avg_time",
    "pstv_swing_avg_time", "neg_swing_avg_time", "top_10_lrg_pstv_total_rand_per_change",
    "top_10_lrg_pstv_avg_time", "top_10_sml_pstv_total_rand_per_change", "top_10_sml_pstv_avg_time",
    "top_10_lrg_neg_avg_time", "top_10_sml_neg_avg_time", "zero_rand_avg_swings_time",
    "zero_rand_pstv_sp_avg_swings_time", "zero_rand_neg_sp_avg_swings_time", "all_swing_avg_rsi_diff",
    "pstv_swing_avg_rsi_diff", "neg_swing_avg_rsi_diff", "top_10_lrg_pstv_avg_rsi_diff",
    "top_10_sml_pstv_avg_rsi_diff", "top_10_lrg_neg_avg_rsi_diff", "top_10_sml_neg_avg_rsi_diff",
    "zero_rand_avg_swings_rsi_diff", "zero_rand_pstv_sp_avg_swings_rsi_diff",
    "zero_rand_neg_sp_avg_swings_rsi_diff", "total_fb", "total_pstv_fb", "total_neg_fb"
]

layer_3_rank_3_col_names = [
    "coin_name", "coin_time_tf", "last_swing_per", "last_swing_rand_per", "last_swing_time",
    "last_swing_rsi_dif", "last_3_s_per_sum", "last_3_s_rand_avg", "last_3_s_avg_time",
    "last_3_s_rsi_diff_avg", "all_swing_count", "all_swings_pp_count", "all_swings_np_count",
    "all_swing_per_sum", "all_swings_pp_sum", "all_swings_np_sum", "t_10_lrg_pp_sp_sum",
    "t_10_lrg_np_sp_sum", "t_10_sml_pp_sp_sum", "t_10_sml_np_sp_sum", "sp_pp_cnt_0_2_lst",
    "sp_pp_cnt_2_4_lst", "sp_pp_cnt_4_7_lst", "sp_pp_cnt_7_15_lst", "sp_pp_cnt_15_25_lst",
    "sp_np_cnt_0_2_lst", "sp_np_cnt_2_4_lst", "sp_np_cnt_4_7_lst", "sp_np_cnt_7_15_lst",
    "sp_np_cnt_15_25_lst", "all_swings_rand_pp_avg", "all_swings_rand_np_avg",
    "t_10_lrg_pp_rand_sp_avg", "t_10_lrg_np_rand_sp_avg", "t_10_sml_pp_rand_sp_avg",
    "t_10_sml_np_rand_sp_avg", "all_swings_zero_rand_count", "all_swings_zero_rand_pp_count",
    "all_swings_zero_rand_np_count", "all_swings_zero_rand_pp_mean", "all_swings_zero_rand_np_mean",
    "t_10_lrg_pp_zero_rand_sp_avg", "t_10_lrg_np_zero_rand_sp_avg",
    "t_10_sml_pp_zero_rand_sp_avg", "t_10_sml_np_zero_rand_sp_avg", "rand_pp_cnt_0_to_0_25_lst",
    "rand_pp_cnt_0_25_to_0_5_lst", "rand_pp_cnt_0_to_0_5_lst", "rand_pp_cnt_0_5_to_1_lst",
    "rand_pp_cnt_1_to_1_5_lst", "rand_pp_cnt_0_5_to_1_5_lst", "rand_pp_cnt_1_5_to_3_5_lst",
    "rand_pp_cnt_3_5_to_7_lst", "rand_pp_cnt_7_to_15_lst", "rand_np_cnt_0_to_0_25_lst",
    "rand_np_cnt_0_25_to_0_5_lst", "rand_np_cnt_0_to_0_5_lst", "rand_np_cnt_0_5_to_1_lst",
    "rand_np_cnt_1_to_1_5_lst", "rand_np_cnt_0_5_to_1_5_lst", "rand_np_cnt_1_5_to_3_5_lst",
    "rand_np_cnt_3_5_to_7_lst", "rand_np_cnt_7_to_15_lst", "all_swing_avg_time",
    "pstv_swing_avg_time", "neg_swing_avg_time", "top_10_lrg_pstv_total_rand_per_change",
    "top_10_lrg_pstv_avg_time", "top_10_sml_pstv_total_rand_per_change", "top_10_sml_pstv_avg_time",
    "top_10_lrg_neg_avg_time", "top_10_sml_neg_avg_time", "zero_rand_avg_swings_time",
    "zero_rand_pstv_sp_avg_swings_time", "zero_rand_neg_sp_avg_swings_time", "all_swing_avg_rsi_diff",
    "pstv_swing_avg_rsi_diff", "neg_swing_avg_rsi_diff", "top_10_lrg_pstv_avg_rsi_diff",
    "top_10_sml_pstv_avg_rsi_diff", "top_10_lrg_neg_avg_rsi_diff", "top_10_sml_neg_avg_rsi_diff",
    "zero_rand_avg_swings_rsi_diff", "zero_rand_pstv_sp_avg_swings_rsi_diff",
    "zero_rand_neg_sp_avg_swings_rsi_diff", "total_fb", "total_pstv_fb", "total_neg_fb"
]

layer_3_rank_4_col_names = [
    "coin_name","coin_time_tf","last_swing_per","last_swing_rand_per","last_swing_time","last_swing_rsi_dif","last_3_s_per_avg","last_3_s_rand_avg","last_3_s_avg_time","last_3_s_rsi_diff_avg","all_swing_count","all_swings_pp_count","all_swings_np_count","all_swings_pp_avg","all_swings_np_avg","t_10_lrg_pp_sp_avg","t_10_lrg_np_sp_avg","t_10_sml_pp_sp_avg","t_10_sml_np_sp_avg","sp_pp_cnt_0_2_lst","sp_pp_cnt_2_4_lst","sp_pp_cnt_4_7_lst","sp_pp_cnt_7_15_lst","sp_pp_cnt_15_25_lst","sp_np_cnt_0_2_lst","sp_np_cnt_2_4_lst","sp_np_cnt_4_7_lst","sp_np_cnt_7_15_lst","sp_np_cnt_15_25_lst","all_swing_rand_per_sum","all_swings_rand_pp_sum","all_swings_rand_np_sum","t_10_lrg_pp_rand_sp_sum","t_10_lrg_np_rand_sp_sum","t_10_sml_pp_rand_sp_sum","t_10_sml_np_rand_sp_sum","all_swings_zero_rand_count","all_swings_zero_rand_pp_count","all_swings_zero_rand_np_count","all_swings_zero_rand_pp_sum","all_swings_zero_rand_np_sum","all_swing_zero_rand_per_sum","t_10_lrg_pp_zero_rand_sp_sum","t_10_lrg_np_zero_rand_sp_sum","t_10_sml_pp_zero_rand_sp_sum","t_10_sml_np_zero_rand_sp_sum","rand_pp_cnt_0_to_0_25_lst","rand_pp_cnt_0_25_to_0_5_lst","rand_pp_cnt_0_to_0_5_lst","rand_pp_cnt_0_5_to_1_lst","rand_pp_cnt_1_to_1_5_lst","rand_pp_cnt_0_5_to_1_5_lst","rand_pp_cnt_1_5_to_3_5_lst","rand_pp_cnt_3_5_to_7_lst","rand_pp_cnt_7_to_15_lst","rand_np_cnt_0_to_0_25_lst","rand_np_cnt_0_25_to_0_5_lst","rand_np_cnt_0_to_0_5_lst","rand_np_cnt_0_5_to_1_lst","rand_np_cnt_1_to_1_5_lst","rand_np_cnt_0_5_to_1_5_lst","rand_np_cnt_1_5_to_3_5_lst","rand_np_cnt_3_5_to_7_lst","rand_np_cnt_7_to_15_lst","all_swing_avg_time","pstv_swing_avg_time","neg_swing_avg_time","top_10_lrg_pstv_total_rand_per_change","top_10_lrg_pstv_avg_time","top_10_sml_pstv_total_rand_per_change","top_10_sml_pstv_avg_time","top_10_lrg_neg_avg_time","top_10_sml_neg_avg_time","zero_rand_avg_swings_time","zero_rand_pstv_sp_avg_swings_time","zero_rand_neg_sp_avg_swings_time","all_swing_avg_rsi_diff","pstv_swing_avg_rsi_diff","neg_swing_avg_rsi_diff","top_10_lrg_pstv_avg_rsi_diff","top_10_sml_pstv_avg_rsi_diff","top_10_lrg_neg_avg_rsi_diff","top_10_sml_neg_avg_rsi_diff","zero_rand_avg_swings_rsi_diff","zero_rand_pstv_sp_avg_rsi_diff","zero_rand_neg_sp_avg_swings_rsi_diff","total_fb","total_pstv_fb","total_neg_fb"
]

layer_3_rank_5_col_names = [
    "coin_name","coin_time_tf","last_swing_per","last_swing_rand_per","last_swing_time","last_swing_rsi_dif","last_3_s_per_avg","last_3_s_rand_avg","last_3_s_avg_time","last_3_s_rsi_diff_avg","all_swing_count","all_swings_pp_count","all_swings_np_count","all_swings_pp_avg","all_swings_np_avg","t_10_lrg_pp_sp_avg","t_10_lrg_np_sp_avg","t_10_sml_pp_sp_avg","t_10_sml_np_sp_avg","sp_pp_cnt_0_2_lst","sp_pp_cnt_2_4_lst","sp_pp_cnt_4_7_lst","sp_pp_cnt_7_15_lst","sp_pp_cnt_15_25_lst","sp_np_cnt_0_2_lst","sp_np_cnt_2_4_lst","sp_np_cnt_4_7_lst","sp_np_cnt_7_15_lst","sp_np_cnt_15_25_lst","all_swings_rand_pp_avg","all_swings_rand_np_avg","t_10_lrg_pp_rand_sp_avg","t_10_lrg_np_rand_sp_avg","t_10_sml_pp_rand_sp_avg","t_10_sml_np_rand_sp_avg","all_swings_zero_rand_count","all_swings_zero_rand_pp_count","all_swings_zero_rand_np_count","all_swings_zero_rand_pp_mean","all_swings_zero_rand_np_mean","t_10_lrg_pp_zero_rand_sp_avg","t_10_lrg_np_zero_rand_sp_avg","t_10_sml_pp_zero_rand_sp_avg","t_10_sml_np_zero_rand_sp_avg","rand_pp_cnt_0_to_0_25_lst","rand_pp_cnt_0_25_to_0_5_lst","rand_pp_cnt_0_to_0_5_lst","rand_pp_cnt_0_5_to_1_lst","rand_pp_cnt_1_to_1_5_lst","rand_pp_cnt_0_5_to_1_5_lst","rand_pp_cnt_1_5_to_3_5_lst","rand_pp_cnt_3_5_to_7_lst","rand_pp_cnt_7_to_15_lst","rand_np_cnt_0_to_0_25_lst","rand_np_cnt_0_25_to_0_5_lst","rand_np_cnt_0_to_0_5_lst","rand_np_cnt_0_5_to_1_lst","rand_np_cnt_1_to_1_5_lst","rand_np_cnt_0_5_to_1_5_lst","rand_np_cnt_1_5_to_3_5_lst","rand_np_cnt_3_5_to_7_lst","rand_np_cnt_7_to_15_lst","all_swing_avg_time","pstv_swing_avg_time","neg_swing_avg_time","top_10_lrg_pstv_total_rand_per_change","top_10_lrg_pstv_avg_time","top_10_sml_pstv_total_rand_per_change","top_10_sml_pstv_avg_time","top_10_lrg_neg_avg_time","top_10_sml_neg_avg_time","zero_rand_avg_swings_time","zero_rand_pstv_sp_avg_swings_time","zero_rand_neg_sp_avg_swings_time","all_swing_avg_rsi_diff","pstv_swing_avg_rsi_diff","neg_swing_avg_rsi_diff","top_10_lrg_pstv_avg_rsi_diff","top_10_sml_pstv_avg_rsi_diff","top_10_lrg_neg_avg_rsi_diff","top_10_sml_neg_avg_rsi_diff","zero_rand_avg_swings_rsi_diff","zero_rand_pstv_sp_avg_rsi_diff","zero_rand_neg_sp_avg_swings_rsi_diff","total_fb","total_pstv_fb","total_neg_fb"]

layer_3_rank_6_col_names = [
    "coin_name","coin_time_tf","last_swing_per","last_swing_rand_per","last_swing_time","last_swing_rsi_dif","last_3_s_per_avg","last_3_s_rand_avg","last_3_s_avg_time","last_3_s_rsi_diff_avg","all_swing_count","all_swings_pp_count","all_swings_np_count","all_swings_pp_med","all_swings_np_med","t_10_lrg_pp_sp_med","t_10_lrg_np_sp_med","t_10_sml_pp_sp_med","t_10_sml_np_sp_med","sp_pp_cnt_0_2_lst","sp_pp_cnt_2_4_lst","sp_pp_cnt_4_7_lst","sp_pp_cnt_7_15_lst","sp_pp_cnt_15_25_lst","sp_np_cnt_0_2_lst","sp_np_cnt_2_4_lst","sp_np_cnt_4_7_lst","sp_np_cnt_7_15_lst","sp_np_cnt_15_25_lst","all_swings_rand_pp_med","all_swings_rand_np_med","t_10_lrg_pp_rand_sp_med","t_10_lrg_np_rand_sp_med","t_10_sml_pp_rand_sp_med","t_10_sml_np_rand_sp_med","all_swings_zero_rand_count","all_swings_zero_rand_pp_count","all_swings_zero_rand_np_count","all_swings_zero_rand_pp_med","all_swings_zero_rand_np_med","t_10_lrg_pp_zero_rand_sp_med","t_10_lrg_np_zero_rand_sp_med","t_10_sml_pp_zero_rand_sp_med","t_10_sml_np_zero_rand_sp_med","rand_pp_cnt_0_to_0_25_lst","rand_pp_cnt_0_25_to_0_5_lst","rand_pp_cnt_0_to_0_5_lst","rand_pp_cnt_0_5_to_1_lst","rand_pp_cnt_1_to_1_5_lst","rand_pp_cnt_0_5_to_1_5_lst","rand_pp_cnt_1_5_to_3_5_lst","rand_pp_cnt_3_5_to_7_lst","rand_pp_cnt_7_to_15_lst","rand_np_cnt_0_to_0_25_lst","rand_np_cnt_0_25_to_0_5_lst","rand_np_cnt_0_to_0_5_lst","rand_np_cnt_0_5_to_1_lst","rand_np_cnt_1_to_1_5_lst","rand_np_cnt_0_5_to_1_5_lst","rand_np_cnt_1_5_to_3_5_lst","rand_np_cnt_3_5_to_7_lst","rand_np_cnt_7_to_15_lst","all_swing_median_time","pstv_swing_median_time","neg_swing_median_time","top_10_lrg_pstv_total_rand_per_change","top_10_lrg_pstv_median_time","top_10_sml_pstv_total_rand_per_change","top_10_sml_pstv_median_time","top_10_lrg_neg_median_time","top_10_sml_neg_median_time","zero_rand_med_swings_time","zero_rand_pstv_sp_med_swings_time","zero_rand_neg_sp_med_swings_time","all_swing_median_rsi_diff","pstv_swing_median_rsi_diff","neg_swing_median_rsi_diff","top_10_sml_pstv_median_rsi_diff","top_10_lrg_neg_median_rsi_diff","top_10_sml_neg_median_rsi_diff","zero_rand_med_swings_rsi_diff","zero_rand_pstv_sp_med_swings_rsi_diff","zero_rand_neg_sp_med_swings_rsi_diff","total_fb","total_pstv_fb","total_neg_fb"]

binance_coins = [
    "REEFUSDT.P","MOODENGUSDT.P","1000APUUSDT.P","PENGUSDT.P","PIXFIUSDT.P","MOTHERUSDT.P","NEIROETHUSDT.P","PIRATEUSDT.P","1000000BABYDOGEUSDT.P","SILLYUSDT.P","1000CATSUSDT.P","CETUSUSDT.P","IOTXUSDT.P","1000BEERUSDT.P","DOGUSDT.P","ZBCNUSDT.P","LAIUSDT.P","CATIUSDT.P","1000TURBOUSDT.P","MOCAUSDT.P","FIDAUSDT.P","BNXUSDT.P","PRCLUSDT.P","EIGENUSDT.P","ALTUSDT.P","BLURUSDT.P","1000000MOGUSDT.P","MYRIAUSDT.P","VELOUSDT.P","10000WENUSDT.P","PRIMEUSDT.P","SUNUSDT.P","L3USDT.P","1CATUSDT.P","CFXUSDT.P","WUSDT.P","10000COQUSDT.P","1000MUMUUSDT.P","1000RATSUSDT.P","AGIUSDT.P","ARKUSDT.P","LISTAUSDT.P","YGGUSDT.P","VANRYUSDT.P","PHBUSDT.P","ALPACAUSDT.P","SEIUSDT.P","FIOUSDT.P","SXPUSDT.P","AIUSDT.P","COREUSDT.P","DEGENUSDT.P","GASUSDT.P","HIFIUSDT.P","10000000AIDOGEUSDT.P","10000SATSUSDT.P","WIFUSDT.P","BANANAUSDT.P","CELOUSDT.P","IMXUSDT.P","PORTALUSDT.P","ROSEUSDT.P","ZKFUSDT.P","MINAUSDT.P","UMAUSDT.P","KASUSDT.P","ZKUSDT.P","CVXUSDT.P","PIXELUSDT.P","SPELLUSDT.P","TIAUSDT.P","FOXYUSDT.P","GLMUSDT.P","XAIUSDT.P","MBOXUSDT.P","TRBUSDT.P","LQTYUSDT.P","STRKUSDT.P","TAIKOUSDT.P","AVAILUSDT.P","POPCATUSDT.P","ORBSUSDT.P","ATHUSDT.P","IDUSDT.P","XNOUSDT.P","QNTUSDT.P","SUIUSDT.P","UNFIUSDT.P","CTKUSDT.P","BSWUSDT.P","1000LUNCUSDT.P","LPTUSDT.P","NEARUSDT.P","XCHUSDT.P","XEMUSDT.P","AEROUSDT.P","KEYUSDT.P","ACEUSDT.P","1000PEPEUSDT.P","ORDIUSDT.P","JOEUSDT.P","TOKENUSDT.P","QUICKUSDT.P","STGUSDT.P","CVCUSDT.P","GODSUSDT.P","PYTHUSDT.P","NTRNUSDT.P","KAVAUSDT.P","1000000PEIPEIUSDT.P","ARUSDT.P","ILVUSDT.P","SAGAUSDT.P","SSVUSDT.P","WAXPUSDT.P","RIFUSDT.P","LDOUSDT.P","JUPUSDT.P","BONDUSDT.P","API3USDT.P","HOOKUSDT.P","AXLUSDT.P","NFPUSDT.P","OMUSDT.P","SPECUSDT.P","STXUSDT.P","ICXUSDT.P","ONDOUSDT.P","PENDLEUSDT.P","AMBUSDT.P","SUSHIUSDT.P","LUNA2USDT.P","MASKUSDT.P","MAVIAUSDT.P","OPUSDT.P","DYMUSDT.P","ZROUSDT.P","FITFIUSDT.P","HNTUSDT.P","JSTUSDT.P","PYRUSDT.P","RONUSDT.P","SNXUSDT.P","RVNUSDT.P","DRIFTUSDT.P","NYANUSDT.P","ARKMUSDT.P","MAVUSDT.P","FLUXUSDT.P","LINAUSDT.P","MAXUSDT.P","SHIB1000USDT.P","WLDUSDT.P","MDTUSDT.P","VOXELUSDT.P","MONUSDT.P","RENDERUSDT.P","TRUUSDT.P","THETAUSDT.P","BANDUSDT.P","INJUSDT.P","MKRUSDT.P","AEVOUSDC.P","OSMOUSDT.P","DATAUSDT.P","GRTUSDT.P","SCRTUSDT.P","STPTUSDT.P","RAREUSDT.P","AUCTIONUSDT.P","MTLUSDT.P","FXSUSDT.P","FIREUSDT.P","DUSKUSDT.P","SCAUSDT.P","FUNUSDT.P","NMRUSDT.P","XTZUSDT.P","CAKEUSDT.P","AVAXUSDT.P","CKBUSDT.P","MNTUSDT.P","MOBILEUSDT.P","CTSIUSDT.P","RDNTUSDT.P","ZENUSDT.P","QTUMUSDT.P","SOLUSDT.P","AKTUSDT.P","SCUSDT.P","AKROUSDT.P","IOUSDT.P","KNCUSDT.P","PEOPLEUSDT.P","TNSRUSDT.P","EOSUSDT.P","NKNUSDT.P","CRVUSDT.P","WAVESUSDT.P","XVSUSDT.P","BADGERUSDT.P","LRCUSDT.P","SNTUSDT.P","BLASTUSDT.P","MANTAUSDT.P","KSMUSDT.P","ANKRUSDT.P","BTCUSDT.P","GMTUSDT.P","LSKUSDT.P","RLCUSDT.P","ALGOUSDT.P","CHESSUSDT.P","ATAUSDT.P","GLMRUSDT.P","LITUSDT.P","SANDUSDT.P","ZETAUSDT.P","COTIUSDT.P","EGLDUSDT.P","ARPAUSDT.P","ACHUSDT.P","MAGICUSDT.P","ADAUSDT.P","BELUSDT.P","DODOUSDT.P","APEUSDT.P","FLOWUSDT.P","SUPERUSDT.P","RPLUSDT.P","10000LADYSUSDT.P","ARBUSDT.P","BOBAUSDT.P","LEVERUSDT.P","LOOKSUSDT.P","MANAUSDT.P","REQUSDT.P","ZRXUSDT.P","AXSUSDT.P","ENJUSDT.P","JASMYUSDT.P","TLMUSDT.P","BAKEUSDT.P","FTMUSDT.P","GFTUSDT.P","TONUSDT.P","ETCUSDT.P","KLAYUSDT.P","ASTRUSDT.P","SUNDOGUSDT.P","COMPUSDT.P","FLMUSDT.P","STEEMUSDT.P","BIGTIMEUSDT.P","HFTUSDT.P","AUDIOUSDT.P","TRXUSDT.P","BSVUSDT.P","C98USDT.P","ICPUSDT.P","TAOUSDT.P","JTOUSDT.P","OXTUSDT.P","ALICEUSDT.P","ORCAUSDT.P","MBLUSDT.P","DASHUSDT.P","IDEXUSDT.P","MASAUSDT.P","AERGOUSDT.P","SAFEUSDT.P","XMRUSDT.P","ETHUSDT.P","1000FLOKIUSDT.P","YFIUSDT.P","BNTUSDT.P","MEMEUSDT.P","SLFUSDT.P","ETHFIUSDT.P","PERPUSDT.P","GALAUSDT.P","SYSUSDT.P","1000CATUSDT.P","ATOMUSDT.P","BNBUSDT.P","FORTHUSDT.P","BRETTUSDT.P","RADUSDT.P","FILUSDT.P","PHAUSDT.P","PROMUSDT.P","NULSUSDT.P","PONKEUSDT.P","SKLUSDT.P","GTCUSDT.P","CELRUSDT.P","IOSTUSDT.P","EDUUSDT.P","IOTAUSDT.P","HMSTRUSDT.P","XCNUSDT.P","1000BONKUSDT.P","DGBUSDT.P","UNIUSDT.P","VTHOUSDT.P","XLMUSDT.P","BALUSDT.P","POLUSDT.P","CYBERUSDT.P","TOMIUSDT.P","COMBOUSDT.P","1INCHUSDT.P","DOP1USDT.P","BICOUSDT.P","AAVEUSDT.P","DEXEUSDT.P","FTNUSDT.P","XRDUSDT.P","XRPUSDT.P","FLRUSDT.P","ZKJUSDT.P","DOGEUSDT.P","BATUSDT.P","PAXGUSDT.P","LTCUSDT.P","NOTUSDT.P","ZILUSDT.P","GNOUSDT.P","FDUSDUSDT.P","USDEUSDT.P","USDCUSDT.P","DOTUSDT.P","MEWUSDT.P","ORDERUSDT.P","VRAUSDT.P","WOOUSDT.P","ALEOUSDT.P","ENAUSDT.P","GOMININGUSDT.P","RUNEUSDT.P","1000BTTUSDT.P","COSUSDT.P","BLZUSDT.P","SYNUSDT.P","BCHUSDT.P","SFPUSDT.P","DENTUSDT.P","SWEATUSDT.P","METISUSDT.P","AIOZUSDT.P","APTUSDT.P","KMNOUSDT.P","STMXUSDT.P","GMXUSDT.P","DARUSDT.P","AGLDUSDT.P","MYROUSDT.P","VETUSDT.P","DYDXUSDT.P","OGNUSDT.P","ONEUSDT.P","LINKUSDT.P","ORNUSDT.P","RSRUSDT.P","UXLINKUSDT.P","HBARUSDT.P","RENUSDT.P","MANEKIUSDT.P","10000WHYUSDT.P","CTCUSDT.P","GUSDT.P","ZECUSDT.P","1000NEIROCTOUSDT.P","OGUSDT.P","1000XECUSDT.P","GMEUSDT.P","FBUSDT.P","DOGSUSDT.P","CHZUSDT.P","BENDOGUSDT.P","BOMEUSDT.P","SLERFUSDT.P"]