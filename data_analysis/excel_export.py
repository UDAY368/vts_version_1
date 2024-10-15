from datetime import datetime, timezone, timedelta
import os
import pandas as pd
from pandas import DataFrame


def number_to_excel_column(column_int):
    start_index = 1
    column_in_letters = ''
    while column_int > 25 + start_index:
        column_in_letters += chr(65 + int((column_int - start_index)/26) - 1)
        column_int = column_int - (int((column_int - start_index)/26)) * 26
    column_in_letters += chr(65 - start_index + (int(column_int)))
    return column_in_letters


def layer_1_2_excel_export(layer_1_data, fb_excel_lst, output_excel_folder_path, Choose_Time_Frame, swing_per_analysis_lst, swing_pstv_per_range_lst, swing_neg_per_range_lst, swing_rand_per_analysis_lst, swing_zero_rand_per_analysis_lst, swing_rand_pstv_per_range_lst, swing_rand_neg_per_range_lst, swing_time_analysis_lst, swing_rsi_diff_analysis_lst, swing_fb_analysis_lst):
    if not os.path.exists(output_excel_folder_path):
        os.makedirs(output_excel_folder_path)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    if Choose_Time_Frame == 1:
        extracted_excel_file_name = f"layer_1_data_excel_1TF_{timestamp}.xlsx"
    elif Choose_Time_Frame == 2:
        extracted_excel_file_name = f"crypto_coin_data_analysis_{timestamp}.xlsx"
    elif Choose_Time_Frame == 5:
        extracted_excel_file_name = f"layer_1_data_excel_5TF_{timestamp}.xlsx"
    else:
        return {"Status": "Please Select Valid Time frame Either 1 or 5"}
    extracted_excel_file_path = os.path.join(
        output_excel_folder_path, extracted_excel_file_name)

    # Column Names
    layer_1_col_names = ["coin_name", "coin_tf", "swing_1_col", "swing_2_col", "swing_dir", "swing_per", "swing_rand_per",
                         "swing_time(H)", "swing_candles", "swing_1_RSI", "swing_2_RSI", "swing_rsi_diff", "swing_1_ISO_time", "swing_2_ISO_time"]

    fb_col_name = ["coin_name", "coin_tf", "row_num", "fb_pos", "fb_iso_time"]

    swing_fb_analysis_lst_col_names = [
        "coin_name", "coin_time_tf", "total_fb", "total_pstv_fb", "total_neg_fb", "last_fb_time"]

    swing_per_analysis_lst_col_names = [
        "coin_name", "coin_time_tf", "all_swing_count", "all_swings_pp_count", "all_swings_np_count", "all_swing_per_sum",
        "all_swings_pp_sum", "all_swings_np_sum", "all_swings_pp_avg", "all_swings_np_avg", "all_swings_pp_med",
        "all_swings_np_med", "t_5_lrg_pp_sp_lst", "t_5_lrg_np_sp_lst", "t_10_lrg_pp_sp_sum", "t_10_lrg_np_sp_sum",
        "t_10_lrg_pp_sp_avg", "t_10_lrg_np_sp_avg", "t_10_lrg_pp_sp_med", "t_10_lrg_np_sp_med", "t_10_sml_pp_sp_sum",
        "t_10_sml_np_sp_sum", "t_10_sml_pp_sp_avg", "t_10_sml_np_sp_avg", "t_10_sml_pp_sp_med", "t_10_sml_np_sp_med"
    ]
    swing_pstv_per_range_lst_col_names = [
        "coin_name", "coin_time_tf", "sp_pp_cnt_0_1_lst", "sp_pp_cnt_1_2_lst", "sp_pp_cnt_0_2_lst", "sp_pp_cnt_2_3_lst",
        "sp_pp_cnt_3_4_lst", "sp_pp_cnt_2_4_lst", "sp_pp_cnt_4_5_lst", "sp_pp_cnt_5_6_lst", "sp_pp_cnt_6_7_lst",
        "sp_pp_cnt_4_7_lst", "sp_pp_cnt_7_9_lst", "sp_pp_cnt_9_11_lst", "sp_pp_cnt_11_13_lst", "sp_pp_cnt_13_15_lst",
        "sp_pp_cnt_7_15_lst", "sp_pp_cnt_15_18_lst", "sp_pp_cnt_18_22_lst", "sp_pp_cnt_22_25_lst", "sp_pp_cnt_15_25_lst",
        "sp_pp_cnt_25_plus_lst", "t_3_sp_pp_ranges"
    ]
    swing_neg_per_range_lst_col_names = [
        "coin_name", "coin_time_tf", "sp_np_cnt_0_1_lst", "sp_np_cnt_1_2_lst", "sp_np_cnt_0_2_lst", "sp_np_cnt_2_3_lst",
        "sp_np_cnt_3_4_lst", "sp_np_cnt_2_4_lst", "sp_np_cnt_4_5_lst", "sp_np_cnt_5_6_lst", "sp_np_cnt_6_7_lst",
        "sp_np_cnt_4_7_lst", "sp_np_cnt_7_9_lst", "sp_np_cnt_9_11_lst", "sp_np_cnt_11_13_lst", "sp_np_cnt_13_15_lst",
        "sp_np_cnt_7_15_lst", "sp_np_cnt_15_18_lst", "sp_np_cnt_18_22_lst", "sp_np_cnt_22_25_lst", "sp_np_cnt_15_25_lst",
        "sp_np_cnt_25_plus_lst", "t_3_sp_np_ranges"
    ]

    swing_rand_per_analysis_lst_col_names = ["coin_name", "coin_time_tf", "all_swing_rand_count", "all_swings_rand_pp_count", "all_swings_rand_np_count", "all_swing_rand_per_sum", "all_swings_rand_pp_sum", "all_swings_rand_np_sum", "all_swings_rand_pp_avg", "all_swings_rand_np_avg", "all_swings_rand_pp_med", "all_swings_rand_np_med", "t_5_lrg_pp_rand_sp_lst",
                                             "t_5_lrg_np_rand_sp_lst", "t_10_lrg_pp_rand_sp_sum", "t_10_lrg_np_rand_sp_sum", "t_10_lrg_pp_rand_sp_avg", "t_10_lrg_np_rand_sp_avg", "t_10_lrg_pp_rand_sp_med", "t_10_lrg_np_rand_sp_med", "t_10_sml_pp_rand_sp_sum", "t_10_sml_np_rand_sp_sum", "t_10_sml_pp_rand_sp_avg", "t_10_sml_np_rand_sp_avg", "t_10_sml_pp_rand_sp_med", "t_10_sml_np_rand_sp_med"]

    swing_zero_rand_per_analysis_lst_col_names = ["coin_name", "coin_time_tf", "all_swings_zero_rand_count", "all_swings_zero_rand_pp_count", "all_swings_zero_rand_np_count", "all_swings_zero_rand_pp_sum", "all_swings_zero_rand_np_sum", "all_swing_zero_rand_per_sum", "all_swings_zero_rand_pp_mean", "all_swings_zero_rand_np_mean", "all_swings_zero_rand_pp_med", "all_swings_zero_rand_np_med", "t_5_lrg_pp_zero_rand_sp_lst",
                                                  "t_5_lrg_np_zero_rand_sp_lst", "t_10_lrg_pp_zero_rand_sp_sum", "t_10_lrg_np_zero_rand_sp_sum", "t_10_lrg_pp_zero_rand_sp_avg", "t_10_lrg_np_zero_rand_sp_avg", "t_10_lrg_pp_zero_rand_sp_med", "t_10_lrg_np_zero_rand_sp_med", "t_10_sml_pp_zero_rand_sp_sum", "t_10_sml_np_zero_rand_sp_sum", "t_10_sml_pp_zero_rand_sp_avg", "t_10_sml_np_zero_rand_sp_avg", "t_10_sml_pp_zero_rand_sp_med", "t_10_sml_np_zero_rand_sp_med"]

    swing_rand_pstv_per_range_lst_col_names = ["coin_name", "coin_time_tf", "rand_pp_cnt_0_to_0_25_lst", "rand_pp_cnt_0_25_to_0_5_lst", "rand_pp_cnt_0_to_0_5_lst", "rand_pp_cnt_0_5_to_1_lst", "rand_pp_cnt_1_to_1_5_lst", "rand_pp_cnt_0_5_to_1_5_lst", "rand_pp_cnt_1_5_to_2_lst", "rand_pp_cnt_2_to_2_5_lst", "rand_pp_cnt_2_5_to_3_5_lst",
                                               "rand_pp_cnt_1_5_to_3_5_lst", "rand_pp_cnt_3_5_to_4_5_lst", "rand_pp_cnt_4_5_to_5_5_lst", "rand_pp_cnt_5_5_to_7_lst", "rand_pp_cnt_3_5_to_7_lst", "rand_pp_cnt_7_to_9_lst", "rand_pp_cnt_9_to_12_lst", "rand_pp_cnt_12_to_15_lst", "rand_pp_cnt_7_to_15_lst", "rand_pp_cnt_15_plus_lst", "t_3_rand_pp_ranges"]

    swing_rand_neg_per_range_lst_col_names = ["coin_name", "coin_time_tf", "rand_np_cnt_0_to_0_25_lst", "rand_np_cnt_0_25_to_0_5_lst", "rand_np_cnt_0_to_0_5_lst", "rand_np_cnt_0_5_to_1_lst", "rand_np_cnt_1_to_1_5_lst", "rand_np_cnt_0_5_to_1_5_lst", "rand_np_cnt_1_5_to_2_lst", "rand_np_cnt_2_to_2_5_lst", "rand_np_cnt_2_5_to_3_5_lst",
                                              "rand_np_cnt_1_5_to_3_5_lst", "rand_np_cnt_3_5_to_4_5_lst", "rand_np_cnt_4_5_to_5_5_lst", "rand_np_cnt_5_5_to_7_lst", "rand_np_cnt_3_5_to_7_lst", "rand_np_cnt_7_to_9_lst", "rand_np_cnt_9_to_12_lst", "rand_np_cnt_12_to_15_lst", "rand_np_cnt_7_to_15_lst", "rand_np_cnt_15_plus_lst", "t_3_rand_np_ranges"]

    swing_time_analysis_lst_col_names = ["coin_name", "coin_time_tf", "sum_all_s_time", "all_swing_max_time", "all_swing_min_time", "all_swing_avg_time", "all_swing_median_time", "total_pstv_s_time", "pstv_swing_max_time", "pstv_swing_min_time", "pstv_swing_avg_time", "pstv_swing_median_time", "total_neg_s_time", "neg_swing_max_time", "neg_swing_min_time", "neg_swing_avg_time", "neg_swing_median_time", "top_10_lrg_pstv_total_per", "top_10_lrg_pstv_total_rand_per", "top_10_lrg_pstv_total_s_time", "top_10_lrg_pstv_max_time", "top_10_lrg_pstv_min_time", "top_10_lrg_pstv_avg_time", "top_10_lrg_pstv_median_time", "t_5_lrg_pstv_sp_time", "top_10_sml_pstv_total_per", "top_10_sml_pstv_total_rand_per", "top_10_sml_pstv_total_s_time", "top_10_sml_pstv_max_time", "top_10_sml_pstv_min_time", "top_10_sml_pstv_avg_time", "top_10_sml_pstv_median_time", "top_10_lrg_neg_total_per", "top_10_lrg_neg_total_rand_per",
                                         "top_10_lrg_neg_total_s_time", "top_10_lrg_neg_max_time", "top_10_lrg_neg_min_time", "top_10_lrg_neg_avg_time", "top_10_lrg_neg_median_time", "t_5_lrg_neg_sp_time", "top_10_sml_neg_total_per", "top_10_sml_neg_total_rand_per", "top_10_sml_neg_total_s_time", "top_10_sml_neg_max_time", "top_10_sml_neg_min_time", "top_10_sml_neg_avg_time", "top_10_sml_neg_median_time", "zero_rand_total_s_time", "zero_rand_max_s_time", "zero_rand_min_s_time", "zero_rand_avg_s_time", "zero_rand_med_s_time", "zero_rand_pstv_sp_total_s_time", "zero_rand_pstv_sp_total_s_per", "zero_rand_pstv_sp_max_s_time", "zero_rand_pstv_sp_min_s_time", "zero_rand_pstv_sp_avg_s_time", "zero_rand_pstv_sp_med_s_time", "zero_rand_neg_sp_total_s_time", "zero_rand_neg_sp_total_s_per", "zero_rand_neg_sp_max_s_time", "zero_rand_neg_sp_min_s_time", "zero_rand_neg_sp_avg_s_time", "zero_rand_neg_sp_med_s_time"]

    swing_rsi_diff_analysis_lst_col_names = ["coin_name", "coin_time_tf", "sum_all_s_rsi_df", "all_swing_max_rsi_df", "all_swing_min_rsi_df", "all_swing_avg_rsi_df", "all_swing_median_rsi_df", "total_pstv_s_rsi_df", "pstv_swing_max_rsi_df", "pstv_swing_min_rsi_df", "pstv_swing_avg_rsi_df", "pstv_swing_median_rsi_df", "total_neg_s_rsi_df", "neg_swing_max_rsi_df", "neg_swing_min_rsi_df", "neg_swing_avg_rsi_df", "neg_swing_median_rsi_df", "top_10_lrg_pstv_total_per", "top_10_lrg_pstv_total_rand_per", "top_10_lrg_pstv_total_s_rsi_df", "top_10_lrg_pstv_max_rsi_df", "top_10_lrg_pstv_min_rsi_df", "top_10_lrg_pstv_avg_rsi_df", "top_10_lrg_pstv_median_rsi_df", "t_5_lrg_pstv_sp_rsi_df", "top_10_sml_pstv_total_per", "top_10_sml_pstv_total_rand_per", "top_10_sml_pstv_total_s_rsi_df", "top_10_sml_pstv_max_rsi_df", "top_10_sml_pstv_min_rsi_df", "top_10_sml_pstv_avg_rsi_df", "top_10_sml_pstv_median_rsi_df", "top_10_lrg_neg_total_per",
                                             "top_10_lrg_neg_total_rand_per", "top_10_lrg_neg_total_s_rsi_df", "top_10_lrg_neg_max_rsi_df", "top_10_lrg_neg_min_rsi_df", "top_10_lrg_neg_avg_rsi_df", "top_10_lrg_neg_median_rsi_df", "t_5_lrg_neg_sp_rsi_df", "top_10_sml_neg_total_per", "top_10_sml_neg_total_rand_per", "top_10_sml_neg_total_s_rsi_df", "top_10_sml_neg_max_rsi_df", "top_10_sml_neg_min_rsi_df", "top_10_sml_neg_avg_rsi_df", "top_10_sml_neg_median_rsi_df", "zero_rand_total_s_rsi_df", "zero_rand_max_s_rsi_df", "zero_rand_min_s_rsi_df", "zero_rand_avg_s_rsi_df", "zero_rand_med_s_rsi_df", "zero_rnd_pstv_sp_tol_s_rsi_df", "zero_rand_pstv_sp_total_s_per", "zero_rand_pstv_sp_max_s_rsi_df", "zero_rand_pstv_sp_min_s_rsi_df", "zero_rand_pstv_sp_avg_s_rsi_df", "zero_rand_pstv_sp_med_s_rsi_df", "zero_rand_neg_sp_tol_s_rsi_df", "zero_rand_neg_sp_total_s_per", "zero_rand_neg_sp_max_s_rsi_df", "zero_rand_neg_sp_min_s_rsi_df", "zero_rand_neg_sp_avg_s_rsi_df", "zero_rand_neg_sp_med_s_rsi_df"]

    # Data Frame formations
    layer_1_records = [item for sublist in layer_1_data for item in sublist]
    layer_1_df = pd.DataFrame(layer_1_records, columns=layer_1_col_names)

    fb_records = [item for sublist in fb_excel_lst for item in sublist]
    fb_df = pd.DataFrame(fb_records, columns=fb_col_name)

    swing_fb_analysis_lst_records = [
        sublist for sublist in swing_fb_analysis_lst]
    swing_fb_analysis_lst_records_df = pd.DataFrame(
        swing_fb_analysis_lst_records, columns=swing_fb_analysis_lst_col_names)

    swing_per_analysis_lst_records = [
        sublist for sublist in swing_per_analysis_lst]
    swing_per_analysis_lst_records_df = pd.DataFrame(
        swing_per_analysis_lst_records, columns=swing_per_analysis_lst_col_names)

    swing_pstv_per_range_lst_records = [
        sublist for sublist in swing_pstv_per_range_lst]
    swing_pstv_per_range_lst_records_df = pd.DataFrame(
        swing_pstv_per_range_lst_records, columns=swing_pstv_per_range_lst_col_names)

    swing_neg_per_range_lst_records = [
        sublist for sublist in swing_neg_per_range_lst]
    swing_neg_per_range_lst_records_df = pd.DataFrame(
        swing_neg_per_range_lst_records, columns=swing_neg_per_range_lst_col_names)

    swing_rand_per_analysis_lst_records = [
        sublist for sublist in swing_rand_per_analysis_lst]
    swing_rand_per_analysis_lst_records_df = pd.DataFrame(
        swing_rand_per_analysis_lst_records, columns=swing_rand_per_analysis_lst_col_names)

    swing_zero_rand_per_analysis_lst_records = [
        sublist for sublist in swing_zero_rand_per_analysis_lst]
    swing_zero_rand_per_analysis_lst_records_df = pd.DataFrame(
        swing_zero_rand_per_analysis_lst_records, columns=swing_zero_rand_per_analysis_lst_col_names)

    swing_rand_pstv_per_range_lst_records = [
        sublist for sublist in swing_rand_pstv_per_range_lst]
    swing_rand_pstv_per_range_lst_records_df = pd.DataFrame(
        swing_rand_pstv_per_range_lst_records, columns=swing_rand_pstv_per_range_lst_col_names)

    swing_rand_neg_per_range_lst_records = [
        sublist for sublist in swing_rand_neg_per_range_lst]
    swing_rand_neg_per_range_lst_records_df = pd.DataFrame(
        swing_rand_neg_per_range_lst_records, columns=swing_rand_neg_per_range_lst_col_names)

    swing_time_analysis_lst_records = [
        sublist for sublist in swing_time_analysis_lst]
    swing_time_analysis_lst_records_df = pd.DataFrame(
        swing_time_analysis_lst_records, columns=swing_time_analysis_lst_col_names)

    swing_rsi_diff_analysis_lst_records = [
        sublist for sublist in swing_rsi_diff_analysis_lst]
    swing_rsi_diff_analysis_lst_records_df = pd.DataFrame(
        swing_rsi_diff_analysis_lst_records, columns=swing_rsi_diff_analysis_lst_col_names)

    # Sheet Names
    dfs = {"layer_1_data": layer_1_df, "fb_data": fb_df,
           "swing_fb_analysis_lst": swing_fb_analysis_lst_records_df, "swing_per_analysis_lst": swing_per_analysis_lst_records_df, "swing_pstv_per_range_lst": swing_pstv_per_range_lst_records_df, "swing_neg_per_range_lst": swing_neg_per_range_lst_records_df, "swing_rand_per_analysis_lst": swing_rand_per_analysis_lst_records_df, "swing_zero_rand_per_info_lst": swing_zero_rand_per_analysis_lst_records_df, "swing_rand_pstv_per_range_lst": swing_rand_pstv_per_range_lst_records_df, "swing_rand_neg_per_range_lst": swing_rand_neg_per_range_lst_records_df, "swing_time_analysis_lst": swing_time_analysis_lst_records_df, "swing_rsi_diff_analysis_lst": swing_rsi_diff_analysis_lst_records_df}

    with pd.ExcelWriter(extracted_excel_file_path, engine='openpyxl') as writer:
        for sheet_name, df in dfs.items():
            if sheet_name == "layer_1_data":
                df.to_excel(writer, sheet_name=sheet_name, index=False,
                            header=["coin_name", "coin_tf", "swing_1_col", "swing_2_col", "swing_dir", "swing_per", "swing_rand_per",
                                    "swing_time(H)", "swing_candles", "swing_1_RSI", "swing_2_RSI", "swing_rsi_diff", "swing_1_ISO_time", "swing_2_ISO_time"],
                            engine='openpyxl')
                worksheet = writer.sheets[sheet_name]
                for idx, col in enumerate(df):
                    series = df[col]
                    max_len = max((series.astype(str).map(
                        len).max(), len(str(series.name)))) + 5
                    worksheet.column_dimensions[number_to_excel_column(
                        idx + 1)].width = min(max_len, 60)

            elif sheet_name == "fb_data":
                df.to_excel(writer, sheet_name=sheet_name, index=False,
                            header=["coin_name", "coin_tf",
                                    "row_num", "fb_pos", "fb_iso_time"],
                            engine='openpyxl')
                worksheet = writer.sheets[sheet_name]
                for idx, col in enumerate(df):
                    series = df[col]
                    max_len = max((series.astype(str).map(
                        len).max(), len(str(series.name)))) + 5
                    worksheet.column_dimensions[number_to_excel_column(
                        idx + 1)].width = min(max_len, 60)
            elif sheet_name == "swing_fb_analysis_lst":
                df.to_excel(writer, sheet_name=sheet_name, index=False,
                            header=["coin_name", "coin_time_tf", "total_fb",
                                    "total_pstv_fb", "total_neg_fb", "last_fb_time"],
                            engine='openpyxl')
                worksheet = writer.sheets[sheet_name]
                for idx, col in enumerate(df):
                    series = df[col]
                    max_len = max((series.astype(str).map(
                        len).max(), len(str(series.name)))) + 5
                    worksheet.column_dimensions[number_to_excel_column(
                        idx + 1)].width = min(max_len, 60)

            elif sheet_name == "swing_per_analysis_lst":
                df.to_excel(writer, sheet_name=sheet_name, index=False,
                            header=["coin_name", "coin_time_tf", "all_swing_count", "all_swings_pp_count", "all_swings_np_count", "all_swing_per_sum", "all_swings_pp_sum", "all_swings_np_sum", "all_swings_pp_avg", "all_swings_np_avg", "all_swings_pp_med", "all_swings_np_med", "t_5_lrg_pp_sp_lst",
                                    "t_5_lrg_np_sp_lst", "t_10_lrg_pp_sp_sum", "t_10_lrg_np_sp_sum", "t_10_lrg_pp_sp_avg", "t_10_lrg_np_sp_avg", "t_10_lrg_pp_sp_med", "t_10_lrg_np_sp_med", "t_10_sml_pp_sp_sum", "t_10_sml_np_sp_sum", "t_10_sml_pp_sp_avg", "t_10_sml_np_sp_avg", "t_10_sml_pp_sp_med", "t_10_sml_np_sp_med"],
                            engine='openpyxl')
                worksheet = writer.sheets[sheet_name]
                for idx, col in enumerate(df):
                    series = df[col]
                    max_len = max((series.astype(str).map(
                        len).max(), len(str(series.name)))) + 5
                    worksheet.column_dimensions[number_to_excel_column(
                        idx + 1)].width = min(max_len, 60)

            elif sheet_name == "swing_pstv_per_range_lst":
                df.to_excel(writer, sheet_name=sheet_name, index=False,
                            header=["coin_name", "coin_time_tf", "sp_pp_cnt_0_1_lst", "sp_pp_cnt_1_2_lst", "sp_pp_cnt_0_2_lst", "sp_pp_cnt_2_3_lst", "sp_pp_cnt_3_4_lst", "sp_pp_cnt_2_4_lst", "sp_pp_cnt_4_5_lst", "sp_pp_cnt_5_6_lst", "sp_pp_cnt_6_7_lst", "sp_pp_cnt_4_7_lst",
                                    "sp_pp_cnt_7_9_lst", "sp_pp_cnt_9_11_lst", "sp_pp_cnt_11_13_lst", "sp_pp_cnt_13_15_lst", "sp_pp_cnt_7_15_lst", "sp_pp_cnt_15_18_lst", "sp_pp_cnt_18_22_lst", "sp_pp_cnt_22_25_lst", "sp_pp_cnt_15_25_lst", "sp_pp_cnt_25_plus_lst", "t_3_sp_pp_ranges"],
                            engine='openpyxl')
                worksheet = writer.sheets[sheet_name]
                for idx, col in enumerate(df):
                    series = df[col]
                    max_len = max((series.astype(str).map(
                        len).max(), len(str(series.name)))) + 5
                    worksheet.column_dimensions[number_to_excel_column(
                        idx + 1)].width = min(max_len, 60)

            elif sheet_name == "swing_neg_per_range_lst":
                df.to_excel(writer, sheet_name=sheet_name, index=False,
                            header=["coin_name", "coin_time_tf", "sp_np_cnt_0_1_lst", "sp_np_cnt_1_2_lst", "sp_np_cnt_0_2_lst", "sp_np_cnt_2_3_lst", "sp_np_cnt_3_4_lst", "sp_np_cnt_2_4_lst", "sp_np_cnt_4_5_lst", "sp_np_cnt_5_6_lst", "sp_np_cnt_6_7_lst", "sp_np_cnt_4_7_lst",
                                    "sp_np_cnt_7_9_lst", "sp_np_cnt_9_11_lst", "sp_np_cnt_11_13_lst", "sp_np_cnt_13_15_lst", "sp_np_cnt_7_15_lst", "sp_np_cnt_15_18_lst", "sp_np_cnt_18_22_lst", "sp_np_cnt_22_25_lst", "sp_np_cnt_15_25_lst", "sp_np_cnt_25_plus_lst", "t_3_sp_np_ranges"],
                            engine='openpyxl')
                worksheet = writer.sheets[sheet_name]
                for idx, col in enumerate(df):
                    series = df[col]
                    max_len = max((series.astype(str).map(
                        len).max(), len(str(series.name)))) + 5
                    worksheet.column_dimensions[number_to_excel_column(
                        idx + 1)].width = min(max_len, 60)
            elif sheet_name == "swing_rand_per_analysis_lst":
                df.to_excel(writer, sheet_name=sheet_name, index=False,
                            header=["coin_name", "coin_time_tf", "all_swing_rand_count", "all_swings_rand_pp_count", "all_swings_rand_np_count", "all_swing_rand_per_sum", "all_swings_rand_pp_sum", "all_swings_rand_np_sum", "all_swings_rand_pp_avg", "all_swings_rand_np_avg", "all_swings_rand_pp_med", "all_swings_rand_np_med", "t_5_lrg_pp_rand_sp_lst", "t_5_lrg_np_rand_sp_lst",
                                    "t_10_lrg_pp_rand_sp_sum", "t_10_lrg_np_rand_sp_sum", "t_10_lrg_pp_rand_sp_avg", "t_10_lrg_np_rand_sp_avg", "t_10_lrg_pp_rand_sp_med", "t_10_lrg_np_rand_sp_med", "t_10_sml_pp_rand_sp_sum", "t_10_sml_np_rand_sp_sum", "t_10_sml_pp_rand_sp_avg", "t_10_sml_np_rand_sp_avg", "t_10_sml_pp_rand_sp_med", "t_10_sml_np_rand_sp_med"],
                            engine='openpyxl')
                worksheet = writer.sheets[sheet_name]
                for idx, col in enumerate(df):
                    series = df[col]
                    max_len = max((series.astype(str).map(
                        len).max(), len(str(series.name)))) + 5
                    worksheet.column_dimensions[number_to_excel_column(
                        idx + 1)].width = min(max_len, 60)
            elif sheet_name == "swing_zero_rand_per_info_lst":
                df.to_excel(writer, sheet_name=sheet_name, index=False,
                            header=["coin_name", "coin_time_tf", "all_swings_zero_rand_count", "all_swings_zero_rand_pp_count", "all_swings_zero_rand_np_count", "all_swings_zero_rand_pp_sum", "all_swings_zero_rand_np_sum", "all_swing_zero_rand_per_sum", "all_swings_zero_rand_pp_mean", "all_swings_zero_rand_np_mean", "all_swings_zero_rand_pp_med", "all_swings_zero_rand_np_med", "t_5_lrg_pp_zero_rand_sp_lst", "t_5_lrg_np_zero_rand_sp_lst",
                                    "t_10_lrg_pp_zero_rand_sp_sum", "t_10_lrg_np_zero_rand_sp_sum", "t_10_lrg_pp_zero_rand_sp_avg", "t_10_lrg_np_zero_rand_sp_avg", "t_10_lrg_pp_zero_rand_sp_med", "t_10_lrg_np_zero_rand_sp_med", "t_10_sml_pp_zero_rand_sp_sum", "t_10_sml_np_zero_rand_sp_sum", "t_10_sml_pp_zero_rand_sp_avg", "t_10_sml_np_zero_rand_sp_avg", "t_10_sml_pp_zero_rand_sp_med", "t_10_sml_np_zero_rand_sp_med"],
                            engine='openpyxl')
                worksheet = writer.sheets[sheet_name]
                for idx, col in enumerate(df):
                    series = df[col]
                    max_len = max((series.astype(str).map(
                        len).max(), len(str(series.name)))) + 5
                    worksheet.column_dimensions[number_to_excel_column(
                        idx + 1)].width = min(max_len, 60)
            elif sheet_name == "swing_rand_pstv_per_range_lst":
                df.to_excel(writer, sheet_name=sheet_name, index=False,
                            header=["coin_name", "coin_time_tf", "rand_pp_cnt_0_to_0_25_lst", "rand_pp_cnt_0_25_to_0_5_lst", "rand_pp_cnt_0_to_0_5_lst", "rand_pp_cnt_0_5_to_1_lst", "rand_pp_cnt_1_to_1_5_lst", "rand_pp_cnt_0_5_to_1_5_lst", "rand_pp_cnt_1_5_to_2_lst", "rand_pp_cnt_2_to_2_5_lst", "rand_pp_cnt_2_5_to_3_5_lst",
                                    "rand_pp_cnt_1_5_to_3_5_lst", "rand_pp_cnt_3_5_to_4_5_lst", "rand_pp_cnt_4_5_to_5_5_lst", "rand_pp_cnt_5_5_to_7_lst", "rand_pp_cnt_3_5_to_7_lst", "rand_pp_cnt_7_to_9_lst", "rand_pp_cnt_9_to_12_lst", "rand_pp_cnt_12_to_15_lst", "rand_pp_cnt_7_to_15_lst", "rand_pp_cnt_15_plus_lst", "t_3_rand_pp_ranges"],
                            engine='openpyxl')
                worksheet = writer.sheets[sheet_name]
                for idx, col in enumerate(df):
                    series = df[col]
                    max_len = max((series.astype(str).map(
                        len).max(), len(str(series.name)))) + 5
                    worksheet.column_dimensions[number_to_excel_column(
                        idx + 1)].width = min(max_len, 60)
            elif sheet_name == "swing_rand_neg_per_range_lst":
                df.to_excel(writer, sheet_name=sheet_name, index=False,
                            header=["coin_name", "coin_time_tf", "rand_np_cnt_0_to_0_25_lst", "rand_np_cnt_0_25_to_0_5_lst", "rand_np_cnt_0_to_0_5_lst", "rand_np_cnt_0_5_to_1_lst", "rand_np_cnt_1_to_1_5_lst", "rand_np_cnt_0_5_to_1_5_lst", "rand_np_cnt_1_5_to_2_lst", "rand_np_cnt_2_to_2_5_lst", "rand_np_cnt_2_5_to_3_5_lst",
                                    "rand_np_cnt_1_5_to_3_5_lst", "rand_np_cnt_3_5_to_4_5_lst", "rand_np_cnt_4_5_to_5_5_lst", "rand_np_cnt_5_5_to_7_lst", "rand_np_cnt_3_5_to_7_lst", "rand_np_cnt_7_to_9_lst", "rand_np_cnt_9_to_12_lst", "rand_np_cnt_12_to_15_lst", "rand_np_cnt_7_to_15_lst", "rand_np_cnt_15_plus_lst", "t_3_rand_np_ranges"],
                            engine='openpyxl')
                worksheet = writer.sheets[sheet_name]
                for idx, col in enumerate(df):
                    series = df[col]
                    max_len = max((series.astype(str).map(
                        len).max(), len(str(series.name)))) + 5
                    worksheet.column_dimensions[number_to_excel_column(
                        idx + 1)].width = min(max_len, 60)
            elif sheet_name == "swing_time_analysis_lst":
                df.to_excel(writer, sheet_name=sheet_name, index=False,
                            header=["coin_name", "coin_time_tf", "sum_all_s_time", "all_swing_max_time", "all_swing_min_time", "all_swing_avg_time", "all_swing_median_time", "total_pstv_s_time", "pstv_swing_max_time", "pstv_swing_min_time", "pstv_swing_avg_time", "pstv_swing_median_time", "total_neg_s_time", "neg_swing_max_time", "neg_swing_min_time", "neg_swing_avg_time", "neg_swing_median_time", "top_10_lrg_pstv_total_per", "top_10_lrg_pstv_total_rand_per", "top_10_lrg_pstv_total_s_time", "top_10_lrg_pstv_max_time", "top_10_lrg_pstv_min_time", "top_10_lrg_pstv_avg_time", "top_10_lrg_pstv_median_time", "t_5_lrg_pstv_sp_time", "top_10_sml_pstv_total_per", "top_10_sml_pstv_total_rand_per", "top_10_sml_pstv_total_s_time", "top_10_sml_pstv_max_time", "top_10_sml_pstv_min_time", "top_10_sml_pstv_avg_time", "top_10_sml_pstv_median_time", "top_10_lrg_neg_total_per", "top_10_lrg_neg_total_rand_per",
                                    "top_10_lrg_neg_total_s_time", "top_10_lrg_neg_max_time", "top_10_lrg_neg_min_time", "top_10_lrg_neg_avg_time", "top_10_lrg_neg_median_time", "t_5_lrg_neg_sp_time", "top_10_sml_neg_total_per", "top_10_sml_neg_total_rand_per", "top_10_sml_neg_total_s_time", "top_10_sml_neg_max_time", "top_10_sml_neg_min_time", "top_10_sml_neg_avg_time", "top_10_sml_neg_median_time", "zero_rand_total_s_time", "zero_rand_max_s_time", "zero_rand_min_s_time", "zero_rand_avg_s_time", "zero_rand_med_s_time", "zero_rand_pstv_sp_total_s_time", "zero_rand_pstv_sp_total_s_per", "zero_rand_pstv_sp_max_s_time", "zero_rand_pstv_sp_min_s_time", "zero_rand_pstv_sp_avg_s_time", "zero_rand_pstv_sp_med_s_time", "zero_rand_neg_sp_total_s_time", "zero_rand_neg_sp_total_s_per", "zero_rand_neg_sp_max_s_time", "zero_rand_neg_sp_min_s_time", "zero_rand_neg_sp_avg_s_time", "zero_rand_neg_sp_med_s_time"],
                            engine='openpyxl')
                worksheet = writer.sheets[sheet_name]
                for idx, col in enumerate(df):
                    series = df[col]
                    max_len = max((series.astype(str).map(
                        len).max(), len(str(series.name)))) + 5
                    worksheet.column_dimensions[number_to_excel_column(
                        idx + 1)].width = min(max_len, 60)
            elif sheet_name == "swing_rsi_diff_analysis_lst":
                df.to_excel(writer, sheet_name=sheet_name, index=False,
                            header=["coin_name", "coin_time_tf", "sum_all_s_rsi_df", "all_swing_max_rsi_df", "all_swing_min_rsi_df", "all_swing_avg_rsi_df", "all_swing_median_rsi_df", "total_pstv_s_rsi_df", "pstv_swing_max_rsi_df", "pstv_swing_min_rsi_df", "pstv_swing_avg_rsi_df", "pstv_swing_median_rsi_df", "total_neg_s_rsi_df", "neg_swing_max_rsi_df", "neg_swing_min_rsi_df", "neg_swing_avg_rsi_df", "neg_swing_median_rsi_df", "top_10_lrg_pstv_total_per", "top_10_lrg_pstv_total_rand_per", "top_10_lrg_pstv_total_s_rsi_df", "top_10_lrg_pstv_max_rsi_df", "top_10_lrg_pstv_min_rsi_df", "top_10_lrg_pstv_avg_rsi_df", "top_10_lrg_pstv_median_rsi_df", "t_5_lrg_pstv_sp_rsi_df", "top_10_sml_pstv_total_per", "top_10_sml_pstv_total_rand_per", "top_10_sml_pstv_total_s_rsi_df", "top_10_sml_pstv_max_rsi_df", "top_10_sml_pstv_min_rsi_df", "top_10_sml_pstv_avg_rsi_df", "top_10_sml_pstv_median_rsi_df", "top_10_lrg_neg_total_per", "top_10_lrg_neg_total_rand_per",
                                    "top_10_lrg_neg_total_s_rsi_df", "top_10_lrg_neg_max_rsi_df", "top_10_lrg_neg_min_rsi_df", "top_10_lrg_neg_avg_rsi_df", "top_10_lrg_neg_median_rsi_df", "t_5_lrg_neg_sp_rsi_df", "top_10_sml_neg_total_per", "top_10_sml_neg_total_rand_per", "top_10_sml_neg_total_s_rsi_df", "top_10_sml_neg_max_rsi_df", "top_10_sml_neg_min_rsi_df", "top_10_sml_neg_avg_rsi_df", "top_10_sml_neg_median_rsi_df", "zero_rand_total_s_rsi_df", "zero_rand_max_s_rsi_df", "zero_rand_min_s_rsi_df", "zero_rand_avg_s_rsi_df", "zero_rand_med_s_rsi_df", "zero_rnd_pstv_sp_tol_s_rsi_df", "zero_rand_pstv_sp_total_s_per", "zero_rand_pstv_sp_max_s_rsi_df", "zero_rand_pstv_sp_min_s_rsi_df", "zero_rand_pstv_sp_avg_s_rsi_df", "zero_rand_pstv_sp_med_s_rsi_df", "zero_rand_neg_sp_tol_s_rsi_df", "zero_rand_neg_sp_total_s_per", "zero_rand_neg_sp_max_s_rsi_df", "zero_rand_neg_sp_min_s_rsi_df", "zero_rand_neg_sp_avg_s_rsi_df", "zero_rand_neg_sp_med_s_rsi_df"],
                            engine='openpyxl')
                worksheet = writer.sheets[sheet_name]
                for idx, col in enumerate(df):
                    series = df[col]
                    max_len = max((series.astype(str).map(
                        len).max(), len(str(series.name)))) + 5
                    worksheet.column_dimensions[number_to_excel_column(
                        idx + 1)].width = min(max_len, 60)
            else:
                print("No data Available in the Excel")
    print("Excel file created successfully.")


