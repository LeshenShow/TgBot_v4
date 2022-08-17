import yfinance
import sqlite3 as sq
import requests
from bs4 import BeautifulSoup
import re

# ~~~Создание таблицы stock_bd.db~~~
with sq.connect('stock_bd.db') as con:
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS stock_bd (
        ticker_id INTEGER PRIMARY KEY AUTOINCREMENT,
        tick TEXT UNIQUE,
        sector TEXT,
        name TEXT,
        moex_check TEXT,
        leshen_check TEXT,
        moex_k TEXT,
        leshen_k TEXT,
        capital INTEGER,
        moex_capital INTEGER,
        leshen_capital INTEGER,
        moex_share FLOAT,
        leshen_share FLOAT
        )""")

# # ~~~Обработка данных с эксель в stock_bd.db~~~
with open("for_bd.csv", "r", encoding="utf-8") as file:
    file = file.readlines()
file_result = []

for x, y in enumerate(file):
    file_result.append(y.split(','))
    file_result[x] = file_result[x]+[3, 2, 4, 6.0, 5.0]

# ~~~Запись данных в stock_bd.db~~~
with sq.connect('stock_bd.db') as con:
    cur = con.cursor()
    for x in file_result:
        x = tuple(x)
        try:
            cur.execute('INSERT INTO stock_bd VALUES(NULL, ?, ?, ?, ?, ? ,?, ?, ?, ?, ?, ?, ?)', x)
        except:
            cur.execute('REPLACE INTO stock_bd VALUES(NULL, ?, ?, ?, ?, ? ,?, ?, ?, ?, ?, ?, ?)', x)

# ~~~Сбор данных о капитализации~~~
capital_stock = []
for _, info in enumerate(file_result):
    result = []
    flag = False
    try:
        url = f'http://iss.moex.com/iss/engines/stock/markets/shares/securities/{info[0]}.xml'
        pages = requests.get(url, timeout=(5, 5))
        soup = BeautifulSoup(pages.text, 'xml')
        info_moex = soup.find_all('row')
        for x in info_moex:
            if x.get('ISSUECAPITALIZATION') not in (None, ''):
                cap = int(float(x.get('ISSUECAPITALIZATION')))
                flag = True
                print('moex', info[0], cap)
                break
        if not flag:
            url = f'https://eninvs.com/company.php?name={info[0]}'
            pages = requests.get(url, timeout=(5, 5))
            soup = BeautifulSoup(pages.text, 'lxml')
            info_eninvs = soup.find('div', id='main_fin_data').text
            info_eninvs = re.split("\n|:|: |;|,", info_eninvs)
            for _ in info_eninvs:
                if _ not in ('', ' '):
                    result.append(_.strip(' '))
            result = {_: __ for _, __ in enumerate(result)}
            qty = result.get(22).split(' ')
            price = float(result.get(19))
            cap = int((int(''.join(qty)) * price))
            print('parser', info[0], cap)
    except:
        info_yahoo = yfinance.Ticker(info[0] + ".ME").info
        cap = info_yahoo.get('marketCap')
        print('yahoo', info[0], cap)
    capital_stock.append([info[0], cap])
    # print(capital_stock)
    # print(cap, info[0])

# ~~~ CAPITAL LIST FOR TESTING ~~~

# capital_stock = [['ABRD', 16954031832], ['AFKS', 144750000000], ['AFLT', 66295801349], ['AKRN', 746717348000],
#                  ['ALRS', 475408531416], ['AQUA', 42005038222], ['BELU', 36355800000], ['BSPB', 33174663224],
#                  ['CBOM', 167349127589], ['CHMF', 709380161288], ['DSKY', 52025600000], ['ENRU', 15910279886],
#                  ['FESH', 93613650000], ['FIVE', 267227706048], ['FIXP', 251685000000], ['GAZP', 4409191777625],
#                  ['GCHE', 111086192502], ['GLTR', 55933394843], ['GMKN', 2615816318976], ['GTRK', 1321243912],
#                  ['HHRU', 47213460000], ['HYDR', 351343266898], ['INGR', 50825237769], ['IRAO', 361224000000],
#                  ['KAZT', 92863096403], ['KMAZ', 64994396472], ['LENT', 65772918168], ['LKOH', 2736473327019],
#                  ['MAGN', 349868272300], ['MGNT', 427823868290], ['MOEX', 193539651959], ['MTSS', 560645950866],
#                  ['MVID', 34120009484], ['NFAZ', 1993646208], ['NKHP', 21124062500], ['NKNC', 124066712000],
#                  ['NLMK', 812082291020], ['NMTP', 103040012390], ['NVTK', 3112213650000], ['OZON', 153040453056],
#                  ['PHOR', 996114000000], ['PIKK', 490089029248], ['PLZL', 1088215026500], ['POGR', 12272130378],
#                  ['POLY', 168184677468], ['POSI', 52104000000], ['RENI', 24478074681], ['ROLO', 19935664500],
#                  ['ROSN', 3938282876797], ['RTKM', 216677863314], ['RUAL', 824145091189], ['RUGR', 821252304],
#                  ['SBER', 2837172575640], ['SELG', 39217858929], ['SGZH', 126163290000], ['SIBN', 1900549960293],
#                  ['SMLT', 168696651241], ['SNGS', 910476975056], ['TATN', 943373073100], ['TCSG', 383962030338],
#                  ['TRNFP', 188606337500], ['VKCO', 65870221495], ['VTBR', 240418041807], ['YNDX', 537508795140]]

# # ~~~Запись капитализации, долей~~~
with sq.connect('stock_bd.db') as con:
    cur = con.cursor()
    for _, y in enumerate(capital_stock):
        cur.execute(f"UPDATE stock_bd "
                    f"SET capital ={y[1]} "
                    f"where tick ='{y[0]}'")  # {y[1]}
        cur.execute(f"UPDATE stock_bd "
                    f"SET moex_capital = capital * moex_k, "
                    f"leshen_capital = capital * leshen_k "
                    f"where tick ='{y[0]}'")
    cur.execute(f"UPDATE stock_bd "
                f"SET leshen_capital= max"
                f"((SELECT sum(capital)*0.0005 "
                f"from stock_bd "
                f"where leshen_check= 'LESHEN'), "
                f"(select capital * leshen_k)) "
                f"where leshen_check= 'LESHEN'")
    sum_cap_leshen = cur.execute("SELECT sum(leshen_capital) "
                                 "FROM stock_bd").fetchone()[0]
    sum_cap = cur.execute("SELECT sum(moex_capital) "
                          "FROM stock_bd").fetchone()[0]
    for _, y in enumerate(capital_stock):
        cap_from_id = cur.execute(f"SELECT moex_capital "
                                  f"FROM stock_bd "
                                  f"where tick='{y[0]}'").fetchone()[0]
        share = float("{0:.2f}".format(cap_from_id / sum_cap * 100))
        cur.execute(f"UPDATE stock_bd "
                    f"SET moex_share = {share} "
                    f"where tick ='{y[0]}'")
        cap_from_id = cur.execute(f"SELECT leshen_capital "
                                  f"FROM stock_bd "
                                  f"where tick='{y[0]}'").fetchone()[0]
        share = float("{0:.2f}".format(cap_from_id / sum_cap_leshen * 100))
        cur.execute(f"UPDATE stock_bd "
                    f"SET leshen_share = {share} "
                    f"where tick='{y[0]}'")


# ~~~Добавление столбца в таблицу ~~~
# with sq.connect('stock_bd.db') as con:
#     cur = con.cursor()
#     cur.execute("""ALTER TABLE stock_all ADD COLUMN test TEXT""")

# ~~~ Получение данных ~~~
# with sq.connect('stock_bd.db') as test:
#     cur = test.cursor()
#     cur.execute("SELECT leshen_check FROM stock_all WHERE tick == 'GAZP'")
#     result = cur.fetchall()
#     print(result)
#     cur.execute("SELECT sum(moex_capital) FROM stock_bd")
#     result = cur.fetchone()
#     print(result)
