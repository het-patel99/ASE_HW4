import random
import math
import os
import sys
import traceback
import collections


sys.path.append(os.path.abspath('../src'))

from src.cols import Cols
from src.num import Num
from src.sym import Sym
from src.data import should_dump, get_crashing_behavior_message, get_file, get_csv_contents, Data, show, fmt, rnd, o, rand, rint, any, many

def round_to(n, nPlaces = 3):
    mult = math.pow(10, nPlaces)
    return math.floor(n*mult + 0.5) / mult

def print_res(function_name: str, res: bool):
    print("\n" + function_name + (": PASS" if res else ": FAIL"))


def test_show_dump():
    test_exception = Exception("This is a test exception")
    try:
        raise test_exception
    except Exception as e:
        expected_output = str(test_exception)
        output = get_crashing_behavior_message(test_exception)

        if should_dump():
            res = len(output) > len(expected_output) and expected_output in output
            print_res("test_show_dump", res)
            assert res
        else:
            res = expected_output == output
            print_res("test_show_dump", res)
            assert res

def test_syms():
    sym = Sym()
    values = ['a', 'a', 'a', 'a', 'b', 'b', 'c']
    for value in values:
        sym.add(value)

    res = ('a' == sym.mid()) and (1.379 == round_to(sym.div(), 3))
    print_res("test_syms", res)
    assert res

def test_nums():
    num = Num()
    values = [1, 1, 1, 1, 2, 2, 3]
    for value in values:
        num.add(value)
    
    res = ((11/ 7) == num.mid()) and (0.787 == round_to(num.div(), 3))
    print_res("test_nums", res)
    assert res


def test_data():
    test_data = Data(get_file())
    # i know this is horrible
    excepted_output = '\ny\tmid\t{ :Lbs- 2970.42 :Acc+ 15.57 :Mpg+ 23.84}\n \tdiv\t{ :Lbs- 846.84 :Acc+ 2.76 :Mpg+ 8.34}\nx\tmid\t{ :Clndrs 5.45 :Volume 193.43 :Model 76.01 :origin 1}\n \tdiv\t{ :Clndrs 1.7 :Volume 104.27 :Model 3.7 :origin 1.3273558482394003}'


    y_mid_report = '{'
    y_div_report = '{'
    for y in test_data.cols.y:
        y_mid_report = y_mid_report + ' :' + y.txt + ' ' + str(y.rnd(y.mid(), 2))
        y_div_report = y_div_report + ' :' + y.txt + ' ' + str(y.rnd(y.div(), 2))
    y_mid_report = y_mid_report + '}'
    y_div_report = y_div_report + '}'

    x_mid_report = '{'
    x_div_report = '{'
    for x in test_data.cols.x:
        x_mid_report = x_mid_report + ' :' + x.txt + ' ' + str(x.rnd(x.mid(), 2))
        x_div_report = x_div_report + ' :' + x.txt + ' ' + str(x.rnd(x.div(), 2))
    x_mid_report = x_mid_report + '}'
    x_div_report = x_div_report + '}'

    res_string = '\ny\tmid\t' + y_mid_report + '\n \tdiv\t' + y_div_report + '\nx\tmid\t' + x_mid_report + '\n \tdiv\t' + x_div_report
    res = res_string == excepted_output
    print_res("\ntest_data", res)
    print(res_string)
    assert res

def test_clone():
    data1= Data(get_file())
    data2= data1.clone()
    assert len(data1.rows) == len(data2.rows) and data1.cols.y[1].w == data2.cols.y[1].w and data1.cols.x[1].at == data2.cols.x[1].at and len(data1.cols.x) == len(data2.cols.x)
    

def test_around():
    data= Data(get_file())
    print(0,0,o(data.rows[1].cells))
    for n,t in enumerate(collections.OrderedDict(map(sorted(Data.around(data.rows[1])).items()))):
        if n % 50 == 0:
            print(n,rnd(t.dist,2), o(t.rows.cells))
    assert True

def test_half():
    data = Data(get_file())
    left,right,A,B,mid,c = data.half([],None,None) # arguments in half ??
    print(len(left), len(right), len(data.rows))
    print(o(A.cells()))
    print(o(B.cells()))
    print(o(mid.cells())) 

    assert True

def test_cluster():
    data = Data(get_file())
    show(data.cluster(1,2,3,4), "mid", data.cols.y,1)
    assert True

def test_optimize():
    data = Data(get_file())
    show(data.sway(1,2,3,4), "mid", data.cols.y,1)
    assert True