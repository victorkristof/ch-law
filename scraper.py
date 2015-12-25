from pyquery import PyQuery as pq
from lxml import html
import os
from progressbar import ProgressBar
import requests
import pickle
import time
import datetime


def get_html(url):
        r = requests.get(url)
        if r.status_code == 200:
            return str(r.text)
        elif r.status_code == 404:
            return None


def save_html(html, filename):
    if html:
        with open(filename, 'wb') as f:
            pickle.dump(html, f)


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
    bar = ProgressBar(81)
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
            bar.update((i-1) * 9 + j)

    count_laws = len(law_links)
    print("Law links: %d" % count_laws)

    # Download law pages
    print('Downloading law pages...')
    template_url = admin_url + "%s"
    now = int(time.time())
    bar = ProgressBar(count_laws)
    for i, link in enumerate(law_links):
        law_id = link.split('/')[4]
        html = get_html(template_url % link)
        filename = laws_dir + '/%s.html' % law_id
        save_html(html, filename)
        bar.update(i)
    after = int(time.time())
    elapsed_time = datetime.timedelta(seconds=(after - now))
    print('Done. Elapsed time: %s' % elapsed_time)
    print(elapsed_time)
