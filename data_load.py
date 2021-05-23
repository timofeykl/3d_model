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

df.to_excel('source_data.xlsx')