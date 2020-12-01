
import requests
from bs4 import BeautifulSoup
import pandas as pd


#create a scrape_hm function that scrapes the newly-arrived H&M women apparels
hm_lis = []
def scrape_hm():
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0'}
    hm_url = 'https://www2.hm.com/en_us/women/new-arrivals/view-all.html?sort=stock&image-size=small&image=stillLife&offset=0'
    size = 36
    #try the first param to get the total number of products we need to scrape, and change the size later
    param = {'page-size': size}
    hm_test = requests.get(hm_url, headers=headers, params=param)
    soup = BeautifulSoup(hm_test.content, features='html.parser')
    new_size = {'page-size': int(soup.find_all('div', {'class': 'filter-pagination'})[0].text[3:8])}
    hm = requests.get(hm_url, headers=headers, params=new_size)
    soup = BeautifulSoup(hm.content, features='html.parser')
    products = soup.find_all('li', {'class': 'product-item'})
    # print(products[0])
    #iterate through all the products, and record each info, append them in the list
    for product in products:
        price = product.find('article').find('span', 'price regular').text
        description = product.find('img')['alt']
        articlecode = product.find('article')['data-articlecode']
        category = product.find('article')['data-category']
        if product.find('article').find('a', 'swatch')!=None:
            color = product.find('article').find('a', 'swatch')['title']
        brand = 'H&M'
        hm_lis.append((description, price, articlecode, category, color, brand))
        #convert the list into a panda dataframe, and store the dataframe as a csv on the disk as well
    df = pd.DataFrame(hm_lis, columns=['description', 'price', 'articlecode', 'category', 'color', 'brand'])
    df.to_csv('data/H&M_product.csv', index=False, sep=',')
    return df