# -*- coding: utf-8 -*-
import glob
import re
import pickle
from pyquery import PyQuery as pq
from lxml import html
from progressbar import ProgressBar
from collections import Counter

laws_dir = "data/droit-interne/laws"

def extract_subtitle(h2):
    subtitle = ""
    if len(h2) > 0:
        for h in h2:
            h = pq(h).remove('sup')
            h_text = pq(h).text()
            if h_text and h_text[0] == '(':
                subtitle = h_text[1:-1]
                if subtitle[-1] == ' ':
                    subtitle = subtitle[:-1]
    return subtitle


def extract_introduction(preamble):
    preamble = preamble.remove('h1')
    preamble = preamble.remove('a[name="kopf"]')
    intro = []
    for tag in preamble.children():
        intro.append((tag.tag, pq(tag).html()))
    return intro


def is_collapseable(node):
    return node.tag == "div" and node.get('class') and node.get('class') == "collapseable"


def generate_article_id(name, law_id):
    article_id = name.replace('Art. ', '').replace('§', '').replace(' ','-')
    article_id = re.sub('<sup>.*</sup>', '', article_id)
    article_id = law_id + '-' + article_id
    return article_id

def extract_article_name(article, law_id, law_content):
    title_node = pq(article.getprevious())
    links = pq(title_node)("a")
    name = None
    foot_notes = {}
    for link in links:
        if pq(link).text():
            href = link.get('href')
            if href[0] == "#":
                foot_ref = int(pq(link).text())
                foot_texts = pq(law_content)("a[name]")
                for foot_text in foot_texts:
                    if foot_text.get('name') == href[1:]:
                        text = pq(foot_text.getparent()).html().split('<br/>')[foot_ref-1].replace('<a name="%s"><sup>%s</sup></a> ' % (foot_text.get('name'), foot_ref), '')
                        foot_notes[foot_ref] = text
            if "index.html" in href:
                name = pq(link).text()
    for k in foot_notes.keys():
        name += "<sup>%s</sup>" % k

    assert(name is not None)

    article_id = generate_article_id(name, law_id)

    return article_id, name, foot_notes


def extract_article_content(article, law_id, law_content, foot_notes):
    return {}, foot_notes


def extract_articles(law_id, law_content):
    article_lists = []
    articles = pq(law_content)('div.collapseableArticle')
    for article in articles:
        article_id, name, foot_notes = extract_article_name(article, law_id, law_content)
        article_content, content_foot_notes = extract_article_content(article, law_id, law_content, foot_notes)
        a = {
            'article_id': article_id,
            'name': name,
            'foot_notes': foot_notes,
            'content': article_content
            }
        article_lists.append(a)
    return article_lists


if __name__ == '__main__':
    # Get all the HTML files
    laws_html = glob.glob(laws_dir + '/*')

    laws = dict()
    types = Counter()

    bar = ProgressBar(len(laws_html))
    bar.start()
    for i, law_html in enumerate(laws_html):

        # Prepare parsed elements
        tree = html.parse(law_html)
        law_content = pq(tree.xpath('//*[@id="lawcontent"]'))
        preamble = pq(tree.xpath('//*[@id="lawcontent"]/div[2]'))
        h1 = preamble('h1')
        h2 = preamble('h2')

        # Extract law data
        subtitle = extract_subtitle(h2)
        intro = extract_introduction(preamble)
        law_id = h1[0].text
        title = h1[1].text
        law_type = title.split()[0].lower()
        articles = extract_articles(law_id, law_content)

        # Data analysis
        types.update([law_type])

        # Store law data
        laws[law_id] = {
            'title': title,
            'type': law_type,
            'subtitle': subtitle,
            'preamble': intro,
            'articles': articles
            }

        bar.update(i)

    # Save data
    with open(laws_dir + '/../laws.pkl', 'wb') as f:
        pickle.dump(laws, f)

    # Data analysis
    for t, c in types.items():
        print("%s: %s" % (c, t))

    #print(laws)