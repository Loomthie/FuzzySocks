import numpy as np


class Column:
    def __init__(self, header, values):
        self.head = header
        self.vals = [0] * len(values)
        for i in range(len(self.vals)):
            self.vals[i] = values[i]

    def operation(self, func):
        res = [0] * len(self.vals)
        for i in range(len(self.vals)):
            if self.vals[i] == np.NaN:
                res[i] = np.NaN
                continue
            res[i] = func(self.vals[i])
        return res


class MissingColumnError(IndexError):
    pass


class Table:
    def __init__(self, **kwargs):
        self.columns = [0] * len(kwargs)
        ind = 0
        for i in kwargs:
            self.columns[ind] = Column(i, kwargs[i])
            ind += 1
        self.rows = max([len(i) for i in kwargs.values()])
        for i in range(len(self.columns)):
            while len(self.columns[i].vals) < self.rows:
                self.columns[i].vals.append(np.NaN)
            ind += 1

    def __find_column(self,title):
        for i in self.columns:
            i:Column
            if i.head == title:
                return i
        raise MissingColumnError(f'{title} is either missing or spelled incorrectly')

    def __repr__(self):
        head = [0] * len(self.columns)
        vals = [0] * len(self.columns)
        ind = 0
        for i in self.columns:
            head[ind] = i.head
            vals[ind] = i.vals
            ind += 1
        msg = ''
        width = max([len(str(i)) for i in vals])
        width = max([width, max([len(j) for j in head])]) + 4
        msg += f' {"_" * width * len(head)}{"_" * (len(head) - 1)}\n'
        empty_cell = (" " * width) + "|"
        msg += f'|{empty_cell * len(self.columns)}\n|'
        for i in head:
            pad = width - len(i)
            if pad % 2 != 0:
                pad += 1
                msg += f'{" " * int(pad / 2)}{i}{" " * int(pad / 2 - 1)}|'
            else:
                msg += f'{" " * int(pad / 2)}{i}{" " * int(pad / 2)}|'
        msg += '\n'
        temp = f'{"_" * width}|'
        msg += f"|{(temp) * len(head)}\n"
        for i in range(self.rows):
            msg += f'|{empty_cell * len(self.columns)}\n|'
            for col in range(len(head)):
                pad = width - len(str(vals[col][i]))
                if pad % 2 != 0:
                    pad += 1
                    msg += f'{" " * int(pad / 2)}{vals[col][i]}{" " * int(pad / 2 - 1)}|'
                else:
                    msg += f'{" " * int(pad / 2)}{vals[col][i]}{" " * int(pad / 2)}|'
            msg += '\n'
            msg += f'|{temp * len(self.columns)}\n'
        return msg

    def select_cols(self,*args,remove_NaN_vals=True):
        kwargs = {}
        for i in args:
            n = self.__find_column(i)
            if not remove_NaN_vals:
                kwargs[n.head]=n.vals
            else:
                vals = n.vals[:]
                k=0
                for j in range(len(vals)):
                    j=j-k
                    if str(vals[j])=="nan":
                        del vals[j]
                        k+=1
                kwargs[n.head]=vals
        return Table(**kwargs)





