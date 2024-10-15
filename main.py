import time
import ast
import os
import glob
import json
from fastapi import FastAPI, Query, File, UploadFile, HTTPException, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from auto_download.auto_download import auto_download_excel, display_position, auto_alarm
from utils.json_ops import store_default_value_dict, load_json_from_file
from utils.csv_ops import check_path_total_csv, csv_files_info_1TF, csv_files_info_2TF, csv_files_info_5TF, delete_files_in_folders, missing_coins_lst, get_csv_file_size
from default_values.constants import default_values_file_path, vts_software_folder_path, layer_3_rank_1_col_weights, layer_3_rank_2_col_weights, layer_3_rank_3_col_weights, layer_3_rank_4_col_weights, layer_3_rank_5_col_weights, layer_3_rank_6_col_weights, layer_3_rank_1_col_names, layer_3_rank_2_col_names, layer_3_rank_3_col_names, layer_3_rank_4_col_names, layer_3_rank_5_col_names, layer_3_rank_6_col_names, btc_excel_folder_path
from data_analysis.analysis import layer_1_analysis, layer_2_analysis, layer_3_analysis, get_coin_rank_analysis
from data_analysis.excel_export import layer_1_2_excel_export, layer_3_rank_excel_export
from data_analysis.extraction import get_btc_last_3_swings_info, btc_last_swing_info, best_swing_per_rankings

# Create the Fast API app
app = FastAPI(
    title="VTS Trading Solutions",
    description="Vidyudaya Trading Solutions (VTS) software provides the best alt coins to trade every hour, with complete detailed statistical analysis.",
    version="1.0.0"
)

# Mount the static files directory
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Default Value Dictionary
default_value_dict = {"set_software_path": "NA",
                      "wait_time_sec": 0,
                      "set_calender_x_y_position": [0, 0, 0, 0, 0, 0],
                      "set_chart_x_y_positions": [0, 0, 0, 0, 0, 0, 0],
                      "output_excel_folder_path": "NA"}


# Know the cursor position
@app.get("/know_your_cursor/", tags=["Auto Download"])
def know_your_cursor():
    try:
        cursor_pos = display_position()
        return {"positions":  cursor_pos, "Status": "Display the Coordinates successful"}
    except Exception as e:
        return {"Status": f"unable display coordinate due to : {e}"}


