import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time

# MySQL 연결 설정
conn = mysql.connector.connect(
        user="your ID",
        password="Your pwd",
        host="localhost",
        database="Your DB"
)

# 커서 생성
cursor = conn.cursor()

# Selenium 웹 드라이버 초기화
driver = webdriver.Chrome()

# 크롤링할 URL 설정
url = "https://www.koreabaseball.com/Record/Player/HitterBasic/BasicOld.aspx?sort=HRA_RT"

# Selenium을 사용하여 웹 페이지 열기
driver.get(url)

time.sleep(5)

# 1. 시즌 선택
season_select = Select(driver.find_element(By.ID, "cphContents_cphContents_cphContents_ddlSeries_ddlSeries"))
season_select.select_by_visible_text("KBO 정규시즌")  # 원하는 시즌 선택

time.sleep(3)

# 2. 년도 선택                                      
year_select = Select(driver.find_element(By.ID, "cphContents_cphContents_cphContents_ddlSeason_ddlSeason"))
year_select.select_by_visible_text("2022")  # 원하는 년도 선택

time.sleep(3)

# 3. 팀 선택
team_select = Select(driver.find_element(By.ID, "cphContents_cphContents_cphContents_ddlTeam_ddlTeam"))
team_select.select_by_visible_text("SSG")  # 원하는 팀 선택

time.sleep(3)

# 4. 페이지 변경 (페이지 번호를 원하는 페이지로 변경)
page_element = driver.find_element(By.XPATH, "//a[@id='cphContents_cphContents_cphContents_ucPager_btnNo2']")
page_element.click()

time.sleep(3)



# 데이터 추출 및 MySQL에 저장
table = driver.find_element(By.CLASS_NAME, 'record_result')
soup = BeautifulSoup(table.get_attribute('outerHTML'), 'html.parser')

for row in soup.find_all('tr')[1:]:
    columns = row.find_all('td')
    if len(columns) >= 16:  # Ensure the correct number of columns
        player_name = columns[1].text.strip()
        team = columns[2].text.strip()
        avg = float(columns[3].text.strip()) if columns[3].text.strip() != '-' else 0.0
        g = int(columns[4].text.strip())
        pa = int(columns[5].text.strip())
        ab = int(columns[6].text.strip())
        r = int(columns[7].text.strip())
        h = int(columns[8].text.strip())
        doubles = int(columns[9].text.strip())
        triples = int(columns[10].text.strip())
        hr = int(columns[11].text.strip())
        tb = int(columns[12].text.strip())
        rbi = int(columns[13].text.strip())
        sac = int(columns[14].text.strip())
        sf = int(columns[15].text.strip())

        # 데이터를 MySQL에 저장
        insert_query = "INSERT INTO regular_2022_hitter (ht_Playername, ht_Teamname, ht_AVG, ht_G, ht_PA, ht_AB, ht_R, ht_H, ht_2B, ht_3B, ht_HR, ht_TB, ht_RBI, ht_SAC, ht_SF) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE ht_Playername=ht_Playername"

        data = (player_name, team, avg, g, pa, ab, r, h, doubles, triples, hr, tb, rbi, sac, sf)
        cursor.execute(insert_query, data)

# 변경사항을 커밋하고 연결 종료
conn.commit()
conn.close()

# Selenium 웹 드라이버 종료
driver.quit()
