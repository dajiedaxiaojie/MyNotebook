from playwright.sync_api import sync_playwright
import time
import csv

def scrape_page_data(page):
    results = []
    # 假設資料以表格或特定class區塊呈現，需根據網站實際結構調整selector
    rows = page.query_selector_all("table tbody tr")  # 或其他適合的選擇器
    for row in rows:
        cells = row.query_selector_all("td")
        if len(cells) < 9:
            continue
        data = {
            "國籍": cells[0].inner_text().strip(),
            "性別": cells[1].inner_text().strip(),
            "年齡": cells[2].inner_text().strip(),
            "希望工作類別": cells[3].inner_text().strip(),
            "希望工作區域": cells[4].inner_text().strip(),
            "媒合限制到期日": cells[5].inner_text().strip(),
            "公告到期日": cells[6].inner_text().strip(),
            "移工連絡電話": cells[7].inner_text().strip(),
            "詳細資料": cells[8].inner_text().strip(),
        }
        results.append(data)
    return results

def main():
    page_num = 0

    for i in range(page_num, 800):

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            url = "https://fw.wda.gov.tw/wda-employer/home/fortrans/foreign-labor"
            page.goto(url)

            all_data = []

            # 頁碼從36到63
            print(f"正在爬取第 {i} 頁")
            # 網站可能有分頁按鈕或頁碼輸入框，這裡示範點擊分頁按鈕
            # 先等待頁面載入
            # 等待分頁按鈕出現
            # page.wait_for_selector(f"button:has-text('{page_num}')", timeout=10000)
            page.click(f"text={i}")
            # 等待新資料載入
            page.wait_for_selector("table tbody tr", timeout=10000)

            # 擷取資料
            data = scrape_page_data(page)
            all_data.extend(data)

            browser.close()

            # 寫入CSV
            keys = ["國籍", "性別", "年齡", "希望工作類別", "希望工作區域", "媒合限制到期日", "公告到期日", "移工連絡電話", "詳細資料"]
            with open("foreign_labor_data.csv", "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(all_data)

            print("資料已存入 foreign_labor_data.csv")

if __name__ == "__main__":
    main()
