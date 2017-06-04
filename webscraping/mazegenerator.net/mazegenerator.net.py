# https://kaijento.github.io/2017/06/04/web-scraping-mazegenerator.net/
import requests
from   bs4 import BeautifulSoup

url = 'http://mazegenerator.net/'

with requests.session() as s:
    s.headers['user-agent'] = 'Mozilla/5.0'

    r = s.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')

    state = { 
        tag['name']: tag['value'] for tag in soup.select('input[name^=__]')
    }

    data = dict(
        ShapeDropDownList=1,
        S1TesselationDropDownList=1,
        S1WidthTextBox=20,
        S1HeightTextBox=20,
        S1InnerWidthTextBox=0,
        S1InnerHeightTextBox=0,
        S1StartsAtDropDownList=1,
        AlgorithmParameter1TextBox=50,
        AlgorithmParameter2TextBox=100,
        GenerateButton='Generate'
    )

    data.update(state)

    r = s.post(url, data=data)
    soup = BeautifulSoup(r.content, 'html5lib')

    img = soup.find('img', id='MazeDisplay')

    print(url + img['src'])

    with open('maze.svg', 'wb') as f:
        maze = s.get(url + img['src']).content
        f.write(maze)
