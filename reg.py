import pandas as pd
import numpy as np
from scipy.optimize import minimize
from scipy import optimize
import scipy.stats as stats
import datetime
import matplotlib.pyplot as plt

def gReturn():
	path = r'./scraped/gold.csv'
	df = pd.read_csv(path)
	goldPrice=df['USD']
	gReturn=[]
	for i in range(0,len(goldPrice)-1):
		log=np.log(goldPrice[i+1]/goldPrice[i])
		gReturn.append(log)
	return np.array(gReturn)

def iReturn(name):
	path=r'./scraped/%s.csv' %name
	df = pd.read_csv(path, header=0, names=['Name', 'PI'])
	idx=df['PI']
	iReturn=[]
	for i in range(0, len(idx)-1):
		log=np.log(idx[i+1]/idx[i])
		iReturn.append(log)

	print np.mean(iReturn)
	print min(iReturn)
	print max(iReturn)
	return np.array(iReturn)
	
name=raw_input('Index name: ')
x=iReturn(name)
y=gReturn()

#A=np.vstack([x,np.ones(len(x))]).T
#a,b=np.linalg.lstsq(A,y)[0]
#print a,b

def regress1(params):
	a = params[0]
	bt = params[1]
	et=params[2]

	ypred = a+bt*x
	LL= -np.sum(stats.norm.logpdf(y,loc=ypred, scale=et))
	return LL

initParams1=[5,5,5]
results1=minimize(regress1, initParams1, method='nelder-mead')
print results1.x

estParms1=results1.x
yout=ypred=estParms1[0]+estParms1[1]*x+estParms1[2]

'''
#Lst sqrs for checking purpose
A=np.vstack([x,np.ones(len(x))]).T
a,b=np.linalg.lstsq(A,y)[0]
print a,b

fig = plt.figure("xxxx", figsize=(70,55))
ax=fig.add_subplot(111)
ax.clear()
ax.plot(x,y,'o')
ax.plot(x,a*x+b,'r')
plt.grid(True)
plt.show()
'''

def regress2(params):
	c0=params[0]
	c1=params[1]
	c2=params[2]
	c3=params[3]

	#bpred=c0+c1+c2+c3
	q10=np.percentile(x,10)
	q5=np.percentile(x,5)
	q1=np.percentile(x,1)

	b=[]
	for elem in x:
		if elem <q1:
			bpred=c0+c1+c2+c3
		elif elem>q1 and elem<q5:
			bpred=c0+c1+c2
		elif elem>q5 and elem<q10:
			bpred=c0+c1
		else:
			bpred=c0
		b.append(bpred)

	LL= -np.sum(stats.norm.logpdf(b, loc=estParms1[1]))
	return LL

initParams2=[0.001,0.001,0.001,0.001]
results2=minimize(regress2, initParams2, method='nelder-mead')
print results2.x

u=np.ones(len(x))
for i in range(0, len(x)):
	u[i]=y[i]-estParms1[0]-estParms1[1]*x[i]

#print u

def garch(params, u):
	omega, alpha, beta = params**2
	n=len(u)
	h=np.ones(n)
	for i in range(1,n):
		h[i]=omega+alpha*u[i-1]**2+beta*h[i-1]


	LL=0.5*((np.log(h)+u**2/(h)).sum()+n/np.log(2*np.pi))
	return LL

results3=optimize.fmin(garch, np.array([0.01,0.01,0.01]), args=(u,), full_output=1)
#print results3

m=np.ones(len(x))
for i in (1, len(x)-1):
	m[i] = results3[0][0]+results3[0][1]*u[i-1]**2+results3[0][2]*m[i-1]

#print m

'''
def regress3():
	c0=params[0]
	c1=params[1]
	c2=params[2]
	c3=params[3]

	#bt = c0+c1+c2+c3
	q10=np.percentile(m,10)
	q5=np.percentile(m,5)
	q1=np.percentile(m,1)

	for elem in m:
		if elem <q1:
			bpred=c0+c1+c2+c3
		elif elem>q1 and elem<q5:
			bpred=c0+c1+c2
		elif elem>q5 and elem<q10:
			bpred=c0+c1
		else:
			bpred=c0

	LL= -np.sum(stats.norm.logpdf(estParms1[1],loc=bpred))
	return LL

initParams3=[0,0,0,0]
results3=minimize(regress3, initParams3, method='nelder-mead')
print results3.x
'''

def plot():
	fig = plt.figure("xxxx", figsize=(50,30))
	path1 = r'./scraped/gold.csv'
	df1 = pd.read_csv(path1)
	y1=df1['USD']

	path2=r'./scraped/world.csv'
	df2 = pd.read_csv(path2, header=0, names=['Date', 'PI'])
	y2=df2['PI']

	x=df2['Date']
	new_x=[]
	for elem in x:
		new=datetime.datetime.strptime(elem, '%d/%m/%Y')
		new_x.append(new)

	years=dates.YearLocator()

	ax1=fig.add_subplot(111)
	ax1.clear()
	ax1.plot_date(new_x,y2, '-',color='#245678')
	ax1.set_ylabel('World Price', color='#245678')

	ax2=ax1.twinx()
	ax2.plot_date(new_x,y1, '-',color='#00398f')  #?????????
	ax2.set_ylabel('Gold Price', color='#00398f')
	xfmt=dates.DateFormatter('%Y')
	ax1.xaxis.set_major_locator(years)
	ax1.xaxis.set_major_formatter(xfmt)

	plt.grid(True)
	fig.autofmt_xdate()
	plt.show()

#plot()

