import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns

import warnings

# 경고 무시, 폰트 지정
warnings.filterwarnings(action='ignore')
plt.rcParams['font.family'] = 'Malgun Gothic'


restaurant = pd.read_csv(r"C:\Users\wogml\1_shutdown\data\seoul_restaurant.csv",\
                            encoding="utf-8")

ax = plt.subplots(figsize=(12, 7))

ax = sns.countplot(x="GU", 
              hue='IS_FRANCHISE', 
              palette='Set3', 
              dodge=False, 
              data=restaurant)

ax.set_xticklabels(ax.get_xticklabels(), rotation = 60)