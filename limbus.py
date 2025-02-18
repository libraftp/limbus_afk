import time
import keyboard
import cv2
import input_pic  # 引入 input_pic.py
import screenshot  # 引入 screenshot.py
import press  # 引入 press.py
import mission  #引入mission.py
import pyautogui
from time import sleep
# 取得目標視窗
window_title = "LimbusCompany"

#一些參數設定
element = "pierce"
position = [2, 3]
sinner_order = [6, 7, 3, 9, 5, 1]
refresh_times = 3

###這三個不用改
reward = False
sinner_select = False
shop_refresh = False
# 取得視窗物件
window = press.get_window_object(window_title)

# 全域變數用於控制暫停狀態
is_paused = False

def toggle_pause():
    global is_paused
    is_paused = not is_paused
    print("程式暫停中..." if is_paused else "程式繼續執行中...")

# 綁定 Pause 鍵的監聽事件
keyboard.add_hotkey('pause', toggle_pause)

# 讀取模板圖片
input_pic.load_templates()
while True:
    if not is_paused:
        try:
            # 擷取遊戲畫面
            window.activate()
            gray, frame = screenshot.screenshot("LimbusCompany")

            loc, template = input_pic.match_template(gray, "home.png")
            if loc[0].size > 0:
                x, y = press.window_cal(405, 570, template)
                press.move_click(x, y)
                reward = False
                sinner_select = False
                shop_refresh = False

            loc, template = input_pic.match_template(gray, "mirror.png")
            if loc[0].size > 0:
                x, y = loc[1][0], loc[0][0] # 從 array([y]) 和 array([x]) 中取得 y, x 座標
                x, y = press.window_cal(x, y, template)
                press.move_click(x, y)

            # 判斷是否找到 attack.png
            loc, template = input_pic.match_template(gray, "auto_attack.png")
            if loc[0].size > 0:
                x, y = loc[1][0], loc[0][0] # 從 array([y]) 和 array([x]) 中取得 y, x 座標
                x, y = press.window_cal(x - 530, y, template)
                press.move_click(x, y)
                press.press_keys(["p", "enter"])
            
            # 不知道為甚麼位置很奇怪
            # 判斷是否找到 dungoen_enter.PNG
            loc, template = input_pic.match_template(gray, "dungoen_enter.png")
            if loc[0].size > 0:
                x, y = loc[1][0], loc[0][0] # 從 array([y]) 和 array([x]) 中取得 y, x 座標
                x, y = press.window_cal(x, y, template)
                press.move_click(x, y)
                time.sleep(0.5)
                press.press_keys(["enter"])
            
            # 判斷是否找到 dreamstar.png
            loc, template = input_pic.match_template(gray, "dreamstar.png")
            if loc[0].size > 0:
                print("選擇dreamstar中")
                if mission.dream_star(gray):
                    x, y = loc[1][0], loc[0][0]
                    x, y = press.window_cal(x, y, template)
                    press.move_click(x, y)
                    sleep(1)
                    press.press_keys(["enter"])

            # 判斷是否找到 team confirm.png
            loc, template = input_pic.match_template(gray, "team confirm.png")
            if loc[0].size > 0:
                print("確認隊伍")
                x, y = loc[1][0], loc[0][0]
                x, y = press.window_cal(x, y, template)
                press.move_click(x, y)
            

            # 判斷是否找到 battle.png
            loc, template = input_pic.match_template(gray, "battle.png")
            if loc[0].size > 0 and sinner_select:
                print("進入戰鬥")
                press.press_keys(["enter"])
                reward = True
            elif loc[0].size > 0:
                print("選擇出戰罪人")
                loc, template = input_pic.match_template(gray, "clear selection.png")
                if loc[0].size > 0:
                    x, y = loc[1][0], loc[0][0]
                    x, y = press.window_cal(x, y, template)
                    press.move_click(x, y)
                    sleep(0.3)
                    gray, frame = screenshot.screenshot("LimbusCompany")
                    loc, template = input_pic.match_template(gray, "window_confirm.png")
                    if loc[0].size > 0:
                        press.press_keys(["enter"])
                        press.press_keys(["enter"])
                        print("清除罪人選擇")

                mission.sinner(sinner_order, template)
                sinner_select = True
            
            #判斷找到confrim.png
            loc, template = input_pic.match_template(gray, "confirm.png", 0.7)
            re_loc, re_template = input_pic.match_template(gray, "reward_card.png")
            if loc[0].size > 0 and re_loc[0].size > 0 and reward:
                print("選擇獎勵")
                if mission.reward():
                    reward = False
            elif loc[0].size > 0:
                print("找到 confirm.png！")
                x, y = loc[1][0], loc[0][0]
                x, y = press.window_cal(x, y, template, window_title, 0, 0)
                press.move_click(x, y)

            #判斷是否找到 into.png
            loc, template = input_pic.match_template(gray, "into.png")
            if loc[0].size > 0:
                press.press_keys(["enter"])
            
            # 判斷是否找到 skip.png
            sk_loc, sk_template = input_pic.match_template(gray, "skip.png")
            if sk_loc[0].size > 0:
                print(sk_loc, "進入question任務中。")
                if mission.question(sk_loc, sk_template):
                    print("完成問號任務")
            
            # 判斷是否找到 inmirror.png
            loc, template = input_pic.match_template(gray, "inmirror.png")
            if loc[0].size > 0:
                ###增加點一下火車頭
                sleep(2)
                print("在mirror中，選擇關卡")
                if mission.select():  # 傳入視窗物件
                    print("成功選擇關卡！")
            
            # 判斷是否找到 inshop.png
            loc, template = input_pic.match_template(gray, "inshop.png")
            if loc[0].size > 0:
                print("在shop中")
                if mission.shop(element, shop_refresh):
                    print("離開商店！")
            
            #判斷找到select_ego_gift.png
            loc, template = input_pic.match_template(gray, "select_ego_gift.png")
            if loc[0].size > 0:
                print(f"選擇初始ego禮物，將選擇 {element}")
                if mission.initialEGOgift(gray, element, position):

                    print("選完初始ego")
            
            #判斷找到select_ego_gift.png
            loc, template = input_pic.match_template(gray, "warning ego.png")
            if loc[0].size > 0:
                mission.warningEGOgift(gray, element)

            #判斷找到theme pack.png
            loc, template = input_pic.match_template(gray, "theme pack.png")
            if loc[0].size > 0:
                print("選擇卡包")
                mission.pack_select(gray, refresh_times)
            
            loc, template = input_pic.match_template(gray, "exploration complete.png")
            if loc[0].size > 0:
                x, y = press.window_cal(720, 485, template)
                press.move_click(x, y)
            
            loc, template = input_pic.match_template(gray, "claim.png")
            if loc[0].size > 0:
                x, y = loc[1][0], loc[0][0]
                x, y = press.window_cal(x, y, template)
                press.move_click(x, y)
                sleep(3)
                press.press_keys(["enter"])


            #cv2.imshow("test", gray)
            cv2.waitKey(1)
        except Exception as e:
            print(f"錯誤：{e}")

        #print("執行中...")
        time.sleep(1)
    else:
        time.sleep(0.1)
