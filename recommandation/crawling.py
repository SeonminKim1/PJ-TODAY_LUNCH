# 요기요 크롤링
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time, os
import pandas as pd
import requests


# 한식 요기요 페이지 가게 리스트
link = "https://www.yogiyo.co.kr/mobile/#/"

# 크롬드라이버 연결
driver = webdriver.Chrome('D:/chromedriver_win32/chromedriver.exe')
driver.get(link)
driver.refresh()

# 화면 크기 지정
driver.maximize_window() # 화면 최대화 모드로 변경
time.sleep(1)

# 요소 찾기 - 검색창찾고 키 전송
search = driver.find_element_by_css_selector('.form-control')
search.clear()
search.send_keys('서울특별시 강남구 역삼동 858 강남역')

# 데이터 프레임 생성
df = pd.DataFrame(columns=['name', 'address', 'image'])

for i in range(1, 50):
    # 검색어 새로 고침
    search.send_keys(Keys.ENTER)
    time.sleep(3)

    # 카테고리 리스트 클릭
    driver.find_element_by_xpath('//*[@id="category"]/ul/li[6]').click()
    time.sleep(2)

    if i >= 25:
        # 화면 맨아래로 스크롤 한번
        driver.execute_script('window.scrollTo(0, 550);')
        time.sleep(2)

    # 가게찾아서 클릭
    driver.find_element_by_xpath(f'//*[@id="content"]/div/div[4]/div/div[2]/div[{i}]/div').click()
    time.sleep(2)

    # 크롤링 작업
    # 레스토랑 정보 선택
    restaurant_info = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]')
    # 레스토랑 정보들 긁어와서 퓨티풀수프해서 HTML 파싱
    soup = BeautifulSoup(restaurant_info.get_attribute('innerHTML'), 'html.parser')
    # 가게이름, 주소, 가게 대표 이미지 찾기
    name = soup.find(class_='restaurant-name ng-binding').text
    address = soup.select_one('#info > div:nth-child(2) > p:nth-child(4) > span').text
    image = soup.find(class_='logo')['style']
    # 가게 대표 이미지 url 가져와서 파일로 저장
    image_url = image.split('url')[1].split('"')[1]

    img_data = requests.get(image_url).content
    path = 'static/' + name + '.jpg'
    with open(path, 'wb') as handler:
        handler.write(img_data)

    print(name, address, image_url)

    df = df.append({
        'name': name,
        'address': address,
        'image': path,
        'category': '양식'
    }, ignore_index=True)

print(df)
# csv 파일로 저장
df.to_csv('restaurant_we.csv', index=False)

driver.stop_client()
driver.close()
