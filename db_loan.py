import pandas as pd
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

df = pd.read_excel("export_excel.xlsx")


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
#
# dsn = """(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)
# (HOST=rnb-vmdwh-dbpr04.rci.renault.ru)(PORT=1521))
# (ADDRESS=(PROTOCOL=TCP)(HOST=rnb-vmdwh-dbpr03.rci.renault.ru)(PORT=1521))
# (LOAD_BALANCE= yes))(CONNECT_DATA=(SERVER=DEDICATED)(SERVICE_NAME=DWHPR_DG)))
# """
# connection = cx.connect("iz01340", "iz01340", dsn)
#
# print('fine')
# query = """
# select
# brand
# , PRODUCT_NAME
# , GENERATION
# , GOS_PROGRAM_STATUS
# , BRAND
# , CAR_PRICE
# , INITIAL_PAYMENT
# , TOTAL_FINANCE_AMOUNT
# , CPI_PREMIUM_CONTRACT
# , CASCO_PREMIUM
# , M_OF_FINANCING
# , Y_OF_FINANCING
# , MODEL_CODE
# , INIT_CONTRIB_INT_RATE
# , FIO_APPLICANT
# , LOAN_FOR_CAR_SUM
# , dealer_service_sum
# , GOS_PROGRAM_NAME
# , GOS_PROGRAM_AMOUNT
# , GOS_PROGRAM_SUBSIDY
# from dwh.v_indicator_fpa
# WHERE CREDIT_ISSUE_DATE>=DATE'2020-08-01' AND CREDIT_ISSUE_DATE<DATE'2021-02-01'
# AND BRAND='Renault' and NEW_USED='NEW'
#            """
#
# dwh_ind = pd.read_sql(query, con=connection)
# print(1)
#
# print(dwh_ind.shape)
# print(dwh_ind[['M_OF_FINANCING', 'LOAN_FOR_CAR_SUM',
#                'CAR_PRICE', 'INIT_CONTRIB_INT_RATE']].
#       groupby(['M_OF_FINANCING']).
#       agg(['mean', 'count']))
#
# print('done')
