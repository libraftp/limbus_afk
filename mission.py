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
        ("warning.png", 0.7),
        ("shop.png", 0.6),
        ("question_task.png", 0.8),
        ("easy_battle.png", 0.6),
        ("normal_battle_d.png", 0.7),
    ]

    while True:
        gray, frame = screenshot.screenshot("LimbusCompany") # 每次都重新截圖
        for target, similar in targets:

            loc, template = input_pic.match_template(gray, "into.png")
            if loc is not None and loc[0].size > 0:
                press.press_keys(["enter"])
                return True  # 找到 "into.png"，結束函式
            
            loc, template = input_pic.match_template(gray, target, similar)
            if loc[0].size > 0:
                matches = loc[0].size  # 匹配到的目標數量
                for i in range(matches):
                    x, y = loc[1][i], loc[0][i]
                    x, y = press.window_cal(x, y, template)
                    press.move_click(x, y)
                    sleep(0.5)
                    # 檢查是否找到 "into.png"
                    gray, frame = screenshot.screenshot("LimbusCompany")
                    loc, template = input_pic.match_template(gray, "into.png")
                    if loc is not None and loc[0].size > 0:
                        press.press_keys(["enter"])
                        return True  # 找到 "into.png"，結束函式

def question(sk_loc, sk_template):
    """
    按照指定順序尋找並點擊圖片，直到找到 "into.png" 為止。
    """
    targets = [
        "select.png",
        "check.png",
    ]

    percentage = [
        "very high.png",
        "high.png",
        "normal.png",
    ]
    while True:
        gray, frame = screenshot.screenshot("LimbusCompany") # 每次都重新截圖
        
        # 判斷是否找到 choise.png
        loc, template = input_pic.match_template(gray, "choise.png")
        if loc[0].size > 0:
                    for target in targets:
                    #優先選擇select(不用拚點又有ego gift的)
                        loc, template = input_pic.match_template(gray, target)
                        if loc is not None and loc[0].size > 0:
                            matches = loc[0].size  # 匹配到的目標數量
                            print(target, matches)
                            for i in range(matches):
                                x, y = loc[1][i], loc[0][i]
                                x, y = press.window_cal(x, y, template)
                                press.move_click(x, y)
                    
        loc, template = input_pic.match_template(gray, "proceed.png")
        if loc[0].size > 0:
            x, y = loc[1][0], loc[0][0]
            x, y = press.window_cal(x, y, template)
            press.move_click(x, y)
        
        loc, template = input_pic.match_template(gray, "continue.png")
        if loc[0].size > 0:
            x, y = loc[1][0], loc[0][0]
            x, y = press.window_cal(x, y, template)
            press.move_click(x, y)
            return True
        
        else:
            print("沒東西")
            x, y = sk_loc[1][0], sk_loc[0][0]
            x, y = press.window_cal(x, y, sk_template)
            press.move_click(x, y)
            sleep(0.1)
            press.move_click(x, y)
            sleep(0.1)
            press.move_click(x, y)
                
        for target in percentage:
            loc, template = input_pic.match_template(gray, target)
            if loc is not None and loc[0].size > 0:
                matches = loc[0].size  # 匹配到的目標數量
                for i in range(matches):
                    x, y = loc[1][i], loc[0][i]
                    x, y = press.window_cal(x, y, template)
                    press.move_click(x, y)
                    sleep(0.5)

                    # 檢查是否找到 "commence.png"
                    gray, frame = screenshot.screenshot("LimbusCompany")
                    loc, template = input_pic.match_template(gray, "commence.png")
                    if loc[0].size > 0:
                        x, y = loc[1][0], loc[0][0]
                        x, y = press.window_cal(x, y, template)
                        press.move_click(x, y)
                        sleep(3)
                        return True

def shop():
    while True:
        gray, frame = screenshot.screenshot("LimbusCompany")
        loc, template = input_pic.match_template(gray, "leave.png")
        if loc[0].size > 0:
            x, y = loc[1][0], loc[0][0] # 從 array([y]) 和 array([x]) 中取得 y, x 座標
            x, y = press.window_cal(x, y, template)
            press.move_click(x, y)
            sleep(0.5)
            press.press_keys(["enter"])
            return True