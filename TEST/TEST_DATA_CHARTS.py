import yfinance
import pandas as pd
import datetime
# qwe = yfinance.Ticker('AAPL').history(period='1y', interval='1wk')["Date"]
# print(qwe)
# data = yfinance .download('AAPL', '2016-01-01','2019-08-01')['Adj Close']






data = yfinance .download('^GSPC', period='1y', interval='1wk')['Adj Close']
df = pd.DataFrame(data)
price = df.values.tolist()
index = df.index.tolist()

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
print(price_clean)
print(len(price_clean))
# check = qwe.index('nan')
# print(check)
# qwe.pop(check)
# ind.pop(check)
#
# check = qwe.index('nan')
# print(check)
# qwe.pop(check)
# ind.pop(check)
#
# check = qwe.index('nan')
# print(check)
# qwe.pop(check)
# ind.pop(check)
#
# check = qwe.index('nan')
# print(check)
# qwe.pop(check)
# ind.pop(check)
#
# print(ind)
# print(qwe)
# print(len(qwe) == len(ind))