import sqlite3 as sq
from os import getenv

token = getenv("BOT_TOKEN")
text_info = f"""Возможности бота:
    1. Конвертация валют с сайта МосБиржи, либо Yahoo, если сервер не ответит.
Пример: пишем в следующем виде без кавычек '$', '10$', '322.58$' и т.д. получим курс $ помноженный на значение.
Отправляем 10$ Получаем 607.52 руб. 
Аналогично работает и с "€", и  с "¥"(китайский юань), данные предоставляются МосБиржей и Yahoo.
    2. Получение котировок акций с МосБиржи и американских бирж (NYSE, Nasdaq и т.д.) в формате:
Цена акции, капитализация в млрд., изменение за день с открытия торгов в %, поставщик услуг
Пример: отправляем AAPL или SBER (или !AAPL, !SBER) - получаем сообщение с показателями и наименованием информатора.
Для иностранных акций доступен график за год + сравнение с индексом S&P 500/
Для всех акций доступно получение более широкого списка показателей P/E, P/B, Sector и т.д. от Yahoo
P.S. Для групповых чатов запрос доступен ТОЛЬКО через "!" (!GAZP), при этом дополнительные опции отключены.
    3. Получение информации по индексу МосБиржи "IMOEX", и по индексу S&P 500 через запрос 'snp' или 's&p' (или ^GSPC).
Для индексов доступны те же режимы, что и для акций. 
Дополнительно для индекса МосБиржи есть такие опции:
* Получение списка топ 10 акций в составе индекса с доп. информацией: долей в индексе и т.д.
* Получение остального списка (№10 и до окончания) с доп. информацией.
* Круговая диаграмма списка топ 10 для наглядного представления распределения активов.
* Гистограмма остального  списка.
P.S. запрос через Yahoo может составлять 5-6 секунд, это нормально.
Вопросы, предложения: @leshen_also
Поставщики информации:
MOEX:   https://www.moex.com/
Yahoo:  https://finance.yahoo.com/
Eninvs: https://eninvs.com/
Внимание! с августа 2022 Yahoo отключил поставку данных для российских инструментов, связи с чем могут быть ненадежные 
данные по расширенным показателям акций/ индексов из России.
"""

# ~~~ Получение данных ~~~
file = 'C:/My projects/TgBot_v4/sql_mar_cap/stock_bd.db'
with sq.connect(file) as test:
    cur = test.cursor()
    moex = [list(_) for _ in cur.execute("SELECT tick, sector, name, moex_share "
                                         "FROM stock_bd "
                                         "WHERE moex_check == 'MOEX' "
                                         "ORDER BY moex_share DESC").fetchall()]
    # leshen = [list(_) for _ in cur.execute("SELECT tick, sector, name, leshen_share "
    #                                        "FROM stock_bd2 "
    #                                        "WHERE leshen_check == 'LESHEN' "
    #                                        "ORDER BY leshen_share DESC").fetchall()]
    # stock = [x[0] for x in [list(_) for _ in cur.execute("SELECT tick "
    #                                                      "FROM stock_bd2 "
    #                                                      "ORDER BY capital DESC").fetchall()][:12]] +
    #                                                      ['Index MOEX', 'Index Leshen']


def new_list(arg):
    dop_info = ['Ticker  Sector      Name            Share,%']
    for y in arg:
        y[0] = y[0].ljust(8, ' ')
        y[1] = y[1].ljust(12, ' ')
        y[2] = y[2].ljust(16, ' ')
        y[3] = str(y[3]).ljust(5, ' ')

    top_10 = '\n'.join(dop_info + [''.join(y) for y in arg[:10]])
    top_any = '\n'.join(dop_info + [''.join(y) for y in arg[10:]])
    return top_10, top_any


list_index = new_list(moex)
