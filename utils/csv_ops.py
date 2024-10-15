import os
import glob
from typing import List, Tuple
import pandas as pd
from pandas import DataFrame
from datetime import datetime
from default_values.constants import binance_coins
import statistics


def check_path_total_csv(auto_download_excel_path) -> Tuple[List[str], int]:
    try:
        if os.path.isdir(auto_download_excel_path):
            files_in_folder = os.listdir(auto_download_excel_path)
            csv_files = [
                file for file in files_in_folder if file.endswith('.csv')]
            total_csv_files = len(csv_files)
            if csv_files:
                print(
                    f"Total {total_csv_files} CSV files Present in the Folder")
                print("========================================================")
            else:
                print("No CSV files found in the selected folder.")
        else:
            print(
                f"The folder path {auto_download_excel_path} does not exist or is not a directory.")
        return csv_files, total_csv_files
    except Exception as e:
        print(
            f"Error in check_path_total_csv path {auto_download_excel_path} {e}")


def get_csv_file_size(auto_download_excel_path) -> Tuple[List[str], int]:
    try:
        if os.path.isdir(auto_download_excel_path):
            files_in_folder = os.listdir(auto_download_excel_path)
            csv_files_with_size = [
                [filename, round(os.path.getsize(os.path.join(
                    auto_download_excel_path, filename)) / 1024, 2)]
                for filename in files_in_folder if filename.endswith('.csv')
            ]
            total_csv_files = len(csv_files_with_size)
            if csv_files_with_size:
                print(
                    f"Total {total_csv_files} CSV files Present in the Folder")
                print("========================================================")
            else:
                print("No CSV files found in the selected folder.")
        else:
            print(
                f"The folder path {auto_download_excel_path} does not exist or is not a directory.")
        return csv_files_with_size
    except Exception as e:
        print(
            f"Error in check_path_total_csv path {auto_download_excel_path} {e}")


def read_validate_csv_file(auto_download_excel_path, csv_file) -> Tuple[int, DataFrame]:
    try:
        file_path = os.path.join(auto_download_excel_path, csv_file)
        df = pd.read_csv(file_path)
        # df.dropna(inplace=True)
        print(f"{csv_file} file read success full")
        df_shape = df.shape
        print("df_shape ===>", df_shape)
    except Exception as e:
        print(f"Error reading {csv_file}: {e}")
        return 0
    try:
        if df_shape[1] == 18:
            columns_list = df.columns.tolist()
            if columns_list[-1] == "Plot":
                # Test: write the test case for 18 columns
                # df = df.dropna(subset=[df.columns[16]])
                df = df.drop(
                    df.columns[[9, 10, 11, 12, 13, 14, 15, 16]], axis=1)
                # print("The data frame is ==>", df.head())
                if df_shape[0] > 0:
                    print(f"{csv_file} file validation success full")
                    return 1, df
                else:
                    print(f"{csv_file} file contain the zero rows")
                    return 0
            else:
                return f"Plot Column not present in the data frame in: {csv_file} csv file"
        elif df_shape[1] == 14:
            columns_list = df.columns.tolist()
            if columns_list[-1] == "Plot":
                # Test: write the test case for 14 columns
                df = df.drop(df.columns[[9, 10, 11, 12]], axis=1)
                df = df.dropna(subset=[df.columns[12]])
                if df_shape[0] > 0:
                    print(f"{csv_file} file validation success full")
                    return 1, df
                else:
                    print(f"{csv_file} file contain the zero rows")
                    return 0
            else:
                return f"Plot Column not present in the data frame in: {csv_file} csv file"
        else:
            print(f"{csv_file} file not contain the 18 or 14 columns")
            return 0
    except Exception as e:
        print(f"{csv_file} file shape validation failed due to : {e}")