@app.post("/set_default_values/", tags=["Auto Download"])
def set_default_values(
    vts_software_folder_path: str = Query(..., title="software download path", description='''please enter the software downloaded folder path''',
                                          example='''D:\\VTS_Software\\downloads\\auto_download_excels\\auto_download_excels_1TF'''),
    output_excel_folder_path: str = Query(..., title="output excel path", description='''please enter the output excel folder path''',
                                          example='''D:\\VTS_Software\\downloads\\output_excels\\output_excel_1TF'''),
    btc_excel_folder_path: str = Query(..., title="btc folder path", description='''please enter the btc folder path''',
                                       example='''D:\\VTS_Software\\downloads\\auto_download_excels\\btc_excels'''),
    wait_time_sec: int = Query(..., title="Waiting time in sec",
                               description='''Please enter wait time in sec for change tab''', example=5),
    calender_1_tf: list = Query(..., title="calender x and y positions", description='''Please enter calender_1_tf x,y position in a list format. 
    Ex: [[817,452]]'''),
    calender_2_tf: list = Query(..., title="calender x and y positions", description='''Please enter calender_2_tf x,y position in a list format. 
    Ex: [[521,582],[1257,523]]'''),
    calender_5_tf: list = Query(..., title="calender x and y positions", description='''Please enter calender_5_tf x,y position in a list format. 
    Ex: [[411,225],[883,306],[1380,288],[525,714],[1359,711]]'''),
    go_to_calender: list = Query(..., title="calender x and y positions", description='''Please enter go to calender x,y position in a list format. 
    Ex: [441,954]'''),
    choose_date: list = Query(..., title="choose date x and y positions", description='''Please enter date x,y position in a list format
    Ex: [866,617]'''),
    go_to_button: list = Query(..., title="go to button x and y positions", description='''Please enter go_to button x,y position in a list format
    Ex: [1084,853]'''),
    arrow_button: list = Query(..., title="arrow_button x and y positions", description='''Please enter arrow button x,y position in a list format. 
    Ex: [1609,75]'''),
    export_chart: list = Query(..., title="export_chart x and y positions", description='''Please enter export chart x,y position in a list format
    Ex: [1726,329]'''),
    chart_button: list = Query(..., title="chart_button x and y positions", description='''Please enter chart button x,y position in a list of list format
    Ex: [978,532]'''),
    one_TF_chart: list = Query(..., title="one_TF_chart x and y positions", description='''Please enter one timeframe chart x,y position in a list of list format
    Ex: [[1012,579]]'''),
    two_TF_chart: list = Query(..., title="two_TF_chart x and y positions", description='''Please enter two timeframe chart x,y position in a list of list format
    Ex: [[1012,579],[1008,621]]'''),
    five_TF_chart: list = Query(..., title="five_TF_chart x and y positions", description='''Please enter five timeframe chart x,y position in a list of list format
    Ex: [[1012,579],[1008,621],[1008,657],[1012,699],[1012,740]]'''),
    export_button: list = Query(..., title="export_button x and y positions", description='''Please enter export button x,y position in a list format
    Ex: [1142,708]'''),
    initial_click: list = Query(..., title="export_button x and y positions", description='''Please enter initial_click x,y position in a list format
    Ex: [782, 443]'''),
    indicator_click: list = Query(..., title="export_button x and y positions", description='''Please enter indicator_click x,y position in a list format
    Ex: [237,152]'''),
    dots_click: list = Query(..., title="export_button x and y positions", description='''Please enter dots_click x,y position in a list format
    Ex: [417,151]'''),
    add_alert: list = Query(..., title="export_button x and y positions", description='''Please enter add_alert x,y position in a list format
    Ex: [631,195]'''),
    high_low_create_button: list = Query(..., title="export_button x and y positions", description='''Please enter high_low_create_button x,y position in a list format
    Ex: [1184,961]'''),
    click_condition: list = Query(..., title="export_button x and y positions", description='''Please enter click_condition x,y position in a list format
    Ex: [984,344]'''),
    choose_low: list = Query(..., title="export_button x and y positions", description='''Please enter choose_low x,y position in a list format
    Ex: [979,120]''')
):
    try:
        default_value_dict["set_software_path"] = vts_software_folder_path
        default_value_dict["output_excel_folder_path"] = output_excel_folder_path
        default_value_dict["btc_excel_folder_path"] = btc_excel_folder_path
        default_value_dict["wait_time_sec"] = wait_time_sec
        default_value_dict["set_calender_x_y_position"] = [json.loads(calender_1_tf[0]), json.loads(calender_2_tf[0]), json.loads(
            calender_5_tf[0]), json.loads(go_to_calender[0]), json.loads(choose_date[0]), json.loads(go_to_button[0])]

        default_value_dict["set_chart_x_y_positions"] = [json.loads(arrow_button[0]), json.loads(export_chart[0]), json.loads(
            chart_button[0]), json.loads(one_TF_chart[0]), json.loads(two_TF_chart[0]), json.loads(five_TF_chart[0]), json.loads(export_button[0])]

        default_value_dict["auto_alert_positions"] = [json.loads(initial_click[0]), json.loads(indicator_click[0]), json.loads(
            dots_click[0]), json.loads(add_alert[0]), json.loads(high_low_create_button[0]), json.loads(click_condition[0]), json.loads(choose_low[0])]

        store_default_value_dict(default_value_dict)
        return {"Response": default_value_dict, "Status": "All default positions set successful !!!"}
    except Exception as e:
        return {"Status": f"unable set the default values due to : {e}"}


