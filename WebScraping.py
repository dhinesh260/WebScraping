import requests
from bs4 import BeautifulSoup
import psycopg2
import re


con = psycopg2.connect(database='webscraping', user='postgres', password='root', host='localhost', port='5432')
cur = con.cursor()

filename = 'IphonesList.csv'
fh = open(filename, 'w', encoding='utf-8')
print('Model, Rating, Price', file=fh)

cur.execute('''
      CREATE TABLE iphones (model VARCHAR(100), rating real, price money);
''')

url = 'https://www.flipkart.com/search?q=iphone&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as' \
      '=off&as-pos=0&as-type=HISTORY '

r = requests.get(url)

html = r.text

soup = BeautifulSoup(html, 'lxml')

# prettify_soup = soup.prettify()
# print(prettify_soup)

for col in soup.findAll('div', attrs={'class': '_1-2Iqu row'}):
    name = col.find('div', attrs={'class': '_3wU53n'}).text
    rating = col.find('div', attrs={'class': 'hGSR34'}).text
    price = col.find('div', attrs={'class': '_1vC4OE _2rQ-NK'}).text
    print(name + ',' + rating + ',' + price)

    formatted_name = re.sub(',', '', name)
    formatted_price = re.sub(',', '', price[1:])
    print(formatted_name.strip() + ',' + rating.strip() + ',' + formatted_price.strip(), file=fh)

    insert_query = "INSERT INTO iphones (model, rating, price) VALUES ('{}', {}, '{}');".format(name, rating,
                                                                                                price[1:])
    cur.execute(insert_query)
    con.commit()


fh.close()
con.close()


# for spec in col.findAll('li', attrs={'class': 'tVe95H'}):
#      print(spec.text)





