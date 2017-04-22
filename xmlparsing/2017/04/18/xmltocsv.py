'''
https://kaijento.github.io/2017/04/18/parsing-xml-with-python/
'''
import csv, sys, lxml.etree

xmlfile = 'input.xml'

fieldnames = [
    'EA', 'I3', 'TP', 'TI', 'ST', 'ED', 'AU', 
    'TR', 'BC', 'BI', 'CO', 'MP', 'PD', 'PA', 
    'NP', 'RP', 'RI', 'RE', 'DI', 'EI', 'PU', 
    'YP', 'RS', 'SR', 'IU', 'DE', 'RF', 'WE', 
    'SG', 'IB', 'AV', 'PI', 'GC', 'NC', 'IL', 
    'CP', 'LA', 'RC', 'SE', 'PT', 'PN', 'SI'
]

writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
writer.writeheader()

tags = set(fieldnames)
doc  = lxml.etree.iterparse(xmlfile)

row = {}
for event, elem in doc:
    if elem.tag == 'Record':
        if row:
            writer.writerow(row)
            row = {}
    elif elem.tag not in tags:
        continue
    else: 
        value = elem.text
        if elem.tag in ('EA', 'I3'):
            value = '%.2E' % int(value)
        if elem.tag in row:
            row[elem.tag] += " " + value
        else:
            row[elem.tag] = value
