import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

# Make a request to the webpage you want to scrape
for page in range(1, 10):

    response = requests.get('https://exam.ioe.edu.np/' + "/?page=" + str(page), timeout=60)

    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.text, 'html.parser')
    dates = soup.select("#datatable > tbody:nth-child(2) > tr > td:nth-child(3)")

    tabled = soup.table.find_all('tr')[1:]  # search the table for notice title and link
    spans = soup.find_all('span')
    for row, date in zip(tabled, dates):
        link = row.a
        notice_title = row.span

        # notice_title = notice_title.lower()
        if ('Notice' in str(notice_title) or 'Result' in str(notice_title)) and 'BE' in str(notice_title):
            text = row.span.text
            href = row.a.get('href')
            href = href.replace(' ', '%20')
            url = urljoin('https://exam.ioe.edu.np/', href)
            response = requests.get(url)
            name = text.replace('/', '').replace('(', '').replace(')', '').replace(',', '').replace(':', '')
            if 'Notice' in str(notice_title):
                with open('./pdf/Notice ' + name + '.pdf', 'wb') as f:
                    # print("completed0")
                    f.write(response.content)
                    # i=i+1
            else:
                with open('./pdf/Result ' + name + '.pdf', 'wb') as f:
                    f.write(response.content)
                    # j=j+1
                    # print("completed1")
            print('Date: ' + date.text)
            print(f'Name: {text}')
            print(f'href: {url}\n')