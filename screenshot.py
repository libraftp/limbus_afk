import pygetwindow as gw
import pyautogui
import cv2
import numpy as np
import pygetwindow as gw
import pyautogui

def screenshot(window_title):
    # 找到目標視窗
    window = gw.getWindowsWithTitle(window_title)[0]
    if window is None:
        raise Exception(f"找不到視窗：{window_title}")

    # 獲取視窗尺寸
    left, top, width, height = window.left, window.top, window.width, window.height

    # 擷取視窗內容
    window.activate()  # 先將視窗激活
    screenshot = pyautogui.screenshot(region=(left, top, width, height))

    # 將截圖轉換為OpenCV圖像
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    return gray, frame

def screenshot_region(window_title, region):
    """
    擷取指定視窗指定區域的畫面。

    Args:
        window_title: 視窗標題 (字串)。
        region: 截圖區域，格式為 (left, top, width, height) 的 tuple。

    Returns:
        gray: 灰階圖像 (numpy array)。
        frame: 彩色圖像 (numpy array)。
    """
    # 找到目標視窗
    window = gw.getWindowsWithTitle(window_title)
    if not window:  # 檢查是否找到視窗
        raise Exception(f"找不到視窗：{window_title}")
    window = window[0]  # 取得第一個符合標題的視窗

    # 獲取視窗的左上角座標
    window_left, window_top = window.left, window.top

    # 計算截圖區域的絕對座標
    left = window_left + region[0]
    top = window_top + region[1]
    width = region[2] - region[0]  # 寬度
    height = region[3] - region[1]  # 高度

    # 擷取指定區域的視窗內容
    window.activate()  # 先將視窗激活
    screenshot = pyautogui.screenshot(region=(left, top, width, height))

    # 將截圖轉換為OpenCV圖像
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    return gray, frame