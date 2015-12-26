from pyquery import PyQuery as pq
from lxml import html
import os
from scraper import Scraper


data_dir = "data/droit-interne"
themes_dir = data_dir + "/themes"
laws_dir = data_dir + "/laws"
admin_url = "https://www.admin.ch"


if __name__ == '__main__':

    # Crete laws directory
    os.mkdir(laws_dir)

    # Start retrieving law link
    print("Retrieving law links...")
    law_links = []
    for i in range(1, 10):
        folder = themes_dir + '/%s' % i
        for j in range(0, 10):
            law_id = str(i) + str(j)
            file = folder + '/%s.html' % law_id
            if os.path.exists(file):
                tree = html.parse(file)
                table_body = tree.xpath('//*[@id="content"]/table/tbody')
                for row in pq(table_body):
                    links = pq(row)('tr td a[href]')
                    for link in links:
                        href = link.get('href')
                        if href[-5:] == ".html":
                            law_links.append(href)

    print('Downloading %s law pages...' % len(law_links))

    # Create list of links and destinations
    template_url = admin_url + "%s"
    links = []
    destinations = []
    for i, link in enumerate(law_links):
        law_id = link.split('/')[4]
        url = template_url % link
        file_name = laws_dir + '/%s.html' % law_id
        links.append(url)
        destinations.append(file_name)

    # Download law pages
    scraper = Scraper()
    scraper.download_pages(links, destinations)

    print('Done.')
