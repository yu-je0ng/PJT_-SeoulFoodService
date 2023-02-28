import requests
import json
import pandas as pd

def crawl_direct_franchise():

    url = 'https://www.foodsafetykorea.go.kr/ajax/portal/specialinfo/searchBsnList.do'

    resp = requests.post(url, data={
        'menu_no': 2813,
        'menu_grp': 'MENU_NEW04',
        'menuNm': '업체 검색',
        'copyUrl': 'https://www.foodsafetykorea.go.kr:443/portal/specialinfo/searchInfoCompany.do?menu_grp=MENU_NEW04&menu_no=2813',
        'favorListCnt': 0,
        'menu_grp': 'MENU_NEW04',
        'menu_no': 2813,
        's_mode': 1,
        's_opt': 'rstrt',
        's_sido_cd': 11,
        's_bsn_nm': '점',
        's_opt1': 'N',
        's_opt2': 'N',
        's_opt3': 'N',
        's_opt4': 'I',
        's_opt5': 'N',
        's_opt6': '1',
        's_opt7': 'N',
        's_induty_cd': '104,101,120,121,105',
        's_order_by': 'reg_dt',
        's_list_cnt': 40418,  # 데이터 갯수
        's_page_num': 1,
        's_tx_id': 1,
        'chk_sido': 11,
        'bsn_nm': '점',  # 검색어
        'opt4': 'I',
        'opt6_1': 1,
        'chk_sido': 11,
        'upjongOne': all,
        'opt6_2': 1,
        'opt4': 'I'

    })

    dj = resp.json()

    bsnList = dj['bsnList']
    nm_list = []

    # BSSH_NM (가게 이름만 추출)
    for i in bsnList:
        nm = i.get('BSSH_NM')
        nm_list.append(nm)

    # 데이터 프레임으로
    df = pd.DataFrame(nm_list, columns=['franchise_nm'])

    # 저장
    ## json

    save_file = open('C:/worksplaces/save_data/direct_franchise_open.json', 'w')
    json.dump(dj, save_file)
    save_file.close()

    df.to_csv("C:/worksplaces/save_data/direct_franchise_open.csv", index=False, encoding='utf-8-sig')