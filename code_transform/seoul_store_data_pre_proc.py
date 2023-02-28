import findspark
findspark.init()
import pyspark


import pyspark.pandas as pd

from sqlalchemy import create_engine
import pymysql

def pre_proc():
    myConf = pyspark.SparkConf()
    spark = pyspark.sql.SparkSession.builder.getOrCreate()

    data = spark.read.format('csv').option('header', 'true').load('/user/ubuntu/raw_data/api_data/seoul_store_data.csv')

    data_df = data.toPandas()

    data_df.drop(['_c0','brchNm', 'ksicCd', 'ksicNm', 'plotSctCd', 'plotSctNm', 'lnoMnno', 'lnoSlno', 'ldongCd', 'lnoCd', 'ldongNm', 'lnoAdr', 'bldMnno', 'bldSlno', 'bldMngNo', 'bldNm', 'oldZipcd', 'newZipcd', 'dongNo', 'flrNo', 'hoNo', 'rdnmAdr', 'bizesId', 'indsLclsCd', 'indsLclsNm'], axis = 1, inplace = True)

    data_df.reset_index(inplace=True)
    # db 저장
    pymysql.install_as_MySQLdb()

    user="root"
    password="1234"
    url="localhost:3306/airflow_test"
    dbtable="seoul_store_data_pre_proc"

    db_connection = create_engine(f'mysql+mysqldb://{user}:{password}@{url}', encoding='utf-8')

    data_df.to_sql(name=dbtable, con=db_connection, if_exists='replace', index=False)
