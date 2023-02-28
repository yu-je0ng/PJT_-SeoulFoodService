import requests
import pprint
import json
import pandas as pd

def seoul_store_data():

    for pageNo in range(1, 119):
        url = 'https://apis.data.go.kr/B553077/api/open/sdsc2/storeListInDong?serviceKey=vDPsHfRauBIF%2BjBMpO%2Fec6aUByTVO02YSht%2BoAdhZoLORXaMfX8XXWTG0PNuIV6NG8EHDi%2B4yfaKhFeG1vJmKw%3D%3D&pageNo='+str(pageNo)+'&numOfRows=1000&divId=ctprvnCd&key=11&indsLclsCd=Q&type=json'
        response = requests.get(url, verify = False)
        contents = response.text
        json_ob = json.loads(contents)
        body = json_ob['body']['items']
        df = pd.DataFrame(body)
        if pageNo == 1:
            result = df
        else:
            result = pd.concat([result, df])

    result.to_csv("seoul_store_data.csv", mode='w', encoding = 'utf-8-sig')