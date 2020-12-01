
import requests
from bs4 import BeautifulSoup
import pandas as pd

#No API credential needed

#First dataset comes from scraping Farfetch.com, which is a luxury apparel online shoppin website.
product_lis=list()
#I set the header for scrapping, and I am only aiming for women apparel that are newly arived
Farfetch_url = 'https://www.farfetch.com/sets/women/new-in-this-week-eu-women.aspx?'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0'}
#The scraper would start from page 1 to 7
def scrape_farfetch():
    product_lis = list()
    Farfetch_url = 'https://www.farfetch.com/sets/women/new-in-this-week-eu-women.aspx?'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0'}
    page=1
    while True:
        try:
            param = {'page': page}
            farfetch = requests.get(Farfetch_url, params=param, headers =headers)
            farfetch.raise_for_status()
    # If we request a page that doesn't exist, we'll raise this exception, and break out of the loop
        except requests.exceptions.HTTPError as e:
            print(e)
            break
        if page>7:
            break
        else:
        # If we're successful, print out some information, and add this page's results to our list
            #print(f'{farfetch.url} was successfully retrieved with status code {farfetch.status_code}')
            farfetch_result=BeautifulSoup(farfetch.content,features='html.parser')
            products=farfetch_result.find_all('li',{'data-test':'productCard'})
        #Parsing the response using beautiful soup, and find the corresponding product information
            for product in products:
                product_info = product.find_all('div')
                product_image = product.find_all('meta')[0]['content']
                Description = product_info[1].p.text
                Brand = product_info[1].h3.text
                Currency = product_info[1].meta['content']
                Price = product_info[1].find_all('meta')[1]['content']
                product_lis.append((Description,Brand,product_image,Currency,Price))
            page = page + 1
    # create a panda dataframe to store the information of products, and convert it to a csv file
    df = pd.DataFrame(product_lis,columns=['description','brand','img','currency','price'])
    df.to_csv("data/farfetch_product.csv", index=False, sep=',')
    return df
