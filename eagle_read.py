#!/bin/env python3
'''
Takes one argument:
    Berkshire eagle article full URL
Opens up the HTML in the browser
'''

import requests
import sys
import webbrowser
from bs4 import BeautifulSoup

def findPrintArticle(articleUrl='https://www.berkshireeagle.com') -> str: #Returns article text as a string
    text = requests.get(articleUrl).text
    soup = BeautifulSoup(text, 'html.parser')
    paragraphs = [str(i) for i in soup.find_all('p') if str(i).startswith('<p>')]
    return '\n'.join(paragraphs)

def writeHTML(fname, articleText) -> None: # Writes article to local html file
    with open(fname, 'w+') as f:
        f.write('<!DOCTYPE HTML>\n')
        f.write('<html>\n')
        f.write('<body>\n')
        f.write(f'{articleText}\n')
        f.write('</body>\n')
        f.write('</html>\n')

if __name__ == '__main__':
    articleUrl = sys.argv[1]
    articleText = findPrintArticle(articleUrl)
    fname = articleUrl.split('/')[-1].replace('-', '_').replace(',', '_') + '.html'
    writeHTML(fname, articleText)
    webbrowser.open(fname)
