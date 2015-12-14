'''
Created on Nov 24, 2015
@author: hanhanwu
Get product info from Camel(Amazon) RSS
'''
import re
import os
import datetime
import feedparser
import MySQLdb
from bs4 import BeautifulSoup
from urllib2 import urlopen

# Get all product categories in Camel Amazon
def get_product_category():
    path = 'http://camelcamelcamel.com/popular?deal=0&period=now&bn=\w+'
    d = feedparser.parse(path)
    summary = d['feed']['summary']
    ptn = '<option value=\"([\w\s-]*)\">'
    lst = re.findall(ptn, summary)
    categories = []
    for elem in lst:
        if elem == "" or elem == 'UTC' or elem == 'other' or elem == 'everything-else':
            continue
        categories.append(elem)
    return categories


# Get product information based on a given url
def get_product_info(category_url):
    category = category_url[0]  
    url = category_url[1]
    product_info_dict = {}
    category_dict = {}
    if category not in category_dict.keys():
        category_dict[category] = []
    soup = BeautifulSoup(urlopen(url), "html.parser")
    items = soup.find_all('item')
    for item in items:
        name = item.find('title').get_text()
        category_dict[category].append(name)
        description = item.find('description').get_text()
        parsed_pub_date = item.find('pubdate').get_text().split(' ')
        date_str = parsed_pub_date[1]+'-'+parsed_pub_date[2]+'-'+parsed_pub_date[3]
        dt = datetime.datetime.strptime(date_str, '%d-%b-%Y')
        pub_date = datetime.date.strftime(dt, '%Y-%m-%d')
        subsoup = BeautifulSoup(description, "html.parser")
        ps = subsoup.find_all('p')
        current_price = ps[0].get_text().split(' ')[2]
        a_s = ps[3].find_all('a')[1]
#         sub_url = a_s.get('href')  # Amazon removed historical price from Camel HTML
#         price_history_dict = get_price_history(sub_url)  # Amazon removed historical price from Camel HTML
        product_info_dict[name] = {}
        product_info_dict[name]['pub_date'] = pub_date
        product_info_dict[name]['current_price'] = current_price
#         product_info_dict[name]['price_history_dict'] = price_history_dict  # Amazon removed historical price from Camel HTML
#         product_info_dict[name]['sub_url'] = sub_url   # Amazon removed historical price from Camel HTML
    return product_info_dict, category_dict
        
    
# Get Amazon historical price data
def get_price_history(suburl):
    soup = BeautifulSoup(urlopen(suburl), "html.parser")
    price_history_dict = {}

    lst = soup.find_all('tbody')
    for tbody in lst:
        trs = tbody.find_all('tr')
        for elem in trs:
            tr_class = elem.get('class')
            if tr_class != None:
                if tr_class[0] == 'highest_price' or tr_class[0] == 'lowest_price':
                    tds = elem.find_all('td')
                    td_label = tds[0].get_text().split(' ')[0]
                    td_price = tds[1].get_text()
                    td_date = tds[2].get_text()
                    dt = datetime.datetime.strptime(td_date, '%b %d, %Y')
                    td_date = datetime.date.strftime(dt, '%Y-%m-%d')
                    if td_label in price_history_dict.keys():
                        price_history_dict[td_label].append((td_price, td_date))
                    else:
                        price_history_dict[td_label] = [(td_price, td_date)]
            else:
                tds = elem.find_all('td')
                td_label = tds[0].get_text().split(' ')[0]  
                if td_label == 'Average':
                    td_price = tds[1].get_text()
                    if td_label in price_history_dict.keys():
                        price_history_dict[td_label].append(td_price)
                    else:
                        price_history_dict[td_label] = [td_price]
    
    ps = soup.find_all('p')
    for p in ps:
        p_class = p.get('class')
        if p_class != None and len(p_class) == 2 and p_class[0] == 'smalltext' and p_class[1] == 'grey':
            p_text = p.get_text()
            m = re.search('since([\w\d,\s]+)\.', p_text)
            if m:
                date = m.group(1)
                dt = datetime.datetime.strptime(date, ' %b %d, %Y')
                price_history_dict['start_date'] = datetime.date.strftime(dt, '%Y-%m-%d')
            else:
                price_history_dict['start_date'] = None
            break
    return price_history_dict
    
    
