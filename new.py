import pandas as pd
import numpy as np
from scipy.optimize import minimize
from scipy import optimize
from scipy import stats as stats
import datetime
import matplotlib.pyplot as plt

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

q10=np.percentile(x,10)
q5=np.percentile(x,5)
q1=np.percentile(x,1)

dq10=[]
for elem in x:
	if elem<q10:
		dq10.append(1)
	else:
		dq10.append(0)
dq10=np.array(dq10)
print dq10

dq5=[]
for elem in x:
	if elem<q5:
		dq5.append(1)
	else:
		dq5.append(0)
dq5=np.array(dq5)
print dq5

dq1=[]
for elem in x:
	if elem<q1:
		dq1.append(1)
	else:
		dq1.append(0)
dq1=np.array(dq1)
print dq1

def reg(params):
	a=params[0]
	c0=params[1]
	c1=params[2]
	c2=params[3]
	c3=params[4]
	et=params[5]

	ypred=a+x*(c0+c1*dq10+c2*dq5+c3*dq1)+et
	LL= -np.sum(stats.norm.logpdf(y, loc=ypred, scale=et))
	return LL

initParams=[0.1,0.1,0.1,0.1,0.1,0.1]
results=minimize(reg, initParams, method='nelder-mead')
print results.x

estParms=results.x
residuals=y-(estParms[0]+x*(estParms[1]+estParms[2]*dq10+estParms[3]*dq5+estParms[4]*dq1))
#print residuals

def garch11(param, y):
	n=len(y)
	pi, alpha, beta=param
	ht=np.ones(n)
	ht[0]=np.var(residuals)
	for i in range (1,n):
		ht[i]=pi+alpha*residuals[i-1]**2+beta*(ht[i-1])
	stdRes=residuals/np.sqrt(ht)
	LogL=-((0.5*np.log(2*np.pi)+0.5*np.log(ht)+0.5*stdRes**2).sum())
	return LogL

R=optimize.fmin(garch11,np.array([.1,.1,.1]),args=(y,),full_output=1)
print R

pi=R[0][0]
alpha=R[0][1]
beta=R[0][2]

ht=np.ones(len(y))
ht[0]=np.var(residuals)
for i in range (1,len(y)):
	ht[i]=pi+alpha*residuals[i-1]**2+beta*(ht[i-1])
print ht