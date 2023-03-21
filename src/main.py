# ------------------- MAIN PROGRAM FLOW -------------------

## run_test counts the number of arguments that have been passed and failed and it also,
## it displays the names tests passed and failed.

import sys
sys.path.append("./src")
from data import *
import re
import traceback

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
    
# api-side function to get the current input csv filepath
def get_file():
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
def get_seed():
    return seed

# api-side function to get the current dump boolean status
def should_dump():
    return dump

## find_arg_values gets the value of a command line argument
# first it gets set of args
# second it get option A (-h or -d or -s or -f )
# third is get option B (--help or --dump or --seed or --file)
def find_arg_value(args, optionA, optionB):
    index = args.index(optionA) if optionA in args else args.index(optionB)
    if (index + 1) < len(args):
        return args[index + 1]
    return None


def cli(options):
    args = sys.argv[1:]
    for key, value in options.items():

        for n, x in enumerate(args):
            if x == '-'+ key[0] or x == '--'+ key:
                  value = "false" if value == "true" else "true" if value == "false" else args[n+1]
        options[key] = coerce(value)
    return options

def settings(s):
    return dict(re.findall("\n[\s]+[-][\S]+[\s]+[-][-]([\S]+)[^\n]+= ([\S]+)", s))

def main(options, help, funs):
    saved = {}
    fails = 0
    for k,v in cli(settings(help)).items():
        options[k] = v
        saved[k] = v

    if options['help']:
        print(help)
    else:
        for what, fun in funs.items():
            if options['go'] == 'all' or options['go'] == what:
                print("--")
                for k,v in saved.items():
                    options[k] = v
                Seed = options['seed']
                if funs[what]() == False:
                    fails += 1
                    print("❌ fail:", what)
                else:
                    print("✅ pass:", what)