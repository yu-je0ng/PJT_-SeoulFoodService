from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import requests
from bs4 import BeautifulSoup
import csv


def get_page_num():
    url = 'https://franchise.ftc.go.kr/mnu/00013/program/userRqst/list.do?selUpjong=21&pageUnit=300'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    # page_num = soup.find('ul', {'class': 'paginationList'}).contents
    # nums = list(filter(None, map(lambda x: x.text if x.text.isdigit() else None, page_num)))
    max_num = soup.find('li', {'class': 'paginationLast'}).contents[0].get('href')[-2:]
    nums = list(range(1, int(max_num) + 1))
    return nums


def get_titles(i):
    title_list = list()
    sub_url = 'https://franchise.ftc.go.kr/mnu/00013/program/userRqst/list.do?selUpjong=21&pageUnit=300&pageIndex=' + str(
        i)
    soup = BeautifulSoup(requests.get(sub_url).text, 'html.parser')
    titles = soup.select('tbody tr td:nth-of-type(3)')
    for title in titles:
        title_list.append(title.text.strip())
    return title_list


def get_all_page_thread(nums):
    titles = list()
    with ThreadPoolExecutor(max_workers=10) as executor:
        for num in nums:
            future = executor.submit(get_titles, num)
            titles.extend(future.result())
    return titles


if __name__ == '__main__':
    nums = get_page_num()
    titles = get_all_page_thread(nums)

    with open('../data_raw/franchises_list.csv', 'w', encoding='utf-8') as file:
        write = csv.writer(file)
        write.writerow(titles)

    print(len(titles))