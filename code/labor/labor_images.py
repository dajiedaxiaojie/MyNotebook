import os
import time
import uuid
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

# 參數設定
START_PAGE = 36
END_PAGE = 110
SAVE_DIR = "screenshots"
MAX_REFRESH = 3  # 回列表頁找不到 select id="page" 時的最大重試次數

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 15)

driver.get("https://fw.wda.gov.tw/wda-employer/home/fortrans/foreign-labor")

# 選擇「家庭看護工」
wait.until(EC.element_to_be_clickable((By.ID, "conditions[workCategory]_9"))).click()
# 選擇「台北市」
wait.until(EC.presence_of_element_located((By.ID, "conditionsacceptedJobService.id")))
select = Select(driver.find_element(By.ID, "conditionsacceptedJobService.id"))
select.select_by_visible_text("台北市")
# 點擊查詢
search_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='查詢']")))
driver.execute_script("arguments[0].click();", search_btn)
time.sleep(3)

def parse_date(date_str):
    try:
        return datetime.strptime(date_str.strip(), "%Y/%m/%d")
    except:
        return None

def wait_for_page_select():
    """回到列表頁後，等待分頁下拉選單出現，失敗時自動刷新重試。"""
    for i in range(MAX_REFRESH):
        try:
            wait.until(EC.presence_of_element_located((By.ID, "page")))
            return True
        except Exception:
            print(f"分頁下拉選單未出現，刷新第 {i+1} 次")
            driver.refresh()
            time.sleep(3)
    print("多次刷新後仍未載入分頁下拉選單，跳過本頁。")
    return False

def get_screenshot_path(page_num, idx, expiry_date_str):
    safe_date_str = expiry_date_str.replace("/", "") if expiry_date_str else "nodate"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex[:6]
    filename = f"{safe_date_str}_page{page_num}_row{idx+1}_{timestamp}_{unique_id}.png"
    return os.path.join(SAVE_DIR, filename)

def fullpage_screenshot(driver, path, zoom=80):
    driver.execute_script(f"document.body.style.zoom='{zoom}%'")
    time.sleep(0.5)
    scroll_height = driver.execute_script("return document.body.scrollHeight")
    # for y in range(0, scroll_height, 500):
    #     driver.execute_script(f"window.scrollTo(0, {y});")
    #     time.sleep(0.2)
    width = driver.execute_script("return document.body.scrollWidth")
    height = driver.execute_script("return document.body.scrollHeight")
    driver.set_window_size(width, height)
    time.sleep(0.5)
    driver.save_screenshot(path)
    driver.execute_script("document.body.style.zoom='100%'")

def process_page(page_num):
    print(f"處理第 {page_num} 頁")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "tbody.tbody")))

    today = datetime.today()
    rows = driver.find_elements(By.CSS_SELECTOR, "tbody.tbody tr")
    print(f"本頁資料筆數: {len(rows)}")

    for idx in range(len(rows)):
        try:
            # 每次都重新定位該列，避免 stale
            rows = driver.find_elements(By.CSS_SELECTOR, "tbody.tbody tr")
            row = rows[idx]
            cells = row.find_elements(By.TAG_NAME, "td")

            def get_cell_text(label_start):
                for cell in cells:
                    if cell.get_attribute("data-label").startswith(label_start):
                        return cell.text.strip()
                return ""

            hope_job = get_cell_text("工作類別｜")
            hope_area = get_cell_text("希望工作區域｜")
            match_expiry_str = get_cell_text("媒合限制到期日｜")
            match_expiry_date = parse_date(match_expiry_str)

            if hope_job == "家庭看護工" and "台北市" in hope_area and match_expiry_date and match_expiry_date > today:
                detail_link = None
                for cell in cells:
                    if cell.get_attribute("data-label").startswith("詳細資料｜"):
                        detail_link = cell.find_element(By.TAG_NAME, "a")
                        break

                if detail_link:
                    driver.execute_script("arguments[0].click();", detail_link)
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.btn.btn-warning.btn-back")))
                    time.sleep(1)

                    screenshot_path = get_screenshot_path(page_num, idx, match_expiry_str)
                    fullpage_screenshot(driver, screenshot_path)
                    print(f"已保存全頁截圖: {screenshot_path}")

                    try:
                        back_btn = wait.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.btn-warning.btn-back"))
                        )
                        driver.execute_script("arguments[0].click();", back_btn)
                        print("已點擊返回上頁")
                    except Exception as e:
                        print(f"返回上頁按鈕點擊失敗: {e}")
                        driver.back()

                    if not wait_for_page_select():
                        print(f"第{page_num}頁回列表頁失敗，跳過")
                        return
                    time.sleep(2)
        except (StaleElementReferenceException, TimeoutException) as e:
            print(f"處理第{page_num}頁第{idx+1}筆資料失敗: {e}")

for page_num in range(START_PAGE, END_PAGE + 1):
    print(f"跳轉到第 {page_num} 頁")
    value_str = str(page_num - 1)

    if not wait_for_page_select():
        print(f"第{page_num}頁分頁下拉選單無法載入，跳過。")
        continue

    page_select = Select(driver.find_element(By.ID, "page"))
    wait.until(EC.element_to_be_clickable((By.ID, "page")))
    page_select.select_by_value(value_str)

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "tbody.tbody")))
    time.sleep(1)
    process_page(page_num)

driver.quit()
