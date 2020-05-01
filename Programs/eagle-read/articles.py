import requests
import os
import re
import sys
from bs4 import BeautifulSoup
from pprint import pprint

#Replace substrings with a dict of replacements.
#https://gist.github.com/carlsmith/b2e6ba538ca6f58689b4c18f46fef11c
def replace(string, substitutions):
    substrings = sorted(substitutions, key=len, reverse=True)
    regex = re.compile('|'.join(map(re.escape, substrings)))

    return regex.sub(lambda match: substitutions[match.group(0)], string)

def articleParser(url):
    response = requests.get(url)
    htmlText = response.text

    soup = BeautifulSoup(htmlText, features='html.parser')
    htmlParaTags = [str(tag) for tag in soup.findAll('p')]

    try:
        byline = str(soup.findAll('div', {'class': 'byline'})[0])
        bylineParsed = byline.split('<div class="byline" id="byline">')[-1].replace('</div>', '')
    except IndexError:
        bylineParsed = None

    #'<span class="copy View fullscreen</span>'
    htmlSubstitutions = {'<button class="btn btn-xs btn-default': '',
                         '<i aria-hidden="true" class="fa fa-desktop': '',
                         '<span class="copy">View fullscreen</span>': '',
                         '\n': '',
                         '</button>': '',
                         '<p>': '',
                         '</p>': '',
                         '<em>': '',
                         '</em>': '',
                         '<i>': '',
                         '</i>': '',
                         '<b>': '',
                         '</b>': '',
                         '<a href="': '',
                         '</a>': '',
                         '&amp;': '&',
                         '">': ' ',
                         '<br/>': '\n'}

    articleContent = []
    for paraTag in htmlParaTags:
        if not '<p style=' in paraTag and not '<p class=' in paraTag and not '<a href="mailto:news@berkshireeagle.com">' in paraTag:
            sub = replace(paraTag, htmlSubstitutions)

            articleContent.append(sub)

    articlesDir = os.path.join(os.getcwd(), 'Articles')

    fname = url.split('/')[-1]
    fname = fname.replace('-', '_')
    fname = fname.replace(',', '_')
    fname = fname + '.txt'
    fname = fname.replace('?', '')

    try:
        os.makedirs(articlesDir)
    except OSError:
        pass

    articlePath = os.path.join(articlesDir, fname)

    with open(articlePath, 'w+') as article:
        if bylineParsed:
            article.write(bylineParsed + '\n')
            article.write(url + '\n\n')

        for para in articleContent:
            words = para.split(' ')
            for j, word in enumerate(words):
                if (j % 10 == 0 and j != 0):
                    article.write('\n')

                try:
                    article.write(word + ' ')
                except UnicodeEncodeError:
                    pass

                if len(word) >= 75:
                    article.write('\n')

            article.write('\n\n')

    print()
    print(fname)
    print()
    articlePrint = open(articlePath, 'r').read().splitlines()
    for line in articlePrint:
        print(line)

def singleArticle():
    #print('https://www.berkshireeagle.com/stories/tracy-wilson-approaches-career-coda-but-love-of-music-will-go-on,601624')
    #url = input('Berkshire Eagle URL >> ')
    articleParser(sys.argv[1])

if __name__ == '__main__':
    singleArticle()
