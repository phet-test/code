'''
author: Karl Thornton <karl.genockey.thornton@gmail.com>
https://kaijento.github.io/2017/03/27/PDF-scraping-gwinnetttaxcommissioner.publicaccessnow.com/
'''
import csv, re, requests, sys
from   subprocess import Popen, PIPE

url = (
    'http://gwinnetttaxcommissioner.publicaccessnow.com/'
    'Portals/0/PDF/Excess%20funds%20all%20years%20-%20rev02232017.pdf'
)

command = ['pdftotext', '-layout', '-', '-']

p = Popen(command, stdout=PIPE, stdin=PIPE)
r = requests.get(url, headers={'user-agent': 'Mozilla/5.0'})

stdin  = r.content
output = p.communicate(input=stdin)[0].decode()

writer = csv.writer(sys.stdout)
for line in re.findall('(?m)^\d.+\d$', output):
    line = re.sub(r'\$ +', '$', line)
    line = re.sub(r' (R\d{4}) *(\d{3}[A-Z]?) ', r' \1\2 ', line)
    row  = re.split(r' {2,}', line)
    writer.writerow(row)
