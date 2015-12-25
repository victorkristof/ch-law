import requests
import os
from progressbar import ProgressBar

droit_interne_data_dir = 'data/droit-interne'
themes_dir = droit_interne_data_dir + '/themes'


def get_html(url):
    r = requests.get(url)
    if r.status_code == 200:
        return str(r.text)
    elif r.status_code == 404:
        return None


def save_html(html, filename):
    if html:
        with open(filename, 'w') as f:
            f.write(html)


if __name__ == '__main__':
    print('Downloading "Droit interne" themes...')
    os.mkdir(themes_dir)
    template_url = 'https://www.admin.ch/opc/fr/classified-compilation/%s.html'
    bar = ProgressBar(81)
    # Get main themes
    for i in range(1, 10):
        html = get_html(template_url % i)
        law_folder = '%s/%s' % (themes_dir, i)
        filename = law_folder + '.html'
        save_html(html, filename)
        os.mkdir('%s/%s' % (themes_dir, i))
        for j in range(0, 10):
            law_id = i * 10 + j
            url = template_url % law_id
            html = get_html(url)
            filename = '%s/%s.html' % (law_folder, law_id)
            save_html(html, filename)
            bar.update((i-1) * 9 + j)

    print('Done.')