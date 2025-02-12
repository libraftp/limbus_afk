import time
import pyautogui
import pywinauto.mouse  # 引入 pywinauto.mouse 模組
import pygetwindow as gw
from pywinauto.application import Application
import numpy as np

# 全域變數用於儲存視窗物件
window = None

def get_window_object(window_title):
    """取得視窗物件"""
    global window
    try:
        window = gw.getWindowsWithTitle(window_title)[0]
        print(f"找到視窗: {window_title}")
        return window
    except IndexError:
        print("找不到指定的視窗")
        return None

def press_keys(keys):
    """按下指定的按鍵序列

    Args:
        keys: 一個包含要按下的按鍵的列表，例如 ["p", "enter"] 或 ["w", "a", "s", "d"]
    """
    if window is None:
        print("視窗物件尚未初始化")
        return

    for key in keys:
        window.activate()  # 切換到目標視窗
        pyautogui.press(key)  # 使用 pyautogui.press() 來模擬按鍵輸入
        time.sleep(0.1)  # 等待遊戲反應

def window_cal(x, y, template, window_title="LimbusCompany"):
    """將滑鼠移動到指定視窗的相對位置並點擊左鍵

    Args:
        target_loc: 模板匹配位置的座標 (tuple)
        template: 模板圖片 (numpy array)
        window_title: 視窗標題 (string)
    """
    app = Application(backend="uia").connect(title_re=window_title, timeout=5)
    window = app.window(title_re=window_title)

    window_rect = window.wrapper_object().rectangle()  # 使用 wrapper_object().rectangle()

    window_x = window_rect.left  # 視窗左上角 x 座標
    window_y = window_rect.top  # 視窗左上角 y 座標
    template_height, template_width = template.shape[:2]

    # 計算滑鼠要移動到的視窗相對位置 (將匹配位置加上模板中心偏移量)
    target_x_relative = x + template_width // 2  # 模板中心 x 座標
    target_y_relative = y + template_height // 2 # 模板中心 y 座標

    # 將視窗相對位置轉換為螢幕絕對位置
    target_x_absolute = window_x + target_x_relative
    target_y_absolute = window_y + target_y_relative

    return target_x_absolute, target_y_absolute

def move_click(x, y):
    #將滑鼠移動到指定視窗的相對位置並點擊左鍵
    pyautogui.moveTo(x, y)
    print(x, y)
    pyautogui.click()

def move_and_drag_down(x, y):
    """將滑鼠移動到指定位置並向下拖曳

    Args:
        x: 目標位置的 x 座標
        y: 目標位置的 y 座標
    """
    pyautogui.moveTo(x, y)  # 移動到指定位置
    pyautogui.mouseDown()  # 按下鼠標左鍵
    pyautogui.dragRel(0, 500, 1)  # 向下拖曳
    time.sleep(0.1)
    pyautogui.mouseUp()  # 放開鼠標左鍵