import math, json
import re
import copy
import sys
from pathlib import Path
import data

seed = 937162211

def show(node, what=None,cols=None,nPlaces=None,lvl=0):
    if node:
        lvl = lvl or 0
        print("|.. " * lvl, end="")
        if ("left" not in node):
            print(last(last(node["data"].rows).cells))
        else:
            print(str(int(100 * node["C"])))
        show(node.get("left", None), what,cols, nPlaces, lvl+1)
        show(node.get("right", None), what,cols,nPlaces, lvl+1)

# Numeric Functions

def rint(lo, hi):
    return math.floor(0.5 + rand(lo,hi))

def any(t):
    return t[rint(0, len(t))]

def many(t, n, u):
    u = []
    for i in range(n):
        u.append(any(t))
    return u

def rand(lo, hi):
    global seed
    lo, hi = lo or 0, hi or 1
    seed = (16807 * seed) % 2147483647
    return lo + (hi-lo) * seed / 2147483647

def cosine(a,b,c):
    x1 = (a**2 + c**2 - b**2) / (2*c)
    x2 = max(0, min(1, x1))
    y = (a**2 - x2**2)**.5
    return x2, y

# String Functions

def coerce(s):
    try:
        return int(s)
    except:
        try:
            return float(s)
        except:
            pass

    if s == "true" or s == "True":
        return True
    elif s == "false" or s == "False":
        return False
    else:
        return s

def rnd(n, nPlaces = 3):
    mult = 10**(nPlaces or 3)
    return math.floor(n * mult + 0.5) / mult

def map(t, fun):
    u = {}
    for k,v in enumerate(t):
        v,k = fun(v)
        print(v,k)
        u[k or (1+len(u))] = v
    return u   

def kap(t, fun):
    u = {}
    for k, v in enumerate(t):
        v, k = fun(k, v)
        u[k or (1+len(u))] = v

    return u 

def oo(t):
    td = t.__dict__
    td['a'] = t.__class__.__name__
    td['id'] = id(t)
    print(dict(sorted(td.items())))

# Main

def settings(s):
    t={}
    res = re.findall("\n[\s]+[-][\S]+[\s]+[-][-]([\S]+)[^\n]+= ([\S]+)", s)
    for k,v in res:
            t[k] = coerce(v)
    return t

def transpose(t):
    u = []
    for i in range(0, len(t[0])):
        row = []
        for j in range(len(t)):
            row.append(t[j][i])
        u.append(row)
    return u

def repCols(cols):
    cols = copy.deepcopy(cols)
    for col in cols:
        col[-1] = str(col[0]) + ":" + str(col[-1])
        for j in range(1,len(col)):
            col[j-1] = col[j] 
        col.pop()
    cols.insert(0,["Num" + str(i) for i in range(len(cols[0]))])
    cols[0][-1] = "thingX"
    return data.Data(cols)

def repRows(t, rows):
    rows = copy.deepcopy(rows)
    for j, s in enumerate(rows[-1]):
        rows[0][j] = str(rows[0][j]) + ":" + str(s)
    rows.pop()
    for n, row in enumerate(rows):
        if n == 0:
            row.append("thingX")
        else:
            u = t["rows"][len(t["rows"]) - n]
            row.append(u[-1])
    return data.Data(rows)

def repPlace(data):
    n,g = 20,[]
    for i in range(n+1):
        g.append([])
        for j in range(n+1):
            g[i].append(" ")
    maxy=0
    print("")
    for r,row in enumerate(data.rows):
        c = chr(r+65)
        print(c, last(row.cells))
        x, y= int(row.x*n), int(row.y*n)
        maxy = max(maxy,y)
        g[y][x] = c
    print("")
    for y in range(maxy):
        print("{" + "".join(g[y]) + "}")

def last(t):
    return t[-1]

def dofile(filepath):
    filepath = (Path(__file__).parent / filepath).resolve()
    file = open(filepath,"r",encoding = "utf-8")
    temp = (
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
    f = json.loads(re.sub(r"(\w+):", r'"\1":', temp)[:-2] + "}")
    return f

def repgrid(sFile):
    t = dofile(sFile) 
    rows = repRows(t, transpose(t["cols"])) 
    cols = repCols(t["cols"])
    show(rows.cluster())
    show(cols.cluster())
    repPlace(rows)


def csv(sFilename, fun):
    filePath = Path(sFilename)
    filePath = filePath.absolute()
    filePath = filePath.resolve()
    print(filePath)
    f = open(filePath,"r")
    readLines = f.readlines()
    f.close()
    for line in readLines:
        t = []
        for s1 in re.findall("([^,]+)", line):
            t.append(coerce(s1))
        fun(t) 

def cli(options):
    for k, v in options.items():
        v = str(v)
        for n, x in enumerate(sys.argv):
            if x== "-" + k[0] or x == "--" + k:
                v = (sys.argv[n + 1] if n + 1 < len(
                    sys.argv) else False) or v == "False" and "true" or v == "True" and "false"
            options[k] = coerce(v)
    return options