@app.get("/get_default_values/", tags=["Auto Download"])
def check_default_values():
    try:
        stored_default_value_dict = load_json_from_file(
            default_values_file_path)
        if not stored_default_value_dict:
            return {"Response": "The Default value JSON file is empty. Please Set Default Values"}
        else:
            return {"Response": stored_default_value_dict}
    except Exception as e:
        return {"Status": f"unable to display default values due to : {e}"}


@app.get("/empty_auto_download_folders/", tags=["Auto Download"])
def empty_auto_download_folders():
    try:
        folders_to_clean = ["downloads\\auto_download_excels\\auto_download_excels_1TF",
                            "downloads\\auto_download_excels\\auto_download_excels_2TF", "downloads\\auto_download_excels\\auto_download_excels_5TF"]
        delete_files_in_folders(folders_to_clean)
        return {"Response": f"Delete all the files Successful !!!"}
    except Exception as e:
        return {"Response": f"Unable to delete the files in a folders due to : {e}"}


@app.post("/download_charts/", tags=["Auto Download"])
def auto_download_charts(
        select_time_frame: int = Query(..., title="Select Time Frame",
                                       description='''Please enter the Time Frame to Auto Download 1/2/5 Note: Please set the date first before auto download''', example=1),
        num_of_charts: int = Query(..., title="Chart Download",
                                   description='''Please Enter the Number of Chart to download From 1 to 296 Note: Please set the date first before auto download''', example=296)
):
    try:
        result = auto_download_excel(num_of_charts, select_time_frame)
        if select_time_frame == 1:
            expected_download_files = 1 * num_of_charts
        elif select_time_frame == 2:
            expected_download_files = 2 * num_of_charts
        elif select_time_frame == 5:
            expected_download_files = 5 * num_of_charts
        else:
            return {"Status": "Please Enter the valid Time Frame"}
        return {"Status": result, "Expected_download_files": expected_download_files}
    except Exception as e:
        return {"Status": f"Auto Download Failed due to : {e}"}


@app.get("/get_missing_coin_data/", tags=["File Operations"])
def get_missing_coin_data(
        Choose_Time_Frame: int = Query(..., title="Choose_Time_Frame",
                                       description='''Please Choose Time Frame Either 5 or 1''', example=2),
        csv_files_min_size: int = Query(..., title="csv_files_min_size", description='''Please Choose Minimum CSV file size in KB''', example=50)):
    if Choose_Time_Frame == 1:
        auto_download_excel_path = str(vts_software_folder_path)
    elif Choose_Time_Frame == 2:
        auto_download_excel_path = str(
            vts_software_folder_path).replace("1", "2")
    elif Choose_Time_Frame == 5:
        auto_download_excel_path = str(
            vts_software_folder_path).replace("1", "5")
    else:
        return {"Status": "Please Select Valid Time frame Either 1 or 5"}
    csv_files_with_size = get_csv_file_size(
        auto_download_excel_path)
    missing_coin_data = missing_coins_lst(
        csv_files_with_size, auto_download_excel_path, csv_files_min_size)
    return {"missing_coin_data": missing_coin_data}


