'''
Created on Dec 10, 2015
@author: hanhanwu
This Model serves like a homepage, it provides both reactive and proactive recommendations for sellers
'''
from numpy import *
import re
import NewsParser
import NMF
import RSSParser
import MyClassifiers
import Levenshtein
import MySQLdb

# In case something went wrong with the News Report systems, the pts here can be used as sorted_vote
def get_patterns_incase():
    incase_path = '/Users/hanhanwu/Desktop/lab project/pattern_count_incase.txt'
    f = open(incase_path,'r')
    pts = []
    for le in f:
        l = le[1:-1]
        break
    lst = l.split(', ')
    i = 0
    while (i < (len(lst)-1)):
        pt = lst[i][2:-1]
        c = lst[i+1][:-1]
        pts.append((pt,int(c)))
        i += 2
    return pts
        

def main():
    # Proactive recommendations, based on daily news
    print 'Proactive Daily Recommendations: '
    # Daily News are extracted from these feeds
    feedlist = [
                'http://rss.cnn.com/rss/edition_business.rss',
                'https://news.google.com/news/section?topic=b&output=rss',
                ]
    
    all_words, article_titles, article_words = NewsParser.get_news_text(feedlist)
    articlemx, word_vec = NewsParser.make_article_matrix(all_words, article_words)
    # Get weight and feature matrix
    v = matrix(articlemx)
    pattern_num = 30
    iter = 10
    weights, feats = NMF.factorize(v,pattern_num,iter)
    top_num = 15;
    # Get 30 patterns from daily news
    pattern_names = NewsParser.get_features(top_num, weights, feats, word_vec)           
    
    # Train the data
    trainingdata_file = open('/Users/hanhanwu/Documents/workspace/PythonLearning/Sellers++/training_data','r')
    cl1 = MyClassifiers.classifier(MyClassifiers.get_words)
    cl2 = MyClassifiers.fisherclassifier(MyClassifiers.get_words)
    for line in trainingdata_file:
        elems = line.split('****')
        cate = elems[1].split(',')[0]
        item = elems[0]
        cl1.train(item, cate)
        cl2.train(item, cate)
    trainingdata_categories = cl2.categories()
    amazon_categories = RSSParser.get_product_category()
    new_categories = list(set(amazon_categories) - set(trainingdata_categories))
    # When new categories appear, send me a notice
    if len(new_categories) > 0:
        print 'Update the training data: '
        print new_categories
    category_vote = {}
    for p in pattern_names:
        fit_category, max_prob = MyClassifiers.get_category(cl2, trainingdata_categories, p)
        category_vote.setdefault(fit_category, 0)
        category_vote[fit_category] += 1
    sorted_vote = sorted(category_vote.iteritems(), key = lambda (k,v): (v,k), reverse = True)
    
    # Based on this sorted votes, recommended new products in each voted category based on the ratio, products with deals come first
    daily_recommendations = {}
    for t in sorted_vote:
        prod_category = t[0]  
        prod_amount = t[1]
        new_product_info = {}
        new_product_info = RSSParser.get_newproduct_info(prod_category, prod_amount)
        if len(new_product_info) < prod_amount:
            new_product_info_nodeal = RSSParser.get_newproduct_info(prod_category, prod_amount, deal=0)
            new_product_info.update(new_product_info_nodeal)
        daily_recommendations.update(new_product_info)
    print 'daily recommendations: '
    for pname, pinfo in daily_recommendations.iteritems():
        print 'Product Name: ', pname
        print 'Product Price: ', pinfo['current_price']
        
    print '**********************************************************'
    
    # This variable is the user input, you can change this to test
    user_input = 'Stark Electric Small Mini Portable Compact Washer Washing'
     
    # Reactive recommendations, based on the product name provided by the user
    conn = MySQLdb.connect(host='localhost',
                           user='root',
                           passwd='sellers',
                           db='dbSellers'
                          )
    x = conn.cursor()
    max_ratio = 0
    real_pname = ''
    try:
        x.execute("""
                  SELECT ProductName FROM tbProducts;
                  """)
        numrows = x.rowcount
         
        for i in xrange(0,numrows):
            p_name = x.fetchone()[0]
            ledist = Levenshtein.ratio(p_name, user_input)
            if ledist > max_ratio:
                max_ratio = ledist
                real_pname = p_name   
                 
        if real_pname != '':
            print 'Product Name', real_pname
            x.execute("""
            SELECT CurrentPrice FROM tbProducts WHERE ProductName = %s
            """, (real_pname,))
            print 'Predicted Price', x.fetchall()[0][0]
    except:
        conn.rollback()
         
    x.close()
    conn.close()
    
if __name__ == "__main__":
    main()
