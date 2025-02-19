import input_pic
import press
import screenshot  # 引入 screenshot 模組
from time import sleep
import pyautogui

def select():
    """
    按照指定順序尋找並點擊圖片，直到找到 "into.png" 為止。
    """
    targets = [
        ("warning.png", 0.7),
        ("another_warning.png", 0.7),
        ("shop_u.png", 0.7),
        ("shop_d.png", 0.7),
        ("shop_m.png", 0.7),
        ("question_task_m.png", 0.8),
        ("question_task_u.png", 0.8),
        ("question_task_d.png", 0.8),
        ("easy_battle_m.png", 0.8),
        ("easy_battle_u.png", 0.8),
        ("easy_battle_d.png", 0.8),
        ("normal_battle_d.png", 0.7),
        ("normal_battle.png", 0.7),
        ("hard_battle_m.png", 0.8),
        ("hard_battle_u.png", 0.8),
        ("specific_battle.png", 0.8),
        ("specific_money_d.png", 0.8)
    ]

    while True:
        for target, similar in targets:
            gray, frame = screenshot.screenshot("LimbusCompany") # 每次都重新截圖
            se_gray, se_frame = screenshot.screenshot_region("LimbusCompany", (380, 80, 580, 550))
                    
            loc, template = input_pic.match_template(gray, "into.png")
            if loc is not None and loc[0].size > 0:
                press.press_keys(["enter"])
                return True  # 找到 "into.png"，結束函式
            
            loc, template = input_pic.match_template(gray, "battle.png")
            if loc[0].size > 0:
                return False
            
            loc, template = input_pic.match_template(gray, "skip.png")
            if loc[0].size > 0:
                return False
            
            loc, template = input_pic.match_template(gray, "finish_confirm.png")
            if loc[0].size > 0:
                return False
            
            loc, template = input_pic.match_template(gray, "confirm.png")
            if loc[0].size > 0:
                return False
            
            loc, template = input_pic.match_template(se_gray, target, similar)
            if loc[0].size > 0:
                matches = loc[0].size  # 匹配到的目標數量
                #print(target,matches, loc)
                for i in range(matches):
                    x, y = loc[1][i], loc[0][i]
                    #print(x, y)
                    x, y = press.window_cal(x + 380, y + 80, template)
                    press.move_click(x, y)
                    sleep(0.5)
                    # 檢查是否找到 "into.png"
                    gray, frame = screenshot.screenshot("LimbusCompany")
                    into_loc, into_template = input_pic.match_template(gray, "into.png")
                    if into_loc[0].size > 0:
                        press.press_keys(["enter"])
                        return True  # 找到 "into.png"，結束函式
            

def question(sk_loc, sk_template):
    """
#需要在修改一下判斷順序
    """
    targets = [
        "select.png",
        "check1.png",
        "check2.png",
        "gain.png"
    ]

    percentage = [
        "very high.png",
        "high.png",
        "normal.png",
    ]

    x, y = sk_loc[1][0], sk_loc[0][0]
    skipx, skipy = press.window_cal(x, y, sk_template)
    times = 0

    while True:
        gray, frame = screenshot.screenshot("LimbusCompany") # 每次都重新截圖
        operation = False

        loc, template = input_pic.match_template(gray, "proceed.png")
        if loc[0].size > 0:
            operation = True
            x, y = loc[1][0], loc[0][0]
            x, y = press.window_cal(x, y, template)
            press.move_click(x, y)
        
        loc, template = input_pic.match_template(gray, "continue.png")
        if loc[0].size > 0:
            operation = True
            x, y = loc[1][0], loc[0][0]
            x, y = press.window_cal(x, y, template)
            press.move_click(x, y)
            if finish:
                return True

        for target in targets:
        #優先選擇select(不用拚點又有ego gift的)
            loc, template = input_pic.match_template(gray, target, 0.7)
            if loc is not None and loc[0].size > 0:
                operation = True
                if target == "select.png":
                    finish = True
                x, y = loc[1][0], loc[0][0]
                x, y = press.window_cal(x, y, template)
                press.move_click(x, y)

        for target in percentage:
            loc, template = input_pic.match_template(gray, target)
            if loc is not None and loc[0].size > 0:
                x, y = loc[1][0], loc[0][0]
                x, y = press.window_cal(x, y, template)
                press.move_click(x, y)
                sleep(1)
                gray, frame = screenshot.screenshot("LimbusCompany")
                loc, template = input_pic.match_template(gray, "commence.png")
                if loc[0].size > 0:
                    x, y = loc[1][0], loc[0][0]
                    x, y = press.window_cal(x, y, template)
                    press.move_click(x, y)
                    sleep(5)
                    for i in range(3):
                        press.move_click(skipx, skipy)
                        sleep(0.5)
                    continue

        if times >= 20:
                x, y = press.window_cal(520, 290, sk_template)
                press.move_click(x, y)
                times = 0
        if not operation:
            print("沒東西")
            for i in range(3):
                press.move_click(skipx, skipy)
                sleep(0.1)
                times += 1

