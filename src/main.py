from tests import *
import utils

def main(inputs, help, funcs, saved = {}, fails = 0):
    for k, v in utils.cli(utils.settings(help)).items():
        inputs[k] = v
        saved[k] = v
    if inputs["help"]:
        print(help)
    else:
        print("Testing...")
        for what in funcs:
            if inputs["go"] == "data" or what == inputs["go"]:
                for k,v in saved.items():
                    inputs[k] = v
                if funcs[what]() == False:
                    fails = fails + 1
                    print(what, ": failing")
                else:
                    print(what, ": passing")
    exit(fails)

the = {'dump': False, 'go': 'data', 'help': False, 'seed': 937162211, 'file' : '../etc/data/repgrid3.csv'}

help = """"   
grid.lua : a rep grid processor
(c)2022, Tim Menzies <timm@ieee.org>, BSD-2 
USAGE: grid.lua  [OPTIONS] [-g ACTION]
OPTIONS:
  -d  --dump    on crash, dump stack   = false
  -f  --file    name of file           = ../etc/data/repgrid3.csv
  -g  --go      start-up action        = data
  -h  --help    show help              = false
  -p  --p       distance coefficient   = 2
  -s  --seed    random number seed     = 937162211
ACTIONS:
"""
egs = {}
def eg(key, str, func):
    egs[key] = func
    inputs.help = inputs.help + ("  -g  %s\t%s\n" % (key,str))

eg("sym","check syms",test_sym)
eg("num","check nums",test_nums)
eg("the","show settings", test_the)
eg("repCols","check repCols",test_repCols)
eg("repRows","check repRows",test_repRows)
eg("synonyms","check synonyms", test_synonyms)
eg("prototypes","check prototypes",test_prototypes)
eg("position","check position", test_position)
eg("every","check every", test_every)

print(egs)
main(inputs.the, inputs.help, egs)