def layer_3_rank_excel_export(layer_3_str_info_excel_lst, layer_3_rank_1_excel_lst, layer_3_rank_2_excel_lst, layer_3_rank_3_excel_lst, layer_3_rank_4_excel_lst, layer_3_rank_5_excel_lst, layer_3_rank_6_excel_lst, output_excel_folder_path, Choose_Time_Frame, layer_3_rank_1_lst, layer_3_rank_2_lst, layer_3_rank_3_lst, layer_3_rank_4_lst, layer_3_rank_5_lst, layer_3_rank_6_lst, layer_3_rank_7_lst, sort_last_s_excel_lst, sort_last_3_s_excel_lst):
    if not os.path.exists(output_excel_folder_path):
        os.makedirs(output_excel_folder_path)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    if Choose_Time_Frame == 1:
        extracted_excel_file_name = f"layer_3_rank_data_1TF_{timestamp}.xlsx"
    elif Choose_Time_Frame == 2:
        extracted_excel_file_name = f"crypto_coin_ranking_analysis_{timestamp}.xlsx"
    elif Choose_Time_Frame == 5:
        extracted_excel_file_name = f"layer_3_rank_data_5TF_{timestamp}.xlsx"
    else:
        return {"Status": "Please Select Valid Time frame Either 1 or 5"}
    extracted_excel_file_path = os.path.join(
        output_excel_folder_path, extracted_excel_file_name)

    # Column Names
    sort_last_s_excel_col_names = ["rank", "coin_name", "coin_tf", "last_S_info",
                                   "last_S_dir", "last_S_per", "last_s_rand_per", "last_s_time"]

    sort_last_3_s_excel_col_names = ["rank", "coin_name", "coin_tf", "S_3_score", "S_3_per_sum",
                                     "S_3_per_avg", "last_S_info", "swing_2_info", "swing_3_info", "S_3_rand_sum", "S_3_rand_avg"]

    layer_3_str_info_col_names = [
        'coin_name', 'coin_time_tf', 'swing_1_info', 'swing_2_info', 'swing_3_info', 'swing_1_dir', 'swing_2_dir', 'swing_3_dir', 't_5_lrg_pp_sp_lst', 't_5_lrg_np_sp_lst', 't_3_sp_pp_ranges', 't_3_sp_np_ranges', 't_5_lrg_pp_rand_sp_lst', 't_5_lrg_np_rand_sp_lst', 't_5_lrg_pp_zero_rand_sp_lst', 't_5_lrg_np_zero_rand_sp_lst', 't_3_rand_pp_ranges', 't_3_rand_np_ranges', 'last_fb_time']

    layer_3_rank_1_col_names = [
        "Rank", "coin_name", "coin_time_tf", "last_swing_per", "last_swing_rand_per", "last_swing_time", "last_swing_rsi_dif", "last_3_s_per_sum", "last_3_s_per_avg", "last_3_s_rand_sum", "last_3_s_rand_avg", "last_3_s_avg_time", "last_3_s_rsi_diff_avg", "all_swing_count", "all_swings_pp_count", "all_swings_np_count", "all_swing_per_sum", "all_swings_pp_sum", "all_swings_np_sum", "all_swings_pp_avg", "all_swings_np_avg", "all_swings_pp_med", "all_swings_np_med", "t_10_lrg_pp_sp_sum", "t_10_lrg_np_sp_sum", "t_10_lrg_pp_sp_avg", "t_10_lrg_np_sp_avg", "t_10_lrg_pp_sp_med", "t_10_lrg_np_sp_med", "t_10_sml_pp_sp_sum", "t_10_sml_np_sp_sum", "t_10_sml_pp_sp_avg", "t_10_sml_np_sp_avg", "t_10_sml_pp_sp_med", "t_10_sml_np_sp_med", "sp_pp_cnt_0_2_lst", "sp_pp_cnt_2_4_lst", "sp_pp_cnt_4_7_lst", "sp_pp_cnt_7_15_lst", "sp_pp_cnt_15_25_lst", "sp_np_cnt_0_2_lst", "sp_np_cnt_2_4_lst", "sp_np_cnt_4_7_lst", "sp_np_cnt_7_15_lst", "sp_np_cnt_15_25_lst", "all_swing_rand_per_sum", "all_swings_rand_pp_sum", "all_swings_rand_np_sum", "all_swings_rand_pp_avg", "all_swings_rand_np_avg", "all_swings_rand_pp_med", "all_swings_rand_np_med", "t_10_lrg_pp_rand_sp_sum", "t_10_lrg_np_rand_sp_sum", "t_10_lrg_pp_rand_sp_avg", "t_10_lrg_np_rand_sp_avg", "t_10_lrg_pp_rand_sp_med", "t_10_lrg_np_rand_sp_med", "t_10_sml_pp_rand_sp_sum", "t_10_sml_np_rand_sp_sum", "t_10_sml_pp_rand_sp_avg", "t_10_sml_np_rand_sp_avg", "t_10_sml_pp_rand_sp_med", "t_10_sml_np_rand_sp_med", "all_swings_zero_rand_count", "all_swings_zero_rand_pp_count", "all_swings_zero_rand_np_count", "all_swings_zero_rand_pp_sum", "all_swings_zero_rand_np_sum", "all_swing_zero_rand_per_sum", "all_swings_zero_rand_pp_mean", "all_swings_zero_rand_np_mean", "all_swings_zero_rand_pp_med", "all_swings_zero_rand_np_med", "t_10_lrg_pp_zero_rand_sp_sum", "t_10_lrg_np_zero_rand_sp_sum", "t_10_lrg_pp_zero_rand_sp_avg", "t_10_lrg_np_zero_rand_sp_avg", "t_10_lrg_pp_zero_rand_sp_med", "t_10_lrg_np_zero_rand_sp_med", "t_10_sml_pp_zero_rand_sp_sum", "t_10_sml_np_zero_rand_sp_sum", "t_10_sml_pp_zero_rand_sp_avg", "t_10_sml_np_zero_rand_sp_avg", "t_10_sml_pp_zero_rand_sp_med", "t_10_sml_np_zero_rand_sp_med", "rand_pp_cnt_0_to_0_25_lst", "rand_pp_cnt_0_25_to_0_5_lst", "rand_pp_cnt_0_to_0_5_lst", "rand_pp_cnt_0_5_to_1_lst", "rand_pp_cnt_1_to_1_5_lst", "rand_pp_cnt_0_5_to_1_5_lst", "rand_pp_cnt_1_5_to_3_5_lst", "rand_pp_cnt_3_5_to_7_lst", "rand_pp_cnt_7_to_15_lst", "rand_np_cnt_0_to_0_25_lst", "rand_np_cnt_0_25_to_0_5_lst", "rand_np_cnt_0_to_0_5_lst", "rand_np_cnt_0_5_to_1_lst", "rand_np_cnt_1_to_1_5_lst", "rand_np_cnt_0_5_to_1_5_lst", "rand_np_cnt_1_5_to_3_5_lst", "rand_np_cnt_3_5_to_7_lst", "rand_np_cnt_7_to_15_lst", "all_swing_max_time", "all_swing_avg_time", "all_swing_median_time", "pstv_swing_max_time", "pstv_swing_avg_time", "pstv_swing_median_time", "neg_swing_max_time", "neg_swing_avg_time", "neg_swing_median_time", "top_10_lrg_pstv_total_rand_per_change", "top_10_lrg_pstv_max_time", "top_10_lrg_pstv_avg_time", "top_10_lrg_pstv_median_time", "top_10_sml_pstv_total_rand_per_change", "top_10_sml_pstv_max_time", "top_10_sml_pstv_avg_time", "top_10_sml_pstv_median_time", "top_10_lrg_neg_total_rand_per_change", "top_10_lrg_neg_max_time", "top_10_lrg_neg_avg_time", "top_10_lrg_neg_median_time", "top_10_sml_neg_total_rand_per_change", "top_10_sml_neg_max_time", "top_10_sml_neg_avg_time", "top_10_sml_neg_median_time", "zero_rand_max_swings_time", "zero_rand_avg_swings_time", "zero_rand_med_swings_time", "zero_rand_pstv_sp_max_swings_time", "zero_rand_pstv_sp_avg_swings_time", "zero_rand_pstv_sp_med_swings_time", "zero_rand_neg_sp_max_swings_time", "zero_rand_neg_sp_avg_swings_time", "zero_rand_neg_sp_med_swings_time", "all_swing_max_rsi_diff", "all_swing_avg_rsi_diff", "all_swing_median_rsi_diff", "pstv_swing_max_rsi_diff", "pstv_swing_avg_rsi_diff", "pstv_swing_median_rsi_diff", "neg_swing_max_rsi_diff", "neg_swing_avg_rsi_diff", "neg_swing_median_rsi_diff", "top_10_lrg_pstv_max_rsi_diff", "top_10_lrg_pstv_avg_rsi_diff", "top_10_lrg_pstv_median_rsi_diff", "top_10_sml_pstv_max_rsi_diff", "top_10_sml_pstv_avg_rsi_diff", "top_10_sml_pstv_median_rsi_diff", "top_10_lrg_neg_max_rsi_diff", "top_10_lrg_neg_avg_rsi_diff", "top_10_lrg_neg_median_rsi_diff", "top_10_sml_neg_max_rsi_diff", "top_10_sml_neg_avg_rsi_diff", "top_10_sml_neg_median_rsi_diff", "zero_rand_max_swings_rsi_diff", "zero_rand_avg_swings_rsi_diff", "zero_rand_med_swings_rsi_diff", "zero_rand_pstv_sp_max_swings_rsi_diff", "zero_rand_pstv_sp_avg_swings_rsi_diff", "zero_rand_pstv_sp_med_swings_rsi_diff", "zero_rand_neg_sp_max_swings_rsi_diff", "zero_rand_neg_sp_avg_swings_rsi_diff", "zero_rand_neg_sp_med_swings_rsi_diff", "total_fb", "total_pstv_fb", "total_neg_fb"]

    layer_3_rank_2_col_names = [
        "Rank", "coin_name", "coin_time_tf", "last_swing_per", "last_swing_rand_per", "last_swing_time",
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
        "Rank", "coin_name", "coin_time_tf", "last_swing_per", "last_swing_rand_per", "last_swing_time",
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
        "Rank", "coin_name", "coin_time_tf", "last_swing_per", "last_swing_rand_per", "last_swing_time", "last_swing_rsi_dif", "last_3_s_per_avg", "last_3_s_rand_avg", "last_3_s_avg_time", "last_3_s_rsi_diff_avg", "all_swing_count", "all_swings_pp_count", "all_swings_np_count", "all_swings_pp_avg", "all_swings_np_avg", "t_10_lrg_pp_sp_avg", "t_10_lrg_np_sp_avg", "t_10_sml_pp_sp_avg", "t_10_sml_np_sp_avg", "sp_pp_cnt_0_2_lst", "sp_pp_cnt_2_4_lst", "sp_pp_cnt_4_7_lst", "sp_pp_cnt_7_15_lst", "sp_pp_cnt_15_25_lst", "sp_np_cnt_0_2_lst", "sp_np_cnt_2_4_lst", "sp_np_cnt_4_7_lst", "sp_np_cnt_7_15_lst", "sp_np_cnt_15_25_lst", "all_swing_rand_per_sum", "all_swings_rand_pp_sum", "all_swings_rand_np_sum", "t_10_lrg_pp_rand_sp_sum", "t_10_lrg_np_rand_sp_sum", "t_10_sml_pp_rand_sp_sum", "t_10_sml_np_rand_sp_sum", "all_swings_zero_rand_count", "all_swings_zero_rand_pp_count", "all_swings_zero_rand_np_count", "all_swings_zero_rand_pp_sum", "all_swings_zero_rand_np_sum", "all_swing_zero_rand_per_sum", "t_10_lrg_pp_zero_rand_sp_sum", "t_10_lrg_np_zero_rand_sp_sum", "t_10_sml_pp_zero_rand_sp_sum", "t_10_sml_np_zero_rand_sp_sum", "rand_pp_cnt_0_to_0_25_lst", "rand_pp_cnt_0_25_to_0_5_lst", "rand_pp_cnt_0_to_0_5_lst", "rand_pp_cnt_0_5_to_1_lst", "rand_pp_cnt_1_to_1_5_lst", "rand_pp_cnt_0_5_to_1_5_lst", "rand_pp_cnt_1_5_to_3_5_lst", "rand_pp_cnt_3_5_to_7_lst", "rand_pp_cnt_7_to_15_lst", "rand_np_cnt_0_to_0_25_lst", "rand_np_cnt_0_25_to_0_5_lst", "rand_np_cnt_0_to_0_5_lst", "rand_np_cnt_0_5_to_1_lst", "rand_np_cnt_1_to_1_5_lst", "rand_np_cnt_0_5_to_1_5_lst", "rand_np_cnt_1_5_to_3_5_lst", "rand_np_cnt_3_5_to_7_lst", "rand_np_cnt_7_to_15_lst", "all_swing_avg_time", "pstv_swing_avg_time", "neg_swing_avg_time", "top_10_lrg_pstv_total_rand_per_change", "top_10_lrg_pstv_avg_time", "top_10_sml_pstv_total_rand_per_change", "top_10_sml_pstv_avg_time", "top_10_lrg_neg_avg_time", "top_10_sml_neg_avg_time", "zero_rand_avg_swings_time", "zero_rand_pstv_sp_avg_swings_time", "zero_rand_neg_sp_avg_swings_time", "all_swing_avg_rsi_diff", "pstv_swing_avg_rsi_diff", "neg_swing_avg_rsi_diff", "top_10_lrg_pstv_avg_rsi_diff", "top_10_sml_pstv_avg_rsi_diff", "top_10_lrg_neg_avg_rsi_diff", "top_10_sml_neg_avg_rsi_diff", "zero_rand_avg_swings_rsi_diff", "zero_rand_pstv_sp_avg_rsi_diff", "zero_rand_neg_sp_avg_swings_rsi_diff", "total_fb", "total_pstv_fb", "total_neg_fb"
    ]

    layer_3_rank_5_col_names = [
        "Rank", "coin_name", "coin_time_tf", "last_swing_per", "last_swing_rand_per", "last_swing_time", "last_swing_rsi_dif", "last_3_s_per_avg", "last_3_s_rand_avg", "last_3_s_avg_time", "last_3_s_rsi_diff_avg", "all_swing_count", "all_swings_pp_count", "all_swings_np_count", "all_swings_pp_avg", "all_swings_np_avg", "t_10_lrg_pp_sp_avg", "t_10_lrg_np_sp_avg", "t_10_sml_pp_sp_avg", "t_10_sml_np_sp_avg", "sp_pp_cnt_0_2_lst", "sp_pp_cnt_2_4_lst", "sp_pp_cnt_4_7_lst", "sp_pp_cnt_7_15_lst", "sp_pp_cnt_15_25_lst", "sp_np_cnt_0_2_lst", "sp_np_cnt_2_4_lst", "sp_np_cnt_4_7_lst", "sp_np_cnt_7_15_lst", "sp_np_cnt_15_25_lst", "all_swings_rand_pp_avg", "all_swings_rand_np_avg", "t_10_lrg_pp_rand_sp_avg", "t_10_lrg_np_rand_sp_avg", "t_10_sml_pp_rand_sp_avg", "t_10_sml_np_rand_sp_avg", "all_swings_zero_rand_count", "all_swings_zero_rand_pp_count", "all_swings_zero_rand_np_count", "all_swings_zero_rand_pp_mean", "all_swings_zero_rand_np_mean", "t_10_lrg_pp_zero_rand_sp_avg", "t_10_lrg_np_zero_rand_sp_avg", "t_10_sml_pp_zero_rand_sp_avg", "t_10_sml_np_zero_rand_sp_avg", "rand_pp_cnt_0_to_0_25_lst", "rand_pp_cnt_0_25_to_0_5_lst", "rand_pp_cnt_0_to_0_5_lst", "rand_pp_cnt_0_5_to_1_lst", "rand_pp_cnt_1_to_1_5_lst", "rand_pp_cnt_0_5_to_1_5_lst", "rand_pp_cnt_1_5_to_3_5_lst", "rand_pp_cnt_3_5_to_7_lst", "rand_pp_cnt_7_to_15_lst", "rand_np_cnt_0_to_0_25_lst", "rand_np_cnt_0_25_to_0_5_lst", "rand_np_cnt_0_to_0_5_lst", "rand_np_cnt_0_5_to_1_lst", "rand_np_cnt_1_to_1_5_lst", "rand_np_cnt_0_5_to_1_5_lst", "rand_np_cnt_1_5_to_3_5_lst", "rand_np_cnt_3_5_to_7_lst", "rand_np_cnt_7_to_15_lst", "all_swing_avg_time", "pstv_swing_avg_time", "neg_swing_avg_time", "top_10_lrg_pstv_total_rand_per_change", "top_10_lrg_pstv_avg_time", "top_10_sml_pstv_total_rand_per_change", "top_10_sml_pstv_avg_time", "top_10_lrg_neg_avg_time", "top_10_sml_neg_avg_time", "zero_rand_avg_swings_time", "zero_rand_pstv_sp_avg_swings_time", "zero_rand_neg_sp_avg_swings_time", "all_swing_avg_rsi_diff", "pstv_swing_avg_rsi_diff", "neg_swing_avg_rsi_diff", "top_10_lrg_pstv_avg_rsi_diff", "top_10_sml_pstv_avg_rsi_diff", "top_10_lrg_neg_avg_rsi_diff", "top_10_sml_neg_avg_rsi_diff", "zero_rand_avg_swings_rsi_diff", "zero_rand_pstv_sp_avg_rsi_diff", "zero_rand_neg_sp_avg_swings_rsi_diff", "total_fb", "total_pstv_fb", "total_neg_fb"]

    layer_3_rank_6_col_names = [
        "Rank", "coin_name", "coin_time_tf", "last_swing_per", "last_swing_rand_per", "last_swing_time", "last_swing_rsi_dif", "last_3_s_per_avg", "last_3_s_rand_avg", "last_3_s_avg_time", "last_3_s_rsi_diff_avg", "all_swing_count", "all_swings_pp_count", "all_swings_np_count", "all_swings_pp_med", "all_swings_np_med", "t_10_lrg_pp_sp_med", "t_10_lrg_np_sp_med", "t_10_sml_pp_sp_med", "t_10_sml_np_sp_med", "sp_pp_cnt_0_2_lst", "sp_pp_cnt_2_4_lst", "sp_pp_cnt_4_7_lst", "sp_pp_cnt_7_15_lst", "sp_pp_cnt_15_25_lst", "sp_np_cnt_0_2_lst", "sp_np_cnt_2_4_lst", "sp_np_cnt_4_7_lst", "sp_np_cnt_7_15_lst", "sp_np_cnt_15_25_lst", "all_swings_rand_pp_med", "all_swings_rand_np_med", "t_10_lrg_pp_rand_sp_med", "t_10_lrg_np_rand_sp_med", "t_10_sml_pp_rand_sp_med", "t_10_sml_np_rand_sp_med", "all_swings_zero_rand_count", "all_swings_zero_rand_pp_count", "all_swings_zero_rand_np_count", "all_swings_zero_rand_pp_med", "all_swings_zero_rand_np_med", "t_10_lrg_pp_zero_rand_sp_med", "t_10_lrg_np_zero_rand_sp_med", "t_10_sml_pp_zero_rand_sp_med", "t_10_sml_np_zero_rand_sp_med", "rand_pp_cnt_0_to_0_25_lst", "rand_pp_cnt_0_25_to_0_5_lst", "rand_pp_cnt_0_to_0_5_lst", "rand_pp_cnt_0_5_to_1_lst", "rand_pp_cnt_1_to_1_5_lst", "rand_pp_cnt_0_5_to_1_5_lst", "rand_pp_cnt_1_5_to_3_5_lst", "rand_pp_cnt_3_5_to_7_lst", "rand_pp_cnt_7_to_15_lst", "rand_np_cnt_0_to_0_25_lst", "rand_np_cnt_0_25_to_0_5_lst", "rand_np_cnt_0_to_0_5_lst", "rand_np_cnt_0_5_to_1_lst", "rand_np_cnt_1_to_1_5_lst", "rand_np_cnt_0_5_to_1_5_lst", "rand_np_cnt_1_5_to_3_5_lst", "rand_np_cnt_3_5_to_7_lst", "rand_np_cnt_7_to_15_lst", "all_swing_median_time", "pstv_swing_median_time", "neg_swing_median_time", "top_10_lrg_pstv_total_rand_per_change", "top_10_lrg_pstv_median_time", "top_10_sml_pstv_total_rand_per_change", "top_10_sml_pstv_median_time", "top_10_lrg_neg_median_time", "top_10_sml_neg_median_time", "zero_rand_med_swings_time", "zero_rand_pstv_sp_med_swings_time", "zero_rand_neg_sp_med_swings_time", "all_swing_median_rsi_diff", "pstv_swing_median_rsi_diff", "neg_swing_median_rsi_diff", "top_10_sml_pstv_median_rsi_diff", "top_10_lrg_neg_median_rsi_diff", "top_10_sml_neg_median_rsi_diff", "zero_rand_med_swings_rsi_diff", "zero_rand_pstv_sp_med_swings_rsi_diff", "zero_rand_neg_sp_med_swings_rsi_diff", "total_fb", "total_pstv_fb", "total_neg_fb"]

    coin_rank_cols = ["Rank", "coin_name", "coin_time_tf",
                      "coin_score", "coin_stop_loss", "coin_step"]

    # Data Frames
    sort_last_s_excel_records = [sublist for sublist in sort_last_s_excel_lst]
    sort_last_s_excel_records_df = pd.DataFrame(
        sort_last_s_excel_records, columns=sort_last_s_excel_col_names)

    sort_last_3_s_excel_records = [
        sublist for sublist in sort_last_3_s_excel_lst]
    sort_last_3_s_excel_records_df = pd.DataFrame(
        sort_last_3_s_excel_records, columns=sort_last_3_s_excel_col_names)

    layer_3_str_info_records = [
        sublist for sublist in layer_3_str_info_excel_lst]
    layer_3_str_info_records_df = pd.DataFrame(
        layer_3_str_info_records, columns=layer_3_str_info_col_names)

    layer_3_rank_7_coin_records = [sublist for sublist in layer_3_rank_7_lst]
    layer_3_rank_7_coin_records_df = pd.DataFrame(
        layer_3_rank_7_coin_records, columns=coin_rank_cols)

    layer_3_rank_1_coin_records = [sublist for sublist in layer_3_rank_1_lst]
    layer_3_rank_1_coin_records_df = pd.DataFrame(
        layer_3_rank_1_coin_records, columns=coin_rank_cols)

    layer_3_rank_1_records = [sublist for sublist in layer_3_rank_1_excel_lst]
    layer_3_rank_1_records_df = pd.DataFrame(
        layer_3_rank_1_records, columns=layer_3_rank_1_col_names)

    layer_3_rank_2_coin_records = [sublist for sublist in layer_3_rank_2_lst]
    layer_3_rank_2_coin_records_df = pd.DataFrame(
        layer_3_rank_2_coin_records, columns=coin_rank_cols)

    layer_3_rank_2_records = [sublist for sublist in layer_3_rank_2_excel_lst]
    layer_3_rank_2_records_df = pd.DataFrame(
        layer_3_rank_2_records, columns=layer_3_rank_2_col_names)

    layer_3_rank_3_coin_records = [sublist for sublist in layer_3_rank_3_lst]
    layer_3_rank_3_coin_records_df = pd.DataFrame(
        layer_3_rank_3_coin_records, columns=coin_rank_cols)

    layer_3_rank_3_records = [sublist for sublist in layer_3_rank_3_excel_lst]
    layer_3_rank_3_records_df = pd.DataFrame(
        layer_3_rank_3_records, columns=layer_3_rank_3_col_names)

    layer_3_rank_4_coin_records = [sublist for sublist in layer_3_rank_4_lst]
    layer_3_rank_4_coin_records_df = pd.DataFrame(
        layer_3_rank_4_coin_records, columns=coin_rank_cols)

    layer_3_rank_4_records = [sublist for sublist in layer_3_rank_4_excel_lst]
    layer_3_rank_4_records_df = pd.DataFrame(
        layer_3_rank_4_records, columns=layer_3_rank_4_col_names)

    layer_3_rank_5_coin_records = [sublist for sublist in layer_3_rank_5_lst]
    layer_3_rank_5_coin_records_df = pd.DataFrame(
        layer_3_rank_5_coin_records, columns=coin_rank_cols)

    layer_3_rank_5_records = [sublist for sublist in layer_3_rank_5_excel_lst]
    layer_3_rank_5_records_df = pd.DataFrame(
        layer_3_rank_5_records, columns=layer_3_rank_5_col_names)

    layer_3_rank_6_coin_records = [sublist for sublist in layer_3_rank_6_lst]
    layer_3_rank_6_coin_records_df = pd.DataFrame(
        layer_3_rank_6_coin_records, columns=coin_rank_cols)

    layer_3_rank_6_records = [sublist for sublist in layer_3_rank_6_excel_lst]
    layer_3_rank_6_records_df = pd.DataFrame(
        layer_3_rank_6_records, columns=layer_3_rank_6_col_names)

    # Data Frame Dict
    dfs = {"s_per_rank": sort_last_s_excel_records_df, "last_3_s_rank": sort_last_3_s_excel_records_df, "final_coin_ranks": layer_3_rank_7_coin_records_df, "rank_1": layer_3_rank_1_coin_records_df, "rank_1_data": layer_3_rank_1_records_df, "rank_2": layer_3_rank_2_coin_records_df, "rank_2_data": layer_3_rank_2_records_df, "rank_3": layer_3_rank_3_coin_records_df,
           "rank_3_data": layer_3_rank_3_records_df, "rank_4": layer_3_rank_4_coin_records_df, "rank_4_data": layer_3_rank_4_records_df, "rank_5": layer_3_rank_5_coin_records_df, "rank_5_data": layer_3_rank_5_records_df, "rank_6": layer_3_rank_6_coin_records_df, "rank_6_data": layer_3_rank_6_records_df, "coin_str_info": layer_3_str_info_records_df}

    with pd.ExcelWriter(extracted_excel_file_path, engine='openpyxl') as writer:
        for sheet_name, df in dfs.items():
            if sheet_name == "coin_str_info":
                df.to_excel(writer, sheet_name=sheet_name, index=False,
                            header=['coin_name', 'coin_time_tf', 'swing_1_info', 'swing_2_info', 'swing_3_info', 'swing_1_dir', 'swing_2_dir', 'swing_3_dir', 't_5_lrg_pp_sp_lst', 't_5_lrg_np_sp_lst', 't_3_sp_pp_ranges',
                                    't_3_sp_np_ranges', 't_5_lrg_pp_rand_sp_lst', 't_5_lrg_np_rand_sp_lst', 't_5_lrg_pp_zero_rand_sp_lst', 't_5_lrg_np_zero_rand_sp_lst', 't_3_rand_pp_ranges', 't_3_rand_np_ranges', 'last_fb_time'],
                            engine='openpyxl')
                worksheet = writer.sheets[sheet_name]
                for idx, col in enumerate(df):
                    series = df[col]
                    max_len = max((series.astype(str).map(
                        len).max(), len(str(series.name)))) + 5
                    worksheet.column_dimensions[number_to_excel_column(
                        idx + 1)].width = min(max_len, 60)
            elif sheet_name == "s_per_rank":
                df.to_excel(writer, sheet_name=sheet_name, index=False,
                            header=["Rank", "coin_name", "coin_tf", "last_S_info",
                                    "last_S_dir", "last_S_per", "last_s_rand_per", "last_s_time"],
                            engine='openpyxl')
                worksheet = writer.sheets[sheet_name]
                for idx, col in enumerate(df):
                    series = df[col]
                    max_len = max((series.astype(str).map(
                        len).max(), len(str(series.name)))) + 5
                    worksheet.column_dimensions[number_to_excel_column(
                        idx + 1)].width = min(max_len, 60)
            elif sheet_name == "last_3_s_rank":
                df.to_excel(writer, sheet_name=sheet_name, index=False,
                            header=["Rank", "coin_name", "coin_tf", "S_3_score", "S_3_per_sum", "S_3_per_avg",
                                    "last_S_info", "swing_2_info", "swing_3_info", "S_3_rand_sum", "S_3_rand_avg"],
                            engine='openpyxl')
                worksheet = writer.sheets[sheet_name]
                for idx, col in enumerate(df):
                    series = df[col]
                    max_len = max((series.astype(str).map(
                        len).max(), len(str(series.name)))) + 5
                    worksheet.column_dimensions[number_to_excel_column(
                        idx + 1)].width = min(max_len, 60)
            elif sheet_name == "final_coin_ranks":
                df.to_excel(writer, sheet_name=sheet_name, index=False,
                            header=["Rank", "coin_name", "coin_time_tf",
                                    "coin_score", "coin_stop_loss", "coin_step"],
                            engine='openpyxl')
                worksheet = writer.sheets[sheet_name]
                for idx, col in enumerate(df):
                    series = df[col]
                    max_len = max((series.astype(str).map(
                        len).max(), len(str(series.name)))) + 5
                    worksheet.column_dimensions[number_to_excel_column(
                        idx + 1)].width = min(max_len, 60)
            elif sheet_name == "rank_1":
                df.to_excel(writer, sheet_name=sheet_name, index=False,
                            header=["Rank", "coin_name", "coin_time_tf",
                                    "coin_score", "coin_stop_loss", "coin_step"],
                            engine='openpyxl')
                worksheet = writer.sheets[sheet_name]
                for idx, col in enumerate(df):
                    series = df[col]
                    max_len = max((series.astype(str).map(
                        len).max(), len(str(series.name)))) + 5
                    worksheet.column_dimensions[number_to_excel_column(
                        idx + 1)].width = min(max_len, 60)
            elif sheet_name == "rank_1_data":
                df.to_excel(writer, sheet_name=sheet_name, index=False,
                            header=["Rank", "coin_name", "coin_time_tf", "last_swing_per", "last_swing_rand_per", "last_swing_time", "last_swing_rsi_dif", "last_3_s_per_sum", "last_3_s_per_avg", "last_3_s_rand_sum", "last_3_s_rand_avg", "last_3_s_avg_time", "last_3_s_rsi_diff_avg", "all_swing_count", "all_swings_pp_count", "all_swings_np_count", "all_swing_per_sum", "all_swings_pp_sum", "all_swings_np_sum", "all_swings_pp_avg", "all_swings_np_avg", "all_swings_pp_med", "all_swings_np_med", "t_10_lrg_pp_sp_sum", "t_10_lrg_np_sp_sum", "t_10_lrg_pp_sp_avg", "t_10_lrg_np_sp_avg", "t_10_lrg_pp_sp_med", "t_10_lrg_np_sp_med", "t_10_sml_pp_sp_sum", "t_10_sml_np_sp_sum", "t_10_sml_pp_sp_avg", "t_10_sml_np_sp_avg", "t_10_sml_pp_sp_med", "t_10_sml_np_sp_med", "sp_pp_cnt_0_2_lst", "sp_pp_cnt_2_4_lst", "sp_pp_cnt_4_7_lst", "sp_pp_cnt_7_15_lst", "sp_pp_cnt_15_25_lst", "sp_np_cnt_0_2_lst", "sp_np_cnt_2_4_lst", "sp_np_cnt_4_7_lst", "sp_np_cnt_7_15_lst", "sp_np_cnt_15_25_lst", "all_swing_rand_per_sum", "all_swings_rand_pp_sum", "all_swings_rand_np_sum", "all_swings_rand_pp_avg", "all_swings_rand_np_avg", "all_swings_rand_pp_med", "all_swings_rand_np_med", "t_10_lrg_pp_rand_sp_sum", "t_10_lrg_np_rand_sp_sum", "t_10_lrg_pp_rand_sp_avg", "t_10_lrg_np_rand_sp_avg", "t_10_lrg_pp_rand_sp_med", "t_10_lrg_np_rand_sp_med", "t_10_sml_pp_rand_sp_sum", "t_10_sml_np_rand_sp_sum", "t_10_sml_pp_rand_sp_avg", "t_10_sml_np_rand_sp_avg", "t_10_sml_pp_rand_sp_med", "t_10_sml_np_rand_sp_med", "all_swings_zero_rand_count", "all_swings_zero_rand_pp_count", "all_swings_zero_rand_np_count", "all_swings_zero_rand_pp_sum", "all_swings_zero_rand_np_sum", "all_swing_zero_rand_per_sum", "all_swings_zero_rand_pp_mean", "all_swings_zero_rand_np_mean", "all_swings_zero_rand_pp_med", "all_swings_zero_rand_np_med", "t_10_lrg_pp_zero_rand_sp_sum", "t_10_lrg_np_zero_rand_sp_sum", "t_10_lrg_pp_zero_rand_sp_avg", "t_10_lrg_np_zero_rand_sp_avg", "t_10_lrg_pp_zero_rand_sp_med", "t_10_lrg_np_zero_rand_sp_med", "t_10_sml_pp_zero_rand_sp_sum", "t_10_sml_np_zero_rand_sp_sum", "t_10_sml_pp_zero_rand_sp_avg", "t_10_sml_np_zero_rand_sp_avg", "t_10_sml_pp_zero_rand_sp_med", "t_10_sml_np_zero_rand_sp_med", "rand_pp_cnt_0_to_0_25_lst", "rand_pp_cnt_0_25_to_0_5_lst", "rand_pp_cnt_0_to_0_5_lst", "rand_pp_cnt_0_5_to_1_lst", "rand_pp_cnt_1_to_1_5_lst", "rand_pp_cnt_0_5_to_1_5_lst", "rand_pp_cnt_1_5_to_3_5_lst",
                                    "rand_pp_cnt_3_5_to_7_lst", "rand_pp_cnt_7_to_15_lst", "rand_np_cnt_0_to_0_25_lst", "rand_np_cnt_0_25_to_0_5_lst", "rand_np_cnt_0_to_0_5_lst", "rand_np_cnt_0_5_to_1_lst", "rand_np_cnt_1_to_1_5_lst", "rand_np_cnt_0_5_to_1_5_lst", "rand_np_cnt_1_5_to_3_5_lst", "rand_np_cnt_3_5_to_7_lst", "rand_np_cnt_7_to_15_lst", "all_swing_max_time", "all_swing_avg_time", "all_swing_median_time", "pstv_swing_max_time", "pstv_swing_avg_time", "pstv_swing_median_time", "neg_swing_max_time", "neg_swing_avg_time", "neg_swing_median_time", "top_10_lrg_pstv_total_rand_per_change", "top_10_lrg_pstv_max_time", "top_10_lrg_pstv_avg_time", "top_10_lrg_pstv_median_time", "top_10_sml_pstv_total_rand_per_change", "top_10_sml_pstv_max_time", "top_10_sml_pstv_avg_time", "top_10_sml_pstv_median_time", "top_10_lrg_neg_total_rand_per_change", "top_10_lrg_neg_max_time", "top_10_lrg_neg_avg_time", "top_10_lrg_neg_median_time", "top_10_sml_neg_total_rand_per_change", "top_10_sml_neg_max_time", "top_10_sml_neg_avg_time", "top_10_sml_neg_median_time", "zero_rand_max_swings_time", "zero_rand_avg_swings_time", "zero_rand_med_swings_time", "zero_rand_pstv_sp_max_swings_time", "zero_rand_pstv_sp_avg_swings_time", "zero_rand_pstv_sp_med_swings_time", "zero_rand_neg_sp_max_swings_time", "zero_rand_neg_sp_avg_swings_time", "zero_rand_neg_sp_med_swings_time", "all_swing_max_rsi_diff", "all_swing_avg_rsi_diff", "all_swing_median_rsi_diff", "pstv_swing_max_rsi_diff", "pstv_swing_avg_rsi_diff", "pstv_swing_median_rsi_diff", "neg_swing_max_rsi_diff", "neg_swing_avg_rsi_diff", "neg_swing_median_rsi_diff", "top_10_lrg_pstv_max_rsi_diff", "top_10_lrg_pstv_avg_rsi_diff", "top_10_lrg_pstv_median_rsi_diff", "top_10_sml_pstv_max_rsi_diff", "top_10_sml_pstv_avg_rsi_diff", "top_10_sml_pstv_median_rsi_diff", "top_10_lrg_neg_max_rsi_diff", "top_10_lrg_neg_avg_rsi_diff", "top_10_lrg_neg_median_rsi_diff", "top_10_sml_neg_max_rsi_diff", "top_10_sml_neg_avg_rsi_diff", "top_10_sml_neg_median_rsi_diff", "zero_rand_max_swings_rsi_diff", "zero_rand_avg_swings_rsi_diff", "zero_rand_med_swings_rsi_diff", "zero_rand_pstv_sp_max_swings_rsi_diff", "zero_rand_pstv_sp_avg_swings_rsi_diff", "zero_rand_pstv_sp_med_swings_rsi_diff", "zero_rand_neg_sp_max_swings_rsi_diff", "zero_rand_neg_sp_avg_swings_rsi_diff", "zero_rand_neg_sp_med_swings_rsi_diff", "total_fb", "total_pstv_fb", "total_neg_fb"],
                            engine='openpyxl')
                worksheet = writer.sheets[sheet_name]
                for idx, col in enumerate(df):
                    series = df[col]
                    max_len = max((series.astype(str).map(
                        len).max(), len(str(series.name)))) + 5
                    worksheet.column_dimensions[number_to_excel_column(
                        idx + 1)].width = min(max_len, 60)
            elif sheet_name == "rank_2":
                df.to_excel(writer, sheet_name=sheet_name, index=False,
                            header=["Rank", "coin_name", "coin_time_tf",
                                    "coin_score", "coin_stop_loss", "coin_step"],
                            engine='openpyxl')
                worksheet = writer.sheets[sheet_name]
                for idx, col in enumerate(df):
                    series = df[col]
                    max_len = max((series.astype(str).map(
                        len).max(), len(str(series.name)))) + 5
                    worksheet.column_dimensions[number_to_excel_column(
                        idx + 1)].width = min(max_len, 60)
            elif sheet_name == "rank_2_data":
                df.to_excel(writer, sheet_name=sheet_name, index=False,
                            header=["Rank", "coin_name", "coin_time_tf", "last_swing_per", "last_swing_rand_per", "last_swing_time",
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
                                    "zero_rand_neg_sp_avg_swings_rsi_diff", "total_fb", "total_pstv_fb", "total_neg_fb"],
                            engine='openpyxl')
                worksheet = writer.sheets[sheet_name]
                for idx, col in enumerate(df):
                    series = df[col]
                    max_len = max((series.astype(str).map(
                        len).max(), len(str(series.name)))) + 5
                    worksheet.column_dimensions[number_to_excel_column(
                        idx + 1)].width = min(max_len, 60)
            elif sheet_name == "rank_3":
                df.to_excel(writer, sheet_name=sheet_name, index=False,
                            header=["Rank", "coin_name", "coin_time_tf",
                                    "coin_score", "coin_stop_loss", "coin_step"],
                            engine='openpyxl')
                worksheet = writer.sheets[sheet_name]
                for idx, col in enumerate(df):
                    series = df[col]
                    max_len = max((series.astype(str).map(
                        len).max(), len(str(series.name)))) + 5
                    worksheet.column_dimensions[number_to_excel_column(
                        idx + 1)].width = min(max_len, 60)
            elif sheet_name == "rank_3_data":
                df.to_excel(writer, sheet_name=sheet_name, index=False,
                            header=["Rank", "coin_name", "coin_time_tf", "last_swing_per", "last_swing_rand_per", "last_swing_time",
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
                                    "zero_rand_neg_sp_avg_swings_rsi_diff", "total_fb", "total_pstv_fb", "total_neg_fb"],
                            engine='openpyxl')
                worksheet = writer.sheets[sheet_name]
                for idx, col in enumerate(df):
                    series = df[col]
                    max_len = max((series.astype(str).map(
                        len).max(), len(str(series.name)))) + 5
                    worksheet.column_dimensions[number_to_excel_column(
                        idx + 1)].width = min(max_len, 60)
            elif sheet_name == "rank_4":
                df.to_excel(writer, sheet_name=sheet_name, index=False,
                            header=["Rank", "coin_name", "coin_time_tf",
                                    "coin_score", "coin_stop_loss", "coin_step"],
                            engine='openpyxl')
                worksheet = writer.sheets[sheet_name]
                for idx, col in enumerate(df):
                    series = df[col]
                    max_len = max((series.astype(str).map(
                        len).max(), len(str(series.name)))) + 5
                    worksheet.column_dimensions[number_to_excel_column(
                        idx + 1)].width = min(max_len, 60)
            elif sheet_name == "rank_4_data":
                df.to_excel(writer, sheet_name=sheet_name, index=False,
                            header=["Rank", "coin_name", "coin_time_tf", "last_swing_per", "last_swing_rand_per", "last_swing_time", "last_swing_rsi_dif", "last_3_s_per_avg", "last_3_s_rand_avg", "last_3_s_avg_time", "last_3_s_rsi_diff_avg", "all_swing_count", "all_swings_pp_count", "all_swings_np_count", "all_swings_pp_avg", "all_swings_np_avg", "t_10_lrg_pp_sp_avg", "t_10_lrg_np_sp_avg", "t_10_sml_pp_sp_avg", "t_10_sml_np_sp_avg", "sp_pp_cnt_0_2_lst", "sp_pp_cnt_2_4_lst", "sp_pp_cnt_4_7_lst", "sp_pp_cnt_7_15_lst", "sp_pp_cnt_15_25_lst", "sp_np_cnt_0_2_lst", "sp_np_cnt_2_4_lst", "sp_np_cnt_4_7_lst", "sp_np_cnt_7_15_lst", "sp_np_cnt_15_25_lst", "all_swing_rand_per_sum", "all_swings_rand_pp_sum", "all_swings_rand_np_sum", "t_10_lrg_pp_rand_sp_sum", "t_10_lrg_np_rand_sp_sum", "t_10_sml_pp_rand_sp_sum", "t_10_sml_np_rand_sp_sum", "all_swings_zero_rand_count", "all_swings_zero_rand_pp_count", "all_swings_zero_rand_np_count", "all_swings_zero_rand_pp_sum", "all_swings_zero_rand_np_sum", "all_swing_zero_rand_per_sum", "t_10_lrg_pp_zero_rand_sp_sum", "t_10_lrg_np_zero_rand_sp_sum", "t_10_sml_pp_zero_rand_sp_sum", "t_10_sml_np_zero_rand_sp_sum", "rand_pp_cnt_0_to_0_25_lst", "rand_pp_cnt_0_25_to_0_5_lst",
                                    "rand_pp_cnt_0_to_0_5_lst", "rand_pp_cnt_0_5_to_1_lst", "rand_pp_cnt_1_to_1_5_lst", "rand_pp_cnt_0_5_to_1_5_lst", "rand_pp_cnt_1_5_to_3_5_lst", "rand_pp_cnt_3_5_to_7_lst", "rand_pp_cnt_7_to_15_lst", "rand_np_cnt_0_to_0_25_lst", "rand_np_cnt_0_25_to_0_5_lst", "rand_np_cnt_0_to_0_5_lst", "rand_np_cnt_0_5_to_1_lst", "rand_np_cnt_1_to_1_5_lst", "rand_np_cnt_0_5_to_1_5_lst", "rand_np_cnt_1_5_to_3_5_lst", "rand_np_cnt_3_5_to_7_lst", "rand_np_cnt_7_to_15_lst", "all_swing_avg_time", "pstv_swing_avg_time", "neg_swing_avg_time", "top_10_lrg_pstv_total_rand_per_change", "top_10_lrg_pstv_avg_time", "top_10_sml_pstv_total_rand_per_change", "top_10_sml_pstv_avg_time", "top_10_lrg_neg_avg_time", "top_10_sml_neg_avg_time", "zero_rand_avg_swings_time", "zero_rand_pstv_sp_avg_swings_time", "zero_rand_neg_sp_avg_swings_time", "all_swing_avg_rsi_diff", "pstv_swing_avg_rsi_diff", "neg_swing_avg_rsi_diff", "top_10_lrg_pstv_avg_rsi_diff", "top_10_sml_pstv_avg_rsi_diff", "top_10_lrg_neg_avg_rsi_diff", "top_10_sml_neg_avg_rsi_diff", "zero_rand_avg_swings_rsi_diff", "zero_rand_pstv_sp_avg_rsi_diff", "zero_rand_neg_sp_avg_swings_rsi_diff", "total_fb", "total_pstv_fb", "total_neg_fb"],
                            engine='openpyxl')
                worksheet = writer.sheets[sheet_name]
                for idx, col in enumerate(df):
                    series = df[col]
                    max_len = max((series.astype(str).map(
                        len).max(), len(str(series.name)))) + 5
                    worksheet.column_dimensions[number_to_excel_column(
                        idx + 1)].width = min(max_len, 60)
            elif sheet_name == "rank_5":
                df.to_excel(writer, sheet_name=sheet_name, index=False,
                            header=["Rank", "coin_name", "coin_time_tf",
                                    "coin_score", "coin_stop_loss", "coin_step"],
                            engine='openpyxl')
                worksheet = writer.sheets[sheet_name]
                for idx, col in enumerate(df):
                    series = df[col]
                    max_len = max((series.astype(str).map(
                        len).max(), len(str(series.name)))) + 5
                    worksheet.column_dimensions[number_to_excel_column(
                        idx + 1)].width = min(max_len, 60)
            elif sheet_name == "rank_5_data":
                df.to_excel(writer, sheet_name=sheet_name, index=False,
                            header=["Rank", "coin_name", "coin_time_tf", "last_swing_per", "last_swing_rand_per", "last_swing_time", "last_swing_rsi_dif", "last_3_s_per_avg", "last_3_s_rand_avg", "last_3_s_avg_time", "last_3_s_rsi_diff_avg", "all_swing_count", "all_swings_pp_count", "all_swings_np_count", "all_swings_pp_avg", "all_swings_np_avg", "t_10_lrg_pp_sp_avg", "t_10_lrg_np_sp_avg", "t_10_sml_pp_sp_avg", "t_10_sml_np_sp_avg", "sp_pp_cnt_0_2_lst", "sp_pp_cnt_2_4_lst", "sp_pp_cnt_4_7_lst", "sp_pp_cnt_7_15_lst", "sp_pp_cnt_15_25_lst", "sp_np_cnt_0_2_lst", "sp_np_cnt_2_4_lst", "sp_np_cnt_4_7_lst", "sp_np_cnt_7_15_lst", "sp_np_cnt_15_25_lst", "all_swings_rand_pp_avg", "all_swings_rand_np_avg", "t_10_lrg_pp_rand_sp_avg", "t_10_lrg_np_rand_sp_avg", "t_10_sml_pp_rand_sp_avg", "t_10_sml_np_rand_sp_avg", "all_swings_zero_rand_count", "all_swings_zero_rand_pp_count", "all_swings_zero_rand_np_count", "all_swings_zero_rand_pp_mean", "all_swings_zero_rand_np_mean", "t_10_lrg_pp_zero_rand_sp_avg", "t_10_lrg_np_zero_rand_sp_avg", "t_10_sml_pp_zero_rand_sp_avg", "t_10_sml_np_zero_rand_sp_avg", "rand_pp_cnt_0_to_0_25_lst", "rand_pp_cnt_0_25_to_0_5_lst", "rand_pp_cnt_0_to_0_5_lst",
                                    "rand_pp_cnt_0_5_to_1_lst", "rand_pp_cnt_1_to_1_5_lst", "rand_pp_cnt_0_5_to_1_5_lst", "rand_pp_cnt_1_5_to_3_5_lst", "rand_pp_cnt_3_5_to_7_lst", "rand_pp_cnt_7_to_15_lst", "rand_np_cnt_0_to_0_25_lst", "rand_np_cnt_0_25_to_0_5_lst", "rand_np_cnt_0_to_0_5_lst", "rand_np_cnt_0_5_to_1_lst", "rand_np_cnt_1_to_1_5_lst", "rand_np_cnt_0_5_to_1_5_lst", "rand_np_cnt_1_5_to_3_5_lst", "rand_np_cnt_3_5_to_7_lst", "rand_np_cnt_7_to_15_lst", "all_swing_avg_time", "pstv_swing_avg_time", "neg_swing_avg_time", "top_10_lrg_pstv_total_rand_per_change", "top_10_lrg_pstv_avg_time", "top_10_sml_pstv_total_rand_per_change", "top_10_sml_pstv_avg_time", "top_10_lrg_neg_avg_time", "top_10_sml_neg_avg_time", "zero_rand_avg_swings_time", "zero_rand_pstv_sp_avg_swings_time", "zero_rand_neg_sp_avg_swings_time", "all_swing_avg_rsi_diff", "pstv_swing_avg_rsi_diff", "neg_swing_avg_rsi_diff", "top_10_lrg_pstv_avg_rsi_diff", "top_10_sml_pstv_avg_rsi_diff", "top_10_lrg_neg_avg_rsi_diff", "top_10_sml_neg_avg_rsi_diff", "zero_rand_avg_swings_rsi_diff", "zero_rand_pstv_sp_avg_rsi_diff", "zero_rand_neg_sp_avg_swings_rsi_diff", "total_fb", "total_pstv_fb", "total_neg_fb"],
                            engine='openpyxl')
                worksheet = writer.sheets[sheet_name]
                for idx, col in enumerate(df):
                    series = df[col]
                    max_len = max((series.astype(str).map(
                        len).max(), len(str(series.name)))) + 5
                    worksheet.column_dimensions[number_to_excel_column(
                        idx + 1)].width = min(max_len, 60)
            elif sheet_name == "rank_6":
                df.to_excel(writer, sheet_name=sheet_name, index=False,
                            header=["Rank", "coin_name", "coin_time_tf",
                                    "coin_score", "coin_stop_loss", "coin_step"],
                            engine='openpyxl')
                worksheet = writer.sheets[sheet_name]
                for idx, col in enumerate(df):
                    series = df[col]
                    max_len = max((series.astype(str).map(
                        len).max(), len(str(series.name)))) + 5
                    worksheet.column_dimensions[number_to_excel_column(
                        idx + 1)].width = min(max_len, 60)
            elif sheet_name == "rank_6_data":
                df.to_excel(writer, sheet_name=sheet_name, index=False,
                            header=["Rank", "coin_name", "coin_time_tf", "last_swing_per", "last_swing_rand_per", "last_swing_time", "last_swing_rsi_dif", "last_3_s_per_avg", "last_3_s_rand_avg", "last_3_s_avg_time", "last_3_s_rsi_diff_avg", "all_swing_count", "all_swings_pp_count", "all_swings_np_count", "all_swings_pp_med", "all_swings_np_med", "t_10_lrg_pp_sp_med", "t_10_lrg_np_sp_med", "t_10_sml_pp_sp_med", "t_10_sml_np_sp_med", "sp_pp_cnt_0_2_lst", "sp_pp_cnt_2_4_lst", "sp_pp_cnt_4_7_lst", "sp_pp_cnt_7_15_lst", "sp_pp_cnt_15_25_lst", "sp_np_cnt_0_2_lst", "sp_np_cnt_2_4_lst", "sp_np_cnt_4_7_lst", "sp_np_cnt_7_15_lst", "sp_np_cnt_15_25_lst", "all_swings_rand_pp_med", "all_swings_rand_np_med", "t_10_lrg_pp_rand_sp_med", "t_10_lrg_np_rand_sp_med", "t_10_sml_pp_rand_sp_med", "t_10_sml_np_rand_sp_med", "all_swings_zero_rand_count", "all_swings_zero_rand_pp_count", "all_swings_zero_rand_np_count", "all_swings_zero_rand_pp_med", "all_swings_zero_rand_np_med", "t_10_lrg_pp_zero_rand_sp_med", "t_10_lrg_np_zero_rand_sp_med", "t_10_sml_pp_zero_rand_sp_med", "t_10_sml_np_zero_rand_sp_med", "rand_pp_cnt_0_to_0_25_lst", "rand_pp_cnt_0_25_to_0_5_lst", "rand_pp_cnt_0_to_0_5_lst",
                                    "rand_pp_cnt_0_5_to_1_lst", "rand_pp_cnt_1_to_1_5_lst", "rand_pp_cnt_0_5_to_1_5_lst", "rand_pp_cnt_1_5_to_3_5_lst", "rand_pp_cnt_3_5_to_7_lst", "rand_pp_cnt_7_to_15_lst", "rand_np_cnt_0_to_0_25_lst", "rand_np_cnt_0_25_to_0_5_lst", "rand_np_cnt_0_to_0_5_lst", "rand_np_cnt_0_5_to_1_lst", "rand_np_cnt_1_to_1_5_lst", "rand_np_cnt_0_5_to_1_5_lst", "rand_np_cnt_1_5_to_3_5_lst", "rand_np_cnt_3_5_to_7_lst", "rand_np_cnt_7_to_15_lst", "all_swing_median_time", "pstv_swing_median_time", "neg_swing_median_time", "top_10_lrg_pstv_total_rand_per_change", "top_10_lrg_pstv_median_time", "top_10_sml_pstv_total_rand_per_change", "top_10_sml_pstv_median_time", "top_10_lrg_neg_median_time", "top_10_sml_neg_median_time", "zero_rand_med_swings_time", "zero_rand_pstv_sp_med_swings_time", "zero_rand_neg_sp_med_swings_time", "all_swing_median_rsi_diff", "pstv_swing_median_rsi_diff", "neg_swing_median_rsi_diff", "top_10_sml_pstv_median_rsi_diff", "top_10_lrg_neg_median_rsi_diff", "top_10_sml_neg_median_rsi_diff", "zero_rand_med_swings_rsi_diff", "zero_rand_pstv_sp_med_swings_rsi_diff", "zero_rand_neg_sp_med_swings_rsi_diff", "total_fb", "total_pstv_fb", "total_neg_fb"],
                            engine='openpyxl')
                worksheet = writer.sheets[sheet_name]
                for idx, col in enumerate(df):
                    series = df[col]
                    max_len = max((series.astype(str).map(
                        len).max(), len(str(series.name)))) + 5
                    worksheet.column_dimensions[number_to_excel_column(
                        idx + 1)].width = min(max_len, 60)
            else:
                print("No data Available in the Excel")
    print("Excel file created successfully.")
