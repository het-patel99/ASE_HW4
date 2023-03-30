import math
import collections

class Sym:
    def __init__(self, at = 0, txt = ""):
        self.at = at
        self.txt = txt
        self.n   = 0
        self.has = collections.defaultdict(int)
        self.most = 0
        self.mode = None 

    def add(self, x):
        if x != '?':
            self.n += 1 
            if x in self.has:
                self.has[x] += 1
            else:
                self.has[x] = 1
                
            if self.has[x] > self.most:
                self.most, self.mode = self.has[x], x

    def mid(self):
        return self.mode
    
    def div(self):
        def fun(p):
            return p * math.log(p,2)
        e = 0

        for k, v in self.has.items():
            e = e + fun(v/self.n)
        return -e

    def rnd(self, i, x, n=None):
        return x

    def dist(self, s1, s2):
        if s1 == "?" and s2 == "?":
            return 1
        if s1 == s2:
            return 0
        else:
            return 1
