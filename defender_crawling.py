import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time

for i in range(1, 5):
    # MySQL 연결 설정
    conn = mysql.connector.connect(
        user="root",
        password="12345678",
        host="localhost",
        database="baseball_stat"
    )

    # 커서 생성
    cursor = conn.cursor()

    # Selenium 웹 드라이버 초기화
    driver = webdriver.Chrome()

    # 크롤링할 URL 설정
    url = "https://www.koreabaseball.com/Record/Player/Defense/Basic.aspx"

    # Selenium을 사용하여 웹 페이지 열기
    driver.get(url)


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
    team_select.select_by_visible_text("두산")  # 원하는 팀 선택

    time.sleep(3)

    # 4. 페이지 변경 (페이지 번호를 원하는 페이지로 변경)
    page_number = i
    page_element = driver.find_element(By.XPATH, f"//a[@id='cphContents_cphContents_cphContents_ucPager_btnNo{page_number}']")
    page_element.click()

    time.sleep(3)



    # 데이터 추출 및 MySQL에 저장
    table = driver.find_element(By.CLASS_NAME, 'record_result')
    soup = BeautifulSoup(table.get_attribute('outerHTML'), 'html.parser')

    for row in soup.find_all('tr')[1:]:
        columns = row.find_all('td')
        if len(columns) >= 17:  # Ensure the correct number of columns
            player_name = columns[1].text.strip()
            team = columns[2].text.strip()
            pos = columns[3].text.strip()
            g = int(columns[4].text.strip())
            gs = int(columns[5].text.strip())
            ip = columns[6].text.strip()
            e = int(columns[7].text.strip())
            pko = int(columns[8].text.strip())
            po = int(columns[9].text.strip()) if columns[9].text.strip() != '-' else 0.0
            a = columns[10].text.strip()
            dp = int(columns[11].text.strip())
            fpct = float(columns[12].text.strip()) if columns[12].text.strip() != '-' else 0.0
            pbg = int(columns[13].text.strip())
            sb = int(columns[14].text.strip())
            cs = int(columns[15].text.strip())
            cs_per = float(columns[16].text.strip()) if columns[16].text.strip() != '-' else 0.0
            

            # 데이터를 MySQL에 저장
            insert_query = "INSERT INTO regular_2022_defender (df_Playername, df_Teamname, df_POS, df_G, df_GS, df_IP, df_E, df_PKO, df_PO, df_A, df_DP, df_FPCT, df_PB, df_SB, df_CS, df_CS_per) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            data = (player_name, team, pos, g, gs, ip, e, pko, po, a, dp, fpct, pbg, sb, cs, cs_per)
            cursor.execute(insert_query, data)

    # 변경사항을 커밋하고 연결 종료
    conn.commit()
    conn.close()

    # Selenium 웹 드라이버 종료
    driver.quit()
