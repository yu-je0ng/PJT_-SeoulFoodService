import plotly.express as px
from plotly.offline import plot
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots

from .models import GdpEconomicGrowthRate, GniPerCapita, SeoulCommercialArea, BusinessLoanInterest, ConsumerPriceIndex, SeoulRestaurant


# 실질 GDP/GNI 증가율 비교
def economic_real ():
    df1 = pd.DataFrame(list(GdpEconomicGrowthRate.objects.all().values()))
    df2 = pd.DataFrame(list(GniPerCapita.objects.all().values()))

    df = pd.merge(df1, df2, how='inner', on=None)
    df['year'] = df['year'].astype(int)
    df.set_index('year', inplace=True)
    df = df.applymap(lambda x: x.replace(',', '')).astype(float)

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=df.index, y=df['economic_growth_rate'], name="실질 GDP 증가율", mode='lines+markers',
                   marker=dict(color='royalblue')), secondary_y=False)
    fig.add_trace(
        go.Scatter(x=df.index, y=df['real_gni_growth_rate'], name="실질 GNI 증가율", mode='lines+markers',
                   marker=dict(color='turquoise')), secondary_y=True)

    fig.update_traces(hovertemplate='%{x}년: %{y}%증가<extra></extra>')
    fig.update_layout(title={'text': '실질 GDP/GNI 증가율 비교', 'font_size': 18, 'y': 0.95, 'x': 0.5,
                             'xanchor': 'center', 'yanchor': 'top'}, template='plotly_white', showlegend=False,
                      xaxis_showgrid=False, yaxis_showgrid=False)
    fig.update_xaxes(title_text="", tickangle=45)
    fig.update_yaxes(visible=False, showticklabels=False)

    plot_div = plot(fig, output_type='div')

    return plot_div

# 명목 GDP/ GNI 비교
def economic_nomial():
    df1 = pd.DataFrame(list(GdpEconomicGrowthRate.objects.all().values()))
    df2 = pd.DataFrame(list(GniPerCapita.objects.all().values()))
    df = pd.merge(df1, df2, how='inner', on=None)
    df['year'] = df['year'].astype(int)
    df.set_index('year', inplace=True)
    df = df.applymap(lambda x: x.replace(',', '')).astype(float)

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Bar(x=df.index, y=df['nominal_gdp'], name="명목 GDP", width=0.5,
                         marker_color='cornflowerblue', yaxis='y1'))
    fig.add_trace(go.Bar(x=df.index, y=df['nominal_gni_per_capita'], name="명목 GNI", offset=0.1, width=0.5,
                         marker_color='paleturquoise', yaxis='y2'))

    fig.update_layout(title={'text': '명목 GDP/GNI 비교', 'font_size': 18, 'y': 0.95, 'x': 0.5,
                             'xanchor': 'center', 'yanchor': 'top'}, template='plotly_white', showlegend=False,
                      xaxis_showgrid=False, yaxis_showgrid=False)
    fig.update_xaxes(title_text="", tickangle=45)
    fig.update_yaxes(visible=False, showticklabels=False)
    plot_div = plot(fig, output_type='div')

    return plot_div


# 지역별 유동인구수
    # 인구기준 : 명/ha
def location_foot_traffic():

    df = pd.DataFrame(list(SeoulCommercialArea.objects.all().values()))
    df_loc = df.groupby('gu_name').mean()
    df_loc.drop('index_year', axis=1, inplace=True)

    seoul_geo = 'https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json'

    fig = px.choropleth(df_loc, geojson=seoul_geo, locations=df_loc.index, featureidkey='properties.name',
                        color='foot_traffic', color_continuous_scale='Blues')
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_coloraxes(showscale=False)
    fig.update_layout(title={'text': '지역구별 유동인구 수', 'font_size': 18, 'y': 0.95, 'x': 0.5,
                             'xanchor': 'center', 'yanchor': 'top'},
                      margin={"r": 0, "t": 0, "l": 0, "b": 0}, dragmode=False)

    plot_div = plot(fig, output_type='div')

    return plot_div

# 지역별 거주인구수
def location_region_traffic():
    df = pd.DataFrame(list(SeoulCommercialArea.objects.all().values()))
    df_loc = df.groupby('gu_name').mean()
    df_loc.drop('index_year', axis=1, inplace=True)

    seoul_geo = 'https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json'

    fig = px.choropleth(df_loc, geojson=seoul_geo, locations=df_loc.index, featureidkey='properties.name',
                        color='population', color_continuous_scale='Blues')
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_coloraxes(showscale=False)
    fig.update_layout(title={'text': '지역구별 거주인구 수', 'font_size': 18, 'y': 0.95, 'x': 0.5,
                             'xanchor': 'center', 'yanchor': 'top'},
                      margin={"r": 0, "t": 0, "l": 0, "b": 0}, dragmode=False)
    plot_div = plot(fig, output_type='div')

    return plot_div

