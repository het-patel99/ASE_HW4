import math
from utils import *

class Num:
    def __init__(self, at=0, txt=""):
        self.at = at
        self.txt = txt
        self.n = 0
        self.mu = 0
        self.m2 = 0
        self.lo = float('inf')
        self.hi = float('-inf')
        self.w = -1 if '-' in self.txt else 1 


    def add(self, n):
        if n != 0:
            self.n = self.n + 1
            d = n - self.mu
            self.mu = self.mu + (d / self.n)
            self.m2 = self.m2 + (d * (n - self.mu))
            self.lo = min(n, self.lo)
            self.hi = max(n, self.hi)

    def mid(self):
        return self.mu # n; return mean

    #n; return standard deviation using Welford's algorithm 
    def div(self): 
        if self.m2 < 0 or self.n < 2:
            return 0
        else:
            return pow((self.m2/(self.n-1)),0.5)
        
    def rnd(self,x,n):
        if x=='?':
            return x
        return rnd(x,n)
    
    def norm(self, n= None):
        if(n == '?'):
            return n 
        else :
           return (float(n)-self.lo)/(self.hi -self.lo + 1e-32)

    def dist(self, n1 = None, n2 = None):
        if (type(n1) == str or n1 == '?') and (type(n2) == str or n2 == '?'):
            return 1
      
        n1,n2 = self.norm(n1), self.norm(n2)
        if n1 == '?':
            if n2 < 0.5:
                n1 = 1
            else:
                n1 = 0
        if n2 == '?':
            if n1 < 0.5:
                n2 = 1
            else:
                n2 = 0
        return abs(n1-n2)