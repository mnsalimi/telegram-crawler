import pickle
from unittest import registerResult, result
import requests
from bs4 import BeautifulSoup
from hazm import Normalizer
normalizer = Normalizer() 

CSV_COLUMNS = [
    "symbol_code",
    "group",
    "industry_group",
    "tablo",
    "english_symbol",
    "english_symbol_name",
    "persian_symbol",
    "persian_symbol_name",
    "is_certain",
    "is_certain_with_rules",
]

def crawl_symbol():
    URL = "http://www.tsetmc.com/Loader.aspx?ParTree=111C1417"
    resp = requests.get(URL)
    soup = BeautifulSoup(resp.text, "lxml")
    results = []
    trs = soup.select('tr')[1:]
    for tr in trs:
        tds = tr.select('td')
        result = {}
        result['symbol_code'] = tds[0].text
        result['group'] = tds[1].text
        result['industry_group'] = tds[2].text
        result['tablo'] = tds[3].text
        result['english_symbol'] = tds[4].text
        result['english_symbol_name'] = tds[5].text
        result['persian_symbol'] = tds[6].text
        result['persian_symbol_name'] = tds[7].text
        results.append(result)
    with open("symbols.pickle", "wb") as f:
        pickle.dump(results, f)
    import csv
    keys = results[0].keys()
    with open('people.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)

def crawl_symbols_from_nabzebourse():
    URL = "https://nabzebourse.com/fa/news/29381/stock-symbols-news"
    resp = requests.get(URL)
    soup = BeautifulSoup(resp.text, "lxml")
    symbols = []
    tds = soup.select('td')[1:]
    for td in tds:
        atags = td.select('a')
        for atag in atags:
            symbols.append(normalizer.normalize(atag.text))
    return symbols

def add_symbols_to_pickle_and_csv(new_symbols):
    with open("data/symbols/symbols.pickle", "rb") as f:
        pickle_symbols = pickle.load(f)
    for symbol in new_symbols:
        if symbol not in pickle_symbols:
            pickle_symbols[symbol] = {}
    with open("data/symbols/symbols.pickle", "wb") as f:
        pickle.dump(pickle_symbols, f)
    with open("data/symbols/symbols.csv", "w") as f:
        for col in CSV_COLUMNS:
            f.write(col+",")
        f.write("\n")
        for x, y in list(pickle_symbols.items())[1:]:
            try:
                f.write(y['symbol_code']+",")
                f.write(y['group']+",")
                f.write(y['industry_group']+",")
                f.write(y['tablo']+",")
                f.write(y['english_symbol']+",")
                f.write(y['english_symbol_name']+",")
                f.write(x+",")
                f.write(y['persian_symbol_name']+",")
                f.write(y['is_certain']+",")
                f.write("\n")
            except:
                f.write(","*6+x+",\n")

def create_pickle_by_csv():
    with open("data/symbols/symbols.csv", "r") as f:
        lines = [
            line.replace("\n", "").split(",")
            for line in f.readlines()[1:]
        ]
        results = {}
        for line in lines:
            results[line[6]] = {
                "symbol_code": line[0],
                "group": line[1],
                "industry_group": line[2],
                "tablo": line[3],
                "english_symbol": line[4],
                "english_symbol_name": line[5],
                "persian_symbol_name": line[7],
                "is_certain": line[8],
                "is_certain_with_rules": line[9],
            }
        print(len(results))
        with open("data/symbols/symbols.pickle", "wb") as f:
            pickle.dump(results, f)

if __name__ == "__main__":
    # new_symbols = crawl_symbols_from_nabzebourse()
    # add_symbols_to_pickle_and_csv(new_symbols)
    create_pickle_by_csv()