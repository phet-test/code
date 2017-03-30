'''
author: Karl Thornton <karl.genockey.thornton@gmail.com>
https://kaijento.github.io/2017/03/30/BeautifulSoup-Removing-tags/
'''

import csv, json, requests, sys
from   bs4 import BeautifulSoup

url  = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_sector_composition'
r    = requests.get(url)
soup = BeautifulSoup(r.content, 'html5lib')

writer = csv.writer(sys.stdout)
for tr in soup.table('tr')[2:]:
    for tag in tr(['span', 'sup']):
        tag.decompose()
    writer.writerow([ td.text for td in tr('td') ])
