#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import smtplib
from datetime import datetime
import requests
from bs4 import BeautifulSoup as bs
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

#
# URL απο το website της ΧΕ με οτι filters είναι αναγκαία
#
#
# Voreia kai anatolika proasteia
#URL = 'http://www.xe.gr/property/search?System.item_type=re_residence&Transaction.type_channel=117541&Geo.area_id_new__hierarchy=82272&System.age=7&Transaction.price.from=450&Transaction.price.to=650&Item.area.from=60&Item.construction_year.from=2000&Publication.level_num.from=3'

# Voreia kai anatolika proasteia + ampelokipoi,panormou
#URL = 'http://www.xe.gr/property/search?System.item_type=re_residence&Transaction.type_channel=117541&Geo.area_id_new__hierarchy=82272,82370,82371&Transaction.price.to=650&Item.area.from=65&Item.construction_year.from=2000&Publication.level_num.from=3'

#URL = 'http://www.xe.gr/property/search?System.item_type=re_residence&Transaction.type_channel=117541&Geo.area_id_new__hierarchy=82272,82370,82371&Transaction.price.to=650&Item.area.from=65&Publication.level_num.from=3'

#Xolargos kai xalandri apo 1985
URL = 'http://www.xe.gr/property/search?System.item_type=re_residence&Transaction.type_channel=117541&Geo.area_id_new__hierarchy=82448,82447&Transaction.price.from=450&Transaction.price.to=650&Item.area.from=65&Item.construction_year.from=1985&Item.bedrooms.from=2&Publication.level_num.from=3&Publication.age=10'


#gmail username
UNAME = ''
#gmail password
PWD = ''
# sender address
FROM = 'xenotifier@gmail.com'
# comma separated list of recipients
TO = ''

soup = bs(requests.get(URL).content, 'lxml')
houses = soup.findAll('div', class_='lazy r')
houses_list = [] 
with open('seen_houses.txt','a+') as logfile:
    seen = logfile.read().splitlines()
    for house in houses:
        price = 'Not Available'
        date_posted = 'Not Available'
        if house.find('li', class_='r_price'):
            price = house.find('li', class_='r_price').text.encode('utf-8')
        if house.find('p', class_='r_date'):
            date_posted = house.find('p', class_='r_date').text.encode('utf-8')
        url = house.find(href=re.compile('enoikiaseis')).attrs['href']
        if url not in seen:
            logfile.write(url+'\n')
            houses_list.append({'url': url,
                                'price': price,
                                'description': house.find('p').text.encode('utf-8'),
                                'date_posted': date_posted,
                                'tm': [li for li in house.findAll('li') if u' τ.μ.' in li.text][0].text.encode('utf-8')})
if houses_list:
    msg = MIMEMultipart()
    msg['From'] = FROM
    msg['To'] = TO
    msg['Subject'] = "Σπίτια απο Χρυσή ευκαιρία "+datetime.isoformat(datetime.now())

    body = "Γειά ! \r\n"
    for house in houses_list:
        house_str = 'Σπίτι με τιμή ' +house['price'] + '\r\n' + house['tm'] + '\r\n' + house['description'] +'\r\n  Δημοσιεύθηκε στις' + house['date_posted'] + '\r\n' + 'Link στην  Χ.Ε http://www.xe.gr'+house['url']+'\r\n\r\n\r\n'
        body += house_str
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(UNAME,PWD)
    server.sendmail(FROM, TO.split(","), msg.as_string())
    server.quit()
