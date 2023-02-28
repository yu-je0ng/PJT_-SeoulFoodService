import findspark
findspark.init()

import pyspark

def pre_proc():
    myConf = pyspark.SparkConf()
    spark = pyspark.sql.SparkSession.builder.getOrCreate()

    from pyspark.sql.functions import col, isnan, count, when, isnull, \
                                        coalesce, translate, regexp_replace, split, monotonically_increasing_id
    import pandas as pd

    #spark = SparkSession.builder.master('local').appName('myCount').getOrCreate()

    ###### 1. spark 처리 ######
    ## 1-1 데이터 불러오기
    franchise = spark.read.option('header', 'true').csv('raw_data/crawling_data/news_franchise_list.csv')
    direct_open = spark.read.option('header', 'true').csv('raw_data/crawling_data/direct_franchise_open.csv')
    direct_closed = spark.read.option('header', 'true').csv('raw_data/crawling_data/Direct_franchise_closed.csv')

    ## 1-2 column 네임을 구분하기 쉽게 바꿔줍니다.
    direct_closed = direct_closed.withColumnRenamed("0", "franchise_nm")

    ## 1-3 필요한 컬럼만 추출해 칼럼 네임을 똑같이 바꿔줍니다.
    fran = franchise.select('브랜드')
    fran = fran.withColumnRenamed("브랜드", "franchise_nm")
    #direct_open.printSchema()
    #direct_closed.printSchema()


    ###### 2. pandas 처리 ######
    ## 2-1 pandas 데이터프레임으로 변경
    pd_direct_open = direct_open.select("*").toPandas()
    pd_direct_closed = direct_closed.select("*").toPandas()
    pd_fran = fran.select("*").toPandas()

    ## 2-2 split을 위해 띄어쓰기 추가
    pd_fran['franchise_nm'] = pd_fran['franchise_nm'].str.replace("(", " (")
    pd_direct_open['franchise_nm'] = pd_direct_open['franchise_nm'].str.replace("(", " (")
    pd_direct_closed['franchise_nm'] = pd_direct_closed['franchise_nm'].str.replace("(", " (")

    ## 2-3 fran 데이터 먼저 split
    pd_fran['franchise_nm'] = pd_fran.franchise_nm.str.split('(').str[0]

    ## 2-4 concat으로 append 후 split 된 첫 번재 값을 가져오기
    dir_nm = pd.concat([pd_direct_open, pd_direct_closed])
    dir_nm['franchise_nm'] = dir_nm.franchise_nm.str.split(' ').str[0]

    ## 2-5 창업경영신문 데이터와 합쳐주기
    fran_df = pd.concat([pd_fran, dir_nm])

    ## 2-6 중복 제거
    fran_df = fran_df.drop_duplicates()
    #print(fran_df)

    ## 2-7 중간 저장 (데이터 후처리 했기 때문에 이건 절대 불러오면 안됨)
    #fran_df.to_csv('raw_data/merge_franchise.csv', index=False, encoding="utf-8-sig")

    ## 2-8 후처리 후 불러오기
    test_df = spark.read.option('header', 'true').csv('raw_data/processing_data/merge_franchise.csv')
    df = test_df.select("*").toPandas()


    ## 2-9 "점이 들어간 문자 분류 "
    geom_df= df[df['franchise_nm'].str.contains("점")]


    ## 2-10 점 들어간 데이터 삭제, 중복 제거
    idx = list(geom_df.index)

    df_1 = df.drop(idx, axis = 0)
    df_1 = df_1.drop_duplicates()
    #print(len(df_1))

    ## 2-11 한 글자 데이터 삭제
    for i in df_1['franchise_nm']:
        if len(i) == 1:
            ## 해당 하는 데이터만 찾기
            i_df = df_1[df_1['franchise_nm'] == i]

            df_1 = df_1.drop(i_df.index, axis = 0)

    #print(len(df_1))

    ## 2-12 저장
    df_1.to_csv('/home/ubuntu/processed_data/franchise_list_airflow_test.csv', index=False, encoding="utf-8-sig")
