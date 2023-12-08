from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd


def transform_table(target_url):
    result = urlopen(target_url)
    html = result.read()

    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')

    # table 만 parsing
    data = soup.find_all('table')
    temp = data[29].find_all('table')

    # temp[5] 한 번 더 세세하게 분류
    table_df = pd.read_html(str(temp[5]))

    # 9, 10 칼럼 삭제 후 널값 제거
    df = table_df[0].drop([9, 10], axis=1).dropna()
    df.drop(df.tail(1).index, inplace=True)

    return df


if __name__ == '__main__':

    type_list = ['A1', 'H1', 'N1', 'B1', 'L1', 'O1', 'I1', 'J1', 'D1']
    all_df = pd.DataFrame()

    for i in range(len(type_list)):
        for k in range(1, 5):
            url = 'http://sbiznews.com/FranchiseIndex/?page={page_num}&action=list500&menuid=198&mode=upjong&cd2='.format(
                page_num=k)
            target_url = url + type_list[i]

            try:
                df = transform_table(target_url)

                all_df = all_df.append(df)

            except:
                pass

    # print(all_df)

    all_df.drop([0], axis=1, inplace=True)
    all_df.reset_index(drop=True, inplace=True)
    all_df.columns = ['브랜드', '표준점수', '회사규모', '성장', '재무 안정성', '광고홍보', '관리충실도', '가맹점 수익성']

    all_df['브랜드'] = all_df['브랜드'].str.replace("타 ", "타")
    brand_list = all_df['브랜드'].str.split().tolist()

    # 맨 뒤에  "10[한식]" 이런 데이터 삭제
    for i in range(len(brand_list)):
        del brand_list[i][-1]

        brand_list[i] = ' '.join(brand_list[i])

    all_df['브랜드'] = brand_list

    # 저장
    all_df.to_csv("C:/worksplaces/save_data/news_franchise.csv", index=False, encoding='utf-8-sig')
