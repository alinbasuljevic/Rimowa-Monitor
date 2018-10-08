import requests, time
from bs4 import BeautifulSoup as bs

s = requests.Session()
url = input('Enter Product URL: ')
webhook = input('Enter Discord Webhook for Notifications: ')

def Monitor_Function(s, url, webhook):

    headers = {
        'dnt': '1',
        'origin': 'https://www.rimowa.com',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    
    Monitor_Trigger = True
    while Monitor_Trigger:
        product_page = s.get(url, headers=headers)
        soup = bs(product_page.text, 'lxml')
        OOS_Indicator = soup.find('span', attrs={'class':'js-product-availability product-availability'})
        if OOS_Indicator.text == 'Coming soon':
            print ('Out of Stock, Retrying...')
            time.sleep(2)
        else:
            payload = {'content':'{} : Back in Stock! '.format(url)}
            s.post(webhook, data=payload, headers=headers)
            Monitor_Trigger = False

Monitor_Function(s, url, webhook)
