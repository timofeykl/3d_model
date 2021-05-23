import cx_Oracle as cx
import pandas as pd
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#connection to Oracle DB stuff
dsn = """(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)
(HOST=!!!host_address)(PORT=!!!port))
(ADDRESS=(PROTOCOL=TCP)(HOST=!!!host_address)(PORT=1521))
(LOAD_BALANCE= yes))(CONNECT_DATA=(SERVER=DEDICATED)(SERVICE_NAME=!!!SERVICE_NAME)))
"""
connection = cx.connect("USER", "PASSWORD", dsn)

print('fine')
query = """
!!!easy select over here
           """

df = pd.read_sql(query, con=connection)
print(1)

#extracting everything before underscore 
model = df['AGG_COL'].str.split('_').str[0]
#trasforming it to uppercase
model = model.str.upper()

#changing column from previous perspective
df['MODEL'] = model

#hand made stuff 
#under analysis we are to consider earliest month as first one
df['MONTH'] = df['MONTH'].replace({'08':1, '09':2, '10':3, '11':4, '12':5, '01':6})

#k-ing and round-ing, baby
df["CPRICE"] = df["CAR_PRICE"].div(1000).round(2)

#check it out, baby
# print(df)
# group_m_model = df.groupby(["MODEL", "M_OF_FINANCING"])["CAR_PRICE"].describe().unstack()
# print(group_m_model)

#grouping out stuff
df = df.groupby(['MODEL', 'M_OF_FINANCING'])["CAR_PRICE"]\
    .agg(['count', 'mean'])

#nowhere to run from excel
df.to_excel('output.xlsx')

#let's exercise some more with excel
df = pd.read_excel('output.xlsx')
print(df)

#up to 3d we go
fig = plt.figure()
#password: Wolfenstein.. ...you name it
ax = fig.add_subplot(111, projection='3d')


#documentation quotes. you should be realising by now, that we can't be serious here ;)
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

# and another... method I think below 

# td = plt.figure().gca(projection='3d')
# td.scatter(df.index, df['count'], df["M_OF_FINANCING"])
# td.set_xlabel("M_OF_FINANCING")
# td.set_ylabel('Index')
# td.set_zlabel('count')
# plt.show()