def csv_files_info_1TF(total_csv_files_in_folder, csv_files, auto_download_excel_path):
    total_charts = int(total_csv_files_in_folder)
    coin_5_lst = []
    for csv_file in csv_files:
        split_data = csv_file.split(".")
        coin_name = split_data[0][6:]
        tf_data_coma = split_data[1].split(",")
        tf_data_strip = tf_data_coma[1].strip()
        tf_data_under = tf_data_strip.split("_")
        coin_data = [coin_name + "." + tf_data_under[0], int(tf_data_under[0])]
        print(coin_data)
        if coin_data[1] == 5:
            coin_5_lst.append(coin_data)
        else:
            return {"Status": f"Valid Time Frame Data not Extracted !!!"}
    print("coin_5_lst ==>", coin_5_lst)
    return {
        "Auto_Download_CSV_Files_Location": auto_download_excel_path,
        "Total_CSV_Files_in_Folder": total_csv_files_in_folder,
        "Total_Charts_Data": total_charts,
        "Total_5min_TF_Files": [len(coin_5_lst), str(coin_5_lst)],
    }


def csv_files_info_2TF(total_csv_files_in_folder, csv_files, auto_download_excel_path):
    total_charts = total_csv_files_in_folder/2
    coin_5_lst = []
    coin_15_lst = []
    for csv_file in csv_files:
        split_data = csv_file.split(".")
        coin_name = split_data[0][6:]
        tf_data_coma = split_data[1].split(",")
        tf_data_strip = tf_data_coma[1].strip()
        tf_data_under = tf_data_strip.split("_")
        coin_data = [coin_name + "." + tf_data_under[0], int(tf_data_under[0])]
        if coin_data[1] == 5:
            coin_5_lst.append(coin_data)
        elif coin_data[1] == 15:
            coin_15_lst.append(coin_data)
        else:
            return {"Status": f"Valid Time Frame Data not Extracted !!!"}
    all_tf_files_dict = {"coin_5_TF_Files": coin_5_lst,
                         "coin_15_TF_Files": coin_15_lst}
    max_length = max(len(items) for items in all_tf_files_dict.values())
    if len(coin_5_lst) == len(coin_15_lst) == max_length:
        missing_auto_download_excel_status = "There is no missing Files, All Files are Downloaded"
    else:
        keys_with_max_length = [
            key for key, items in all_tf_files_dict.items() if len(items) == max_length]

        print(f"Maximum Array Length: {max_length}")
        print(f"Keys with Maximum Array Length: {keys_with_max_length}")

        items_in_max_arrays = set(
            item[0] for key in keys_with_max_length for item in all_tf_files_dict[key])
        missing_items_dict = {}

        for key, items in all_tf_files_dict.items():
            if len(items) < max_length:
                items_in_current_array = set(item[0] for item in items)
                missing_items = items_in_max_arrays - items_in_current_array
                missing_items_dict[key] = missing_items

        missing_auto_download_excel_status = f"These are the Missing Files in Auto Download {missing_items_dict}"

    return {
        "Auto_Download_CSV_Files_Location": auto_download_excel_path,
        "Total_CSV_Files_in_Folder": total_csv_files_in_folder,
        "Total_Charts_Data": total_charts,
        "Total_5min_TF_Files": [len(coin_5_lst), str(coin_5_lst)],
        "Total_15min_TF_Files": [len(coin_15_lst), str(coin_15_lst)],
        "missing_auto_download_excel_status": missing_auto_download_excel_status
    }


