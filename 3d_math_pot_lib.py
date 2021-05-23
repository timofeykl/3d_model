import cx_Oracle as cx
import pandas as pd
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


dsn = """(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)
(HOST=rnb-vmdwh-dbpr04.rci.renault.ru)(PORT=1521))
(ADDRESS=(PROTOCOL=TCP)(HOST=rnb-vmdwh-dbpr03.rci.renault.ru)(PORT=1521))
(LOAD_BALANCE= yes))(CONNECT_DATA=(SERVER=DEDICATED)(SERVICE_NAME=DWHPR_DG)))
"""
connection = cx.connect("iz01340", "iz01340", dsn)

print('fine')
query = """
select
brand
, PRODUCT_NAME
, GENERATION
, GOS_PROGRAM_STATUS
, BRAND
, CAR_PRICE
, INITIAL_PAYMENT
, TOTAL_FINANCE_AMOUNT
, CPI_PREMIUM_CONTRACT
, CASCO_PREMIUM
, M_OF_FINANCING
, Y_OF_FINANCING
, MODEL_CODE
, INIT_CONTRIB_INT_RATE
, FIO_APPLICANT
, LOAN_FOR_CAR_SUM
, dealer_service_sum
, GOS_PROGRAM_NAME
, GOS_PROGRAM_AMOUNT
, GOS_PROGRAM_SUBSIDY
, CREDIT_ISSUE_DATE
from dwh.v_indicator_fpa
WHERE CREDIT_ISSUE_DATE>=DATE'2020-08-01' AND CREDIT_ISSUE_DATE<DATE'2021-02-01'
AND BRAND='Renault' and NEW_USED='NEW'
           """

df = pd.read_sql(query, con=connection)
print(1)


model = df['MODEL_CODE'].str.split('_').str[0]
model = model.str.upper()

df['MODEL'] = model

df['M_OF_FINANCING'] = df['M_OF_FINANCING'].replace({'08':1, '09':2, '10':3, '11':4, '12':5, '01':6})

df["CAR_PRICE"] = df["CAR_PRICE"].div(1000).round(2)
# print(df)
# group_m_model = df.groupby(["MODEL", "M_OF_FINANCING"])["CAR_PRICE"].describe().unstack()
# print(group_m_model)

df = df.groupby(['MODEL', 'M_OF_FINANCING'])["CAR_PRICE"]\
    .agg(['count', 'mean'])


df.to_excel('output.xlsx')

df = pd.read_excel('output.xlsx')

print(df)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')



# For each set of style and range settings, plot n random points in the box
# defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
for c, m, df['mean'].max, df['mean'].min in [('b', 'o', 790, 1500), ('r', '^', 1500, 2410)]:
    zs = df['mean']
    ys = df['count']
    xs = df['M_OF_FINANCING']
    ax.scatter(xs, ys, zs, c=c, marker=m)

ax.set_zlabel('AVERAGE_CAR_PRICE')
ax.set_ylabel('NUMBER_OF_SALES')
ax.set_xlabel('M_OF_FINANCING')

plt.show()



# td = plt.figure().gca(projection='3d')
# td.scatter(df.index, df['count'], df["M_OF_FINANCING"])
# td.set_xlabel("M_OF_FINANCING")
# td.set_ylabel('Index')
# td.set_zlabel('count')
# plt.show()