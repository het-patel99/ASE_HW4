from sym import Sym
from num import Num
from data import *
import utils
import inputs

data = Data(inputs.the["file"])

def test_sym():
    value = ['a', 'a', 'a', 'a', 'b', 'b', 'c']
    sym1 = Sym()
    for x in value:
        sym1.add(x)
    print("sym1 information: ",sym1)
    print("test_sym : passed")
    return "a"==sym1.mid() and 1.379 == utils.rnd(sym1.div())

def test_nums():
    val = Num()
    lst = [1,1,1,1,2,2,3]
    for a in lst:
        val.add(a)
    assert 11/7 == val.mid() and 0.787 == utils.rnd(val.div())
    print("Val information: ", val)
    return 11/7 == val.mid() and 0.787 == utils.rnd(val.div())

def test_the():
    print(str(inputs.the))

def test_repCols():
    t = utils.repCols(utils.dofile(inputs.the["file"])['cols'])
    for col in t.cols.all:
        utils.oo(col)
    for row in t.rows:
        utils.oo(row)
    print(t)

def test_repRows():
    t = utils.dofile(inputs.the["file"])
    rows = utils.repRows(t, utils.transpose(t['cols']))
    for col in rows.cols.all:
        utils.oo(col)
    for row in rows.rows:
        utils.oo(row)
    print(t)

def test_synonyms():
    print(utils.show(node=utils.repCols(utils.dofile(inputs.the["file"])['cols']).cluster()))

def test_prototypes():
    t = utils.dofile(inputs.the["file"])
    rows = utils.repRows(t, utils.transpose(t['cols']))
    print(utils.show(rows.cluster()))

def test_position():
    t = utils.dofile(inputs.the["file"])
    rows = utils.repRows(t, utils.transpose(t['cols']))
    rows.cluster()
    print(utils.repPlace(rows))

def test_every():
    print(utils.repgrid(inputs.the["file"]))

