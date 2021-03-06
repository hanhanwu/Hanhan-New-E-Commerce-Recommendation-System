# New-E-Commerce-Recommendation-System
I designed and implemented an e-commerce Recommendation System which provides product recommendations in a new way: using daily News text mining and classification techniques

The recommendation system provides 2 types of product recommendations:

• Proactive Recommendation — Users no need to do anything and they will receive daily product
recommendations which is based on daily News report Text mining

• Reactive Recommendation — Users type whatever a product name, then the system will look into the database, using Levenshtein Distance and return the most matched product information

• Implementation Tools: Python, MySql

• Major Implemented algorithms: Fisher Classifier, NMF (Non-negative Matrix Factorization)


Why NMF (Non-negative Matrix Factorization):

• NMF is an algorithm used to extract important features, after checking all the Spark MLLib text mining algorithms, k-means clustering, frequent pattern mining for text and could not the results I expected, finally decided to take a risk and try to implement NMF, it works well on Google News, CNN news, but will not work well on small amount data input like New York Times

Why Fisher Classifier:

• When it comes to text mining, I prefer to choose an algorithm tells how likely that each item fits a category, therefore algorithms like Naive Bayesian which returns probabilities will be my first choice. However, Naive Bayesian will calculate the combined probabilities based on multiple all the probabilities of an items’ features, it will work well when the items amount are the same for each category. In my case, Naive Bayesian will reduce accuracy, Fisher Classifier will overcome this shortage by taking natural log with the multiplied result and then multiple -2. 

********************************************** Part 1: How to Run the Code ***********************************************

1. Do all the installations on a Mac

2. Download Eclipse Juno and install PyDev, because Eclipse Juno will update the following python installations automatically. But if your current Eclipse can install PyDev as the Install Guidance shows, please ignore the Juno Download url below, and just install PyDev on Eclipse.
Install Guidance: https://www.youtube.com/watch?v=czs_QnExBQA
Juno Download url:https://eclipse.org/downloads/packages/eclipse-ide-java-ee-developers/junosr2

3. Install Python BeautifulSoup through command line:
	a. Download beautifulsoup4-4.4.1.tar.gz from http://www.crummy.com/software/BeautifulSoup/,and unzip the file,and unzip the file
	b. Through command line, cd to the unzipped folder
	c. Through command line, type “sudo python setup.py install”

4. Install python Levenshtein
	a. Download pythin-Levenshtein-0.12.0.tar.gz from https://pypi.python.org/pypi/python-Levenshtein/0.12.0, unzip the file
	b. Through command line, cd to the unzipped folder
	c. Through command line, type “sudo python setup.py install”

5. Install python MySqldb
	a. Copy this whole command line to your terminal to install Homebrew:
	ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
	b. Through your command line, type these 2 commands:
	brew install mysql
	pip install MySQL-python

Note: The MySql instance server is on my machine, when you are going to run the code, my machine has to be on. Therefore, please email/call me to let me know the time, so that I will turn on my machine

My Phone: 778-681-7739

My email: hanhanw@sfu.ca

I may not in Canada between Dec. 18th to Dec. 21

6. Open Eclipse PyDev, create a new Python project and put the 5 files under this project. These 5 files are in the source code folder.

7. When you are going to run the code, just open SellersRecommendation.py, and run the code. The output will change based on daily news data or user’s input. There is only one variable you can change to see different results, user_input in line 96, change this variable, you should see different changes. Other things, will parse the data from different resources and provide daily proactive recommendations.

********************************************** Part 2: Source Code Description *******************************************

1. SellersRecommendations.py
	By running this file you will get the daily products recommendations. The daily output has 2 parts: Proactive recommendations and reactive recommendations.

a. Reactive Recommendations: By changing the variable user_input (line 96) with different product names you can come up with, it will search the MySql database and find the most matched product with its price. 

b. Proactive Recommendations: This part will parse the daily Business News from Google Business News, CNN Business news and try to figure out the themes for each news, and predict/recommend the potential products based on the daily news themes.

c. A function "get_patterns_incase" in this file (line 16) will be used only when the News report removes lots of data during Christmas time (they are removing data..). If that happens, feel free to contact with me, I can send a new SellersRecommendations.py. Currently I am not adding those lines of code in case to make the code confusing.

Note: Before you are going to run the code, please call/email me so that I can start MySql instance server on my machine.

My Phone: 778-681-7739

My Email: hanhanw@sfu.ca

