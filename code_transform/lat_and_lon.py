import findspark
findspark.init()
import pyspark

def pre_proc():
    myConf = pyspark.SparkConf()
    spark = pyspark.sql.SparkSession.builder.getOrCreate()

    import pandas as pd
    import numpy as np
    import pyproj
    import folium

    # 불러오기
    df = pd.read_csv("/home/ubuntu/raw_data/processing_data/seoul_ready.csv", encoding="utf-8", usecols=['X','Y'])

    # XY설정해주기
    df['X'] = pd.to_numeric(df['X'], errors="coerce") # TypeError: to_numeric() got an unexpected keyword argument 'errors'
    df['Y'] = pd.to_numeric(df['Y'], errors="coerce")

    df = df.dropna()

    # index는 df길이 만큼 늘린다.
    df.index=range(len(df))

    # 확인용
    # df.tail()

    def XYarray(coord, p1_type, p2_type):
        p1 = pyproj.Proj(init=p1_type) #입력 좌표
        p2 = pyproj.Proj(init=p2_type) #출력 좌표
        fx, fy = pyproj.transform(p1, p2, coord[:, 0], coord[:, 1])
        return np.dstack([fx, fy])[0]

        """
        
        좌표계 변환 함수
        - coord: x, y 좌표 정보가 담긴 NumPy Array
        - p1: 입력 좌표계 정보 ex) epsg:5179
        - p2: 출력 좌표계 정보 ex) epsg:4326
        
        """

    # dataframe -> numpy array . change!

    coord = np.array(df)
    coord

    p1_type = "epsg:2097"
    p2_type = "epsg:4326"

    result = XYarray(coord, p1_type, p2_type)
    result

    df['경도'] = result[:, 0]
    df['위도'] = result[:, 1]

    df = df.drop(columns='X')
    df = df.drop(columns='Y')

    df.to_csv('/home/ubuntu/processed_data/lat_and_lon_airflow_test.csv', sep=',', na_rep='NaN', mode='a')

