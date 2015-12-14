'''
Created on Dec 9, 2015
@author: hanhanwu
'''
import re
import math

class classifier:
    def __init__(self, getfeatures, filename = None):
        # For each feature, count how many this feature in a category
        self.fc = {}
        # Count how many items in each category
        self.cc = {}
        self.getfeatures = getfeatures
        
    # Increase the count of (feature, category) combination
    def infc(self, feat, cate):
        self.fc.setdefault(feat,{})
        self.fc[feat].setdefault(cate,0)
        self.fc[feat][cate] += 1
    
    # Increase the count of category    
    def incc(self, cate):
        self.cc.setdefault(cate,0)
        self.cc[cate] += 1
        
    # Return the number of a feature in a category
    def fcount(self, feat, cate):
        if feat in self.fc and cate in self.fc[feat]:
            return float(self.fc[feat][cate])
        return 0.0
    
    # Return the number of items in a category
    def ccount(self, cate):
        if cate in self.cc:
            return float(self.cc[cate])
        return 0.0
    
    # Return total number of items
    def itemscount(self):
        return sum(self.cc.values())
    
    # Return a list of all categories
    def categories(self):
        return self.cc.keys()
    
    # Get the train data by using getfeatures method
    def train(self, item, cate):
        features = self.getfeatures(item)
        for feat in features:
            self.infc(feat, cate)
        self.incc(cate)
        
    # Calculate the probability that a feature appears in a category
    def fprob(self, feat, cate):
        if self.ccount(cate) == 0:
            return 0
        return self.fcount(feat, cate)/self.ccount(cate)
    
    # Calculated weighted probability, the assumed probability ap starts with 0.5
    # by using assumed probabilities, when a word does not in the training data for this category, at least has a 0.5 probability
    def weightedprob(self, feat, cate, myweight = 1.0, ap = 0.5):
        basicprob = self.fprob(feat, cate)
        
        # Count the number of this feature appeared in all categories
        totals = sum(self.fcount(feat, c) for c in self.categories())
        # Calculate weighted average
        bp = ((myweight*ap)+(totals*basicprob))/(myweight+totals)
        return bp


# Fisher classifier, fit chi-square distribution
class fisherclassifier(classifier):
    def cprob(self, feat, cate):
        # The frequency of this feature in this category
        clf = self.fprob(feat, cate)
        if clf == 0:
            return 0.01
        
        # The frequency of this feature appear in all the categories
        freqsum = sum(self.fprob(feat, c) for c in self.categories())
        
        p = clf/(freqsum)
        return p
    
    # Combine probabilities of the individual features to get the overall probabilities
    def fisherprob(self, features, cate):
        fp = 1
        for feat in features:
            fp*=(self.weightedprob(feat, cate, self.cprob(feat, cate)))
            
        fscore = (-2)*math.log(fp)
        return self.invchi2(fscore, len(features)*2)
    
    def invchi2(self, chi, df):
        m = chi/2.0
        sum = term = math.exp(-m)
        for i in range(1, df/2):
            term *= m/i
            sum += term
        return min(sum, 1.0)


# In this project, get_words is getfeatures in the classifier
def get_words(txt):
    splitter = re.compile('\W')
    words = [s.lower() for s in splitter.split(txt) if len(s) > 2 and len(s) < 20]
    
    # Return unique set of words
    return dict([(w,1) for w in words])


def get_category(fisher_classifier, categories, feats):
    max_prob = 0
    fit_category = ''
    for cate in categories:
        prob = fisher_classifier.fisherprob(feats, cate)
        if prob > max_prob:
            max_prob = prob
            fit_category = cate
    return fit_category, max_prob


def main():
    trainingdata_file = open('/Users/hanhanwu/Documents/workspace/PythonLearning/Sellers++/training_data','r')
    cl1 = classifier(get_words)
    cl2 = fisherclassifier(get_words)
    for line in trainingdata_file:
        elems = line.split('****')
        cate = elems[1].split(',')[0]
        item = elems[0]
        cl1.train(item, cate)
        cl2.train(item, cate)
        
    p1 = cl1.weightedprob('hanhan', 'music')
    p2 = cl2.cprob('hanhan', 'music')
    print p1
    print p2
    words = ['farook', 'bernardino', 'citigroup', 'funded', 'syed', 'lending', 'made', 'times', 'business', 'rose', 'four', 'hollywood', 'will', 'stocks', 'rates']
    cs = cl2.categories()
    for c in cs:
        print c, ': ', cl2.fisherprob(words, c)
    fit_category, max_prob = get_category(cl2, cs, words)
    print fit_category
    print max_prob

if __name__ == "__main__":
    main()
