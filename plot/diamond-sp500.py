import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import matplotlib.animation as anim
from matplotlib import dates

fig = plt.figure("xxxx", figsize=(50,30))

path1 = r'../scraped/diamond_commercial.csv'
df1 = pd.read_csv(path1, nrows=3135)
onect=df1['1 Carat Commercial Index']
halfct=df1['0.5 Carat Commercial Index']
pt3ct=df1['0.3 Carat Commercial Index']

path2=r'../scraped/sp500.csv'
df2 = pd.read_csv(path2, header=0, skiprows=range(1,9917), nrows=3135)
y=df2['S&P 500 COMPOSITE'] 

x=df2['Date']
new_x=[]
for elem in x:
	new=datetime.datetime.strptime(elem, '%d/%m/%Y')
	new_x.append(new)
	
years=dates.YearLocator()

ax1=fig.add_subplot(111)
ax1.clear()
ax1.plot(new_x,y, '-',color='#245678')
ax1.set_ylabel('S&P 500 Composite', color='#245678')

ax2=ax1.twinx()
ax2.plot(new_x,onect, '-',color='#ad3434', label='1 Carat Commercial')
ax2.plot(new_x, halfct, '-',color="#222222", label='0.5 Carat Commercial')
ax2.plot(new_x, pt3ct, '-',color="#3c6630", label='0.5 Carat Commercial')
ax2.set_ylabel('Diamond Commercial Index', color='#ad3434')
xfmt=dates.DateFormatter('%Y')
ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(xfmt)

plt.grid(True)
fig.autofmt_xdate()
plt.savefig('diamond-sp500.png')
plt.show()