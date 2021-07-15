#!/usr/bin/env python
# coding: utf-8

# In[38]:


from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from urllib.request import Request

from datetime import datetime
import time


# In[39]:


directory = r'C:\Users\<username>\Documents\Investment\Finviz Scans'
filename = datetime.today().strftime('%d-%m-%Y') + \
    r'-finviz-long-momentum-stocks' + '.csv'
f = open(directory + '\\' + filename, 'w+')


# In[40]:


numPages = 4
currentPage = 1
tableRowHeaderNumber = 6

longUrl = 'https://finviz.com/screener.ashx?v=111&f=fa_epsqoq_o10,fa_epsyoy_o10,fa_salesqoq_o10,sh_avgvol_o200,sh_curvol_o200,sh_price_o2,ta_sma200_pa,ta_sma50_pa&ft=3&r='
shortUrl = 'https://finviz.com/screener.ashx?v=111&f=fa_epsqoq_o10,fa_epsyoy_o10,fa_salesqoq_o10,sh_avgvol_o200,sh_curvol_o200,sh_price_o10,ta_sma200_pb,ta_sma50_pb&r='

headers = {
    'User-Agent': 'Mozilla/5.0'
}


for page in range(0, numPages):

    # Open up connection
    req = Request(longUrl + str(currentPage), headers=headers)
    uClient = uReq(req)

    # HTML page
    webpage_html = uClient.read()
    uClient.close()

    # HTML parsing
    page_soup = soup(webpage_html, "html.parser")
    # print(page_soup.prettify())

    table = page_soup.find('div', id='screener-content')
    # print(table);

    rows = table.find_all('tr')

    for idx, row in enumerate(rows):

        csvLine = []

        if(idx == tableRowHeaderNumber and page == 0):
            for i in range(5):
                csvLine.append(row.find_all('td')[i].text.replace(",", "|"))
            csvLine.append(row.find_all('td')[8].text.replace(",", "|"))
            data = ','.join(map(str, csvLine)) + '\n'
            f.write(data)

        elif(idx > tableRowHeaderNumber):
            if('Filters: ' in row.find_all('td')[0].text):
                break

            for i in range(5):
                csvLine.append(row.find_all('td')[i].text.replace(",", "|"))
            csvLine.append(row.find_all('td')[8].text.replace(",", "|"))
            data = ','.join(map(str, csvLine)) + '\n'
            f.write(data)

    print('page', (page+1), ' done')
    currentPage += 20
    time.sleep(2)


print('Scraping done')


# In[41]:


f.close()
