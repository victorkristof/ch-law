import requests
from progressbar import ProgressBar
import html

class Scraper:

    def __init__(self):
        """
        Initialize a scraper object to help getting data from web pages.

        """
        pass

    def get_html(self, url):
        """
        Get the HTML from a URL.

        :param url: URL to reach
        :return:    HTML as string or None if got a 404
        """
        r = requests.get(url)
        if r.status_code == 200:
            # Unescape accents to obtain readible text
            return html.unescape(r.text)
        elif r.status_code == 404:
            return None

    def save_html(self, html, filename):
        """
        Save the HTML to a file.

        :param html:        HTML to be saved
        :param filename:    File name
        :return:
        """
        if html:
            with open(filename, 'w') as f:
                f.write(html)

    def download_pages(self, links, destinations):
        """
        Download a save a list of URLs as HTML.

        :param links:           List of URLs
        :param destinations:    List of path with file names
        """
        total = len(links)
        bar = ProgressBar(total)
        for i, url in enumerate(links):
            html = self.get_html(url)
            self.save_html(html, destinations[i])
            bar.update(i)