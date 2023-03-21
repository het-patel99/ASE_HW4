import sys
sys.path.append("./src")
from typing import List
import math
import os
import csv
import random
import cols
import row

import data
import collections
import copy as copy
from utils import *

script_sir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_sir)
os.sys.path.insert(0,parent_dir)

# set to their default values
random_instance = random.Random()
file = '../etc/data/auto93.csv'
seed = 937162211
dump = False
min = 0.5
p = 2
Sample = 512
help = False
Far = 0.95

def get_csv_contents(filepath: str):

    #try to catch relative paths
    if not os.path.isfile(filepath):
        filepath = os.path.join(script_sir, filepath)

    filepath = os.path.abspath(filepath)

    csv_list = []
    with open(filepath, 'r') as csv_file:
        csv_list = list(csv.reader(csv_file, delimiter=','))

    return csv_list


class Data():

    ## constructor created for data.py class
    def __init__(self, src):
        self.rows = []
        self.cols =  None

        ## if the src is string then
        ## it reads the file and then calls the add method to add each row
        src_type = type(src)
        if src_type == str :
            csv_list = get_csv_contents(src)
            for row in csv_list:
                trimmed_row = []
                for item in row:
                    trimmed_row.append(item.strip())
                self.add(trimmed_row)

        elif src_type == List[str]: # else we were passed the columns as a string
            self.add(src)
        # else:
        #     raise Exception("Unsupported type in Data constructor")

    ## add method adds the row read from csv file
    ## It also checks if the col names is being read has already being read or not
    ## if yes then it uses old rows
    ## else add the col rows.
    def add(self, t):

        if(self.cols is None):
            self.cols = cols.Cols(t)
        else:
            new_row = row.Rows(t)
            self.rows.append(new_row)
            self.cols.add(new_row)

    def clone(self):
        new_data = Data(self.cols.names)
        for row in self.rows:
            new_data.add(row)
        return new_data

    def better(self, row1, row2):
        s1,s2,ys = 0,0,self.cols.y
        for _,col in enumerate(ys):
            x = col.norm(row1.cells[col.at])
            y = col.norm[row2.cells[col.at]]
            s1 = s1 - math.exp(col.w*(x-y)/len(ys))
            s2 = s2 - math.exp(col.w*(y-x)/len(ys))
        return s1/len(ys) < s2/len(ys)

    def dist(self, row1, row2):
        n, d = 0,0
        for col in enumerate(cols or self.cols.x):
            n = n + 1
            d = d + col.dist(row1.cells[col.at], row2.cells[col.at]) ^ p
        return (d/n)^(1/p)

    def around(self, row1, rows= None, cols=None ):
        if rows is None: rows = self.rows

        def fun(row2):
            return {"row": row2, "dist": self.dist(row1, row2, cols)}

        mapped = map(fun, rows)
        return sorted(mapped, key=lambda x: x["dist"])

    def stats(self, what, cols, nPlaces):
        def fun(_,cols):
            if what == 'mid':
                val = cols.mid()
            else:
                val = cols.div()
            return cols.rnd(val, nPlaces), cols.txt

        return kap(cols or self.cols.y, fun)



    def furthest(self, row1, rows, cols,t):
        t = self.around(row1,rows,cols)
        furthest = t[len(t)-1]
        return furthest

    def half(self, rows = None , cols = None, above= None):

        rows = rows or self.rows
        some = many(rows,Sample)
        A = any(some)
        B = self.around(A,some)[(Far*len(rows)//1)]
        c = self.dist(A,B)
        left = {}
        right = {}

        def dist(row1, row2):
            return self.dist(row1,row2,cols)
        
        def project(row):
            x,y = cosine(dist(row,A), dist(row,B), c)
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

    def cluster(self, rows, min, cols, above):
        rows = rows or self.rows
        min = min or len(rows)^min
        cols = cols or self.cols.x
        node = data = self.clone()
        if len(rows)>2*min:
            left, right, node.A, node.B, node.mid = self.half(rows,cols,above)
            node.left = self.cluster(left,min,cols,node.A)
            node.right = self.cluster(right,min,cols,node.B)
        return node


    def sway(self,rows,min,cols,above):
        rows = rows or self.rows
        min = min or len(rows)^min
        cols = cols or self.cols.x
        node = data = self.clone()
        if len(rows)>2*min:
            left, right, node.A, node.B, node.mid = self.half(rows,cols,above)
            if self.better(node.B,node.A):
                left,right,node.A,node.B = right,left,node.B,node.A
            else:
                node.left = self.sway(left,min,cols,node.A)
        return node


        
