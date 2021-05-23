import cx_Oracle as cx
import pandas as pd
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.dates as mdates
import matplotlib.cbook as cbook


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
WHERE CREDIT_ISSUE_DATE>=DATE'2020-08-01' AND CREDIT_ISSUE_DATE<DATE'2021-02-24'
AND BRAND='Renault' and NEW_USED='NEW'
           """

df = pd.read_sql(query, con=connection)
print(1)


model = df['MODEL_CODE'].str.split('_').str[0]
model = model.str.upper()

df['MODEL'] = model


df["CAR_PRICE"] = df["CAR_PRICE"].div(1000).round(2)


df = df.groupby(['MODEL', 'CREDIT_ISSUE_DATE'])["CAR_PRICE"]\
    .agg(['count', 'mean'])

df = df.sort_values(by='CREDIT_ISSUE_DATE')

price = df['mean'] < 2000

df = df[price]

df.to_excel('temp_output.xlsx')

df = pd.read_excel('temp_output.xlsx')

print(df)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')






# locator = mdates.AutoDateLocator()
# formatter = mdates.ConciseDateFormatter(locator)
#
#
# ax.xaxis.set_major_locator(locator)
# ax.xaxis.set_major_formatter(formatter)


# For each set of style and range settings, plot n random points in the box
# defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].

# for c, m, df['mean'].max, df['mean'].min in [('b', 'o', 790, 1500), ('r', '^', 1500, 2410)]:

dates = df['CREDIT_ISSUE_DATE']
dates_formatted = [pd.to_datetime(d).month for d in dates]




zs = df['mean']
ys = df['count']
xs = df.index
ax.scatter(xs, ys, zs
               # , c=c, marker=m
               )



ax.set_zlabel('AVG_CAR_PRICE - krub ')
ax.set_ylabel('NUMBER_OF_SALES')
ax.set_xlabel('CREDIT_DATE')

ax.xaxis.set_ticks(xs)
ax.xaxis.set_ticklabels(dates_formatted)

plt.locator_params(axis='x', nbins=20)



plt.show()


#
# zs = df['mean']
# ys = df['count']
# xs = df['CREDIT_ISSUE_DATE']
#
#
# for c, m, df['mean'].max, df['mean'].min in [('b', 'o', 790, 1500), ('r', '^', 1500, 2410)]:
#     ax.scatter(xs, ys, zs, c=c, marker=m)

# locator = mdates.AutoDateLocator()
# formatter = mdates.ConciseDateFormatter(locator)
# days = mdates.DateLocator()
#
# ax.xaxis.set_major_locator(locator)
# ax.xaxis.set_major_formatter(formatter)
# ax.xaxis.set_minor_locator(days)
#
# ax.format_xdata = mdates.DateFormatter('%m-%d')
# ax.grid(True)
# fig.autofmt_xdate()






