import utils
import row
import cols
import math

class Data:
    def __init__(self, src):
        self.rows = []
        self.cols = None

        if type(src) == str:
            utils.csv(src, self.add)
        else:
            for line in src:
                self.add(line)

    def add(self, t):
        if (self.cols):
            t = t if hasattr(t, 'cells') else row.Rows(t)
            self.rows.append(t)
            self.cols.add(t)
        else:
            self.cols = cols.Cols(t)

    def stats(self, what, cols, nPlaces):
        def fun(col):
            f = getattr(col,what or "mid")
            return col.rnd(f(), nPlaces), col.txt
        
        return utils.kap(cols, fun)

    def clone(self, init = []):
        data = Data([self.cols.names])
        for val in init:
            data.add(val)
        return data
    
    def better(self, row1, row2):
        s1, s2, ys = 0, 0, self.cols.y
        for _,col in enumerate(ys):
            x = col.norm(row1[col.at])
            y = col.norm(row2[col.at])
            s1 = s1 - math.exp(col.w * (x - y) / len(ys))
            s2 = s2 - math.exp(col.w * (y - x) / len(ys))
        
        return s1/len(ys) < s2/len(ys)

    def dist(self, row1, row2, cols=None):
        n, d = 0, 0
        for _, col in enumerate(cols or self.cols.x):
            n = n + 1
            val = col.dist(row1.cells[col.at], row2.cells[col.at])
            d = d + val ** 2
            
        return (d / n) ** (1 / 2)

    def around(self, row1, rows=None, cols=None):
        if not rows:
            rows = self.rows
        def fun(row2):
            return {'row': row2, 'dist':self.dist(row1,row2,cols)}
        u = map(fun, rows)
        return sorted(u, key=lambda x: x['dist'])

    def half(self,rows=None,cols=None,above=None):

        def dist1(row1,row2):
            return self.dist(row1, row2, cols)

        def project(row):
            x, y = utils.cosine(dist1(row, A), dist1(row, B), c)
            row.x = row.x or x
            row.y = row.y or y
            return {"row": row, "x": x, "y": y}

        if not rows:
            rows = self.rows
    
        A  = above or utils.any(rows)
        B = self.furthest(A, rows)['row']
        c  = dist1(A,B)
        left, right = [], []
        res = [project(row) for row in rows]
        sorted_res = sorted(res, key=lambda x: x["x"])
        for n, tmp in enumerate(sorted_res):
            if n + 1 <= len(rows) // 2: 
                left.append(tmp["row"])
                mid = tmp["row"]
            else: 
                right.append(tmp["row"])
        return left, right, A, B, mid, c

    def cluster(self, rows=None,cols=None, above=None):
        rows = rows or self.rows
        cols = cols or self.cols.x
        node = {'data': self.clone(rows)} 

        if len(rows) >= 2:
            left, right, node["A"], node["B"], node["mid"], node["C"] = self.half(rows, cols, above)
            node["left"]  = self.cluster(left,cols, node["A"])
            node["right"] = self.cluster(right,cols, node["B"])
        
        return node 
    
    def sway(self, rows=None, min=None, cols=None, above=None):
        rows = rows or self.rows
        min = min or len(rows) ** 0.5
        cols = cols or self.cols.x
        node = {"data": self.clone(rows)}

        if len(rows) > 2 * min:
            left, right, node["A"], node["B"], node["min"], _ = self.half(rows, cols, above)
            if self.better(node["B"], node["A"]):
                left, right, node["A"], node["B"] = right, left, node["B"], node["A"]
            node["left"] = self.sway(left, min, cols, node["A"])

        return node

    def furthest(self, row1=None, rows=None, cols=None):
        t = self.around(row1,rows,cols)
        return t[-1]