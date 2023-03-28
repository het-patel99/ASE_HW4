import sys
sys.path.append("./src")

from num import Num
from sym import Sym
from utils import utils
from data import *
from main import *
from pathlib import Path
import os 



def test_syms():
    value = ['a', 'a', 'a', 'a', 'b', 'b', 'c']
    sym1 = Sym()
    for x in value:
        sym1.add(x)
    print("test_syms: PASS\n")
    return "a"==sym1.mid() and 1.379 == utils.rnd(sym1.div(),3)

def test_the():
    # oo(options)
    print(options)
    return True


def test_copy():  # copy
    t1 = {'a': 1, 'b': {'c': 2, 'd': [3]}}
    t2 = utils.copy(t1)
    t2['b']['d'][0] = 10000
    print('b4', t1, '\nafter', t2)

def test_nums():
    val = Num()
    lst = [1,1,1,1,2,2,3]
    for a in lst:
        val.add(a)
    print("test_nums: PASS\n")
    return 11/7 == val.mid() and 0.787 == utils.rnd(val.div(),3)

def test_repCols():
    root = str(Path(__file__).parent.parent.parent)
    csv_path = os.path.join(root, "ASE_HW4/etc/data/repgrid2.csv")
    t = utils.repCols(utils.dofile(csv_path)['cols'])
    for col in t.cols.all:
        utils.oo(col)
    for row in t.rows:
        utils.oo(row)


def test_repRows():
    root = str(Path(__file__).parent.parent.parent)
    csv_path = os.path.join(root, "ASE_HW4/etc/data/repgrid2.csv")
    t = utils.dofile(csv_path)
    rows = utils.repRows(t, utils.transpose(t['cols']))
    for col in rows.cols.all:
        utils.oo(col)
    for row in rows.rows:
        utils.oo(row)


def test_synonyms():
    root = str(Path(__file__).parent.parent.parent)
    csv_path = os.path.join(root, "ASE_HW4/etc/data/repgrid2.csv")
    utils.show(node=utils.repCols(utils.dofile(csv_path)['cols']).cluster())


def test_prototypes():
    root = str(Path(__file__).parent.parent.parent)
    csv_path = os.path.join(root, "ASE_HW4/etc/data/repgrid2.csv")
    t = utils.dofile(csv_path)
    rows = utils.repRows(t, utils.transpose(t['cols']))
    utils.show(rows.cluster())


def test_position():
    root = str(Path(__file__).parent.parent.parent)
    csv_path = os.path.join(root, "ASE_HW4/etc/data/repgrid2.csv")
    t = utils.dofile(csv_path)
    rows = utils.repRows(t, utils.transpose(t['cols']))
    rows.cluster()
    utils.repPlace(rows)


def test_every():
    root = str(Path(__file__).parent.parent.parent)
    csv_path = os.path.join(root, "ASE_HW4/etc/data/repgrid2.csv")
    utils.repgrid(csv_path)

