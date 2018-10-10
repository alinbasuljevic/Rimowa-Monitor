import requests, time, logging, threading, colorama
from bs4 import BeautifulSoup as bs
from threading import Thread
from colorama import Fore, init
init(convert=True)

class Viewer():

    def __init__(self, url, webhook):
        self.url = url
        self.webhook = webhook

    def Monitor_Function(self):
        s = requests.Session()
        headers = {
            'dnt': '1',
            'origin': 'https://www.rimowa.com',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        Monitor_Trigger = True
        while Monitor_Trigger:
            product_page = s.get(self.url, headers=headers)
            soup = bs(product_page.text, 'lxml')
            OOS_Indicator = soup.find('span', attrs={'class':'js-product-availability product-availability'})
            if OOS_Indicator.text == 'Coming soon':
                logging.info('Out of Stock, Retrying...')
                time.sleep(2)
            else:
                payload = {'content':'{} : Back in Stock! '.format(self.url)}
                s.post(self.webhook, data=payload, headers=headers)
                Monitor_Trigger = False

logging.basicConfig(level = logging.INFO, format = Fore.WHITE + '[%(asctime)s][%(threadName)s]: %(message)s', datefmt=('%I:%M:%S %p'))

###### This is where you update for your own webhook and url ######
###(ex. Viewer('https://www.rimowa.com/blahblahblah', 'personal webhook')##############

task_1 = Viewer('https://www.rimowa.com/us/en/%22see-through%22-white/83290002.html?cgid=limited-edition#start=2','')
task_2 = Viewer('https://www.rimowa.com/us/en/%22personal-belongings%22/92590014.html?cgid=limited-edition#start=1','')
task_3 = Viewer('https://www.rimowa.com/us/en/%22see-through%22-black/83290004.html?cgid=limited-edition#start=3', '')

Thread(target = task_1.Monitor_Function).start()
Thread(target = task_2.Monitor_Function).start()
Thread(target = task_3.Monitor_Function).start()
