'''
https://kaijento.github.io/2017/03/28/pdf-scraping-tim-hortons-invoice/
'''
import json, re, subprocess

pdfname = 'invoice.pdf'

output = subprocess.check_output(
    ['pdftotext', '-layout', pdfname, '-']).decode()

pages = output.strip('\f').split('\f')
page  = pages[-1]

address = re.search(r'(?s)(?<=Sold To:).+?(?=\n\n)', pages[-1]).group()
address = address.replace('Deliver To:', '').splitlines()

sold_to, delivered_to = zip(
    *(re.split(r'\s{2,}', line.strip()) for line in address))

bill_of_lading = re.search(r'Bill Of Lading:\s*(\S+)'    ,page).group(1)
currency       = re.search(r'Currency:\s*(\S+)'          ,page).group(1)
customer_po    = re.search(r'Customer PO:\s*(\S+)'       ,page).group(1)
due_date       = re.search(r'Due Date:\s*(\S+)'          ,page).group(1)
invoice_number = re.search(r'Invoice Number:\s*(\S+)'    ,page).group(1)
invoice_date   = re.search(r'Invoice Date:\s*(\S+)'      ,page).group(1)
order_number   = re.search(r'Order #:\s*(\S+)'           ,page).group(1)
payment_term   = re.search(r'Payment Term:\s*(.+?)\s{2,}',page).group(1)
sales_tax_base = re.search(r'Sales Tax Base\s*:\s*(\S+)' ,page).group(1)
gst_hst_base   = re.search(r'GST/HST Base\s*:\s*(\S+)'   ,page).group(1)

expenses = re.search(
    r'(?s)(Description\s*Extended Price\s*.+?Grand Total\s*\S+)', page).group()
expenses = re.sub(
    r'Price including\s*\n\s*Sales Tax', 'Price Including Sales Tax', expenses)

expenses = [
    re.split(r'\s{2,}', line.strip()) for line in expenses.splitlines()
]

total, fuel_surcharge, gst_hst_total, grand_total = [
    expense[-1] for expense in expenses[-4:]
]

summary = {
    'Sold To'       : sold_to,        'Delivered To'  : delivered_to, 
    'Bill of Lading': bill_of_lading, 'Currency'      : currency,
    'Customer PO'   : customer_po,    'Due Date'      : due_date,
    'Invoice Number': invoice_number, 'Invoice Date'  : invoice_date,
    'Order Number'  : order_number,   'Payment Term'  : payment_term,
    'Sales Tax Base': sales_tax_base, 'GST/HST Base'  : gst_hst_base,
    'Total'         : total,          'Fuel Surcharge': fuel_surcharge,
    'GST/HST Total' : gst_hst_total,  'Grand Total'   : grand_total
}

summary['Expenses'] = [
    dict(zip(expenses[0], expense)) for expense in expenses[1:-4]
]

print(json.dumps(summary, indent=4, sort_keys=True))
