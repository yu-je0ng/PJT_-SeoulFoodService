import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
from pprint import pprint


def getYearData(driver) :

    url = 'https://golmok.seoul.go.kr/region/selectYearData.json'
    resp = requests.post(url)

    year_json = resp.json()

    year_years = list(map(lambda x : x['YEARS'], year_json))

    return year_years

def getMonthData(yearData):
    url = 'https://golmok.seoul.go.kr/region/selectMonthData.json'
    year_month = list()
    for i in yearData:
        resp = requests.post(url, data={'stdrYyCd': i })
        # pprint(resp.json())
        mmcode_json = resp.json()
        mmcode = list(map(lambda x: x['MMCODE'], mmcode_json))
        for j in mmcode:
            year_month.append(j)
    # print(year_month)
    return year_month

def foot_traffic(driver, i, j):
    url = 'https://golmok.seoul.go.kr/region/selectPopulation.json'
    resp = requests.post(url, data={
        'stdrYyCd' : i, # yearData : ['2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014']
        'stdrSlctQu': 'beforeQu', # 고정된 값으로 추출
        'stdrQuCd': j, # 1 ~ 4라서 따로 요청 받지 않음.
        'stdrMnCd': f'{i}12', # monthData > year+12 형태. -> getMonthData 필요없음.
        'selectTerm': 'quarter', # 여기서부터 밑의 끝까지는 고정된 값
        'svcIndutyCdL': 'CS000000',
        'svcIndutyCdM': 'all',
        'stdrSigngu': 11,
        'selectInduty': 1,
        'infoCategory': 'population'
    } )

    foot_traffic_json = resp.json()

    foot_traffic = dict()
    foot_traffic[f'{i}년{j}분기'] = foot_traffic_json
    print(foot_traffic)

    return foot_traffic


if __name__ == '__main__':
    target_url = 'https://golmok.seoul.go.kr/stateArea.do'

    sleep(3)
    service = Service('C:\workspaces\project_bigdata\drivers\chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    # 브라우저 크기 최대화
    driver.maximize_window()
    sleep(1)

    sleep(3)
    driver.get(target_url)
    sleep(1)

    yearData = getYearData(driver)

    getMonthData(yearData)

    monthData = getMonthData(yearData)


    list_all = list()
    for i in yearData:
        for j in range(1, 5):
            result = foot_traffic(driver, i, j)
            list_all.append(result)


    dict_all = dict()
    dict_all['인구수'] = list_all

    json_all = json.dumps(dict_all, ensure_ascii=False)

    with open('../data_raw/seoul_commercial_area_population.json', 'w', encoding='utf-8') as file:
        file.write(json_all)