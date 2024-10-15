import pyautogui
import time
import tkinter as tk
from tkinter import messagebox

from utils.json_ops import load_json_from_file
default_values_file_path = 'default_values\default_values.json'
# Read the Json File
stored_default_value_dict = load_json_from_file(default_values_file_path)

if not stored_default_value_dict:
    pass
else:
    from default_values.constants import vts_software_folder_path, wait_time_sec, calender_1_tf, calender_2_tf, calender_5_tf, go_to_calender, choose_date, go_to_button, arrow_button, export_chart, chart_button, one_TF_chart, two_TF_chart, five_TF_chart, export_button, initial_click, indicator_click, dots_click, add_alert, nh_create_button, click_condition, choose_low, nl_create_button


def display_position():
    try:
        pyautogui.sleep(5)
        check_position_x, check_position_y = pyautogui.position()
        cursor_positions = f"X = {check_position_x},  Y = {check_position_y}"
        pyautogui.alert(text=cursor_positions,
                        title='Cursor Position', button='OK')
        return cursor_positions
    except Exception as e:
        return {"Status": f"unable display coordinate due to : {e}"}

# Note make sure the select calender in a right place


def select_date(go_to_calender, choose_date, go_to_button):
    # pyautogui.sleep(2)
    go_to_calender_x = go_to_calender[0]
    go_to_calender_y = go_to_calender[1]
    choose_date_x = choose_date[0]
    choose_date_y = choose_date[1]
    go_to_button_x = go_to_button[0]
    go_to_button_y = go_to_button[1]
    pyautogui.moveTo(go_to_calender_x, go_to_calender_y, duration=0.25)
    pyautogui.click()
    pyautogui.sleep(0.15)
    pyautogui.moveTo(choose_date_x, choose_date_y, duration=0.25)
    pyautogui.click()
    pyautogui.sleep(0.2)
    pyautogui.moveTo(go_to_button_x, go_to_button_y, duration=0.25)
    pyautogui.click()
    pyautogui.sleep(0.2)


def calender_click_fun(calender_click):
    calender_click_x = calender_click[0]
    calender_click_y = calender_click[1]
    pyautogui.moveTo(calender_click_x, calender_click_y, duration=0.5)
    pyautogui.click()
    pyautogui.sleep(0.2)


def auto_download_excel(total_charts, select_time_frame):

    pyautogui.sleep(2.5)
    if select_time_frame == 1:
        charts_positions = one_TF_chart
        calender_clicks = calender_1_tf
    elif select_time_frame == 2:
        charts_positions = two_TF_chart
        calender_clicks = calender_2_tf
    elif select_time_frame == 5:
        charts_positions = five_TF_chart
        calender_clicks = calender_5_tf
    else:
        return f"Please Enter Valid select_time_frame, Note:  Enter 3 or 720 "

    click_duration = 0.15

    def chart_wise_click(charts_position):
        chart_1_x, chart_1_y = charts_position[0], charts_position[1]
        pyautogui.moveTo(chart_1_x, chart_1_y, duration=0.5)
        pyautogui.click()

    def auto_download_excel_pos(charts_position):
        arrow_button_x = arrow_button[0]
        arrow_button_y = arrow_button[1]
        pyautogui.moveTo(arrow_button_x, arrow_button_y,
                         duration=click_duration)
        pyautogui.click()

        export_chart_x = export_chart[0]
        export_chart_y = export_chart[1]
        pyautogui.moveTo(export_chart_x, export_chart_y,
                         duration=click_duration)
        pyautogui.click()
        pyautogui.sleep(0.75)
        # chart_button_x = chart_button[0]
        # chart_button_y = chart_button[1]
        # pyautogui.moveTo(chart_button_x, chart_button_y,
        #                  duration=click_duration)
        # pyautogui.click()

        # chart_wise_click(charts_position)

        export_button_x = export_button[0]
        export_button_y = export_button[1]
        pyautogui.moveTo(export_button_x, export_button_y,
                         duration=click_duration)
        pyautogui.click()
        pyautogui.sleep(0.75)

    def go_to_next_chart():
        pyautogui.press('down')
        if select_time_frame == 1:
            pyautogui.sleep(1.5)
        else:
            pyautogui.sleep(3)

    total_start = time.time()
    for i in range(1, total_charts+1):
        start = time.time()
        for charts_position, calender_click in zip(charts_positions, calender_clicks):
            print("charts_position", charts_position)
            print("calender_click", calender_click)
            # calender_click_fun(calender_click)
            # select_date(go_to_calender, choose_date, go_to_button)
            # pyautogui.sleep(1)
            auto_download_excel_pos(charts_position)
        end = time.time()
        print(f"Time taken by {i} chart is : {end-start} secs")
        go_to_next_chart()
    messagebox.showinfo("Info", "Auto Download Completed Successfully !!!")
    pyautogui.sleep(0.01)
    pyautogui.press('enter')
    total_end = time.time()
    time_in_min = (total_end-total_start)/60
    return f"Successfully Downloaded !! Time taken for Download {total_charts} Charts is : {time_in_min} Min"


