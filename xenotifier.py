#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import smtplib
from datetime import datetime
import requests
from bs4 import BeautifulSoup as bs
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import os

#
# URL απο το website της ΧΕ με οτι filters είναι αναγκαία
#
# Galatsi
URL = 'http://www.xe.gr/property/search?System.item_type=re_residence&Transaction.type_channel=117541&Transaction.price.to=500&Item.area.from=70&Geo.area_id_new__hierarchy=82376,82375,82999,82998,83175,83178,83181,83174' # noqa

# gmail username
UNAME = os.environ.get('GMAIL_USERNAME')
# gmail password
PWD = os.environ.get('GMAIL_PWD')
# sender address
FROM = 'xenotifier@gmail.com'
# comma separated list of recipients
TO = os.environ.get('XE_RECIPIENTS')

soup = bs(requests.get(URL).content, 'lxml')
houses = soup.findAll('div', class_='lazy r')
houses_list = []

with open('seen_houses.txt', 'ra+') as logfile:
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
            houses_list.append({
                'url': url,
                'price': price,
                'description': house.find('p').text.encode('utf-8'),
                'date_posted': date_posted,
                'tm': [
                    li for li in house.findAll('li') if u' τ.μ.' in li.text
                ][0].text.encode('utf-8')
            })

body = ''
for house in houses_list:
    house_str = """Σπίτι με τιμή %(price)s,
    %(tm)s τ.μ.
    %(description)s
    Δημοσιεύθηκε στις %(date_posted)s
    Link στην  Χ.Ε http://www.xe.gr%(url)s


    """ % house
    body += house_str

if houses_list and (UNAME and PWD and FROM and TO):
    body = "Γειά ! \n" + body
    msg = MIMEMultipart()
    msg['From'] = FROM
    msg['To'] = TO
    msg['Subject'] = "Σπίτια απο Χρυσή ευκαιρία %s" % datetime.isoformat(
        datetime.now()
    )
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(UNAME, PWD)
    server.sendmail(FROM, TO.split(","), msg.as_string())
    server.quit()
