import pandas as pd
import numpy as np
import scipy.stats as stats
'''
def calc(name):
	path=r'./scraped/%s.csv' %name
	df = pd.read_csv(path, header=0, names=['Date', 'Price'])
	price = df['Price']
	returnSeries = []
	for i in range(0,len(price)-1):
		logRet = np.log(price[i+1]/price[i])
		returnSeries.append(logRet)
	return np.array(returnSeries)

sp500Ret=calc('sp500')
name=raw_input('Index name: ')
ret=calc(name)
print np.mean(ret)
print np.std(ret)
print np.min(ret)
print np.max(ret)
print stats.skew(ret)
print stats.kurtosis(ret)
print np.corrcoef(ret,sp500Ret)
'''

def readSP():
	path=r'./scraped/sp500.csv'
	df=pd.read_csv(path, header=0, skiprows=range(1,2871))
	idx = df['S&P 500 COMPOSITE']
	returnSeries = []
	for i in range(0,len(idx)-1):
		logRet = np.log(idx[i+1]/idx[i])
		returnSeries.append(logRet)
	return np.array(returnSeries)

sp500Ret=readSP()

def calcDiamond(name, carat):
	path=r'./scraped/%s.csv' %name
	df = pd.read_csv(path, header=0, names=['Date', '1ct','0.5ct','0.3ct'])
	col_name='%sct' %carat
	price=df[col_name]
	returnSeries=[]
	for i in range(0,len(price)-1):
		logRet = np.log(price[i+1]/price[i])
		returnSeries.append(logRet)
	return np.array(returnSeries)

name=raw_input('Index name: ')
carat=raw_input('Carat: ')
ret=calcDiamond(name, carat)
print np.mean(ret)
print np.std(ret)
print np.min(ret)
print np.max(ret)
print stats.skew(ret)
print stats.kurtosis(ret)
print np.corrcoef(ret,sp500Ret)