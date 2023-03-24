import re
import num 
import sym
import utils 

class Cols:
     def __init__(self, t):
        self.names = t
        self.all = []
        self.x = []
        self.y = []
        self.klass = None

        for n, s in enumerate(t):
            col = num.Num(n,s) if re.match("^[A-Z]",s) else sym.Sym(n,s)
            self.all.append(col)
            if not re.match("X$",s):
                if re.match("!$",s):
                    self.klass = col
                if re.search("[!+-]$", s):
                    self.y.append(col)
                else:
                    self.x.append(col)
    
     def add(self, row):
        lst = [self.x,self.y]
        for _, t in enumerate(lst):
            for _, col in enumerate(t):
                col.add(row.cells[col.at])