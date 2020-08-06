import requests
from pymongo import MongoClient



def sort(url):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'
          }
    r = requests.get(url, headers=headers)

    #print(r.text)
    with open('URL.txt', mode="w", encoding='utf8') as output_file:
      output_file.write(r.text)

    f = open('URL.txt', encoding='utf8')
    a = 'lowPrice'
    for line in f:
      if a in line:
        ab = line
        #print(line)
    sp = list()
    j = 0
    for i in ab:
      if j > 17 and i != '"':
        sp.append(i)
      elif j>17 and i =='"':
        break
      j+=1
    cc = ""
    print(cc.join(sp))
    price = open('price.txt', 'w')
    global output_price
    output_price = cc.join(sp)
    price.write(cc.join(sp))
    price.close()
    f.close()
    return cc.join(sp)