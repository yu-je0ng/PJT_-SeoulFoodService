import findspark
findspark.init()
import pyspark
from pyspark.sql.functions import *
from sqlalchemy import create_engine
import pymysql

def pre_proc():
    myConf = pyspark.SparkConf()
    spark = pyspark.sql.SparkSession.builder.getOrCreate()



    df17 = spark.read.format('csv').option('header', 'true').option('encoding', 'UTF-8').load('/user/ubuntu/raw_data/file_data/indivisual_business_loan_interest_rate_2017.csv')
    df18 = spark.read.format('csv').option('header', 'true').option('encoding', 'UTF-8').load('/user/ubuntu/raw_data/file_data/indivisual_business_loan_interest_rate_2018.csv')
    df19 = spark.read.format('csv').option('header', 'true').option('encoding', 'UTF-8').load('/user/ubuntu/raw_data/file_data/indivisual_business_loan_interest_rate_2019.csv')

    df17 = df17.select('은행','_c7').withColumnRenamed('은행', 'bank').withColumnRenamed('_c7', '2017')
    df18 = df18.select('은행','_c7').withColumnRenamed('은행', 'bank').withColumnRenamed('_c7', '2018')
    df19 = df19.select('은행','_c7').withColumnRenamed('은행', 'bank').withColumnRenamed('_c7', '2019')

    df = df17.join(df18, 'bank', 'inner').join(df19, 'bank', 'inner')

    df.write.format('csv').option('header', 'true').mode('append').save('/user/ubuntu/processed_data')

    df = df.select("*").toPandas()



    pymysql.install_as_MySQLdb()

    user="user"
    password="password"
    url="localhost:3306/airflow_test"
    table="business_loan_interest"

    db_connection = create_engine(f'mysql+mysqldb://{user}:{password}@{url}', encoding='utf-8')
    df.to_sql(name=table, con=db_connection, if_exists='replace', index=False)

