import sys
sys.path.append("./src")
import math
import re 
import json
import io
import copy as copyy
from data import *
from pprint import pprint
egs = dict()
options = dict()

def fmt(sControl: str, *args): #control string (format string)
    for string in args:
        print(string.format(sControl))

# show function needs to be added
def show(node, what= None, cols= None, nPlaces= None, lvl = 0):
    if node:
        lvl = lvl or 0
        print("|.." * lvl, str(len(node["data"].rows)), " ")
        if not node.get("left", None) or lvl == 0:
            print(o(node["data"].stats("mid", node["data"].cols.y, nPlaces)))
        else:
            print("")
        show(node.get("left", None), what, cols, nPlaces, lvl + 1)
        show(node.get("right", None), what, cols, nPlaces, lvl + 1)

def rnd(n, nPlaces = 3):
    mult = math.pow(10, nPlaces)
    return math.floor(n*mult + 0.5) / mult

def o(t, isKeys=None):
    return str(t)

def rand(lo,hi):
    lo = lo or 0
    hi = hi or 1
    seed = (16807 * seed) % 2147483647
    return lo + (hi-lo) * seed / 2147483647

def rint(lo,hi):
    return math.floor(0.5 + rand(lo,hi))

def any(t):
    return t[rint(len(t))]

def copy(t):
    return copyy.deepcopy(t)

def many(t,n):
    u = {}
    for i in range(1,n):
        u[1+len(u)] = any(t)
    return u

def cosine(a, b, c):
    x1 = (a**2 + c**2 - b**2) / (2*c)
    x2 = max(0, min(1, x1))
    y  = (a**2 - x2**2)**.5
    return x2, y

def sort(t):
    #Doubt
    return t

# function sort(t, fun) --> t; return `t`,  sorted by `fun` (default= `<`)
#   table.sort(t,fun); return t end

def lt(x):
    def fun(a, b):
        return a[x] < b[x]

def keys(t):
    #Doubt
    pass

def push(t, x):
    t.append(x)

def repCols(cols):
    cols = copy(cols)
    # for i,col in enumerate(cols):
    #     col[len(col) - 1] = col[0] + ":" + col[len(col) - 1]
    #     for j in range(1, len(col)):
    #         col[j - 1] = col[j]
    #     col.pop()
    # s=[]
    # for i in range(len(cols[0])):
    #     s.append("Num"+str(i))
    # cols.insert(0, s)
    # cols[0][len(cols[0]) - 1] = "thingX"
    # data = Data(cols)
    # return data

    
    for col in cols:
        col[-1] = str(col[0]) + ":" + str(col[-1])
        for j in range(1, len(col)):
            col[j-1] = col[j]
        col.pop()
    cols.insert(0, ["Num" + str(i) for i in range(1, len(cols[0]) + 1)])
    cols[0][-1] = "thingX"
    return Data(cols)


def push(t, x):
    """
    push `x` to end of list; return `x` 
    """
    t.append(x)
    return x

def repRows(t, rows):
    rows = copy(rows)
    for j, s in enumerate(rows[-1]):
        rows[0][j] = str(rows[0][j]) + ":" + str(s)
    rows.pop()
    for n, row in enumerate(rows):
        if (n==0):
            row.append('thingX')
        else:
            u=t["rows"][len(t["rows"])-n]
            row.append(u[len(u) - 1])
    return  Data(rows)

def dofile(file):
    file = open(file, "r", encoding="utf-8")
    text = (
        re.findall(r"(?<=return )[^.]*", file.read())[0]
        .replace("{", "[")
        .replace("}", "]")
        .replace("=", ":")
        .replace("[\n", "{\n")
        .replace(" ]", " }")
        .replace("'", '"')
        .replace("_", '"_"')
    )
    file.close()
    file_json = json.loads(re.sub(r"(\w+):", r'"\1":', text)[:-2] + "}")
    return file_json

def repgrid(file):
    t = dofile(file)
    rows = repRows(t, transpose(t['cols']))
    cols = repCols(t['cols'])
    show(rows.cluster())
    show(cols.cluster())
    repPlace(rows)

def repPlace(data):
    n,g = 20,{}
    for i in range(1, n+1):
        g[i]={}
        for j in range(1, n+1):
            g[i][j]=" "
    maxy = 0
    print("")
    for r,row in enumerate(data.rows):
        c = chr(97+r).upper()
        print(c, row.cells[-1])
        
        if( math.isnan(row.x) or math.isnan(row.y)):
            continue
        x=int(row.x*n/1)
        y=int(row.y*n/1)
        maxy = int(max(maxy, y+1))
        g[y+1][x+1] = c
    print("")
    for y in range(1,maxy+1):
        print(" ".join(g[y].values()))

def transpose(t):
    result=[]
    for i in range(len(t[1])):
        result.append([])
        for j in range(len(t)):
            result[i].append(t[j][i])

    return result

def kap(t, fun):
    u = {}
    for k,v in enumerate(t):
        v,k = fun(k,v)
        u[k or (1+len(u))] = v
    
    return u

def coerce(s): #Doubt
    if s == "true":
        return True
    elif s == "false":
        return False
    elif re.search(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?$", s) is not None:
        return float(s)
    else:
        return s
    
def oo(t):
    print(o(t))
    return t


    
def settings(s, t):
    return dict(re.findall(r"\n[\s]+[-][\S]+[\s]+[-][-]([\S]+)[^\n]+= ([\S]+)", s))