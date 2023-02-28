import findspark
findspark.init()
import pyspark

def pre_proc():
    myConf = pyspark.SparkConf()
    spark = pyspark.sql.SparkSession.builder.getOrCreate()

    from pyspark.sql import SparkSession
    from pyspark.sql.functions import col, isnan, count, when, isnull, coalesce, translate, regexp_replace
    import pandas as pd
    import numpy as np

    #spark = SparkSession.builder.master('local').appName('myCount').getOrCreate()


    ###### 1. 데이터 불러오기 ######
    ## 1-1
    df = spark.read.option('header', 'true').csv('raw_data/api_data/restaurant_in_seoul.csv')
    seoul_rest = df.select('BPLCNM','UPTAENM', 'DCBYMD', 'SITEWHLADDR', 'RDNWHLADDR', 'FACILTOTSCP', 'DTLSTATENM', 'X', 'Y')    # MGTNO 살려주세요..
    #seoul_rest.show()

    ## 1-2 널 값 확인
    #seoul_rest.select([count(when(isnull(c), c)).alias(c) for c in seoul_rest.columns]).show()


    ###### 2. 데이터 전처리 ######
    ## 2-1 BPLCNM, FACILTOTSCP, DTLSTATENM 해당 컬럼들은 널 값의 특성을 정의할 수 없으므로 널 값을 먼저 처리해 줍니다.
    seoul_rest = seoul_rest.na.drop("any", subset=["BPLCNM", "FACILTOTSCP", "DTLSTATENM", "UPTAENM", "X", "Y"])

    ## 2-2 주소에 없는 데이터를 도로명 주소로 대체
    seoul_rest = seoul_rest.withColumn('SITEWHLADDR', coalesce('SITEWHLADDR', 'RDNWHLADDR'))

    ## 2-3 도로명 주소 컬럼 삭제
    seoul_rest = seoul_rest.drop('RDNWHLADDR')


    ## 2-4 UPTAENM 이상값 수정
    seoul_rest = seoul_rest.withColumn('UPTAENM', translate('UPTAENM', "?", ""))
    seoul_rest = seoul_rest.withColumn('UPTAENM', regexp_replace('UPTAENM', "ㅑ", "정종/"))
    seoul_rest = seoul_rest.withColumn('UPTAENM', regexp_replace('UPTAENM', "커피숍", "까페"))
    #seoul_rest.select('UPTAENM').distinct().collect()


    ## 2-5 폐업 15 ~ 19 년도 데이터 추출
    year_datefilter = seoul_rest.filter(col("DCBYMD").between('2015-01-13','2019-12-31'))


    ## 2-6 null (현재 운영 중인) 데이터 추출 ->  null 20221231 로 치환
    year_nullfilter = seoul_rest.filter(col("DCBYMD").isNull())
    year_nullfilter = year_nullfilter.na.fill(value='20221231', subset=['DCBYMD'])

    ## 2-7 year_datefilter + year_nullfilter 합져주기
    seoul_target = year_datefilter.union(year_nullfilter)




    ###### 3. X, Y 윤지원 팀원이 transform 한 데이터로 수정 ######
    seoul_data = seoul_target.select("*").toPandas()


    ## 3-1 기존 X, Y 삭제
    seoul_data = seoul_data.drop(['X', 'Y'], axis=1)


    ## 3-2 위경도 수정
    map_data = spark.read.option('header', 'true').csv('processed_data/lat_and_lon.csv')
    map_loc = map_data.select("*").toPandas()
    # lat_and_lon DB에 저장 후
    # df = pd.read_sql_table(테이블명, con=db_connection.connect())
    # 으로 불러내면 위 2줄 하나로 줄일 수 있음

    map_loc = map_loc[['경도', '위도']]
    map_loc.columns = ['X', 'Y']
    map_loc


    seoul = pd.concat([seoul_data, map_loc], axis= 1)



    ## 3-3 중간 저장 (활성화 안해도 됨)
    #seoul.to_csv("raw_data/seoul_sample.csv", index=False, encoding="utf-8-sig")


    ###### 4. pandas 처리 ######

    ## 4-1 franchise 데이터 불러오기
    franchise = spark.read.option('header', 'true').csv('processed_data/franchise_list.csv')


    ## 4-2 pandas 데이터 프레임으로 변환
    fran = franchise.select("*").toPandas()
    # 이것도 franchise_list DB에 저장 후
    # df = pd.read_sql_table(테이블명, con=db_connection.connect())
    # 으로 불러내면 됨


    fran_list = list(fran['franchise_nm'])
    #print(fran_list)


    ## 4-3 프래차이즈 여부 인덱스를 리스트로 만들기 ######
    idx_list = []

    for i in fran_list:
        try:
            result = seoul[seoul['BPLCNM'].str.contains(i)]

            nm_idx = list(result.index)

            if len(nm_idx) > 4:
                idx_list.append(nm_idx)

        except:
            pass

    ## 4-4 list extend start
    idx_list_1 = idx_list[0]
    idx_list_2 = idx_list[1:]

    ## 4-5 리스트안에 리스트 해제 후 extend
    for i in range(len(idx_list_2)):
        idx_list_1.extend(idx_list_2[i])

    ## 4-6 중복 제거
    result_set = set(idx_list_1)
    result = list(result_set)

    ## 4-7 중간 저장 (활성화 안해도 됨)
    # seoul.to_csv("raw_data/seoul_ready.csv", index=False, encoding='utf-8-sig')


    ###### 5. 프랜차이즈 여부 체크 ######

    ## 5-1  먼저 null 값을 가지 franchise 리스트를 만들어줍니다.
    seoul['franchise'] = np.nan
    #print(seoul)


    ## 5-2 인덱스에 해당하는 부분만 1로 채워줍니다.
    for i in result:
        seoul['franchise'].iloc[i] = 1


    ## 5-3 null 값은 0으로 대체
    seoul['franchise'] = seoul['franchise'].fillna(0)
    #print(seoul)


    ## 5-4 구, 동 컬럼 추가
    addr_list = seoul['SITEWHLADDR'].str.split(' ')
    seoul['gu'] = addr_list.str.get(1)
    seoul['dong'] = addr_list.str.get(2)


    ## 5-5 저장
    #seoul.to_csv("raw_data/seoul_result.csv", index=False, encoding='utf-8-sig')

    # DB적재
    from sqlalchemy import create_engine
    import pymysql
    pymysql.install_as_MySQLdb()

    user="root"
    password="1234"
    url="localhost:3306/airflow_test"
    table="seoul_restarant"

    db_connection = create_engine(f'mysql+mysqldb://{user}:{password}@{url}', encoding='utf-8')
    seoul.to_sql(name=table, con=db_connection, if_exists='replace', index=False)