# 지역별 직장인구수
def location_work_traffic():
    df = pd.DataFrame(list(SeoulCommercialArea.objects.all().values()))
    df_loc = df.groupby('gu_name').mean()
    df_loc.drop('index_year', axis=1, inplace=True)

    seoul_geo = 'https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json'

    fig = px.choropleth(df_loc, geojson=seoul_geo, locations=df_loc.index, featureidkey='properties.name',
                        color='workers', color_continuous_scale='Blues')
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_coloraxes(showscale=False)
    fig.update_layout(title={'text': '지역구별 직장인구 수', 'font_size': 18, 'y': 0.95, 'x': 0.5,
                             'xanchor': 'center', 'yanchor': 'top'},
                      margin={"r": 0, "t": 0, "l": 0, "b": 0}, dragmode=False)
    plot_div = plot(fig, output_type='div')

    return plot_div

# 지역별 음식점 수(밀도)
def location_store_density():
    df = pd.DataFrame(list(SeoulCommercialArea.objects.all().values()))
    df_loc = df.groupby('gu_name').mean()
    df_loc.drop('index_year', axis=1, inplace=True)

    seoul_geo = 'https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json'

    fig = px.choropleth(df_loc, geojson=seoul_geo, locations=df_loc.index, featureidkey='properties.name',
                        color='density', color_continuous_scale='Blues')
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_coloraxes(showscale=False)
    fig.update_layout(title={'text': '지역구별 음식점 수(밀도)', 'font_size': 18, 'y': 0.95, 'x': 0.5,
                             'xanchor': 'center', 'yanchor': 'top'},
                      margin={"r": 0, "t": 0, "l": 0, "b": 0}, dragmode=False)
    plot_div = plot(fig, output_type='div')

    return plot_div

# 은행별 평균 개인 사업자 대출금리
def business_loan_interest():
    df = pd.DataFrame(list(BusinessLoanInterest.objects.all().values()))

    df.columns = ['bank', 'number_2017', 'number_2018', 'number_2019']

    df_loan = df.transpose()

    df_loan.columns = ['BNK경남은행', 'BNK부산은행', 'DGB대구은행', 'IBK기업은행', 'KB국민은행', 'KDB산업은행', 'NH농협은행', 'SH수협은행', '광주은행',
                       '스탠다드차타드은행', '신한은행', '우리은행', '전북은행', '제주은행', '하나은행', '한국씨티은행']
    df_loan.drop('bank', inplace=True)

    # display(df_loan)

    fig = px.line(df_loan, markers=True)

    fig.update_layout(title={'text': '평균 개인사업자 대출금리', 'font_size': 18, 'y': 0.95, 'x': 0.5,
                             'xanchor': 'center', 'yanchor': 'top'}, template='plotly_white', showlegend=False)
    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="", visible=False, showticklabels=False)

    plot_div = plot(fig, output_type='div')

    return plot_div

# 소비자 물가지수 변화율
def consumer_price_index():
    df_cpi = pd.DataFrame(list(ConsumerPriceIndex.objects.all().values()))
    df_cpi.set_index('years', inplace=True)

    # display(df_cpi)

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Bar(x=df_cpi.index, y=df_cpi['cpi'], name="소비자물가지수",
                         marker=dict(color=df_cpi['cpi'], colorscale='blues'), yaxis='y1'))

    fig.add_trace(go.Scatter(x=df_cpi.index, y=df_cpi['cpi_inflation'], name="증가율", mode='lines+markers',
                             marker=dict(color='pink'), yaxis='y2'))

    fig.update_layout(title={'text': '소비자물가지수(CPI) 변화(2020=100)', 'font_size': 18, 'y': 0.9, 'x': 0.5,
                             'xanchor': 'center', 'yanchor': 'top'}, template='plotly_white', showlegend=False,
                      xaxis_showgrid=False, yaxis_showgrid=False)

    fig.update_xaxes(title_text="")
    fig.update_yaxes(visible=False, showticklabels=False)

    fig.update_yaxes(range=[70, 103], secondary_y=False)
    fig.update_yaxes(range=[0, 4.5], secondary_y=True)
    plot_div = plot(fig, output_type='div')

    return plot_div

# 구별 프랜차이즈 현황
def seoul_restaurant():
    df_res = pd.DataFrame(list(SeoulRestaurant.objects.all().values()))
    df_res_all = df_res.groupby('gu')['franchise'].count()
    df_res_fr = df_res.groupby('gu')['franchise'].sum()
    df_res = pd.merge(df_res_all, df_res_fr, how='inner', on='gu')
    df_res.columns = ['count', 'Yes']
    df_res['No'] = df_res['count'] - df_res['Yes']
    df_res.drop('count', axis=1, inplace=True)

    # fig = px.bar(df_res, color_discrete_sequence=['pink', 'skyblue'])
    fig = go.Figure()
    fig.add_bar(x=df_res.index, y=df_res['Yes'], marker_color='cornflowerblue')
    fig.add_bar(x=df_res.index, y=df_res['No'], marker_color='paleturquoise')

    fig.update_layout(title={'text': '지역구별 프랜차이즈 현황', 'font_size': 40, 'y': 0.95, 'x': 0.5,
                             'xanchor': 'center', 'yanchor': 'top'}, barmode='relative', template='plotly_white',
                      showlegend=False, xaxis_showgrid=False, yaxis_showgrid=False)

    fig.update_xaxes(title_text="")
    fig.update_yaxes(visible=False, showticklabels=False)
    plot_div = plot(fig, output_type='div')

    return plot_div