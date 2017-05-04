# https://kaijento.github.io/2017/05/04/web-scraping-eventtarget-viewstate/

import requests
from   bs4 import BeautifulSoup

url = 'http://www.privataaffarer.se/borsguiden/analyser/'

with requests.session() as s:
    s.headers['user-agent'] = 'Mozilla/5.0'

    r    = s.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')

    target = (
        'ctl00$FhMainContent$FhContent$ctl00'
        '$AnalysesCourse$CustomPager$dataPager$ctl01$ctl{:02d}'
    )

    # unsupported CSS Selector 'input[name^=ctl00][value]'
    data  = { tag['name']: tag['value'] 
                  for tag in soup.select('input[name^=ctl00]') if tag.get('value') }
    state = { tag['name']: tag['value'] for tag in soup.select('input[name^=__]') }

    data.update(state)

    # data['ctl00$FhMainContent$FhContent$ctl00$AnalysesCourse$CustomPager$total']
    last_page = int(soup.find('div', 'custom_pager_total_pages').input['value'])

    # for page in range(last_page + 1):
    for page in range(3):
        data['__EVENTTARGET'] = target.format(page)

        r    = s.post(url, data=data)
        soup = BeautifulSoup(r.content, 'html5lib')

        # unsupported CSS Selector 'tr:not(.tr_header)'
        for tr in soup.select('.analysis_table tr'):
            row = [ td.text.strip() for td in tr('td')[1:-1] ]
            if row:
                print(','.join(row))