def csv_files_info_5TF(total_csv_files_in_folder, csv_files, auto_download_excel_path):
    total_charts = total_csv_files_in_folder/5
    coin_5_lst = []
    coin_15_lst = []
    coin_30_lst = []
    coin_60_lst = []
    coin_240_lst = []
    for csv_file in csv_files:
        split_data = csv_file.split(".")
        coin_name = split_data[0][6:]
        tf_data_coma = split_data[1].split(",")
        tf_data_strip = tf_data_coma[1].strip()
        tf_data_under = tf_data_strip.split("_")
        coin_data = [coin_name + "." + tf_data_under[0], int(tf_data_under[0])]
        if coin_data[1] == 5:
            coin_5_lst.append(coin_data)
        elif coin_data[1] == 15:
            coin_15_lst.append(coin_data)
        elif coin_data[1] == 30:
            coin_30_lst.append(coin_data)
        elif coin_data[1] == 60:
            coin_60_lst.append(coin_data)
        elif coin_data[1] == 240:
            coin_240_lst.append(coin_data)
        else:
            return {"Status": f"Valid Time Frame Data not Extracted !!!"}
    all_tf_files_dict = {"coin_5_TF_Files": coin_5_lst, "coin_15_TF_Files": coin_15_lst,
                         "coin_30_TF_Files": coin_30_lst, "coin_60_TF_Files": coin_60_lst,
                         "coin_240_TF_Files": coin_240_lst}
    max_length = max(len(items) for items in all_tf_files_dict.values())
    if len(coin_5_lst) == len(coin_15_lst) == len(coin_30_lst) == len(coin_60_lst) == len(coin_240_lst) == max_length:
        missing_auto_download_excel_status = "There is no missing Files, All Files are Downloaded"
    else:
        keys_with_max_length = [
            key for key, items in all_tf_files_dict.items() if len(items) == max_length]

        print(f"Maximum Array Length: {max_length}")
        print(f"Keys with Maximum Array Length: {keys_with_max_length}")

        items_in_max_arrays = set(
            item[0] for key in keys_with_max_length for item in all_tf_files_dict[key])
        missing_items_dict = {}

        for key, items in all_tf_files_dict.items():
            if len(items) < max_length:
                items_in_current_array = set(item[0] for item in items)
                missing_items = items_in_max_arrays - items_in_current_array
                missing_items_dict[key] = missing_items

        missing_auto_download_excel_status = f"These are the Missing Files in Auto Download {missing_items_dict}"

    return {
        "Auto_Download_CSV_Files_Location": auto_download_excel_path,
        "Total_CSV_Files_in_Folder": total_csv_files_in_folder,
        "Total_Charts_Data": total_charts,
        "Total_5min_TF_Files": [len(coin_5_lst), str(coin_5_lst)],
        "Total_15min_TF_Files": [len(coin_15_lst), str(coin_15_lst)],
        "Total_30min_TF_Files": [len(coin_30_lst), str(coin_30_lst)],
        "Total_60min_TF_Files": [len(coin_60_lst), str(coin_60_lst)],
        "Total_240min_TF_Files": [len(coin_240_lst), str(coin_240_lst)],
        "missing_auto_download_excel_status": missing_auto_download_excel_status
    }


def delete_files_in_folders(folders):
    for folder in folders:
        # Construct the path pattern to match all files in the folder
        pattern = os.path.join(folder, '*')  # Match all files in the folder

        # List all files matching the pattern
        files = glob.glob(pattern)

        # Delete each file
        for file_path in files:
            try:
                if os.path.isfile(file_path):  # Check if it's a file
                    os.remove(file_path)       # Delete the file
                    print(f"Deleted: {file_path}")
                else:
                    print(f"Skipped: {file_path} (not a file)")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")


def missing_coins_lst(csv_files_with_size, auto_download_excel_path, csv_files_min_size):
    coin_15_lst = []
    csv_files = [csv_file[0] for csv_file in csv_files_with_size]
    for csv_file in csv_files:
        split_data = csv_file.split(".")
        # Need to change the coin_name length for bybit
        coin_name = split_data[0][6:]
        tf_data_coma = split_data[1].split(",")
        tf_data_strip = tf_data_coma[1].strip()
        tf_data_under = tf_data_strip.split("_")
        coin_data = [coin_name + "." + "P", int(tf_data_under[0])]
        print(coin_data)
        if coin_data[1] == 15:
            coin_15_lst.append(coin_data)
        else:
            return {"Status": f"Valid Time Frame Data not Extracted !!!"}
    missing_coins = []
    downloaded_coins = [coin[0] for coin in coin_15_lst]
    downloaded_coins.sort()
    for coin in binance_coins:
        if coin not in downloaded_coins:
            missing_coins.append(coin)
    missing_coins.sort()
    # csv_files_avg_size = round(statistics.mean(
    #     [csv_file[1] for csv_file in csv_files_with_size]), 2)
    insufficient_size_files = [[csv_file[0], csv_file[1]]
                               for csv_file in csv_files_with_size if csv_file[1] <= csv_files_min_size]
    print("csv_files_avg_size ==>", csv_files_min_size)
    print("insufficient_size_files ==>", insufficient_size_files)
    return {
        "downloaded_files_Location": auto_download_excel_path,
        "Total_expected_coins": len(binance_coins),
        "Total_downloaded_coins": len(downloaded_coins),
        "Total_missing_coins": len(missing_coins),
        "Total_Insufficient_files": len(insufficient_size_files),
        "Insufficient_files": insufficient_size_files,
        "missing_coin_names": missing_coins,
        "downloaded_coin_names": downloaded_coins
    }
