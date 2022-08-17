import matplotlib.pyplot as plt
import yfinance
import pandas as pd


# price = [100, 150, 200, 250, 200, 150, 250]
# date = [1, 2, 3, 4, 5, 6, 7]
# price2 = [3000, 3400, 3800, 4200, 3200, 2800, 3900]

data = yfinance .download('AAPL', period='1y', interval='1wk')['Adj Close']
df = pd.DataFrame(data)
price = df.values.tolist()
index = df.index.tolist()

data_snp_500 = yfinance .download('^GSPC', period='1y', interval='1wk')['Adj Close']
df = pd.DataFrame(data_snp_500)
price_snp_500 = df.values.tolist()

price_snp_500_clean = []
for x in price_snp_500:
    for q in x:
        price_snp_500_clean.append(str(q))

price_clean = []
for x in price:
    for q in x:
        price_clean.append(str(q))

index_clean = []
for x in index:
    index_clean.append(str(x).strip('Timestamp(').split()[0])

for x in price_clean:
    if price_clean.count('nan') > 0:
        check2 = price_clean.index('nan')
        price_clean.pop(check2)
        index_clean.pop(check2)

price_clean = [float(x) for x in price_clean]
price_snp_500_clean = [float(x) for x in price_snp_500_clean]




date = index_clean
price = price_clean
price2 = price_snp_500_clean



fig, ax = plt.subplots(figsize=(15, 7))
chart = plt.plot(date, price, color='#bf3f27', marker='o', linestyle='solid', linewidth=2, markersize=6)
ax2 = ax.twinx()
ax2.plot(date, price2, color='#5d9497', marker='_', linestyle='dashed', linewidth=1, markersize=6)


ax.set_xlabel("Date", color='#a8bed6', fontsize=12)
ax.tick_params(axis='x', rotation=90, colors='#a8bed6', labelsize=12)
ax.set_ylabel('APPLE', color='#bf3f27', fontsize=12)
ax.tick_params(axis='y', rotation=0, color='#bf3f27', labelcolor='#bf3f27')
ax.grid(alpha=.1)
ax.spines['top'].set_color('#182633')

ax2.set_ylabel("S&P 500", color='#5d9497', fontsize=12)
ax2.tick_params(axis='y', color='#5d9497', labelcolor='#5d9497')
# ax2.set_xticks(np.arange(0, len(x), 60))
# ax2.set_xticklabels(x[::60], rotation=90, fontdict={'fontsize':10})
fig.set_facecolor('#182633')
ax.patch.set_facecolor('#182633')

ax2.spines['top'].set_color('#182633')
ax2.spines['left'].set_color('#bf3f27')
ax2.spines['right'].set_color('#5d9497')
ax2.spines['bottom'].set_color('#a8bed6')
plt.savefig("stock_vs_snp.png", bbox_inches='tight')
plt.show()