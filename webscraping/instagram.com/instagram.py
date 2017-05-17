#  https://kaijento.github.io/2017/05/17/web-scraping-instagram.com/
from __future__ import print_function
import json, re, requests

user = 'thefatfoxcamden'

profile = 'https://www.instagram.com/' + user

with requests.session() as s:
    s.headers['user-agent'] = 'Mozilla/5.0'

    end_cursor = ''
    for count in range(1, 3):
        print('PAGE: ', count)
        r = s.get(profile, params={'max_id': end_cursor})

        data = re.search(r'window._sharedData = (\{.+?});</script>', r.text).group(1)
        j    = json.loads(data)

        for node in j['entry_data']['ProfilePage'][0]['user']['media']['nodes']: 
            if node['is_video']:
                page = 'https://www.instagram.com/p/' + node['code']
                r = s.get(page)
                url = re.search(r'"video_url": "([^"]+)"', r.text).group(1)
                print('VIDEO:', url)
            else:
                print('IMAGE:', node['display_src'])
        
        end_cursor = re.search(r'"end_cursor": "([^"]+)"', r.text).group(1)
