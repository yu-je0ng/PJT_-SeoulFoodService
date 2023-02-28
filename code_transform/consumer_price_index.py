import findspark

findspark.init()
import pyspark
import pandas as pd

def pre_proc():
    myConf = pyspark.SparkConf()
    spark = pyspark.sql.SparkSession.builder.getOrCreate()

    # 불러오기
    df = spark.read.option('header', 'True').csv('/user/ubuntu/raw_data/file_data/consumer_price_index.csv', encoding='utf-8')

    # 버릴거 버리고 칼럼 이름 바꿔주기
    df = df.drop("2011", "2012", "2013", "2014", "2020", "2021")

    # df로 전환
    df = df.toPandas()

    # transpose() 를 이용해서 행 열을 바꿔버리고 print로 출력시켜 확인한다.
    df = df.transpose()

    # 첫번째 행을 column으로 지정
    df.rename(columns=df.iloc[0], inplace=True)

    # 첫번째 행을 삭제
    df.drop(df.index[0], inplace=True)

    # 시점 데이터 인덱스 해제.
    df.reset_index(drop=False, inplace=True)

    # df.drop([3:], axis=1, inplace=True)
    df = df.iloc[:, [0, 1, 2]]

    df.columns = ['years', 'CPI', 'CPI_inflation']

    # 저장
    #df.to_csv('/user/ubuntu/processed_data', sep=',', na_rep='NaN')

    from sqlalchemy import create_engine
    import pymysql

    pymysql.install_as_MySQLdb()

    user="root"
    password="1234"
    url="localhost:3306/airflow_test"
    table="consumer_price_index"
    db_connection = create_engine(f'mysql+mysqldb://{user}:{password}@{url}', encoding='utf-8')
    df.to_sql(name=table, con=db_connection, if_exists='replace', index=False)
