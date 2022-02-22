import numpy as np
from plotly.subplots import make_subplots as plot
import plotly.graph_objects as go
import statistics as stats

class Data:
    vals = {}

    def __init__(self,**kwargs):
        self.vals = kwargs


class Correlation(Data):

    def __init__(self,**kwargs):
        if len(kwargs)==1:
            if 'x' in kwargs.keys():
                kwargs['x0'] = np.arange(0,len(kwargs['x']),1)
            else:
                key = ''
                for i in kwargs:
                    key = i
                kwargs['x'] = np.arange(0,len(kwargs[key]),1)
        super().__init__(**kwargs)

    def plot_relations(self,*args):
        if args == ():
            args = [i for i in self.vals.keys()]
        rows=cols=len(args)
        fig = plot(rows=rows,cols=cols)
        cor_matr = []
        for r in range(rows):
            cor_matr.append([0]*rows)
        for r in range(rows):
            for c in range(cols):
                cor_matr[r][c] = {'x':args[c],'y':args[r]}
        for r in range(rows):
            for c in range(cols):
                fig.add_trace(go.Scatter(x=self.vals[cor_matr[r][c]['x']],y=self.vals[cor_matr[r][c]['y']],
                                         mode='markers'), row=r+1,col=c+1)
        for r in range(rows):
            fig.update_yaxes(title_text=args[r],row=r+1,col=1)
        for c in range(cols):
            fig.update_xaxes(title_text=args[c],row=rows,col=c+1)
        fig.update_layout(showlegend=False,title_text="Correlation Matrix")
        for r in range(len(cor_matr)):
            for c in range(len(cor_matr[r])):
                cor_matr[r][c] = self.__calc_r_sq(self.vals[cor_matr[r][c]['x']],self.vals[cor_matr[r][c]['y']])
        return fig,cor_matr

    @staticmethod
    def __calc_r_sq(x,y):
        r = np.corrcoef(x,y)[0,1]
        return r**2

    def __determine_best_model(self, x, y):
        logy = [np.log10(i) for i in y]
        lny = [np.log(i) for i in y]
        logx = [np.log10(i) for i in x]
        r_vals = {'linear':self.__calc_r_sq(x,y),'power':self.__calc_r_sq(logx,logy),'exp':self.__calc_r_sq(x,lny)}
        for i in r_vals:
            if r_vals[i] == max([j for j in r_vals.values()]):
                return i

    def get_model(self,x,y):

        class Coefficients:
            def __init__(self, slope, intercept):
                self.slope = slope
                self.intercept = intercept

            def __str__(self):
                return f'''
    slope = {self.slope}
Intercept = {self.intercept}
                '''

        x = self.vals[x]
        y = self.vals[y]
        mode = self.__determine_best_model(x,y)
        if mode=='linear':
            m = sum([(xi - stats.mean(x))*(yi-stats.mean(y)) for xi,yi in zip(x,y)])/sum([(xi-stats.mean(x))**2 for xi in x])
            b = stats.mean(y) - m*stats.mean(x)
            func = lambda t:m*t+b
        elif mode=='power':
            new_x = [np.log10(i) for i in x]
            new_y = [np.log10(i) for i in y]
            m = sum([(xi - stats.mean(new_x)) * (yi - stats.mean(new_y)) for xi, yi in zip(new_x, new_y)]) / sum(
                [(xi - stats.mean(new_x))**2 for xi in new_x])
            b = stats.mean(new_y) - m * stats.mean(new_x)
            b = 10**b
            func = lambda t: b*t**m
        else:
            new_y = [np.log(i) for i in y]
            m = sum([(xi - stats.mean(x)) * (yi - stats.mean(new_y)) for xi, yi in zip(x, new_y)]) / sum(
                [(xi - stats.mean(x))**2 for xi in x])
            b = stats.mean(new_y) - m * stats.mean(x)
            b=np.exp(b)
            func = lambda t: b*np.exp(m*t)

        return func, Coefficients(m, b)

    def create_fig(self,x,*args,mode='markers'):
        x = self.vals[x]
        fig = plot()
        for y in args:
            fig.add_trace(go.Scatter(x=x,y=self.vals[y],mode=mode))
        return fig

