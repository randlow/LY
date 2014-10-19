import pandas as pd
import numpy as np
from scipy.optimize import minimize
import scipy.stats as stats
import json
import matplotlib.pyplot as plt

def readGold():
	path = r'./scraped/gold.json'
	data=[]
	with open(path) as f:
		for line in f:
			data.append(json.loads(line))

	y=[]
	for d in data:
		y.append(float(d['closeprice']))
	return np.array(y)

def readIndex(name):
	path=r'./scraped/%s.json' %name
	data=[]
	with open(path) as f:
		for line in f:
			data.append(json.loads(line))

	x=[]
	for d in data:
		x.append(float(d['adjclose'].encode('utf-8').replace(',','')))
	x=np.array(x)
	return x[::-1]

name=raw_input('Index name: ')
x=readIndex(name)
y=readGold()

#A=np.vstack([x,np.ones(len(x))]).T
#a,b=np.linalg.lstsq(A,y)[0]
#print a,b

def regress1(params):
	a = params[0]
	bt = params[1]
	et=params[2]

	ypred = a+bt*x+et
	LL= -np.sum(stats.norm.logpdf(y,loc=ypred, scale=et))
	return(LL)

initParams1=[5,5,5]
results1=minimize(regress1, initParams1, method='nelder-mead')

print results1.x

estParms1=results1.x
yout=ypred=estParms1[0]+estParms1[1]*x+estParms1[2]

#gt10= df[df>df.quantile(0.1)].dropna()   #c1,c2,c3=0
#aygt10=gt10.as_matrix(columns=None)

def regress2(params):
	c0=params[0]
	c1=params[1]
	c2=params[2]
	c3=params[3]

	#bpred=c0+c1+c2+c3
	q10=np.percentile(x,10)
	q5=np.percentile(x,5)
	q1=np.percentile(x,1)

	for elem in x:
		if elem <q1:
			bpred=c0+c1+c2+c3
		elif elem>q1 and elem<q5:
			bpred=c0+c1+c2
		elif elem>q5 and elem<q10:
			bpred=c0+c1
		else:
			bpred=c0
	
	LL= -np.sum(stats.norm.logpdf(estParms1[1],loc=bpred))
	return(LL)

initParams2=[0,0,0,0]
results2=minimize(regress2, initParams2, method='nelder-mead')

print results2.x

#def garch(params):
	

def plot():
	plt.figure(figsize=(70,55))
	plt.plot(x,y,'o', color='#00398f')
	plt.plot(x,yout, 'g')  #?????????
	plt.grid(True)
	plt.show()

#plot()