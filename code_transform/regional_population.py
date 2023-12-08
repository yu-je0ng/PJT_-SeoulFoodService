import findspark
findspark.init()
import pyspark
import pandas as pd
from sqlalchemy import create_engine
import pymysql

def pre_proc():
    myConf = pyspark.SparkConf()
    spark = pyspark.sql.SparkSession.builder.getOrCreate()


    #불러오기
    YP_2015_2019 = spark.read.option('header', 'True').csv('/user/ubuntu/raw_data/file_data/regional_population.csv', encoding='utf-8')

    # 확인
    # YP_2015_2019.show()

    # 필요없는 데이터 삭제
    YP_2015_2019 = YP_2015_2019.drop('전국')
    YP_2015_2019 = YP_2015_2019.drop('부산광역시')
    YP_2015_2019 = YP_2015_2019.drop('대구광역시')
    YP_2015_2019 = YP_2015_2019.drop('인천광역시')
    YP_2015_2019 = YP_2015_2019.drop('광주광역시')
    YP_2015_2019 = YP_2015_2019.drop('대전광역시')
    YP_2015_2019 = YP_2015_2019.drop('울산광역시')
    YP_2015_2019 = YP_2015_2019.drop('세종특별자치시')
    YP_2015_2019 = YP_2015_2019.drop('경기도')
    YP_2015_2019 = YP_2015_2019.drop('강원도')
    YP_2015_2019 = YP_2015_2019.drop('충청북도')
    YP_2015_2019 = YP_2015_2019.drop('충청남도')
    YP_2015_2019 = YP_2015_2019.drop('전라북도')
    YP_2015_2019 = YP_2015_2019.drop('전라남도')
    YP_2015_2019 = YP_2015_2019.drop('경상북도')
    YP_2015_2019 = YP_2015_2019.drop('경상남도')
    YP_2015_2019 = YP_2015_2019.drop('제주특별자치도')

    # 확인용
    # YP_2015_2019.show()

    df = YP_2015_2019.drop("항목")

    df = df.withColumnRenamed('시점', 'year').withColumnRenamed('서울특별시', 'population')

    df = df.toPandas()

    # 필요없는 데이터 삭제
    df = df.drop([0,1,2,3,4,5,6,7,8,10,11,13,14,16,17,19,20,22,23,24,25,26,27,28,29])

    #확인용
    # print(df)

    pymysql.install_as_MySQLdb()

    user="user"
    password="password"
    url="localhost:3306/airflow_test"
    table="regional_population"

    db_connection = create_engine(f'mysql+mysqldb://{user}:{password}@{url}', encoding='utf-8')
    df.to_sql(name=table, con=db_connection, if_exists='replace', index=False)