@app.get("/analyse_excel_data/", tags=["Trading Analysis"])
def analyse_excel_data(
    Choose_Time_Frame: int = Query(..., title="Choose_Time_Frame",
                                   description='''Please Choose Time Frame Either 1/2/5''', example=2),
    output_excel_folder_path: str = Query(..., title="output excel path", description='''please enter the output excel folder path''',
                                          example='''D:\\VTS_Software\\downloads\\output_excels\\output_excel_1TF'''),
):
    start = time.time()
    try:
        # output_excel_folder_path = "D:\\VTS_Software\\downloads\\output_excels\\output_excel_1TF"
        if Choose_Time_Frame == 1:
            auto_download_excel_path = str(vts_software_folder_path)
            output_excel_folder_path = str(output_excel_folder_path)
        elif Choose_Time_Frame == 2:
            auto_download_excel_path = str(
                vts_software_folder_path).replace("1", "2")
            output_excel_folder_path = str(
                output_excel_folder_path).replace("1", "2")
        elif Choose_Time_Frame == 5:
            auto_download_excel_path = str(
                vts_software_folder_path).replace("1", "5")
            output_excel_folder_path = str(
                output_excel_folder_path).replace("1", "5")
        else:
            return {"Status": "Please Select Valid Time frame Either 1 or 5"}
        csv_files, total_csv_files_in_folder = check_path_total_csv(
            auto_download_excel_path)

        # Function calls
        layer_1_data, fb_coin_lst, fb_excel_lst, all_coin_price_lst = layer_1_analysis(
            auto_download_excel_path)

        swing_per_analysis_excel_lst, swing_pstv_per_range_excel_lst, swing_neg_per_range_excel_lst, swing_rand_per_analysis_excel_lst, swing_zero_rand_per_cluster_excel_lst, swing_pstv_rand_per_cluster_excel_lst, swing_neg_rand_per_cluster_excel_lst, swing_time_analysis_excel_lst, swing_rsi_diff_analysis_excel_lst, swing_fb_analysis_excel_lst = layer_2_analysis(
            layer_1_data, fb_coin_lst)

        layer_3_str_info_excel_lst, layer_3_rank_1_excel_lst, layer_3_rank_2_excel_lst, layer_3_rank_3_excel_lst, layer_3_rank_4_excel_lst, layer_3_rank_5_excel_lst, layer_3_rank_6_excel_lst = layer_3_analysis(
            layer_1_data, swing_per_analysis_excel_lst, swing_pstv_per_range_excel_lst, swing_neg_per_range_excel_lst, swing_rand_per_analysis_excel_lst, swing_zero_rand_per_cluster_excel_lst, swing_pstv_rand_per_cluster_excel_lst, swing_neg_rand_per_cluster_excel_lst, swing_time_analysis_excel_lst, swing_rsi_diff_analysis_excel_lst, swing_fb_analysis_excel_lst)

        layer_3_rank_1_lst, layer_3_rank_2_lst, layer_3_rank_3_lst, layer_3_rank_4_lst, layer_3_rank_5_lst, layer_3_rank_6_lst, layer_3_rank_7_lst, layer_3_rank_1_excel_lst_rank, layer_3_rank_2_excel_lst_rank, layer_3_rank_3_excel_lst_rank, layer_3_rank_4_excel_lst_rank, layer_3_rank_5_excel_lst_rank, layer_3_rank_6_excel_lst_rank = get_coin_rank_analysis(
            layer_3_rank_1_col_weights, layer_3_rank_2_col_weights, layer_3_rank_3_col_weights, layer_3_rank_4_col_weights, layer_3_rank_5_col_weights, layer_3_rank_6_col_weights, layer_3_rank_1_col_names, layer_3_rank_2_col_names, layer_3_rank_3_col_names, layer_3_rank_4_col_names, layer_3_rank_5_col_names, layer_3_rank_6_col_names, layer_3_rank_1_excel_lst, layer_3_rank_2_excel_lst, layer_3_rank_3_excel_lst, layer_3_rank_4_excel_lst, layer_3_rank_5_excel_lst, layer_3_rank_6_excel_lst)

        sort_last_s_excel_lst, sort_last_3_s_excel_lst = best_swing_per_rankings(
            layer_1_data, all_coin_price_lst)

        # # Layer_1 and Layer_2 excel export
        layer_1_2_excel_export(layer_1_data, fb_excel_lst, output_excel_folder_path, Choose_Time_Frame, swing_per_analysis_excel_lst, swing_pstv_per_range_excel_lst, swing_neg_per_range_excel_lst, swing_rand_per_analysis_excel_lst,
                               swing_zero_rand_per_cluster_excel_lst, swing_pstv_rand_per_cluster_excel_lst, swing_neg_rand_per_cluster_excel_lst, swing_time_analysis_excel_lst, swing_rsi_diff_analysis_excel_lst, swing_fb_analysis_excel_lst)

        # Layer_3 and ranking excel export
        layer_3_rank_excel_export(layer_3_str_info_excel_lst, layer_3_rank_1_excel_lst_rank, layer_3_rank_2_excel_lst_rank, layer_3_rank_3_excel_lst_rank, layer_3_rank_4_excel_lst_rank, layer_3_rank_5_excel_lst_rank,
                                  layer_3_rank_6_excel_lst_rank, output_excel_folder_path, Choose_Time_Frame, layer_3_rank_1_lst, layer_3_rank_2_lst, layer_3_rank_3_lst, layer_3_rank_4_lst, layer_3_rank_5_lst, layer_3_rank_6_lst, layer_3_rank_7_lst, sort_last_s_excel_lst, sort_last_3_s_excel_lst)

        top_50_coins_lst = [coin[1] for coin in (layer_3_rank_7_lst[:50] if len(
            layer_3_rank_7_lst) >= 50 else layer_3_rank_7_lst)]

        top_50_coins_lst = ["BYBIT:"+coin for coin in top_50_coins_lst]

        top_50_swing_per_lst = [coin[1] for coin in (sort_last_s_excel_lst[:50] if len(
            sort_last_s_excel_lst) >= 50 else sort_last_s_excel_lst)]

        top_50_swing_per_lst = ["BYBIT:" +
                                coin for coin in top_50_swing_per_lst]

        top_50_3_swing_per_lst = [coin[1] for coin in (sort_last_3_s_excel_lst[:50] if len(
            sort_last_3_s_excel_lst) >= 50 else sort_last_3_s_excel_lst)]

        top_50_3_swing_per_lst = ["BYBIT:" +
                                  coin for coin in top_50_3_swing_per_lst]

        top_50_swing_final_coins = top_50_swing_per_lst + \
            [item for item in top_50_3_swing_per_lst if item not in top_50_swing_per_lst]

        final_output_coins = top_50_swing_final_coins + \
            [item for item in top_50_coins_lst if item not in top_50_swing_final_coins]

        end = time.time()
        total_time_min = round(((end - start)/60), 2)
        return {"Status": f"Complete Chart data Extraction Successful for {total_csv_files_in_folder} Excel Files in {total_time_min} Secs",
                "top_50_random_rank_length": len(top_50_coins_lst),
                "top_50_last_swing_length": len(top_50_swing_per_lst),
                "top_50_last_3_swing_length": len(top_50_3_swing_per_lst),
                "final_output_coins_length": len(final_output_coins),
                "final_output_coins": final_output_coins,
                "Download_Excel_Path": output_excel_folder_path}
    except Exception as e:
        return {"Response": f"Unable to analyse data due to : {e}"}


@app.post("/set_auto_alerts/", tags=["Trading Analysis"])
def set_auto_alerts(
        select_time_frame: int = Query(..., title="Select Time Frame",
                                       description='''Please enter the Time Frame to Auto Download 1/2/5 Note: Please set the date first before auto download''', example=1),
        num_of_charts: int = Query(..., title="Chart Download",
                                   description='''Please Enter the Number of Chart to download From 1 to 298 Note: Please set the date first before auto download''', example=50)
):
    result = auto_alarm(num_of_charts, select_time_frame)
    return {"Status": result}


@app.get("/btc_swing_info/", tags=["Trading Analysis"])
def get_btc_last_3_swings_():
    btc_layer_1_data, btc_fb_lst, btc_fb_excel_lst, all_coin_price_lst = layer_1_analysis(
        btc_excel_folder_path)
    btc_last_three_swing_excel_lst = btc_last_swing_info(btc_layer_1_data)
    btc_last_3_swings = get_btc_last_3_swings_info(
        btc_last_three_swing_excel_lst)
    return {"BTC_3_swings_info": btc_last_3_swings, "BTC_last_3_False_breakouts": btc_fb_excel_lst[0][-3:]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
