# ! pip install WordCloud
# ! pip install matplotlip

from sqlalchemy import create_engine
import pandas as pd
import numpy as np

from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def data_load(db, table):
    user_id = 'root'
    user_pw = '1234'
    ip = '35.79.131.28'
    port = '3306'
    
    db_connection_path = f'mysql+mysqldb://{user_id}:{user_pw}@{ip}:{port}/{db}'
    
    df = pd.read_sql_table(table, con=create_engine(db_connection_path, encoding='utf-8').connect())
    return df

df_loc = data_load('team03_erd', 'RESTAURANTS')
df2 = df_loc[["STORE_TYPE","GU_NAME"]]

df3 = df2.groupby(['GU_NAME', 'STORE_TYPE'])
df4 = df3.size().reset_index(name='counts')

# 지역 분류
df4 = df4[df4['GU_NAME'] == '중랑구'] 
freq = df4.set_index("STORE_TYPE").to_dict()["counts"]

# mask 
masking_img = np.array(Image.open('./wordcloudmask/중랑구.png'))

wordcloud = WordCloud(font_path = './NanumSquareEB.ttf', mask = masking_img,
                      width = 800, height = 800, background_color='white',
                      colormap = "winter")
wordcloud.fit_words(freq).to_image()

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

# Save the image in the img folder:
wordcloud.to_file("./wordcloud/중랑구.png")