def attack():
    while True:
        gray, frame = screenshot.screenshot("LimbusCompany")
        loc, template = input_pic.match_template(gray, "auto_attack.png")
        if loc[0].size > 0:
            x, y = loc[1][0], loc[0][0] # 從 array([y]) 和 array([x]) 中取得 y, x 座標
            x, y = press.window_cal(x - 530, y, template)
            press.move_click(x, y)
            press.press_keys(["p", "enter"])
        
        # 判斷是否找到 skip.png
        sk_loc, sk_template = input_pic.match_template(gray, "skip.png")
        if sk_loc[0].size > 0:
            print(sk_loc, "進入question任務中。")
            if question(sk_loc, sk_template):
                print("完成問號任務")
        
        #判斷戰鬥是否結束
        loc, template = input_pic.match_template(gray, "loading.png")
        if loc[0].size > 0:
            print("戰鬥結束")
            return


def shop(element, shop_refresh):
    #可能還需要增加強化和購買功能
    while True:
        gray, frame = screenshot.screenshot("LimbusCompany")
        target_pic = element + "_s.png"

        loc, template = input_pic.match_template(gray, target_pic)
        matches = loc[0].size  # 匹配到的目標數量
        for i in range(matches):
            x, y = loc[1][i], loc[0][i]
            x, y = press.window_cal(x, y, template)
            press.move_click(x, y)
            sleep(0.5)
            x, y = press.window_cal(490, 420, template)
            press.move_click(x, y)
            sleep(0.5)
            press.move_click(x, y + 120)

        if shop_refresh:
            break

        gray, frame = screenshot.screenshot("LimbusCompany")
        loc, template = input_pic.match_template(gray, "shop refresh.png")
        if loc[0].size > 0:
            x, y = loc[1][0], loc[0][0]
            x, y = press.window_cal(x, y, template)
            press.move_click(x, y)
            shop_refresh = True
            sleep(2)

    loc, template = input_pic.match_template(gray, "leave.png")
    if loc[0].size > 0 and shop_refresh:
        x, y = loc[1][0], loc[0][0] # 從 array([y]) 和 array([x]) 中取得 y, x 座標
        x, y = press.window_cal(x, y, template)
        press.move_click(x, y)
        sleep(0.5)
        press.press_keys(["enter"])
        return True

def dream_star(gray):
    targets = [
        "card1.png",
        "card2.png",
        "card3.png",
        "card4.png",
    ]
    i = 0
    while True:
        for target in targets:
            loc, template = input_pic.match_template(gray, target)
            if loc[0].size > 0:
                x, y = loc[1][0], loc[0][0]
                x, y = press.window_cal(x, y, template)
                press.move_click(x, y)
                targets.remove(target)
                i += 1
            
            if i == 4:
                return True

