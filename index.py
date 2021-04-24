from nsetools import Nse
import smtplib, json

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

nse = Nse()


secInfo = open('security.info').read()
creds = json.loads(secInfo)

gmail_username = creds['Username']
gmail_password = creds['Password']
target_mail = creds['Target']

f = open('template.html')
template = f.read()
f.close()

stockDets = nse.get_index_quote('NIFTY 50')
lastPrice = stockDets['lastPrice']
pChange = stockDets['pChange']
color = "#FF0000" if float(pChange) < 0 else "#00FF00"
nifty50 = "<font color='" + color + "'>" + str(lastPrice) + "(" + str(pChange) + ")</font>"

stockDets = nse.get_index_quote('NIFTY IT')
lastPrice = stockDets['lastPrice']
pChange = stockDets['pChange']
color = "#FF0000" if float(pChange) < 0 else "#00FF00"
niftyit = "<font color='" + color + "'>" + str(lastPrice) + "(" + str(pChange) + ")</font>"

stockDets = nse.get_index_quote('NIFTY BANK')
lastPrice = stockDets['lastPrice']
pChange = stockDets['pChange']
color = "#FF0000" if float(pChange) < 0 else "#00FF00"
niftybank = "<font color='" + color + "'>" + str(lastPrice) + "(" + str(pChange) + ")</font>"

stockDets = nse.get_index_quote('NIFTY PHARMA')
lastPrice = stockDets['lastPrice']
pChange = stockDets['pChange']
color = "#FF0000" if float(pChange) < 0 else "#00FF00"
niftypharma = "<font color='" + color + "'>" + str(lastPrice) + "(" + str(pChange) + ")</font>"

stockDets = nse.get_index_quote('NIFTY SMLCAP 50')
lastPrice = stockDets['lastPrice']
pChange = stockDets['pChange']
color = "#FF0000" if float(pChange) < 0 else "#00FF00"
niftysmlcp50 = "<font color='" + color + "'>" + str(lastPrice) + "(" + str(pChange) + ")</font>"

template = template.replace('****NIFTY50****', nifty50)
template = template.replace('****NIFTYIT****', niftyit)
template = template.replace('****NIFTYBANK****', niftybank)
template = template.replace('****NIFTYPHARMA****', niftypharma)
template = template.replace('****NIFTYSMLCP50****', niftysmlcp50)

top_stocks = ""
bottom_stocks = ""
managed_stocks = ""


"""
<tr>
	<th>NPTC</th>
	<td>98.0</td>
	<td>103.0</td>
	<td>98.0</td>
</tr>
"""

for top_stock in nse.get_top_gainers():
	top_stocks += """
	<tr>
		<th>""" + str(top_stock['symbol']) + """</th>
		<td>""" + str(top_stock['openPrice']) + """</td>
		<td>""" + str(top_stock['highPrice']) + """</td>
		<td>""" + str(top_stock['lowPrice']) + """</td>
	</tr>"""

for top_stock in nse.get_top_losers():
	bottom_stocks += """
	<tr>
		<th>""" + str(top_stock['symbol']) + """</th>
		<td>""" + str(top_stock['openPrice']) + """</td>
		<td>""" + str(top_stock['highPrice']) + """</td>
		<td>""" + str(top_stock['lowPrice']) + """</td>
	</tr>"""



template = template.replace('****TOP_PERFORMER_STOCKS****', top_stocks)
template = template.replace('****BTM_PERFORMER_STOCKS****', bottom_stocks)


f = open('stockList')
managedStockList = f.read().split('\n')
f.close()

for managed_stock in managedStockList:
	stock_details = nse.get_quote(managed_stock)
	managed_stocks += """
	<tr>
		<th>""" + str(stock_details['symbol']) + """</th>
		<td>""" + str(stock_details['open']) + """</td>
		<td>""" + str(stock_details['closePrice']) + """</td>
		<td>""" + str(stock_details['pChange']) + """</td>
		<td>""" + str(stock_details['averagePrice']) + """</td>
		<td>""" + str(stock_details['dayLow']) + """</td>
		<td>""" + str(stock_details['dayHigh']) + """</td>
		<td>""" + str(stock_details['high52']) + """</td>
		<td>""" + str(stock_details['low52']) + """</td>
	</tr>"""


template = template.replace('****MANAGED_STOCKS****', managed_stocks)


msg = MIMEMultipart('alternative')
msg['Subject'] = "Stock Prices Update"
msg['From'] = gmail_username
msg['To'] = target_mail
msg.attach(MIMEText(template, 'html'))



# email_text = """\
# From: %s
# To: %s
# Subject: %s

# %s
# """ % (gmail_username, target_mail, 'Stock Prices Update', template)


server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.ehlo()
server.login(gmail_username, gmail_password)
server.sendmail(gmail_username, [target_mail], msg.as_string())
server.close()

print('Mail Sent')

f = open('xyz.html', 'w')
f.write(template)
f.close()



# Q = nse.get_index_quote('nifty 50')
# print(Q)

# print("************************")


# for i in nse.get_top_gainers():
# 	for k in i:
# 		print(k, '\t\t', i[k])
# 	# print(i)
# 	exit()

# print("***********************")
# for i in nse.get_top_losers():
# 	print(i['symbol'])



# all_stock_codes = nse.get_index_list()

# for stockcode in all_stock_codes:
# 	Q = nse.get_index_quote(stockcode)
# 	print(Q)







# import smtplib

# gmail_user = 'sanchitn007@gmail.com'
# gmail_password = 'Alphabeta_9'

# sent_from = gmail_user
# to = ['snayyar1901@gmail.com']
# subject = 'OMG Super Important Message'
# body = 'Hey, what\'s up?\n\n- You'

# email_text = """\
# From: %s
# To: %s
# Subject: %s

# %s
# """ % (sent_from, ", ".join(to), subject, body)

# server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
# server.ehlo()
# server.login(gmail_user, gmail_password)
# server.sendmail(sent_from, to, email_text)
# server.close()

# print('Email sent!')