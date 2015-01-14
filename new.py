import pandas as pd
import numpy as np
from scipy.optimize import minimize
from scipy import optimize
from scipy import stats as stats
import datetime
import matplotlib.pyplot as plt
from matplotlib import dates
import statsmodels
#import rpy2.objects as robjects

# Calculating log returns from asset prices
def calcLogRet(path,rangeVal,rowsVal,priceName):
	df = pd.read_csv(path,skiprows=range(1,rangeVal),nrows=rowsVal)
	price = df[priceName]
	returnSeries = []
	for i in range(0,len(price)-1):
		logRet = np.log(price[i+1]/price[i])
		returnSeries.append(logRet)
	return np.array(returnSeries)
"""		
def gReturn():
	path = r'./scraped/gold.csv'
	df = pd.read_csv(path, skiprows=range(1,2913), nrows=7826)
	goldPrice=df['Gold Bullion']
	gReturn=[]
	for i in range(0,len(goldPrice)-1):
		log=np.log(goldPrice[i+1]/goldPrice[i])
		gReturn.append(log)
	return np.array(gReturn)


def iReturn():
	path=r'./scraped/sp500.csv'
	df = pd.read_csv(path, header=0, skiprows=range(1,3959), nrows=7826, names=['Name', 'PI'])
	idx=df['PI']
	iReturn=[]
	for i in range(0, len(idx)-1):
		log=np.log(idx[i+1]/idx[i])
		iReturn.append(log)
	return np.array(iReturn)
	
x=iReturn()
y=gReturn()
"""

goldRet = calcLogRet(r'./scraped/gold.csv',1,7826,'Price')
usRet = calcLogRet(r'./scraped/sp500.csv',3959,7826,'S&P 500 COMPOSITE')

#print goldRet

# Calculating quartile values from returns series
q10=np.percentile(usRet,10)
q5=np.percentile(usRet,5)
q1=np.percentile(usRet,1)

# Generating indicator variable series for each percentiles
def genIndVar(series,percentileVal):
	indSeries=[]
	for i in range(0,len(series)):
		if series[i]<percentileVal:
			indSeries.append(1)
		else:
			indSeries.append(0)
	return np.array(indSeries)		

indVar_q10 = genIndVar(usRet,q10)
indVar_q5 = genIndVar(usRet,q5)
indVar_q1 = genIndVar(usRet,q1)
'''
X=np.column_stack((np.ones(len(usRet)),usRet,indVar_q10,indVar_q5,indVar_q1))
print X

res=LikelihoodModel(goldRet,X).fit()

print (res.summary())



def reg(params):
	a=params[0]
	c0=params[1]
	c1=params[2]
	c2=params[3]
	c3=params[4]
	et=params[5]

	ypred=a+usRet*(c0+c1*indVar_q10+c2*indVar_q5+c3*indVar_q1)+et
	LL= -np.sum(stats.norm.logpdf(ypred, loc=goldRet, scale=et))
	return LL

initParams=[0.1,0.1,0.1,0.1,0.1,0.1]
results=minimize(reg, initParams, method='BFGS')
print results.x

estParms=results.x
residuals=goldRet-(estParms[0]+usRet*(estParms[1]+estParms[2]*indVar_q10+estParms[3]*indVar_q5+estParms[4]*indVar_q1))
residuals=residuals/1000
print residuals
stdRes = (residuals-np.mean(residuals))/np.std(residuals)
#print stdRes
print np.var(residuals)
print np.std(residuals)

def garch11(param, y):
	n=len(y)
	pi, alpha, beta=param
	ht=np.ones(n)
	ht[0]=np.var(residuals)
	for i in range (1,n):
		ht[i]=pi+alpha*residuals[i-1]**2+beta*(ht[i-1])
	LogL=-((0.5*np.log(2*np.pi)+0.5*np.log(ht)+0.5*stdRes**2).sum())
	return LogL

R=optimize.fmin(garch11,np.array([.1,.1,.1]),args=(goldRet,),full_output=1)
print R

pi=R[0][0]
alpha=R[0][1]
beta=R[0][2]



def plot():
	fig = plt.figure("xxxx", figsize=(50,30))
	path2 = r'./scraped/gold.csv'
	path=r'./scraped/ht.csv'
	df1 = pd.read_csv(path2, nrows=7825, header=0)
	df2=pd.read_csv(path)
	date=df1['Name']
	ht=df2['ht']
	new_x=[]
	for elem in date:
		new=datetime.datetime.strptime(elem, '%d/%m/%Y')
		new_x.append(new)

	years=dates.YearLocator()
	ax=fig.add_subplot(111)
	ax.clear()
	ax.plot_date(new_x,ht, '-',color='#245678')
	xfmt=dates.DateFormatter('%Y')
	ax.xaxis.set_major_locator(years)
	ax.xaxis.set_major_formatter(xfmt)
	plt.grid(True)
	fig.autofmt_xdate()
	plt.show()
plot()
'''

