# https://kaijento.github.io/2017/05/19/web-scraping-youtube.com/
import requests
from   bs4 import BeautifulSoup

with requests.session() as s:
    s.headers['user-agent'] = 'Mozilla/5.0'

    url    = 'http://www.youtube.com/results'
    params = {'search_query': 'dj liquid raving'}

    r    = s.get(url, params=params)
    soup = BeautifulSoup(r.content, 'html5lib')
    
    for a in soup.select('.yt-lockup-title > a[title]'):
        if '&list=' not in a['href']:
            print('http://www.youtube.com' + a['href'], a['title'])

