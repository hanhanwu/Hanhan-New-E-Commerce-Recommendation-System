'''
Created on Dec 2, 2015
@author: hanhanwu
Read Daily News RSS, get daily theme
Classify News based on their theme and product category
'''
import feedparser
import re
import datetime
from datetime import date
import NMF
from numpy import *

def separate_words(text):
    splliter = re.compile('\W*')
    return (s.lower() for s in splliter.split(text) if len(s)>3)


def stripHTML(h):
    p = ''
    s = 0
    for c in h:
        if c == '<':
            s = 1
        elif c == '>':
            p += ' '
            s = 0
        elif s == 0:
            p += c
    return p


# Get words counts from all the daily articles, word counts from each daily article, a list of unique article title
def get_news_text(feedlist):
    article_titles = []
    all_words = {}
    article_words = []
    e_index = 0
    for feed in feedlist:
        rss = feedparser.parse(feed)
        for e in rss.entries:
            title = e.title
            pubDate = e.published
            m = re.search('\w+,\s([\d\w\s]+)\s\d\d:\d\d:\d\d\sGMT', pubDate)
            today = date.today()
            if m:
                pubDate = m.group(1)
                dt = datetime.datetime.strptime(pubDate, '%d %b %Y')
                pubDate = datetime.date.strftime(dt, '%Y-%m-%d')
            if str(today) >= pubDate:  # Just for demo, in reality, it should be str(today) == pubDate
                if title in article_titles or title == '':
                    continue
                txt = e.title.encode('utf-8') + stripHTML(e.description.encode('utf-8'))
                words = separate_words(txt)
                article_titles.append(title)
                article_words.append({})
                
                for w in words:
                    all_words.setdefault(w, 0)
                    article_words[e_index].setdefault(w,0)
                    all_words[w] += 1
                    article_words[e_index][w] += 1
                
                e_index += 1
    return all_words, article_titles, article_words
            

def make_article_matrix(all_words, article_words):
    word_vec = []
    
    # Get those words not too common nor too rare
    for w,c in all_words.items():
        if c > 2 and c < len(article_words)*0.8:
            word_vec.append(w)
    
    # The matrix of articles with word counts, check each article word count, if the word appears in word_vec, show article word count otherwise show 0
    articlemx = [[(word in article_dict and article_dict[word] or 0) for word in word_vec] for article_dict in article_words]
    return articlemx, word_vec


def get_features(top_num, w, h, word_vec):
    features_row, features_col = shape(h)
    pattern_names = []
    
    # Loop over all the features
    for i in range(features_row):
        slist = []
        # Create a list of words and their weights
        for j in range(features_col):
            slist.append((h[i,j],word_vec[j]))
        slist.sort(reverse=True)
        
        # Print the top_num of elements
        n = [s[1] for s in slist[0:top_num]]
        pattern_names.append(n)
        
    return pattern_names
    

def main():
    feedlist = [
                'http://rss.cnn.com/rss/edition_business.rss',
                'https://news.google.com/news/section?topic=b&output=rss',
                ]
    
    all_words, article_titles, article_words = get_news_text(feedlist)
    articlemx, word_vec = make_article_matrix(all_words, article_words)
       
    # Get weight and feature matrix
    v = matrix(articlemx)
    weights, feats = NMF.factorize(v,pc=10,iter=10)
    top_num = 15;
    pattern_names = get_features(top_num, weights, feats, word_vec)
           
    print pattern_names
    
if __name__ == "__main__":
    main()
