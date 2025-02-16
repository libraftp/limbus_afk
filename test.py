import pyautogui
import time
import win32gui

def get_window_coordinates(window_title):
    """
    取得指定視窗的座標

    Args:
        window_title: 視窗標題 (字串)

    Returns:
        視窗的左上角和右下角座標 (tuple)，如果找不到視窗則返回 None
    """
    try:
        hwnd = win32gui.FindWindow(None, window_title)
        if hwnd == 0:
            return None
        rect = win32gui.GetWindowRect(hwnd)
        return rect
    except Exception as e:
        print(f"發生錯誤：{e}")
        return None

def print_mouse_coordinates_in_window(window_title):
    """
    持續印出滑鼠在指定視窗內的座標

    Args:
        window_title: 視窗標題 (字串)
    """
    while True:
        window_rect = get_window_coordinates(window_title)
        if window_rect is None:
            print(f"找不到視窗：{window_title}")
            return

        mouse_x, mouse_y = pyautogui.position()
        window_x1, window_y1, window_x2, window_y2 = window_rect

        if window_x1 <= mouse_x <= window_x2 and window_y1 <= mouse_y <= window_y2:
            x_in_window = mouse_x - window_x1
            y_in_window = mouse_y - window_y1
            print(f"滑鼠在 {window_title} 視窗內的座標：x={x_in_window}, y={y_in_window}")
        
        time.sleep(0.1)  # 每 0.1 秒更新一次座標

if __name__ == "__main__":
    window_title = "LimbusCompany"  # 請替換為您的視窗標題
    print_mouse_coordinates_in_window(window_title)