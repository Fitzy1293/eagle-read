#!/bin/env python3
import requests
from bs4 import BeautifulSoup
from pprint import pprint


def findPrintArticle(articleUrl='https://www.berkshireeagle.com'):

    text = requests.get(articleUrl).text
    soup = BeautifulSoup(text, 'html.parser')

    paragraphs = [str(i) for i in soup.find_all('p') if str(i).startswith('<p>')]
    paragraphsStripTags = [i.replace('<p>', '').replace('</p>', '') for i in paragraphs]

    return '\n'.join(paragraphsStripTags)

articleUrl = 'https://www.berkshireeagle.com/stories/sterling-ready-to-put-her-toolkit-to-work-as-executive-director-of-the-massachusetts-black-and,614950'
readableArticle = findPrintArticle(articleUrl)
print(readableArticle)
