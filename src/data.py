
from typing import List
import math
import os
import csv
import random
import cols
import row
import sys
import data
import collections

script_sir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_sir)
os.sys.path.insert(0,parent_dir)
from tests.tests import *

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

def get_csv_contents(filepath: str) -> list[str]:

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
    def add(self, t: list[str]):

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

    def around(self, rows):
        return map(sorted(map(rows)))

    def half(self, rows, cols, above):
        rows = rows or self.rows
        some = many(rows,Sample)
        A = any(some)
        B = self.around(A,some)[(Far*len(rows)//1)]
        C = self.dist(A,B)
        left = {}
        right = {}
        for n,tmp in enumerate(collections.OrderedDict(sorted(rows.items()))):
            if n<=len(rows)//2:
                left.add(tmp.row)
                mid = tmp.row
            else:
                right.add(tmp.row)
        return left, right, A,B,mid,C

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

def fmt(sControl: str, *args): #control string (format string)
    for string in args:
        print(string.format(sControl))

# show function needs to be added
def show(node, what, cols, nPlaces):
    return ""

def rnd(n, nPlaces = 3):
    mult = math.pow(10, nPlaces)
    return math.floor(n*mult + 0.5) / mult

def o(t: object):
    #todo()
    return ""

def rand(lo,hi):
    lo = lo or 0
    hi = hi or 1
    seed = (16807 * seed) % 2147483647
    return lo + (hi-lo) * seed / 2147483647

def rint(lo,hi):
    return math.floor(0.5 + rand(lo,hi))

def any(t):
    return t[rint(len(t))]

def many(t,n):
    u = {}
    for i in range(1,n):
        u[1+len(u)] = any(t)
    return u


# ------------------- MAIN PROGRAM FLOW -------------------

## run_test counts the number of arguments that have been passed and failed and it also,
## it displays the names tests passed and failed.
def run_tests():
    print("Executing tests...\n")

    passCount = 0
    failCount = 0
    test_suite = [test_csv, test_show_dump, test_syms, test_nums, test_data, test_show_dump] 

    for test in test_suite:
        try:
            test()
            passCount = passCount + 1
        except AssertionError as e:
            failCount = failCount + 1
        

    print("\nPassing: " + str(passCount) + "\nFailing: " + str(failCount))
    
# api-side function to get the current input csv filepath
def get_file() -> str:
    return file

# uses the value of the dump parameter and passed exception to determine what message to display to the user
def get_crashing_behavior_message(e: Exception):
    crash_message = str(e)
    if(dump):
        crash_message = crash_message + '\n'
        stack = traceback.extract_stack().format()
        for item in stack:
            crash_message = crash_message + item

    return crash_message

# api-side function to get the current seed value
def get_seed() -> int:
    return seed

# api-side function to get the current dump boolean status
def should_dump() -> bool:
    return dump



## find_arg_values gets the value of a command line argument
# first it gets set of args
# second it get option A (-h or -d or -s or -f )
# third is get option B (--help or --dump or --seed or --file)
def find_arg_value(args: list[str], optionA: str, optionB: str) -> str:
    index = args.index(optionA) if optionA in args else args.index(optionB)
    if (index + 1) < len(args):
        return args[index + 1]
    return None

help_string = """cluster.lua : an example csv reader script
(c)2022, Tim Menzies <timm@ieee.org>, BSD-2 

USAGE: cluster.lua  [OPTIONS] [-g ACTION]

OPTIONS:
  -d  --dump    on crash, dump stack   = false
  -f  --file    name of file           = ../etc/data/auto93.csv
  -F  --Far     distance to "faraway"  = .95
  -g  --go      start-up action        = data
  -h  --help    show help              = false
  -m  --min     stop clusters at N^min = .5
  -p  --p       distance coefficient   = 2
  -s  --seed    random number seed     = 937162211
  -S  --Sample  sampling data size     = 512

]]"""

if __name__ == "__main__":
    args = sys.argv
    try:
        if '-h' in args or '--help' in args:
            print(help_string)

        if '-d' in args or '--dump' in args:
            dump = True

        if '-f' in args or '--file' in args:
            file = data.data(find_arg_value(args, '-f', '--file'))

        if '-s' in args or '--seed' in args:
            seed_value = find_arg_value(args, '-s', '--seed')
            if seed_value is not None:
                try:
                    seed = int(seed_value)
                except ValueError:
                    raise ValueError("Seed value must be an integer!")
            else:
                print("USAGE: Provide an integer value following an -s or --seed argument to set the seed value.\n Example: (-s 3030, --seed 3030)")

        # NOTE: the seed will be set in main, the rest of the application need not set it
        random_instance.seed(seed)
        if '-g' in args or '--go' in args:
            run_tests()
    except Exception as e:
        print(get_crashing_behavior_message(e))
