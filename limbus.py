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
#製作question select.py處理選到question內的事務
#製作select encounter card處理打完boss後選擇好處
#製作選擇ego
#製作sinner select.py進行選角
#製作select dreamin star.py選擇卡片
#製作選擇初始ego gift
while True:
    if not is_paused:
        try:
            #pyautogui.moveTo(1000, 800)
            # 擷取遊戲畫面
            window.activate()
            gray, frame = screenshot.screenshot("LimbusCompany")

            # 判斷是否找到 attack.png
            loc, template = input_pic.match_template(gray, "auto_attack.png")
            if loc[0].size > 0:
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
                x, y = loc[1][0], loc[0][0]
                x, y = press.window_cal(x, y, template)
                press.move_click(x, y)
            
            # 判斷是否找到 battle.png
            loc, template = input_pic.match_template(gray, "battle.png")
            if loc[0].size > 0:
                print("進入戰鬥")
                press.press_keys(["enter"])
            
            #判斷找到confrim.png
            loc, template = input_pic.match_template(gray, "card_confirm.png")
            if loc[0].size > 0:
                print("找到 confirm.png！")
                x, y = loc[1][0], loc[0][0]
                x, y = press.window_cal(x, y, template)
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
            """
            # 判斷是否找到 inmirror.png
            loc, template = input_pic.match_template(gray, "inmirror.png")
            if loc[0].size > 0:
                ###增加點一下火車頭
                sleep(2)
                print("在mirror中，選擇關卡")
                if mission.select():  # 傳入視窗物件
                    print("成功選擇關卡！")
            """
            # 判斷是否找到 inshop.png
            loc, template = input_pic.match_template(gray, "inshop.png")
            if loc[0].size > 0:
                print("在shop中，準備離開")
                if mission.shop():  # 傳入視窗物件
                    print("離開商店！")
            #cv2.imshow("test", gray)
            cv2.waitKey(1)

        except Exception as e:
            print(f"錯誤：{e}")

        #print("執行中...")
        time.sleep(1)
    else:
        time.sleep(0.1)