def auto_alarm(total_charts, select_time_frame):
    pyautogui.sleep(2.5)
    if select_time_frame == 1:
        pass
    else:
        return f"Select Time Frame should be 1 "

    click_duration = 0.5

    def go_to_next_chart():
        pyautogui.press('down')
        if select_time_frame == 1:
            pyautogui.sleep(1.5)
        else:
            pyautogui.sleep(3)

    def set_alerts():
        sleep_time = 0.1
        # initial_click = [782, 443]
        initial_click_x, initial_click_y = initial_click[0], initial_click[1]
        pyautogui.moveTo(initial_click_x, initial_click_y,
                         duration=click_duration)
        pyautogui.click()
        # pyautogui.sleep(sleep_time)

        # indicator_click = [237, 152]
        indicator_click_x, indicator_click_y = indicator_click[0], indicator_click[1]
        pyautogui.moveTo(indicator_click_x, indicator_click_y,
                         duration=click_duration)
        pyautogui.click()
        # pyautogui.sleep(sleep_time)

        # For High Code
        # dots_click = [417, 151]
        dots_click_x, dots_click_y = dots_click[0], dots_click[1]
        pyautogui.moveTo(dots_click_x, dots_click_y,
                         duration=click_duration)
        pyautogui.click()
        pyautogui.sleep(0.25)

        # add_alert = [631, 195]
        add_alert_x, add_alert_y = add_alert[0], add_alert[1]
        pyautogui.moveTo(add_alert_x, add_alert_y,
                         duration=click_duration)
        pyautogui.click()
        # pyautogui.sleep(sleep_time)

        # nh_create_button = [1184, 961]
        nh_create_button_x, nh_create_button_y = nh_create_button[0], nh_create_button[1]
        pyautogui.moveTo(nh_create_button_x, nh_create_button_y,
                         duration=click_duration)
        pyautogui.click()
        # pyautogui.sleep(sleep_time)

        # For Low code
        # dots_click = [417, 151]
        dots_click_x, dots_click_y = dots_click[0], dots_click[1]
        pyautogui.moveTo(dots_click_x, dots_click_y,
                         duration=click_duration)
        pyautogui.click()
        pyautogui.sleep(0.5)

        # add_alert = [631, 195]
        add_alert_x, add_alert_y = add_alert[0], add_alert[1]
        pyautogui.moveTo(add_alert_x, add_alert_y,
                         duration=click_duration)
        pyautogui.click()
        # pyautogui.sleep(sleep_time)

        # click_condition = [984, 344]
        click_condition_x, click_condition_y = click_condition[0], click_condition[1]
        pyautogui.moveTo(click_condition_x, click_condition_y,
                         duration=click_duration)
        pyautogui.click()
        # pyautogui.sleep(sleep_time)

        # choose_low = [979, 120]
        choose_low_x, choose_low_y = choose_low[0], choose_low[1]
        pyautogui.moveTo(choose_low_x, choose_low_y,
                         duration=click_duration)
        pyautogui.click()
        # pyautogui.sleep(sleep_time)

        # nl_create_button = [1184, 961]
        nl_create_button_x, nl_create_button_y = nl_create_button[0], nl_create_button[1]
        pyautogui.moveTo(nl_create_button_x, nl_create_button_y,
                         duration=click_duration)
        pyautogui.click()
        # pyautogui.sleep(sleep_time)

        # For Lower High
        # dots_click = [417, 151]
        dots_click_x, dots_click_y = dots_click[0], dots_click[1]
        pyautogui.moveTo(dots_click_x, dots_click_y,
                         duration=click_duration)
        pyautogui.click()
        pyautogui.sleep(0.5)

        # add_alert = [631, 195]
        add_alert_x, add_alert_y = add_alert[0], add_alert[1]
        pyautogui.moveTo(add_alert_x, add_alert_y,
                         duration=click_duration)
        pyautogui.click()
        # pyautogui.sleep(sleep_time)

        # click_condition = [984, 344]
        click_condition_x, click_condition_y = click_condition[0], click_condition[1]
        pyautogui.moveTo(click_condition_x, click_condition_y,
                         duration=click_duration)
        pyautogui.click()
        # pyautogui.sleep(sleep_time)

        # choose_low = [979, 120]
        choose_low_x, choose_low_y = 967, 203
        pyautogui.moveTo(choose_low_x, choose_low_y,
                         duration=click_duration)
        pyautogui.click()
        # pyautogui.sleep(sleep_time)

        # nl_create_button = [1184, 961]
        nl_create_button_x, nl_create_button_y = nl_create_button[0], nl_create_button[1]
        pyautogui.moveTo(nl_create_button_x, nl_create_button_y,
                         duration=click_duration)
        pyautogui.click()
        # pyautogui.sleep(sleep_time)

        # For Higher Low code
        # dots_click = [417, 151]
        dots_click_x, dots_click_y = dots_click[0], dots_click[1]
        pyautogui.moveTo(dots_click_x, dots_click_y,
                         duration=click_duration)
        pyautogui.click()
        pyautogui.sleep(0.5)

        # add_alert = [631, 195]
        add_alert_x, add_alert_y = add_alert[0], add_alert[1]
        pyautogui.moveTo(add_alert_x, add_alert_y,
                         duration=click_duration)
        pyautogui.click()
        # pyautogui.sleep(sleep_time)

        # click_condition = [984, 344]
        click_condition_x, click_condition_y = click_condition[0], click_condition[1]
        pyautogui.moveTo(click_condition_x, click_condition_y,
                         duration=click_duration)
        pyautogui.click()
        # pyautogui.sleep(sleep_time)

        # choose_low = [979, 120]
        choose_low_x, choose_low_y = 921, 243
        pyautogui.moveTo(choose_low_x, choose_low_y,
                         duration=click_duration)
        pyautogui.click()
        # pyautogui.sleep(sleep_time)

        # nl_create_button = [1184, 961]
        nl_create_button_x, nl_create_button_y = nl_create_button[0], nl_create_button[1]
        pyautogui.moveTo(nl_create_button_x, nl_create_button_y,
                         duration=click_duration)
        pyautogui.click()
        # pyautogui.sleep(sleep_time)

    total_start = time.time()
    for i in range(1, total_charts+1):
        start = time.time()
        set_alerts()
        go_to_next_chart()
    messagebox.showinfo("Info", "Set Auto Alerts Completed Successfully !!!")
    pyautogui.sleep(0.01)
    pyautogui.press('enter')
    total_end = time.time()
    time_in_min = (total_end-total_start)/60
    return f"Set Auto Alerts Completed Successfully !! Time taken for Set Alerts {total_charts} Charts is : {time_in_min} Min"
