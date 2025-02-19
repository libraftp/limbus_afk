import requests
from bs4 import BeautifulSoup
import ssl

def search_course(course_code):
    """
    搜尋成功大學課程資訊並印出表格內容。

    Args:
        course_code: 要搜尋的課程代碼。
    """

    url = f"https://class-qry.acad.ncku.edu.tw/crm/course_map/course.php?dept=C6&cono={course_code}"

    try:
        context = ssl.create_default_context()
        context.set_ciphers('DEFAULT@SECLEVEL1')  # 嘗試設定 cipher

        response = requests.get(url, context=context)
        response.raise_for_status()

        response = requests.get(url)
        response.raise_for_status()  # 檢查HTTP狀態碼，確保請求成功

        soup = BeautifulSoup(response.content, "html.parser")

        # 找到 class 為 courseTable 的 table
        course_table = soup.find("table", class_="courseTable")

        if course_table:
            # 印出表格內容
            print(course_table.text.strip()) # strip() 移除多餘的空白和換行符號
        else:
            print(f"找不到課程代碼為 {course_code} 的課程資訊。")

    except requests.exceptions.RequestException as e:
        print(f"發生錯誤：{e}")
    except Exception as e:
        print(f"發生未知錯誤：{e}")


if __name__ == "__main__":
    course_code = "C510200"
    search_course(course_code)