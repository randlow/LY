import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import matplotlib.animation as anim
from matplotlib import dates

fig = plt.figure("xxxx", figsize=(50,30))

path1 = r'../scraped/gold.csv'
df1 = pd.read_csv(path1, skiprows=range(1,4437), nrows=7580)
y1=df1['Gold Bullion']

path2=r'../scraped/sp500.csv'
df2 = pd.read_csv(path2, header=0, names=['Date', 'PI'], skiprows=range(1,5483), nrows=7580)
y2=df2['PI']

x=df2['Date']
new_x=[]
for elem in x:
	new=datetime.datetime.strptime(elem, '%d/%m/%Y')
	new_x.append(new)
	
years=dates.YearLocator()

ax1=fig.add_subplot(111)
ax1.clear()
ax1.plot(new_x,y2, '-',color='#245678')
ax1.set_ylabel('S&P 500 Composite', color='#245678')

ax2=ax1.twinx()
ax2.plot(new_x,y1, '-',color='#ad3434')
ax2.set_ylabel('Gold Price (U$/Troy Ounce)', color='#ad3434')
xfmt=dates.DateFormatter('%Y')
ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(xfmt)

plt.grid(True)
fig.autofmt_xdate()
plt.savefig('gold-sp500.png')
plt.show()