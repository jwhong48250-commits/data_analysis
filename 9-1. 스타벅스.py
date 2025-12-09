import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains # 액션 연결
from selenium.webdriver.common.by import By # 셀레니움에서 제공하는 By 모듈
from selenium.webdriver.support.ui import WebDriverWait # 웹드라이버 대기
from selenium.webdriver.support import expected_conditions as EC    # 웹드라이버 조건
from bs4 import BeautifulSoup   #
import re   # 정규 표현식

def fetch_starbucks():
    url = "https://www.starbucks.co.kr/index.do"
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    time.sleep(2)

    # 카피셀렉터 
    # #gnb > div > nav > div > ul > li.gnb_nav03 > h2 > a
    action = ActionChains(driver)
    first_tag = driver.find_element(By.CSS_SELECTOR, "#gnb > div > nav > div > ul > li.gnb_nav03")

    # #gnb > div > nav > div > ul > li.gnb_nav03 > div > div > div > ul:nth-child(1) > li:nth-child(3) > a
    second_tag = driver.find_element(By.CSS_SELECTOR, "#gnb > div > nav > div > ul > li.gnb_nav03 > div > div > div > ul:nth-child(1) > li:nth-child(3) > a")

    action.move_to_element(first_tag).move_to_element(second_tag).click().perform()

    # #container > div > form > fieldset > div > section > article.find_store_cont > article > article:nth-child(4) > div.loca_step1 > div.loca_step1_cont > ul > li:nth-child(1) > a
    seoul_tag = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#container > div > form > fieldset > div > section > article.find_store_cont > article > article:nth-child(4) > div.loca_step1 > div.loca_step1_cont > ul > li:nth-child(1) > a")))
    seoul_tag.click()

    WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "set_gugun_cd_btn")))
    gu_elements = driver.find_elements(By.CLASS_NAME, "set_gugun_cd_btn")
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#mCSB_2_container > ul > li:nth-child(1) > a")))
    gu_elements[0].click()


    # #mCSB_3_container > ul > li:nth-child(1)
    WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "quickResultLstCon")))

    req = driver.page_source
    soup = BeautifulSoup(req, "html.parser")
    stores = soup.find("ul", "quickSearchResultBoxSidoGugun").find_all("li")


    store_list = []
    addr_list = []
    lat_list = []
    lng_list = []
    for store in stores:
        store_name = store.find("strong").text
        store_addr = store.find("p").text
        store_addr = re.sub(r'\d{4}-\d{4}$', '', store_addr).strip()
        store_lat = store['data-lat']
        store_lng = store['data-long']
        store_list.append(store_name)
        addr_list.append(store_addr)
        lat_list.append(store_lat)
        lng_list.append(store_lng)
    df = pd.DataFrame({
        'store': store_list,
        'addr': addr_list,
        'lat': lat_list,
        'lng': lng_list
    })
    driver.quit()
    return df

starbucks_df = fetch_starbucks()
starbucks_df.to_csv("starbucks_seoul.csv", index=False, encoding='utf-8-sig')
print('데이터가 starbucks_seoul.csv 파일로 저장되었습니다.')

# 

# 마우스 가져가기