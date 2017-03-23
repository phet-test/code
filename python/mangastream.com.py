'''
author: Karl Thornton <karl.genockey.thornton@gmail.com>
Takes a mangastream.com chapter URL e.g. 
    http://mangastream.com/r/demons_plan/010/3997/
and extracts all images to title/chapter e.g.
    demons_plan/010/01.png
    demons_plan/010/02.png
See https://kaijento.github.io/2017/03/23/Web-Scraping-mangastream.com/
for details
'''

from __future__ import print_function

import errno, os, requests, sys
from   bs4 import BeautifulSoup

def makedirs(dirname):
    try:
        print('MKDIR: ', dirname)
        os.makedirs(dirname)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(dirname):
            pass
        else:
            raise

def save_image(url):
    filename = url.split('/')[-1]
    path     = os.path.join(dirname, filename)
    with open(path, 'wb') as fh:
        print('GET:   ', url)
        image = s.get(url).content
        print('CREATE:', path)
        fh.write(image)

def parse_page(url):
    print('GET:   ', url)
    r    = s.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')

    img = soup.find(id='manga-page')
    save_image(img['src'])

if __name__ == '__main__':

    url  = sys.argv[1]
    dirname = os.path.join(*url.strip('/').split('/')[-3:-1])

    makedirs(dirname)

    with requests.session() as s:
        s.headers['user-agent'] = 'Mozilla/5.0'

        print('GET:   ', url)
        r    = s.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')

        img = soup.find(id='manga-page')
        save_image(img['src'])

        last = soup.select('.btn-reader-page a')[-1]['href'].split('/')[-1]

        for n in range(2, int(last) + 1):
            next_page = url.strip('/') + '/{}'.format(n)
            parse_page(next_page)
