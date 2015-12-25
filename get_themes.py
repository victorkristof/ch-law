import os
from scraper import Scraper

droit_interne_data_dir = 'data/droit-interne'
themes_dir = droit_interne_data_dir + '/themes'

if __name__ == '__main__':
    print('Downloading "Droit interne" themes...')

    os.mkdir(themes_dir)
    template_url = 'https://www.admin.ch/opc/fr/classified-compilation/%s.html'

    # Create list of URLs for themes themes
    links = []
    destinations = []
    for i in range(1, 10):
        theme_dir = '%s/%s' % (themes_dir, i)
        file_name = theme_dir + '.html'
        links.append(template_url % i)
        destinations.append(file_name)
        os.mkdir('%s/%s' % (themes_dir, i))
        for j in range(0, 10):
            law_id = i * 10 + j
            url = template_url % law_id
            file_name = '%s/%s.html' % (theme_dir, law_id)
            links.append(url)
            destinations.append(file_name)

    # Download pages
    scraper = Scraper()
    scraper.download_pages(links, destinations)

    print('Done.')