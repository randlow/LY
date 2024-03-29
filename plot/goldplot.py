import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import matplotlib.animation as anim
from matplotlib import dates

fig = plt.figure("Gold return")

def graph(i):
	path = r'../scraped/gold.csv'
	data = np.genfromtxt(path, delimiter=",", names=True)
	price=data['closeprice']
	epoch=data['epochtime']

	#convert timestamp to date
	temp=[]
	for e in epoch:
		s=e/1000
		temp.append(datetime.datetime.fromtimestamp(s))

	#plt.ion()
	
	ax=fig.add_subplot(111)
	ax.clear()

	#line, = ax.plot_date(temp, price, '.:', color='#245678')
	ax.plot_date(temp, price, '.:', color='#245678')
	xfmt=dates.DateFormatter('%d/%m/%Y')
	ax.xaxis.set_major_formatter(xfmt)

	#ax.xaxis.set_major_locator(dates.MonthLocator())
	
	plt.xlabel("Month")
	plt.ylabel("Price(USD)")

	plt.grid(True)

	fig.autofmt_xdate()

ani = anim.FuncAnimation(fig, graph, interval=1000)
plt.show()

