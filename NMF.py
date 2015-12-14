'''
Created on Dec 7, 2015
@author: hanhanwu
Do matrix factorization, multicative update rules
NMF (non-negative factorixation) is an important technique for extracting features, it returns non-negative values for features and weights, w,h here indicates weight matrix and feature matrix
Using NMF, we reconstruct the matrix to make it a smaller set but captures common features for the rows
'''

from numpy import *

# Loop over 2 equal-sized matrices, calculate the squares of the differences between them
def diffcost(a, b):
    dif = 0
    
    for i in range(shape(a)[0]):
        for j in range(shape(a)[1]):
            dif += pow(a[i,j]-b[i,j],2)
    return dif
            

# v is data matrix, pc is the number of features; 
# Using multicative update rules to update 2 matrix w, h and convert to arrays
def factorize(v, pc=10, iter=50):
    ic = shape(v)[0]
    fc = shape(v)[1]
    
    # Initialize w, h with random values
    w = matrix([[random.random() for j in range(pc)] for i in range(ic)])
    h = matrix([[random.random() for j in range(fc)] for i in range(pc)])
    
    # Perform operation a maximum of iter times
    for i in range(iter):
        wh = w*h
        
        # Calculate initial difference
        cost = diffcost(v, wh)
        
        # Terminate if the matrix has been fully factorized
        if cost == 0:
            break
        
        # Update the feature matrix
        hn = (transpose(w)*v)
        hd = (transpose(w)*w*h)
        # Using array here so that the number in each row of the 2 matrix multiple with each other
        h = matrix(array(h)*array(hn)/array(hd))*10
        
        # Update the weight matrix
        wn = (v*transpose(h))
        wd = (w*h*transpose(h))
        w = matrix(array(w)*array(wn)/array(wd))*10
        
    return w,h
        

def main():
    l1 = [[1,2,3],[4,5,6],[7,8,9]]
    l2 = [[1,2],[3,4],[5,6]]
     
    m1 = matrix(l1)
    m2 = matrix(l2)
     
    w,h = factorize(m1*m2, 10, 100)
    print w*h
    print m1*m2
 
if __name__ == "__main__":
    main()
