from plotly.subplots import make_subplots
import numpy as np
import scipy.stats as stats
import plotly.graph_objects as go
import statistics as pyStats


class Data:


    def __init__(self, **kwargs):
        self.__vars = []
        for i in kwargs:
            if type(kwargs[i]) != list:
                raise TypeError("Must enter list or array for kwarg arguements")
            self.__dict__[i] = kwargs[i]
            self.__vars.append(i)

    @staticmethod
    def R_calc(x, y):
        sx = pyStats.stdev(x)
        sy = pyStats.stdev(y)
        xy = []
        for i in range(len(x)):
            xy.append([x[i], y[i]])
        r = 1 / (len(x) - 1) * (sum([(i - pyStats.mean(x)) * (j - pyStats.mean(y)) for i, j in xy]) / (sx * sy))
        return r ** 2


class DatasetExamples:

    @classmethod
    def TwoDiceSum(cls, n=1000):
        res = [0] * int(n)
        for i in range(int(n)):
            dice = [np.random.randint(1, 7), np.random.randint(1, 7)]
            res[i] = sum(dice)
        return Distribution(Dice_sum=res)

    @classmethod
    def NormalDistribution(cls, n=1000):
        res = [0] * n
        for i in range(n):
            res[i] = np.random.normal()
        return Distribution(Norm_Values=res)


class Distribution(Data):
    class __DescriptiveStats:
        def __init__(self, data, name='N/A'):
            self.name = name
            self.mean = pyStats.mean(data)
            self.stErr = pyStats.stdev(data) / np.sqrt(len(data))
            self.median = pyStats.median(data)
            #self.mode = pyStats.mode(data)
            self.stDev = pyStats.stdev(data)
            self.var = self.stDev ** 2
            self.kurtosis = len(data) * sum([(i - self.mean) ** 4 for i in data]) / self.var
            self.skewness = sum([(i - self.mean) ** 3 for i in data]) / (len(data) - 1) / self.stDev ** 3
            self.range = max(data) - min(data)
            self.min = min(data)
            self.max = max(data)
            self.count = len(data)
            self.sum = sum(data)

        def __repr__(self):
            msg = f'''

            Dataset: {self.name}

            mean = {self.mean}
            Standard Error = {self.stErr}
            Median = {self.median}
            Standard Deviation = {self.stDev}
            Variance = {self.var}
            Kurtosis = {self.kurtosis}
            Skewness = {self.skewness}
            Range = {self.skewness}
            Minimum = {self.min}
            Maximum = {self.max}
            Count = {self.count}
            Sum = {self.sum}

            '''
            return msg

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for i in self.__dict__:
            try:
                self.__dict__[i]=sorted(self.__dict__[i])
            except:
                continue
            
    def normal_test(self, *arg):
        res = {}
        for i in arg:
            perc = np.arange(0, 1, 1 / (len(self.__dict__[i]) + 1))
            z = [self.z_calc(k) for k in perc[1:]]
            res[i] = [self.__dict__[i], z]
        fig = make_subplots(rows=len(arg), cols=1, x_title="z-values")
        row = 1
        R_vals = ''
        for i in res:
            fig.add_trace(go.Scatter(x=res[i][1], y=res[i][0], name=i, mode="markers"), row=row, col=1)
            fig.update_yaxes(title_text=i, row=row, col=1)
            R_vals += f"<tr>\n<td>{i}</td>\n<td>{self.R_calc(res[i][0], res[i][1])}</td>\n</tr>"
            row += 1
            res[i] = self.R_calc(res[i][0], res[i][1])
        fig.update_layout(showlegend=False)
        with open("Result.html", 'w') as htmlFile:
            htmlFile.write("<!DOCTYPE HTML>\n")
            fig.write_html('temp.txt', full_html=False)
            with open("temp.txt", 'r') as divFile:
                plot = divFile.read()

            msg = f'''
      <html>
      <style>
      {'table {margin: auto; font-size:20px;}'}
      {'.thr {background-color: lightgray; border: 2px solid gray}'}
      {'th,td {text-align:center;}'}
      </style>
      <body>
      {plot}
      <table cellspacing="0">
      <tr class="thr">
        <th>Variable</th>
        <th>R<sup>2</sup> value</th>
      </tr>
      {R_vals}
      </table>
      </body></html>
      '''
            htmlFile.write(msg)
        return res

    def box_plot(self, *args):
        fig = make_subplots()
        if args[0].upper() == "ALL":
            for i in self._Data__vars:
                fig.add_trace(go.Box({'x': self.__dict__[i]}, name=i))
        else:
            for i in args:
                fig.add_trace(go.Box({'x': self.__dict__[i]}, name=i))
        fig.show()

    def histogram(self, *args):
        fig = make_subplots(rows=len(args), cols=1)
        for row in range(len(args)):
            fig.add_trace(go.Histogram({'x': self.__dict__[args[row]]}), row=row + 1, col=1)
        fig.show()

    def desc_stats(self,*args):
        res = []
        for i in args:
            res.append(Data.__DescriptiveStats(self.__dict__[i]))
        return res

    @staticmethod
    def z_calc(p):
        return stats.norm.ppf(p)


class Correlation(Data):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)