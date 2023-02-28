import findspark
findspark.init()
import pyspark

def pre_proc_GDP():
    myConf = pyspark.SparkConf()
    spark = pyspark.sql.SparkSession.builder.getOrCreate()

    df = spark.read.format('csv').option('header', 'true').load('/user/ubuntu/raw_data/file_data/GDP_economic_growth_rate.csv')
    df = df.withColumnRenamed('_c0', 'year')

    df = df.select("*").toPandas().transpose()

    df.columns = df.iloc[0]
    df = df[1:]

    df = df.reset_index(drop=False)
    df = df.rename(columns={'index': 'year', '국내총생산(명목GDP)': 'nominal_GDP', '경제성장률(실질GDP성장률)': 'economic_growth_rate'})


    from sqlalchemy import create_engine
    import pymysql

    pymysql.install_as_MySQLdb()

    user="root"
    password="1234"
    url="localhost:3306/airflow_test"
    table="GDP_economic_growth_rate"

    db_connection = create_engine(f'mysql+mysqldb://{user}:{password}@{url}', encoding='utf-8')
    df.to_sql(name=table, con=db_connection, if_exists='replace', index=False)
