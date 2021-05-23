import pandas as pd
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

df = pd.read_excel("export_excel.xlsx")


#here we just grouping out data

model = df['MODEL_CODE'].str.split('_').str[0]
model = model.str.upper()

df['MODEL'] = model

df['M_OF_FINANCING'] = df['M_OF_FINANCING'].replace({8:1, 9:2, 10:3, 11:4, 12:5, 1:6})

df["CAR_PRICE"] = df["CAR_PRICE"].div(1000).round(2)
print(df)
group_m_model = df.groupby(["MODEL", "M_OF_FINANCING"])["LOAN_FOR_CAR_SUM"].describe().unstack()
print(group_m_model)

df = df.groupby(["MODEL", "M_OF_FINANCING"])["CAR_PRICE"]\
    .agg(['count', 'mean'])

group_m_model.to_excel('LOAN_FOR_CAR.xlsx')

