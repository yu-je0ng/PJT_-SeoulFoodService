import findspark
findspark.init()
import pyspark

def pre_proc():
    myConf = pyspark.SparkConf()
    spark = pyspark.sql.SparkSession.builder.getOrCreate()

    df = spark.read.format('csv').option('header', 'true').load('/user/ubuntu/raw_data/file_data/GNI_per_capita.csv')

    df = df.drop('_c5')

    df = df.withColumnRenamed('_c0', 'year').withColumnRenamed('1인당 실질 국민총소득(만원)', 'real_GNI_per_capita').withColumnRenamed('전년 대비 증가율(%)2', 'real_GNI_growth_rate').withColumnRenamed('1인당 명목 국민총소득(만원)', 'nominal_GNI_per_capita').withColumnRenamed('전년 대비 증가율(%)4', 'nominal_GNI_growth_rate')


    df = df.select("*").toPandas()

    from sqlalchemy import create_engine
    import pymysql


    pymysql.install_as_MySQLdb()

    user="root"
    password="1234"
    url="localhost:3306/airflow_test"
    table="GNI_per_capita"

    db_connection = create_engine(f'mysql+mysqldb://{user}:{password}@{url}', encoding='utf-8')
    df.to_sql(name=table, con=db_connection, if_exists='replace', index=False)
