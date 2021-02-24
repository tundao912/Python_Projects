import scrapy
from datetime import datetime
from os import system
filename = 'savenow_' + datetime.now().strftime("%d-%m-%Y/%H-%M-%S") +'.csv'
system('scrapy crawl savenow -O ' + filename)