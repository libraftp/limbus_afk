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
gray, frame = screenshot("LimbusCompany")