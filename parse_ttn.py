import requests
from sort_url import sort
import pymongo

client = pymongo.MongoClient("mongodb+srv://atlasAdmin:123@cluster0.l91mz.mongodb.net/user?retryWrites=true&w=majority")
db = client.price_catalog



def num_catalog(url, obj, num_page, name):
    global collection
    collection = db[name]
    full_price = open('full_price.txt', 'w')
    full_price.close()
    i = 0
    while i <= num_page:
        sort_catalog(url, obj, i, name)
        i += 1

def sort_catalog(url, obj, num_page, name):
    url = url + '?page=' + str(num_page)
    text_file = open('list_url.txt', mode="w")
    text_file.close()

    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'
          }
    r = requests.get(url, headers=headers)

    #print(r.text)
    with open('URL.txt', mode="w", encoding='utf8') as output_file:
      output_file.write(r.text)

    f = open('URL.txt', encoding='utf8')
    for line in f:
        if obj in line:
            if '<a class="woocommerce-LoopProduct-link woocommerce-loop-product__link woocommerce-loop-product__title title__a' in line:
                #print(line)
                text_file = open('list_url.txt', mode="a", encoding='utf8')
                text_file.write(line)
                text_file.close()
    f.close()

    open_txt = open('list_url.txt', mode="r", encoding='utf8')
    for line in open_txt:
        if line != '':
            sp = list()
            j = 0
            #print(line)
            for i in line:
                if j > 118 and i != '"':
                    sp.append(i)
                elif j > 118 and i == '"':
                    break
                j += 1
            if sp[0] == '/':
                sp.remove('/')
            cc = ""
            cod_url = cc.join(sp)
            full_code = 'https://www.ttn.by/' + cod_url
            #full_price = open('full_price.txt', mode="a", encoding='utf8')
            #full_price.write(full_code + ' ' + sort(full_code))
            #full_price.close()
            #sp_url.append(full_code)
            #sp_price.append(sort(full_code))
            collection.insert_one({'url': full_code, 'price': sort(full_code)})
            #print(full_code)
            #sort(full_code)
    open_txt.close()


