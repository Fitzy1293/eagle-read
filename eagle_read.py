#!/bin/env python3
import requests
import sys
import webbrowser
from bs4 import BeautifulSoup
from pprint import pprint


def findPrintArticle(articleUrl='https://www.berkshireeagle.com') -> str:

    text = requests.get(articleUrl).text
    soup = BeautifulSoup(text, 'html.parser')

    paragraphs = [str(i) for i in soup.find_all('p') if str(i).startswith('<p>')]
    #paragraphsStripTags = [i.replace('<p>', '').replace('</p>', '') for i in paragraphs]

    return '\n'.join(paragraphs)

def writeHTML(fname, articleText) -> None:
    with open(fname, 'w+') as f:
        f.write('<!DOCTYPE HTML>\n')
        f.write('<html>\n')
        f.write('<body>\n')
        f.write(f'{articleText}\n')
        f.write('</body>\n')
        f.write('</html>\n')

if __name__ == '__main__':
    #articleUrl = 'https://www.berkshireeagle.com/stories/sterling-ready-to-put-her-toolkit-to-work-as-executive-director-of-the-massachusetts-black-and,614950'
    articleUrl = sys.argv[1]
    articleText = findPrintArticle(articleUrl)
    fname = articleUrl.split('/')[-1].replace('-', '_').replace(',', '_') + '.html'
    writeHTML(fname, articleText)
    webbrowser.open(fname)
