import findspark
findspark.init()
import pyspark
from sqlalchemy import create_engine
import pymysql

def pre_proc():
    myConf = pyspark.SparkConf()
    spark = pyspark.sql.SparkSession.builder.getOrCreate()

    df = spark.read.format('csv').option('header', 'true').load('/user/ubuntu/raw_data/api_data/seoul_metro_station_api_raw.csv')

    df = df.dropna('all').drop('철도운영기관명')
    df = df.withColumnRenamed('선명', 'line').withColumnRenamed('역명', 'station_name').withColumnRenamed('경도', 'longitude').withColumnRenamed('위도', 'latitude')
    df = df.select('station_name', 'line', 'longitude', 'latitude')

    # df.write.format('csv').option('header', 'true').mode('append').save('/user/ubuntu/processed_data')
    # df.show(df.count())


    df = df.select("*").toPandas()

    
    pymysql.install_as_MySQLdb()

    user="user"
    password="password"
    url="localhost:3306/airflow_test"
    dbtable="seoul_metro_station"

    db_connection = create_engine(f'mysql+mysqldb://{user}:{password}@{url}', encoding='utf-8')
    df.to_sql(name=dbtable, con=db_connection, if_exists='replace', index=False)
