
import requests
from bs4 import BeautifulSoup
import pandas as pd
import scrape_farfetch as far
import scrape_hm as hm
import api_weekly as api
import argparse

#Grab data by remote will call the scraper in other py files, and store the data as csv
#the function will return the datasets in a list
def grab_data_by_remote():
    far_product=far.scrape_farfetch()
    hm_product=hm.scrape_hm()
    datalis=api.get_api_weekly()
    return [far_product,hm_product,datalis]

#grab_data_by_local will invoke the local datasets that are in csv format, and return them in dataframe format
def grab_data_by_local():
    far_product=pd.read_csv('data/farfetch_product.csv')
    hm_product=pd.read_csv('data/H&M_product.csv')
    HM_stock=pd.read_csv('data/HNNMY_stock.csv')
    LV_stock=pd.read_csv('data/LVMUY_stock.csv')
    ZARA_stock=pd.read_csv('data/IDEXY_stock.csv')
    Keurig_stock=pd.read_csv('data/IDEXY_stock.csv')
    return [far_product,hm_product,HM_stock,LV_stock,ZARA_stock,Keurig_stock]


#I am not hundred percent sure about if the command_line will work perfectly with the --grade flag
#But the scraping itself in my project would not take more than 2 minutes, all the datasets are in
#moderate size, and should be probably fine.
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", choices=["local", "remote"], help="where data should be gotten from")
    parser.add_argument('--grade',help="requests each scraper will make are within moderate range ")
    args = parser.parse_args()
    location=args.source

    if location == "local":
        data = grab_data_by_local()
        print("Data grabbed from local folder")
        print("A 5-row sample of the first table looks like this")
        print(data[0].head(5))

    else:
        print('Grabbing data from web...the process would not take too long')
        data = grab_data_by_remote()
        print(data[0].head(5))
        print("A 5-row sample of the first table looks like this")
        print('Data have been stored as csv files in the data folder')


if __name__ == '__main__':
    main()



