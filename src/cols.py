
from num import Num
from sym import Sym
import row
from collections import OrderedDict
import re
from enum import Enum

class Cols:

    def __init__(self, t: list[str]):
        self.names = t
        self.all = []
        self.x = []
        self.y = []
        self.klass = []
        for n, s in enumerate(t):
            if(s[-1].lower() != 'x'):
                col = Num(n, s) if re.search("^[A-Z]+", s) != None else Sym(n, s)
                self.all.append(col)
                if re.search("X$", s) == None:

                    if(re.search("[!+-]$", s)):
                        self.y.append(col)
                    else:
                        self.x.append(col)
                
    def add(self, row: row.Rows):
        for col in self.all:
            col.add(row.cells[col.at])


