import sys
sys.path.append("./src")
import math
import re 
import json
import io

egs = dict()
options = dict()

def fmt(sControl: str, *args): #control string (format string)
    for string in args:
        print(string.format(sControl))

# show function needs to be added
def show(node, what= None, cols= None, nPlaces= None, lvl = None):
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

def copy(t):
    return copy.deepcopy(t)

def many(t,n):
    u = {}
    for i in range(1,n):
        u[1+len(u)] = any(t)
    return u

def cosine(a, b, c):
    if(c == 0):
        den =1
    else:
        den = 2*c
    x1 = ((a**2 + c**2 - b**2)/den)
    x2 = max(0,min(x1,1))
    y = abs((a**2 - x2**2)**0.5)

    return x2,y

def repCols(cols, DATA):
    cols = copy(cols)
    for c in cols:
        c[len(c) - 1] = c[0] + ":" + c[len(c) - 1]
        for j in range(1, len(c)):
            c[j-1] = c[j]
        c.pop()
    c1=list()
    for i in range(len(cols[1])-1):
        c1 = ['Num' + str(i+1)]
    c1.append('thingX')
    cols.insert(0, c1)
    return DATA(cols)

def repRows(t, rows, DATA):
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
            from pprint import pprint
        
    for i in DATA(rows).rows: pprint(vars(i))
    return  DATA(rows)

def dofile(f):
    with open(f,'r', encoding='utf-8') as file:
        text = re.findall(r'(return\s+[^.]+)',  f.read())[0]
        replacements = {'return ' : '', '{' : '[', '}' : ']','=':':', '[\n':'{\n', '\n]':'\n}', '_':'"_"', '\'':'"'}
        for a,b in replacements.items():
            text = text.replace(a, b)

        text = re.sub("(\w+):",r'"\1":', text)
        return json.loads(text)

def repgrid(file, DATA):
    t = dofile(file)
    rows = repRows(t, transpose(t['cols']), DATA)
    cols = repCols(t['cols'], DATA)
    show(rows.cluster(),"mid",rows.cols.all,1)
    show(cols.cluster(),"mid",cols.cols.all,1)
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
    result = {}
    for v in t:
        k = t.index(v)
        v, k = fun(k,v)
        result[k or len(result)] = v
    return result

def coerce(s):
    if s == 'true':
        return True
    elif s == 'false':
        return False
    elif s.isdigit():
        return int(s)
    elif '.' in s and s.replace('.','').isdigit():
        return float(s)
    else:
        return s
    
def oo(t):
    temp = t.__dict__
    temp['a'] = t.__class__.__name__
    temp['id'] = id(t)
    print(dict(sorted(temp.items())))


def eg(key, str, fun):
    egs[key] = fun
    global help 
    help = help + ' -g ' + key + '\t' + str + '\n'

def csv(filename, fun):
    f = io.open(filename)
    while True:
        s = f.readline()
        if s:
            t = []
            for s1 in re.findall("([^,]+)" ,s):
                t.append(coerce(s1))
            fun(t)
        else:
            return f.close()