import numpy as np
from plotly.subplots import make_subplots as plot
import plotly.graph_objects as go


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
