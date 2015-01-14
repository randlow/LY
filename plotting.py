import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
from matplotlib import dates

def plotPrice():
	fig=plt.figure(" ", figsize=(35,15))
	goldPath=r'./scraped/gold.csv'
	silverPath=r'./scraped/silver.csv'
	platiPath=r'./scraped/platinum.csv'
	palladPath=r'./scraped/palladium.csv'
	spPath=r'./scraped/sp500.csv'
	dfGold=pd.read_csv(goldPath, header=0)  #, skiprows=range(1,3567), nrows=522
	dfSilver=pd.read_csv(silverPath, header=0)
	dfPlati=pd.read_csv(platiPath, header=0)
	dfPallad=pd.read_csv(palladPath, header=0)
	dfSP=pd.read_csv(spPath, header=0)

	date=dfGold['Date']
	date_x=[]
	for elem in date:
		newdate=datetime.datetime.strptime(elem, '%d/%m/%Y')
		date_x.append(newdate)

	mths=dates.MonthLocator()
	ax1=fig.add_subplot(111)
	ax1.clear()
	ax1.plot_date(date_x, dfSP['S&P 500 COMPOSITE'], '-', color='#262626')
	ax1.set_ylabel('S&P Price Index', color='#262626')

	ax2=ax1.twinx()
	ax2.plot_date(date_x,dfGold['Price'], '-.',color='#fb7400', label="Gold")
	ax2.plot_date(date_x,dfPlati['Price'], '-',color='#278296', alpha=0.7, label='Platinum')
	ax2.plot_date(date_x,dfPallad['Price'], '-',color='#ec3743', alpha=0.7, label='Palladium')
	ax2.plot_date(date_x,dfSilver['Cts/Troy Ounce'], '--',color='#333333', alpha=0.6, label='Silver')

	ax2.set_ylabel('U$(Cts)/Troy Ounce')

	xfmt=dates.DateFormatter('%m/%Y')
	ax1.xaxis.set_major_locator(mths)
	ax1.xaxis.set_major_formatter(xfmt)
	plt.grid(True)
	plt.legend(loc=1)
	fig.autofmt_xdate()
	plt.show()
plotPrice()

def plotDiamond():
	fig=plt.figure(" ", figsize=(35,15))
	dcPath=r'./scraped/diamond_commercial.csv'
	spPath=r'./scraped/sp500.csv'
	dfDC=pd.read_csv(dcPath, header=0, names=['Date','1 Carat','0.5 Carat','0.3 Carat'])
	dfSP=pd.read_csv(spPath, header=0, skiprows=range(1,2871))

	date=dfDC['Date']
	date_x=[]
	for elem in date:
		newdate=datetime.datetime.strptime(elem, '%d/%m/%Y')
		date_x.append(newdate)
	print len(date_x)
	years=dates.YearLocator()
	ax1=fig.add_subplot(111)
	ax1.clear()
	ax1.plot_date(date_x, dfSP['S&P 500 COMPOSITE'], '-', color='#262626')
	ax1.set_ylabel('S&P Price Index', color='#262626')

	ax2=ax1.twinx()
	ax2.plot_date(date_x,dfDC['1 Carat'], '-.',color='#fb7400', alpha=0.8, label="1 Carat")
	ax2.plot_date(date_x,dfDC['0.5 Carat'], '-',color='#ec3743', alpha=0.7, label="0.5 Carat")
	ax2.plot_date(date_x,dfDC['0.3 Carat'], '-',color='#278296', alpha=0.7, label="0.3 Carat")
	ax2.set_ylabel('Diamond Commercial Index')

	xfmt=dates.DateFormatter('%Y')
	ax1.xaxis.set_major_locator(years)
	ax1.xaxis.set_major_formatter(xfmt)
	plt.grid(True)
	plt.legend(loc=2)
	fig.autofmt_xdate()
	plt.show()

#plotDiamond()