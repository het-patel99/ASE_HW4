# ------------------- MAIN PROGRAM FLOW -------------------

## run_test counts the number of arguments that have been passed and failed and it also,
## it displays the names tests passed and failed.

import sys, getopt
# from tests import test_syms,test_nums, test_the,test_copy,test_repCols,test_repCols,test_synonyms,test_prototypes,test_position,test_every
from tests import *

def run_tests():
    print("Executing tests...\n")

    passCount = 0
    failCount = 0
    test_suite = [test_syms,test_nums, test_the,test_copy,test_repCols,test_repCols,test_synonyms,test_prototypes,test_position,test_every] 
    
    for test in test_suite:
        try:
            test()
            passCount = passCount + 1
        except AssertionError as e:
            failCount = failCount + 1
    print("\nPassing: " + str(passCount) + "\nFailing: " + str(failCount))

argumentList = sys.argv[1:]
b4={}
ENV = {}
for k,v in ENV:
    b4[k]=v

options = "hg"
long_options = []
the = {"seed": 937162211, "dump": False, "go": "data", "help": False, "min" : 0.5, "p" : 2, "Sample" : 512, "Far" : 0.95 }
    
def help():
    help_string = """cluster.lua : an example csv reader script
    (c)2022, Tim Menzies <timm@ieee.org>, BSD-2 
    USAGE: cluster.lua  [OPTIONS] [-g ACTION]
    OPTIONS:
    -d  --dump    on crash, dump stack   = false
    -f  --file    name of file           = ../etc/data/repgrid2.csv
    -F  --Far     distance to "faraway"  = .95
    -g  --go      start-up action        = data
    -h  --help    show help              = false
    -m  --min     stop clusters at N^min = .5
    -p  --p       distance coefficient   = 2
    -s  --seed    random number seed     = 937162211
    -S  --Sample  sampling data size     = 512
    ]]"""

def main():
    try:    
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)
        # checking each argument
        for currentArgument, currentValue in arguments:
             if currentArgument in ('-h', ''):
                 help()
             if currentArgument in ("-g", ''):
                run_tests()
                
    except getopt.error as err:
        print (str(err))

if __name__ == "__main__":
    main()