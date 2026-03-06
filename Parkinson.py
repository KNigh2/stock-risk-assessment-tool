import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
#Get stock data
tkr=yf.Ticker('TSLA')
hist=tkr.history(period='150d')
hist=hist.drop("Dividends",axis=1)
hist=hist.drop("Stock Splits",axis=1)
#Output history of Ticker for 150 days
print(hist.head())
v=hist.index

mid_price = (hist['High'] + hist['Low']) / 2

#Calculate Parkinson volatility with 10-day smoothing
sigm = ((hist['High'] - hist['Low']) / (4 * np.log(2))).rolling(window=10).mean()

current_sigm = sigm.iloc[-1]
mean_sigm = sigm.mean()
dev_rat=current_sigm/mean_sigm
risk_c="black"

#Identify risk levels based on deviation ratio
if dev_rat>1.8:
    risk="Critical Risk"
    risk_c = "red"
elif dev_rat<0.7:
    risk="Calm"
    risk_c = "orange"
else:
    risk="Normal"
    risk_c = "green"
#Output values
print('=='*30)
print(f"Analyse risk for : {tkr.ticker}")
print(f"Hist Norm : {mean_sigm}")
print(f"Sigma now  : {current_sigm}")
print(f"verdict:{risk}")
print('=='*30)
#Plotting the results
plt.plot(v, mid_price, color='black', label='Mid Price', alpha=0.5)
plt.fill_between(v, mid_price + sigm, mid_price - sigm, color='blue', alpha=0.3, label='Dispersion Zone')
plt.plot(v,hist['High'], color='green', alpha=0.5)
plt.plot(v,hist['Open'], linestyle='none', marker='o', markerfacecolor='black', markersize=3)
plt.plot(v,hist['Low'], color='crimson', alpha=0.5)
#Legend for clear data visualization
plt.legend(['Close','Parkinson','High','Open','Low'])
plt.title(f" Анализ {tkr.ticker}  ",color=risk_c,fontsize=13)
plt.suptitle("Green=Normal, Red=Risk, Orange=Calm", color = 'black')
plt.grid(True,linestyle='--',alpha=0.8)
plt.show()
