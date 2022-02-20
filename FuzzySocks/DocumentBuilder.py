import webbrowser as web
from plotly.graph_objs import Figure
import os
import time


class element:
    _class = ''
    style = ''
    body = ''
    tag = ''

    def __init__(self, *args, **kwargs):
        for i in kwargs:
            if i == "class":
                self._class = kwargs[i]
            elif i == "body":
                self.body = kwargs[i]
            else:
                self.style += f'{i}:{kwargs[i]};'

    def __str__(self):
        style = ''
        cls = ''
        if self.style != '':
            style = f"style=\"{self.style}\""
        if self._class != '':
            cls = f'class={self._class}'
        return f'''
        <{self.tag} {style} {cls}>
            {self.body}
        </{self.tag}>
        '''

    def __repr__(self):
        return self.__str__()


class div(element):
    tag = 'div'

    def add_element(self, ele):
        self.body += str(ele)


class h1(element):
    tag = 'h1'

    def __init__(self, *args, **kwargs):
        for i in args:
            self.body += f'{i}<br>'
        super().__init__(*args, **kwargs)


class h2(h1):
    tag = 'h2'


class h3(h1):
    tag = 'h3'


class h4(h1):
    tag = 'h4'


class h5(h1):
    tag = 'h5'


class h6(h1):
    tag = 'h6'


class p(h1):
    tag='p'


class table(element):
    tag='table'

    def add_row(self,*args,header_row=False):
        self.body += '<tr>\n'
        tag = 'td'
        if header_row:
            tag = 'th'
        for i in args:
            self.body += f'<{tag}>{i}</{tag}>\n'
        self.body += '</tr>\n'


class Document:
    __fileContent = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>
            {self.title}
        </title>
        <style>
            {self.style}
        </style>
    </head>
    <body>
        {self.body}
    </body>
    </html>
    '''
    style= '''table {border:2px solid black; text-align:center;margin:auto; border-collapse:collapse; width:50%;}
    tr,th,td {border: 2px solid black; text-align:center;}
    tr:nth-child(even) {background-color: #f2f2f2;}
    th {background-color:#04AA6D; color:white; height:35px;}
    '''
    body= ''
    elements = []
    title = "Fuzzy Sock Original HTML File"

    def add_style(self,**kwargs):
        for i in kwargs:
            self.style += f'{i} {"{"}{kwargs[i]}{"}"}\n'

    def add_element(self, element):
        self.body += str(element)

    def add_plotly_graph(self,fig:Figure):
        fig.write_html('temp.txt',full_html=False)
        with open('temp.txt','r') as file:
            div = file.read()
        os.remove('temp.txt')
        self.body += div

    def open_doc(self):
        with open("temp.html",'w') as file:
            file.write(self.__fileContent.format(self=self))
        web.open(f'file://{os.path.realpath("temp.html")}')
        time.sleep(1)
        os.remove("temp.html")
