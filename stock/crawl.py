from selenium import webdriver
from selenium.webdriver.common.by import By

# 셀레니움에 다양한 옵션을 적용시키기 위한 패키지
from selenium.webdriver.chrome.options import Options

# 크롬 드라이버 매니저를 실행시키기 위해 설치해주는 패키지
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from datetime import datetime

import MySQLdb, time


def execute_query(connection, query, args=None):
    with connection.cursor() as cursor:
        cursor.execute(query, args or ())
        connection.commit()


def saving_data(crawled_data):
    # mysql 연결
    conn = MySQLdb.connect(
        host="localhost",
        user="root",
        password="root",
        database="stockcrawl"
    )

    for i in crawled_data:
        stock_name = i[0]
        o_year, o_month, o_date = map(str, i[1].split("."))
        c_month, c_date = map(str, i[2].split("."))
        open_date = datetime(int(o_year), int(o_month), int(o_date))
        close_date = datetime(int(o_year), int(c_month), int(c_date))
        if i[3] == "-":
            fixed_price = 0
        else:
            fixed_price = int(i[3].replace(",", ""))
        min_hprice = int(i[4].replace(",", ""))
        max_hprice = int(i[5].replace(",", ""))
        trading_firm = i[6]
        crawled_datetime = datetime.now()
        insert_query = """INSERT INTO stock_data(stock_name, open_date, close_date, fixed_price, min_hprice, max_hprice, trading_firm, crawled_datetime) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE fixed_price = %s, crawled_datetime = %s"""
        execute_query(conn, insert_query, (stock_name, open_date, close_date, fixed_price, min_hprice, max_hprice, trading_firm, crawled_datetime, fixed_price, crawled_datetime))


def crawling_data():
    # option 설정을 넣기 위한 초기화
    options_ = Options()
    options_.add_experimental_option('detach', True)
    # 거슬리는 메시지 - 터미널에서
    options_.add_experimental_option("excludeSwitches", ["enable-logging"])
    # 거슬리는 메시지 - 크롬에서
    options_.add_experimental_option("excludeSwitches", ["enable-automation"])
    # 화면 없이도 진행 가능 - 화면이 없다고 해서 속도가 빨라지는 것은 아님 그냥 안보일 뿐
    options_.add_argument("--headless")
    # 헤더 정보 추가 (내가 크롤링할 사이트 들어가서 개발자 도구에 network 에 user-agent 확인 후 복사해서 적용)
    options_.add_argument("user-agent={0}".format("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"))
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options_)

    stock_list = []

    for i in range(1, 6):
        url = f"https://www.38.co.kr/html/fund/index.htm?o=k&page={i}"
        driver.get(url)
        time.sleep(1)
        datas = driver.find_element(By.XPATH, '/html/body/table[3]/tbody/tr/td/table[1]/tbody/tr/td[1]/table[4]/tbody/tr[2]/td/table/tbody')
        for i in datas.text.split("\n"):
            stock_list.append([i.split()[0], i.split()[1].split("~")[0], i.split()[1].split("~")[1], i.split()[2], i.split()[3].split("~")[0], i.split()[3].split("~")[1], i.split()[-1]])

    driver.close()
    saving_data(stock_list)

# def saving_firmData():
#     conn = MySQLdb.connect(
#         host="localhost",
#         user="root",
#         password="root",
#         database="stockcrawl"
#     )
#     firm_dict = {
#         "KB증권": "https://www.kbsec.com/go.able",
#         "NH투자증권": "https://www.nhqv.com/",
#         "SK증권": "https://www.sks.co.kr/main/index.cmd",
#         "한국투자증권": "https://securities.koreainvestment.com/main/Main.jsp",
#         "DB금융투자": "https://www.db-fi.com/main/main.do",
#         "교보증권": "https://www.iprovest.com/index.jsp",
#         "대신증권": "https://www.daishin.com/",
#         "미래에셋증권": "https://securities.miraeasset.com/",
#         "IBK투자증권": "https://www.ibks.com/index.do",
#         "신한투자증권": "https://www.shinhansec.com/",
#         "삼성증권": "https://www.samsungpop.com/",
#         "한화투자증권": "https://www.hanwhawm.com/main/main/index.cmd",
#         "하나증권": "https://www.hanaw.com/main/main/index.cmd",
#         "키움증권": "https://www.kiwoom.com/h/main",
#         "유진증권": "https://www.eugenefn.com/main.do",
#         "신영증권": "https://www.shinyoung.com/",
#         "유안타증권": "https://www.myasset.com/myasset/main/index.cmd",
#         "하이투자증권": "https://www.hi-ib.com/",
#         "상상인증권": "https://sangsanginib.com/main/mainView"
#     }

#     for k in firm_dict.keys():
#         firm_name = k
#         firm_link = firm_dict.get(k)
#         insert_query = """INSERT INTO stock_firmdata(firm_name, firm_link) VALUES (%s, %s)"""
#         execute_query(conn, insert_query, (firm_name, firm_link))
# saving_firmData()
