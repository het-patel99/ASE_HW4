import sys
sys.path.append("./src")
from typing import List
import math,csv
import cols
import row
import copy as copy
import utils 
from main import the

def csv_content(src):
    res = []
    with open(src, mode='r') as file:
        csvFile = csv.reader(file)
        for row in csvFile:
            res.append(row)
    return res
class Data():
    

    ## constructor created for data.py class
    def __init__(self, src):
        self.rows = []
        self.cols = None
        self.count = 0

        if type(src) == str:
            csv_list = csv_content(src)
            for line,row in enumerate(csv_list):
                row_cont = []
                for oth_line,val in enumerate(row):
                    row_cont.append(val.strip())
                    self.count+=1
                self.add(row_cont)

        else:
            for l in src:
                self.add(l)

    # def __init__(self, src):
    #     self.rows = []
    #     self.cols = None

    #     if type(src) == str:
    #         csv(src, self.add)
    #     else:
    #         for t in src:
    #             self.add(t)
    ## add method adds the row read from csv file
    ## It also checks if the col names is being read has already being read or not
    ## if yes then it uses old rows
    ## else add the col rows.
    def add(self, t):
        if (self.cols):
            
            nrow = row.Rows(t)
            self.rows.append(nrow.cells)
            self.cols.add(nrow)
        else:
            self.cols = cols.Cols(t)

    def clone(self,init):
        new_data = Data(self.cols.names)
        for row in init:
            new_data.add(row)
        return new_data

    def better(self, row1, row2):
        s1,s2,ys = 0,0,self.cols.y
        for _,col in enumerate(ys):
            x = col.norm(row1[col.at])
            y = col.norm[row2[col.at]]
            s1 = s1 - math.exp(col.w*(x-y)/len(ys))
            s2 = s2 - math.exp(col.w*(y-x)/len(ys))
        return s1/len(ys) < s2/len(ys)

    def dist(self, row1, row2, cols=None):
        n, d = 0, 0
        for _, col in enumerate(cols or self.cols.x):
            n = n + 1
            val = col.dist(row1[col.at], row2[col.at])
            d = d + val ** 2
        return (d / n) ** (1 / 2)

    def around(self, row1, rows= None, cols=None ):
        if rows is None: rows = self.rows

        def fun(row2):
            return {"row": row2, "dist": self.dist(row1, row2, cols)}

        mapped = map(fun, rows)
        return sorted(mapped, key=lambda x: x["dist"])

    def stats(self,what,cols,nPlaces):
        def fun(k,col):
            f = getattr(col,what)
            return col.rnd(f(),nPlaces), col.txt
        
        return utils.kap(cols,fun)

    def furthest(self, row1, rows=None, cols=None):
        t = self.around(row1,rows,cols)
        furthest = t[len(t)-1]
        return furthest

    def half(self, rows = None , cols = None, above= None):

        rows = rows or self.rows
        some = utils.many(rows,the.Sample)
        A = utils.any(some)
        B = self.around(A,some)[(the.Far*len(rows)//1)]
        # if rows is None: rows = self.rows
        # A = above or any(rows)
        # B = self.furthest(A, rows)['row']
        c = self.dist(A,B)
        left = {}
        right = {}

        def dist(row1, row2):
            return self.dist(row1,row2,cols)
        
        def project(row):
            x,y = utils.cosine(dist(row,A), dist(row,B), c)
            try:
                row.x = row.x
                row.y = row.y
            except:
                row.x = x
                row.y = y
            return (row, x, y)

        result = []
        for row in rows:
            result.append(project(row))
        result = sorted(result, key = lambda x:x[1])

        for n,tmp in enumerate(result):
            if n<=len(rows)//2:
                left.add(tmp.row)
                mid = tmp.row
            else:
                right.add(tmp.row)
        return left, right, A,B,mid,c

    def cluster(self, rows= None, min_size= None, cols= None, above= None):
        rows = rows or self.rows
        min_value = min_size or (len(rows))** 0.5
        if not cols:
            cols = self.cols.x
        node = { 'data' : self.clone(rows) }
        if len(rows)>2*min_value:
            left, right, node.A, node.B, node.mid = self.half(rows,cols,above)
            node.left = self.cluster(left,min,cols,node.A)
            node.right = self.cluster(right,min,cols,node.B)
        return node


    def sway(self, rows=None, min=None, cols=None, above=None):
        rows = rows or self.rows
        min = min or len(rows) ** 0.5
        cols = cols or self.cols.x
        node = {"data": self.clone(rows)}

        if len(rows) > 2 * min:
            left, right, node["A"], node["B"], node["min"], _ = self.half(rows, cols, above)
            if self.better(node["B"], node["A"]):
                left, right, node["A"], node["B"] = right, left, node["B"], node["A"]
            node["left"] = self.sway(left, min, cols, node["A"])

        return node


        
