import findspark
findspark.init()
import pyspark

def pre_proc():
    myConf = pyspark.SparkConf()
    spark = pyspark.sql.SparkSession.builder.getOrCreate()


    from pyspark.sql.functions import col, array, struct, explode, avg, lit, bround

    from sqlalchemy import create_engine
    import pymysql


    df=spark.read.json("raw_data/crawling_data/seoul_commercial_area_population.json")


    df1 = df.select(explode(col('`인구수`')).alias('temp')) \
            .select(col('temp.*'))


    # 연도별, 분기별 데이터

    # 2017, 2018, 2019년도
    # 1~ 4분기.

    # 반복문 밖에서 스키마(데이프레임)만들어서 데이터 넣기

    df2017_1 = df1.select(explode(col('`2017년1분기`')).alias('2017_1'))

    test_df = df2017_1.selectExpr('2017_1.*')
        # test_df.printSchema()

    my_schema = test_df.schema
        # print(my_schema)

    union_df = spark.createDataFrame([], my_schema)
    # union_df.printSchema()
    # union_df.show()


    for i in range(17, 20):

        # tmp1 = df1.select(explode(col(f"20{i}년1분기").alias(f'df20{i}_1'))).selectExpr('col.*').withColumn('YY', lit(f'20{i}'))
        tmp1 = df1.select(explode(col(f"20{i}년1분기").alias(f'df20{i}_1'))).select('col.*').withColumn('YY', lit(f'20{i}'))
        tmp2 = df1.select(explode(col(f"20{i}년2분기").alias(f'df20{i}_2'))).select('col.*').withColumn('YY', lit(f'20{i}'))
        tmp3 = df1.select(explode(col(f"20{i}년3분기").alias(f'df20{i}_3'))).select('col.*').withColumn('YY', lit(f'20{i}'))
        tmp4 = df1.select(explode(col(f"20{i}년4분기").alias(f'df20{i}_4'))).select('col.*').withColumn('YY', lit(f'20{i}'))

        union_df = union_df.unionByName(tmp1, allowMissingColumns=True).\
                    unionByName(tmp2, allowMissingColumns=True).unionByName(tmp3, allowMissingColumns=True).unionByName(tmp4, allowMissingColumns=True)


    # YY 로 년도 구분해 가져기
        # 단위 : ha당 명

    union_df_filter= union_df.select(col('YY'), col('CD'),col('NM'),col('TOT_FLPOP_CO_3'), col('TOT_REPOP_CO_3'), col('TOT_WRC_POPLTN_CO_3')).withColumnRenamed('TOT_FLPOP_CO_3', 'FLPOP').withColumnRenamed('TOT_REPOP_CO_3', 'REPOP').withColumnRenamed('TOT_WRC_POPLTN_CO_3', 'WRC_POPLTN')

        # 2017년
    df_2017 = union_df_filter.filter("YY==2017")
    df_2017_agg = df_2017.groupBy("CD", "NM")\
        .agg(avg("FLPOP").alias("2017FLPOP")\
            ,avg("REPOP").alias("2017REPOP")\
            , avg("WRC_POPLTN").alias("2017WRC_POPLTN"))\
        .sort("CD")


        # 2018년
    df_2018 =  union_df_filter.filter("YY==2018")
    df_2018_agg = df_2018.groupBy("CD")\
        .agg(avg("FLPOP").alias("2018FLPOP")\
            ,avg("REPOP").alias("2018REPOP")\
            , avg("WRC_POPLTN").alias("2018WRC_POPLTN"))\
        .sort("CD")

        # 2019년

    df_2019 =  union_df_filter.filter("YY==2019")
    df_2019_agg = df_2019.groupBy("CD")\
        .agg(avg("FLPOP").alias("2019FLPOP")\
            ,avg("REPOP").alias("2019REPOP")\
            , avg("WRC_POPLTN").alias("2019WRC_POPLTN"))\
        .sort("CD")


    # df_2017.sort(col("NM")).show()
    # df_2017_agg.sort("CD").show()

    df = df_2017_agg.join(df_2018_agg, "CD").join(df_2019_agg, "CD")

        # df.sort("CD").show()

    # null값이 있는 row 삭제
    df = df.na.drop().sort("CD")

    # 소수점 버림, int 변환
    df = df.select("CD", "NM" \
                    , bround("2017FLPOP").cast('integer').alias("2017FLPOP")\
                    , bround("2017REPOP").cast('integer').alias("2017REPOP")\
                    , bround("2017WRC_POPLTN").cast('integer').alias("2017WRC_POPLTN")\
                    , bround("2018FLPOP").cast('integer').alias("2018FLPOP")\
                    , bround("2018REPOP").cast('integer').alias("2018REPOP")\
                    , bround("2018WRC_POPLTN").cast('integer').alias("2018WRC_POPLTN")\
                    , bround("2019FLPOP").cast('integer').alias("2019FLPOP")\
                    , bround("2019REPOP").cast('integer').alias("2019REPOP")\
                    , bround("2019WRC_POPLTN").cast('integer').alias("2019WRC_POPLTN"))


    # df.show()

    # pyspark -> dataframe
    df = df.select("*").toPandas()

    # db 저장
    pymysql.install_as_MySQLdb()

    user="root"
    password="1234"
    url="localhost:3306/airflow_test"
    dbtable="seoul_commercial_area_pop"


    db_connection_path = f"mysql+mysqldb://{user}:{password}@{url}"
    db_connection = create_engine(db_connection_path, encoding='utf-8')
    conn = db_connection.connect()

    df.to_sql(name=dbtable, con=db_connection, if_exists='replace', index=False)



