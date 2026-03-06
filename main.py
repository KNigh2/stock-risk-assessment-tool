import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from yfinance import Ticker

#Get stock data
tkr=yf.Ticker("AAPL")
hist=tkr.history(period="150d")
#Clean data
hist=hist.drop("Dividends", axis=1)
hist=hist.drop("Stock Splits", axis=1)
v=hist.index

#Log Calculation
log_hl=np.log(hist["High"]/hist["Low"])
log_cl=np.log(hist["Close"]/hist["Open"])
#Calculate Garman-Klass Volatility
grks_sigm=0.5*log_hl**2-(2*np.log(2)-1)*log_cl**2
sigm_f=grks_sigm.rolling(window=10).mean()*100


mean_vol=sigm_f.mean()
anomaly_th=mean_vol*1.5
anom=sigm_f[sigm_f>anomaly_th]

#Panel Open/Close

fig,(ax1,ax2,ax3) = plt.subplots(3,1, figsize=(12, 6), sharex=True)
ax1.plot(v,hist["Close"], label="Close",color="blue",alpha=0.5)
ax1.plot(v,hist["Open"],label="Open", color="red",alpha=0.5)
ax1.legend()
ax1.title.set_text("Garman-Klass Volatility")
ax1.grid(True)

#Panel High/Low

ax2.plot(v,hist["High"], label="High",color="green",alpha=0.5)
ax2.plot(v,hist["Low"], label="Low",color="red",alpha=0.5)
ax2.grid(True)
ax2.legend()

#Panel Garman Klass

ax3.fill_between(v, sigm_f, color='blue', alpha=0.3, label="Garman-Klass")
ax3.axhline(anomaly_th, color='red', alpha=0.5, label="Anomaly")
ax3.axhline(mean_vol, color='green', alpha=0.5, label="peak risk")
ax3.scatter(anom.index, anom, color="red", label="anomality risk", s=15, alpha=0.5)
ax3.legend()
ax3.grid(True, linestyle='--', linewidth=0.5, color='black', alpha=0.3)
ax3.set_xlabel("%")
plt.show()

