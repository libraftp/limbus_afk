import cv2
import os
import numpy as np

# 字典用於儲存讀取到的模板圖片
templates = {}

def load_templates():
    """讀取 "pic" 資料夾及其子資料夾中的所有圖片"""
    current_dir = os.path.dirname(__file__)
    pic_dir = os.path.join(current_dir, "pic")

    # 檢查 "pic" 資料夾是否存在
    if not os.path.exists(pic_dir):
        print(f"錯誤：找不到 'pic' 資料夾 {pic_dir}")
        return

    # 遍歷 "pic" 資料夾及其子資料夾
    for root, dirs, files in os.walk(pic_dir):
        for filename in files:
            if filename.endswith((".png")):  # 檢查檔案是否為圖片格式
                template_path = os.path.join(root, filename)
                try:
                    # 檢查是否已有相同檔名的圖片
                    if filename in templates:
                        raise ValueError(f"錯誤：圖片檔名重複：{filename} (位於 {template_path})")
                    
                    template = cv2.imread(template_path, 0)  # 以灰階模式讀取圖片
                    if template is None:
                        print(f"錯誤：無法讀取圖片 {template_path}")
                    else:
                        templates[filename] = template  # 將讀取到的圖片存儲到字典中
                except Exception as e:
                    print(f"讀取圖片 {template_path} 時發生錯誤：{e}")
    """
    for key, val in templates.items():
        print(key)
load_templates()
"""

def match_template(gray_frame, template_name, threshold=0.8):
    """取得指定名稱的模板圖片"""
    if template_name in templates:
        res = cv2.matchTemplate(gray_frame, templates[template_name], cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        return loc, templates[template_name]
    else:
        print(f"錯誤：找不到模板圖片 {template_name}")
        return None
