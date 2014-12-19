import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import matplotlib.animation as anim
from matplotlib import dates

fig = plt.figure(figsize=(50,30))

path1 = r'../scraped/rare_earths.csv'
df1 = pd.read_csv(path1, nrows=2800)
yt=df1['Yttrium']
nd=df1['Neodymium']

path2=r'../scraped/sp500.csv'
df2 = pd.read_csv(path2, header=0, skiprows=range(1,10254), nrows=2800)
y=df2['S&P 500 COMPOSITE'] 

x=df2['Date']
new_x=[]
for elem in x:
	new=datetime.datetime.strptime(elem, '%d/%m/%Y')
	new_x.append(new)
	
years=dates.YearLocator()

ax1=fig.add_subplot(111)
ax1.clear()
ax1.plot(new_x,y, '-',color='#245678', label='S&P 500 Composite Index')
ax1.set_ylabel('S&P 500 Composite', color='#245678')

ax2=ax1.twinx()
ax2.plot(new_x,yt, '-',color='#fc6262', label='Yttrium')
ax2.plot(new_x,nd, '-',color="#222222", label='Neodymium')
ax2.set_ylabel('Rare Earths (USD 99% FOB China)', color='#ad3434')
xfmt=dates.DateFormatter('%Y')
ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(xfmt)

plt.legend(loc=2)
plt.grid(True)
fig.autofmt_xdate()
plt.savefig('re-sp500.png')
plt.show()