2. RSSParser.py
	This is the file that parse the Amazon products information from Cammel. The information will change all the time. Note: From Dec. 12th 2015, I suddenly could not get the historical price from Amazon, I was able to get everything there. I tried to checked the downloaded html file, the historical price part can no longer be downloaded. But in the code I am keeping the code that works for parsing historical price (get_price_history() method), to let you know my works.

3. NMF.py
	In this file, I have implemented Non-Negative Factorization, it is a technique to extract features. By doing the implementations here, I wanted to see how accurate this technique can be used in Text Mining, therefore, this is the file that find themes from daily news.

4. NewsParser.py
	By importing the functions from NMF.py, this file will read daily news, parse the data and finally return the daily news themes.

5. MyClassifiers.py
	In this file, I have implemented Fisher Classifier in order to do classification analysis on daily news, so that based on the themes on the news, I classify them into different categories so that I can match to the categories of products. The recommended categories are sorted on popularity descending order.

********************************************** Part 3: Sample Output *****************************************************

Proactive Daily Recommendations: 

daily recommendations: 

Product Name:  Cricut 2001974 Adhesive Cutting Mat, Standard Grip, 12 x 12-Inch, Pack of 2

Product Price:  $5.99

Product Name:  White Christmas (Diamond Anniversary Edition)

Product Price:  $8.00

Product Name:  Casio Men's AQ-S810W-1AV Solar Sport Combination Watch

Product Price:  $18.75

Product Name:  TMH 20'' Dual Row High Power 126w Cree Xb-d SMD LED Work Light Bar 13000 Lumens

Product Price:  $36.88

Product Name:  Texas Roadhouse Gift Card $25

Product Price:  $25.00

Product Name:  National Geographic Little Kids

Product Price:  $15.00

Product Name:  TIME

Product Price:  $20.00

Product Name:  Outlander: Season One - Volume Two

Product Price:  $18.49

Product Name:  Ant-Man 2-Disc 3D BD Combo Pack [Blu-ray]

Product Price:  $21.00

Product Name:  Sephora Gift Card $25

Product Price:  $25.00

Product Name:  Elf [Blu-ray]

Product Price:  $7.99

Product Name:  Applebee's Gift Card $25

Product Price:  $18.75

Product Name:  National Lampoon's Christmas Vacation [Blu-ray]

Product Price:  $7.99

Product Name:  National Geographic Traveler

Product Price:  $10.00

Product Name:  GoSports Slammo Game Set (Includes 3 Balls, Carrying Case and Rules)

Product Price:  $37.25

Product Name:  Easytle 2 ml (5/8 dram) Amber Glass Essential Oil Bottle with Orifice Reducer and cap- 12 pack

Product Price:  $1.99

Product Name:  Marvel's Avengers: Age of Ultron

Product Price:  $14.96

Product Name:  The Little Mermaid (Diamond Edition) [DVD +Digital Copy]

Product Price:  $14.96

Product Name:  SE CC4580 Military Lensatic Sighting Compass with Pouch

Product Price:  $2.00

Product Name:  The Collected Works of Hayao Miyazaki (Amazon Exclusive) [Blu-ray]

Product Price:  $399.98

Product Name:  Allen Sports Deluxe 3-Bike Hitch Mount Rack with 1.25/2-Inch Receiver

Product Price:  $39.36

Product Name:  [Lad Weather] German Sensor Digital Compass Altimeter Barometer Chronograph Alarm Weather Forecast Outdoor Wrist Sports Watches (Climbing/ Hiking/ Running/ Walking/ Camping) Men's

Product Price:  $45.00

Product Name:  The Polar Express [Blu-ray]

Product Price:  $7.99

Product Name:  Lysol Disinfecting Wipes Value Pack, Lemon and Lime Blossom, 240 Count

Product Price:  $9.97

Product Name:  Ted 2

Product Price:  $17.99

Product Name:  Humans of New York: Stories

Product Price:  $11.11

Product Name:  GameStop Gift Card $25

Product Price:  $25.00

Product Name:  Singer Titanium Universal Regular Point Machine Needles for Woven Fabric, Assorted Sizes, 10-Pack

Product Price:  $5.63

Product Name:  Amazon.com Gift Card with Greeting Card - $25 (Fitting Christmas)

Product Price:  $25.00

Product Name:  Ant-Man (1-Disc DVD)

Product Price:  $14.99

Product Name:  Thing Explainer: Complicated Stuff in Simple Words

Product Price:  $12.99
**********************************************************
Product Name Stark Electric Small Mini Portable Compact Washer Washing Machine (45L Washer)

Predicted Price $69.95