def initialEGOgift(gray, element, position):
    target = element + ".png"
    target_pic = element + "_p.png"
    loc, template = input_pic.match_template(gray, "blood.png")
    x, y = loc[1][0], loc[0][0]
    x, y = press.window_cal(x, y, template)
    pyautogui.moveTo(x, y)

    check = True
    while check:
        gray, frame = screenshot.screenshot("LimbusCompany")
        loc, template = input_pic.match_template(gray, target, 0.9)
        if loc[0].size > 0:
            x, y = loc[1][0], loc[0][0]
            x, y = press.window_cal(x, y, template)
            press.move_click(x, y)
            check = False
        else:
            pyautogui.scroll(-50)
    
    target = {
        1: [589, 270],
        2: [589, 350],
        3: [589, 410]
    }

    sleep(0.5)
    gray, frame = screenshot.screenshot("LimbusCompany")
    loc, template = input_pic.match_template(gray, target_pic)
    if loc[0].size > 0:
        for po in position:
            x, y = target[po]
            x, y = press.window_cal(x, y, template)
            press.move_click(x, y)
            sleep(1)
    loc, template = input_pic.match_template(gray, "ego select.png")
    if loc[0].size > 0:
        x, y = loc[1][0], loc[0][0]
        x, y = press.window_cal(x, y, template)
        press.move_click(x, y)
    return True

def sinner(sinner_order, template):

    sinlist = {
        1: [140, 260],
        2: [230, 260],
        3: [310, 260],
        4: [390, 260],
        5: [480, 260],
        6: [560, 260],
        7: [140, 380],
        8: [230, 380],
        9: [310, 380],
        10: [390, 380],
        11: [480, 380],
        12: [560, 380]
    }

    for sin in sinner_order:
        x, y = sinlist[sin]
        x, y = press.window_cal(x, y, template)
        press.move_click(x, y)
        del sinlist[sin]

    for pos in sinlist.values():
        x, y = pos[0], pos[1]
        x, y = press.window_cal(x, y, template)
        press.move_click(x, y)

def reward():
    targets = [
        "ego gift.png",
        "money and ego.png",
        "money.png",
        "resource.png"
    ]

    gray, frame = screenshot.screenshot("LimbusCompany")
    for target in targets:
        loc, template = input_pic.match_template(gray, target)
        #print(loc)
        if loc[0].size > 0:
            x, y = loc[1][0], loc[0][0]
            x, y = press.window_cal(x, y, template)
            press.move_click(x, y)
            sleep(0.5)
            press.press_keys(["enter"])
            return True
        
def warningEGOgift(gray, element):
    target_pic = element + "_p.png"
    loc, template = input_pic.match_template(gray, target_pic, 0.7)
    if loc[0].size > 0:
        x, y = loc[1][0], loc[0][0]
        x, y = press.window_cal(x, y, template)
        press.move_click(x, y)
    else:
        x, y = press.window_cal(400, 340, template)
        press.move_click(x, y)
    
    loc, template = input_pic.match_template(gray, "ego select.png")
    x, y = loc[1][0], loc[0][0]
    x, y = press.window_cal(x, y, template)
    press.move_click(x, y)
    sleep(0.5)
    press.press_keys(["enter"])

def pack_select(refresh_times):

    pac = ["addicting lust.png",
           "addicting lust.png",
           "devoured gluttony.png",
           "emotional repression.png",
           "emotional subservience.png",
           "Flat-broke gamblers.png",
           "miracle in district 20.png",
           "pierceers and penetrators.png",
           "the magic sea.png",
           "to be cleaved.png",
           "to be pierced.png",
           "degraded gloom.png",
           "vield my flesh to.png"
           ]
    
    gray, frame = screenshot.screenshot("LimbusCompany")
    re_loc, re_template = input_pic.match_template(gray, "refresh.png", 0.7)
    x, y = re_loc[1][0], re_loc[0][0]
    rex, rey = press.window_cal(x, y, re_template)

    while refresh_times > 0:
        print(refresh_times)
        for pack in pac:
            loc, template = input_pic.match_template(gray, pack)
            if loc[0].size > 0:
                x, y = loc[1][0], loc[0][0]
                x, y = press.window_cal(x, y, template)
                press.move_and_drag_down(x, y)
                pac.remove(pack)
                return True
        
        press.move_click(rex, rey)
        refresh_times -= 1
        sleep(3)
        gray, frame = screenshot.screenshot("LimbusCompany")
    
    x, y = press.window_cal(400, 340, template)
    press.move_and_drag_down(x, y)