import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook



def graph():
	path = r'../scraped/gold.csv'
	price = np.genfromtxt(path, delimiter=',', unpack=True)


	plt.figure("Gold return")
	plt.xlabel("")
	plt.ylabel("Price(USD)")
	plt.plot(price)
	plt.show()

graph()