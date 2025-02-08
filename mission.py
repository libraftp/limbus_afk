import cv2
import input_pic
import press
import numpy as np
import screenshot  # 引入 screenshot 模組
from time import sleep
def select(): # 傳入視窗物件
    """
    按照指定順序尋找並點擊圖片，直到找到 "into.png" 為止。
    """
    targets = [
        "warning.png",
        "question_task.png",
        "easy_battle.png",
        "normal_battle.png",
        "specific_battle.png",
    ]

    while True:
        gray, frame = screenshot.screenshot("LimbusCompany") # 每次都重新截圖
        for target in targets:
            loc, template = input_pic.match_template(gray, target)
            if loc is not None and loc[0].size > 0:
                if loc[0].size == 1:  # 只有一個匹配位置
                    pt = (loc[1][0], loc[0][0])  # 提取座標
                    x, y = press.window_cal(np.array([pt]), template)
                    press.move_click(x, y)
                    sleep(0.5)
                    # 檢查是否找到 "into.png"
                    gray, frame = screenshot.screenshot("LimbusCompany")
                    loc, template = input_pic.match_template(gray, "into.png")
                    if loc is not None and loc[0].size > 0:
                        press.press_keys(["enter"])
                        return True  # 找到 "into.png"，結束函式
                    
                else:  # 有兩個或更多匹配位置
                    for pt in zip(*loc[::-1]):
                        x, y = press.window_cal(np.array([pt]), template)
                        press.move_click(x, y)
                        sleep(0.5)
                        # 檢查是否找到 "into.png"
                        gray, frame = screenshot.screenshot("LimbusCompany")
                        loc, template = input_pic.match_template(gray, "into.png")
                        if loc is not None and loc[0].size > 0:
                            press.press_keys(["enter"])
                            return True  # 找到 "into.png"，結束函式