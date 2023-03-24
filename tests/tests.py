import sys
sys.path.append("./src")

from num import Num
from sym import Sym
from utils import *
from data import *
from main import *

def test_syms():
    value = ['a', 'a', 'a', 'a', 'b', 'b', 'c']
    sym1 = Sym()
    for x in value:
        sym1.add(x)
    print("test_syms: PASS\n")
    return "a"==sym1.mid() and 1.379 == rnd(sym1.div(),3)

def test_the():
    # oo(options)
    print(options)
    return True


def test_copy():  # copy
    t1 = {'a': 1, 'b': {'c': 2, 'd': [3]}}
    t2 = copy(t1)
    t2['b']['d'][0] = 10000
    print('b4', t1, '\nafter', t2)

def test_nums():
    val = Num()
    lst = [1,1,1,1,2,2,3]
    for a in lst:
        val.add(a)
    print("test_nums: PASS\n")
    return 11/7 == val.mid() and 0.787 == rnd(val.div(),3)

def test_repCols():
    t = repCols(dofile(options['file'])['cols'], Data)
    for col in t.cols.all:
        oo(col)
    for row in t.rows:
        oo(row)


def test_repRows():
    csv_path = "../etc/data/auto93.csv"
    data = Data(csv_path)
    t = dofile(data)
    rows = repRows(t, transpose(t['cols']), Data)
    for col in rows.cols.all:
        oo(col)
    for row in rows.rows:
        oo(row)


def test_synonyms():
    data = dofile(options['file'])
    show(repCols(dofile(options['file'])['cols'], Data).cluster())


def test_prototypes():
    t = dofile(options['file'])
    rows = repRows(t, transpose(t['cols']), Data)
    show(rows.cluster(), "mid", rows.cols.all, 1)


def test_position():
    
    t = dofile(options['file'])
    rows = repRows(t, transpose(t['cols']), Data)
    rows.cluster()
    repPlace(rows)


def test_every():
    repgrid(options['file'], Data)
