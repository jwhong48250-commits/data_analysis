import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By


driver = webdriver.Chrome()
driver.get('https://comic.naver.com/webtoon/detail?titleId=776601&no=178&week=fri')

time.sleep(1)

xpath = '/html/body/div[1]/div[5]/div/div/div[5]/div[1]/div[3]/div/section/ul/li'
best_connemt_elements = driver.find_elements(By.XPATH, xpath)

for li in best_connemt_elements:
    try:
        comment_p = li.find_element(By.XPATH, "./div[1]/div[2]/div/p")
        comment_text = comment_p.text.strip()
        print(comment_text)
        print("-" * 30)
    except Exception as e:
        print(e)

driver.find_element(By.XPATH, "/html/body/div[1]/div[5]/div/div/div[5]/div[1]/div[3]/div/section/div[4]/button[2]").click()

time.sleep(1)

print('***** 전체댓글 *****')

xpath_all = '/html/body/div[1]/div[5]/div/div/div[5]/div[1]/div[3]/div/section/ul/li'
all_connemt_elements = driver.find_elements(By.XPATH, xpath_all)

for li in all_connemt_elements:
    try:
        comment_p = li.find_element(By.XPATH, "./div[1]/div[2]/div/p")
        comment_text = comment_p.text.strip()
        print(comment_text)
        print("-" * 30)
    except Exception as e:
        print("ⓘ 클린봇이 이용자 보호를 위해 숨긴 댓글입니다.")
        print("-" * 30)

time.sleep(1)
