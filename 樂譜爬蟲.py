# selenium 爬蟲
import requests
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement


# 下載圖片
from cairosvg import svg2png
from os import makedirs
from tqdm import tqdm

# 選擇目錄
import tkinter as tk
from tkinter import filedialog
from os import path

# 1. 設定輸入 & 目錄
urlLink = input("輸入muse網頁譜的url:")
name = input("歌名:")
root = tk.Tk()
root.withdraw()
root_directory = filedialog.askdirectory(title="選擇輸出資料夾路徑:")

def create_folder(folder_name:str):
    """
    創建資料夾
    """
    try:
        # 直接使用 makedirs 創建資料夾，如果資料夾已存在，則忽略
        makedirs(path.join(root_directory,folder_name))
        print(f"資料夾 '{folder_name}' 已成功創建")
    except FileExistsError:
        print(f"資料夾 '{folder_name}' 已存在，無需再次創建")

create_folder(name)

def downloadImg(src,i):
    response = requests.get(src)
    content_type = response.headers.get('Content-Type', '')

    if "image/svg" in content_type:
        png_data = svg2png(bytestring=response.content)

        with open(str(path.join(root_directory, name, f"{name}_{i}.png")).replace("\\", "/"), "wb") as f:
            f.write(png_data)
    elif "image/png" in content_type:
        with open(path.join(root_directory,name,f"{name}_{i}.png"), 'wb') as f:
            f.write(response.content)


chrome_options = Options()
chrome_options.add_argument("--log-level=3")
chrome_options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.get(urlLink)

element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="jmuse-scroller-component"]'))
)
target_text = "EEnGW"
sub_elements = element.find_elements(By.CLASS_NAME,target_text)

def nullWait(e:WebElement) -> bool:
    """
    偵測src是否為null
    """
    if e.get_attribute("src") == None:
        sleep(1)
        return nullWait(e)
    else:
        return True

for i in tqdm(range(len(sub_elements)),desc="Processing",unit="iteration"):
    img_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, f'//*[@id="jmuse-scroller-component"]/div[{i+1}]/img'))
    )
    
    if nullWait(img_element):
        downloadImg(img_element.get_attribute("src"),i)
    driver.execute_script("arguments[0].scrollTop += 1271.88;", element)

print("完成!!")
driver.quit()
