import requests
from bs4 import BeautifulSoup
import csv


def get_page(url):
    response = requests.get(url)
    if not response.ok:
       print('server response ', response.status_code)
    else:
        soup = BeautifulSoup(response.text, 'lxml')
    return soup 

def get_details(soup):
    try:
        title = soup.find('span', id="vi-lkhdr-itmTitl").text.strip()
    except:
        title = ''
    
    try:
        currency, price = soup.find('span', id='prcIsum').text.strip().split(' ')
    except:
        price = ''
        currency = ''

    try:
        shipping = soup.find('span', id="fshippingCost").text.strip()  
 
    except:
        shipping = ''
    
    data = {'title': title,'currency': currency,'price': price,'shipping': shipping}
    return data                       

def index(soup):
    try:
        links = soup.find_all('a', class_="s-item__link")
    except:
        links = []

    urls= [item.get('href') for item in links] 
    return urls   

def to_csv(data, url):
    with open('output.csv', 'a') as file:
        try:
            writer = csv.writer(file)
            row = [data['title'], data['currency'], data['price'], data['shipping'], url]
            writer.writerow(row)
        except:
            pass    
def all_pages(n):
    for i in range(1, n+1):
        url = 'https://www.ebay.com/b/Laptops-Netbooks/175672/bn_1648276?_pgn={}'.format(i)
        products = index(get_page(url))
        for url in products:
            try:
                row = get_details(get_page(url))
            except:
                row = {'title': '','currency': '','price': '','shipping': ''}  
            to_csv(row, url)             


def main():
    # url = 'https://www.ebay.com/b/Laptops-Netbooks/175672/bn_1648276?_pgn=1'
    # products = index(get_page(url))
    # for url in products:
    #     try:
    #         row = get_details(get_page(url))
    #     except:
    #         row = {'title': '','currency': '','price': '','shipping': ''}  
    #     to_csv(row, url)  
    all_pages(2)           



if __name__ == '__main__':
    main()