# Generate all the RSS urls from Camel Amazon website    
def generate_urls(category_list):
    prefix = 'http://camelcamelcamel.com/popular.xml?'
    period = ['now', '1wk', '1mo', '3mo']
    deal = ['1', '0']
    urls = []
    for category in category_list:
        for p in period:
            for d in deal:
                url = prefix+'period='+p+'&deal='+d+'&bn='+category
                urls.append((category, url))
    return urls


# Generate the url for "now" product in this category
def generate_newprod_url(cate, deal=1):
    prefix = 'http://camelcamelcamel.com/popular.xml?'
    url = prefix+'period=now&deal='+str(deal)+'&bn='+cate
    return url

# Get all the new product info
def get_newproduct_info(category, amount, deal=1): 
    url = generate_newprod_url(category, deal)
    count = 0
    product_info_dict = {}
    soup = BeautifulSoup(urlopen(url), "html.parser")
    items = soup.find_all('item')
    for item in items:
        count += 1
        name = item.find('title').get_text()
        description = item.find('description').get_text()
        parsed_pub_date = item.find('pubdate').get_text().split(' ')
        date_str = parsed_pub_date[1]+'-'+parsed_pub_date[2]+'-'+parsed_pub_date[3]
        dt = datetime.datetime.strptime(date_str, '%d-%b-%Y')
        pub_date = datetime.date.strftime(dt, '%Y-%m-%d')
        subsoup = BeautifulSoup(description, "html.parser")
        ps = subsoup.find_all('p')
        current_price = ps[0].get_text().split(' ')[2]
        a_s = ps[3].find_all('a')[1]
        sub_url = a_s.get('href')
        product_info_dict[name] = {}
        product_info_dict[name]['pub_date'] = pub_date
        product_info_dict[name]['current_price'] = current_price
        if count == amount:
            break
    return product_info_dict
    

# Write into .txt file, t is a list and each element will be write into 1 line
def write_to_txt(t, file_name):
    if os.path.exists(file_name):
        f = open(file_name, 'w').close()
    for elem in t:
        f = open(file_name, 'a')
        f.write(elem.encode('utf-8')+'\n')
        f.close()
        
        
def main():
    # Generate all the urls
    c_list = get_product_category()
    write_to_txt(c_list, 'categories')
    category_urls = generate_urls(c_list)
    u_list = map(lambda (c,u):u, category_urls)
    write_to_txt(u_list, 'urls')
    
    # Generate product info based on each url, the data will be insert into MySQL
    for i in range(232):
        product_info_dict, category_dict = get_product_info(category_urls[i])
        print product_info_dict
        
        # Connect to MySQL 
        conn = MySQLdb.connect(host='localhost',
                               user='root',
                               passwd='sellers',
                               db='dbSellers'
                               )
        x = conn.cursor()
        
        # Insert data in product_info_dict to MySql table tbProducts
        for p_name, p_info in product_info_dict.iteritems():
            p_price = p_info['current_price']
            p_date = p_info['pub_date']
            print p_name, p_price, p_date   # for test
            try:
                x.execute("""
                          INSERT INTO tbProducts VALUES (%s,%s,%s)
                          """, (p_name, p_price, p_date))
                conn.commit()
            except:
                conn.rollback()
         
        # Insert data in category_dict to MySql table tbCategoryProduct
        for category,products in category_dict.iteritems():
            print 'category: ', category  # for test
            print 'products number: ', len(products)  # for test
            for product in products:
                print 'product: ', product   # for test
                try:
                    x.execute("""
                              INSERT INTO tbCategoryProduct VALUES (%s,%s)
                              """, (category, product))
                    conn.commit()
                except:
                    conn.rollback()
        conn.close()
    
     
    # Get a specific type of product info with a certain amount, deals come first
    amount = 15
    new_product_info = get_newproduct_info('apps-for-android', amount)
    if len(new_product_info) < amount:
        new_product_info_nodeal = get_newproduct_info('apps-for-android', amount, deal=0)
    new_product_info.update(new_product_info_nodeal)
    print new_product_info
    print len(new_product_info)

if __name__ == "__main__":
    main()
