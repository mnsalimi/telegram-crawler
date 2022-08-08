from locale import normalize
import pickle
from tkinter import Y
from unittest import result
import requests
from bs4 import BeautifulSoup
from hazm import Normalizer
normalizer = Normalizer() 

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
        
if __name__ == "__main__":
    # crawl_symbol()
    # with open("people.csv", "r", encoding="utf-8") as f:
    #     xx = f.readlines()
    #     results = {}
    #     for line in xx:
    #         result = {}
    #         line = [column.rstrip().lstrip().strip() for column in line.split(",")]
    #         result['symbol_code'] = line[0]
    #         result['group'] = line[1]
    #         result['industry_group'] = normalizer.normalize(line[2])
    #         result['tablo'] = normalizer.normalize(line[3])
    #         result['english_symbol'] = line[4]
    #         result['english_symbol_name'] = line[5]
    #         result['persian_symbol'] = normalizer.normalize(line[6])
    #         result['persian_symbol_name'] = normalizer.normalize(line[7])
    #         result['is_certain'] = line[8]
    #         # print(result)
    #         results[result['persian_symbol']] = {
    #             "symbol_code": result['symbol_code'],
    #             "group": result['group'],
    #             "industry_group": result['industry_group'],
    #             "tablo": result['tablo'],
    #             "english_symbol": result['english_symbol'],
    #             "english_symbol_name": result['english_symbol_name'],
    #             "persian_symbol_name": result['persian_symbol_name'],
    #             "is_certain": result['is_certain'],
    #         }
    # with open('data/symbols_new.pickle', 'wb') as output_file:
    #     pickle.dump(results, output_file)
    # crawl_symbol()
    with open('data/symbols.pickle', 'rb') as output_file:
        xs = pickle.load(output_file)
        print(xs)
    #     with open("csv.csv", "w", encoding="utf-8") as f:
    #         for x, y in xs.items():
    #             f.write(
    #                 x + "," + y["group"] + "," + y["industry_group"] + "," + y["tablo"] + "," +\
    #                     y["english_symbol"] + "," + y["english_symbol_name"] + "," +
    #                     y["persian_symbol"] + "," + y["persian_symbol_name"] + "\n"
    #             )
    # xx = list(xs.keys())
    # for x in xx:
    #     if len(x.split())>1:
    #         print(x)
    # res = {}
    # for x, y in xs.items():
    #     res[normalizer.normalize(x)] = {
    #         "symbol_code": normalizer.normalize(y["symbol_code"]),
    #         "group": normalizer.normalize(y["group"]),
    #         "industry_group": normalizer.normalize(y["industry_group"]),
    #         "tablo": normalizer.normalize(y["tablo"]),
    #         "english_symbol": normalizer.normalize(y["english_symbol"]),
    #         "english_symbol_name": normalizer.normalize(y["english_symbol_name"]),
    #         "persian_symbol": normalizer.normalize(y["persian_symbol"]),
    #         "persian_symbol_name": normalizer.normalize(y["persian_symbol_name"]),
    #         "is_certain": normalizer.normalize(y["is_certain"]),
    #     }
    # with open('data/people_new.pickle', 'wb') as output_file:
    #     pickle.dump(res, output_file)