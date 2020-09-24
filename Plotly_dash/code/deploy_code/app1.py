#!/usr/bin/env python
# coding: utf-8

# In[2]:


import yfinance as yf  
import pandas as pd 
import datetime 
import pymongo
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State


# In[3]:


name_ticker={}
with open('stock.txt','r') as file:
    for line in file:
        try:
            ticker=line.split('|')[0]
            name=line.split('|')[1]
            name_ticker[ticker]=name
        except:
            pass


# In[4]:



now=datetime.datetime.now()
year=now.year
month=now.month
date=now.day
today=str(year)+'-0'+str(month)+'-0'+str(date)
before=str(year-5)+'-0'+str(month)+'-0'+str(date)


# In[5]:


def get_yahoo(stock,before,today):
    return yf.download(stock,before,today)[['Adj Close','Close','Open']].reset_index()
def mongo_pd(stock):
    return pd.DataFrame(stocks.find_one({"index":stock})['data'])
def cal_desc(col_name):
    col=np.array(mongo_pd(col_name)['Close'])
    std=np.std(col)
    mean=np.mean(col)
    return [col_name,std,mean]
def create_db(db_name,collection_name):
    client = pymongo.MongoClient("mongodb+srv://Newuser:GLOBALAI@cluster0-ujbuf.mongodb.net/test?retryWrites=true&w=majority")
    db=client[db_name]
    stocks=db[collection_name]
    return db,stocks 


# In[6]:


# create db,collections 
db,stocks=create_db('Jasmine','stocks')


app = dash.Dash()
server=app.server
options=[{'label':j,'value':i} for i,j in name_ticker.items()]
options.append({'label':'Regions Financial Corporation Common Stock','value':'RF'})
app.layout = html.Div([
    html.H1('Stock data',style={'text-align': 'center'}),
    html.Hr(),
    html.Img(
            src='https://images.squarespace-cdn.com/content/5c036cd54eddec1d4ff1c1eb/1557908564936-YSBRPFCGYV2CE43OHI7F/GlobalAI_logo.jpg?content-type=image%2Fpng',
            style={
                'height': '11%',
                'width': '11%',
                'float': 'right',
                'position': 'relative',
                'margin-top': 11,
                'margin-right': 0}, className='two columns'
    ),

    html.Div([
    dbc.Row([
        dbc.Col(html.Div([
        html.H3('Select Stock:', style={'paddingRight':'30px'}),
        dcc.Dropdown(
            id='my_ticker_symbol',
            options=options,
            value=['AAL','PYPL','RF','CASY'],
            multi=True
        )
    ], style={'display':'inline-block', 'verticalAlign':'top', 'width':'30%'}),
   ),
        dbc.Col(html.Div([html.H3('Select Date:'),
                          dcc.DatePickerRange(id='date-range',
                                              min_date_allowed=datetime.datetime(
                                                  year-5, month, date),
                                              max_date_allowed=datetime.datetime.today(),
                                              start_date=datetime.datetime(
                                                  year-1, month, date),
                                              end_date=datetime.datetime.date(datetime.datetime.today()))],
                         style={'display': 'inline-block'}))
    ])]),
    dbc.Button("Generate Graphs", color="primary",
                   block=True, id="button", className="mb-3"),
    dbc.Row([dbc.Col(dcc.Graph(id='ts_graph'))]),
    
    dbc.Row([dbc.Col(dcc.Graph(id='box_graph')),
            dbc.Col(dcc.Graph(id='bar_graph')),
            dbc.Col(dcc.Graph(id='table'))       
                    ])
    
    
])

@app.callback(
    [Output('ts_graph','figure'),
    Output('box_graph', 'figure'),
    Output('bar_graph', 'figure'),
    Output('table','figure')
    ],
    [Input("button", "n_clicks")],
    [State("my_ticker_symbol", "value"),
     State("date-range", "start_date"),
     State("date-range", "end_date")])
def update_graph(n_clicks,stock_ticker,start,end):
    lst=[]
    if type(stock_ticker)==str:
        lst.append(stock_ticker)
        stock_ticker=[i for i in lst]
    else:
        pass
    
    data=pd.DataFrame()
    s_year,s_month,s_day=start.split('-')
    e_year,e_month,e_day=end.split('-')	
    s_day=s_day[0:2]
    e_day=e_day[0:2]
    print(s_day,e_day)
    start=datetime.date(int(s_year),int(s_month),int(s_day))
    end=datetime.date(int(e_year),int(e_month),int(e_day))
    print(start,end)
    for i in stock_ticker:
        data[i]=get_yahoo(i,start,end)['Close']
    data['Date']=get_yahoo(i,start,end)['Date']
    
    
    # TS close
    traces=[]
    for i in stock_ticker:
        traces.append(
            go.Scatter(
                x= data['Date'],
                y=data[i],
                mode='lines+markers',
                name=i
            )
        )
    layout = go.Layout(
        title = '5-year Closeing price for {}'.format(stock_ticker)
    )
    
    ts=go.Figure(data=traces,layout=layout)
    # BOX plot
    traces1=[]
    for i in stock_ticker:
        traces1.append(
            go.Box(
                y=data[i],
                boxpoints='outliers',
                name=i
            )
        )
    
    layout1 = go.Layout(
        title = 'Box plot for {}'.format(stock_ticker)
    )
    box=go.Figure(data=traces1,layout=layout1)
    
    # bar plot for mean return 
    
    temp=[]
    for i in stock_ticker:
        d=get_yahoo(i,start,end)
        d['return']=d['Close']-d['Open']
        mean=np.mean(d['return'])
        std=np.std(d['return'])
        temp.append([i,mean,std])
    data_bar=pd.DataFrame(temp,columns=['company','mean','std'])
        
    traces2=[]
   
    traces2.append(
        go.Bar(
        x=data_bar['company'],
        y=data_bar['mean'],
        
        )
    )
    layout2 = go.Layout(title='Mean return for {}'.format(stock_ticker)) 
    bar=go.Figure(data=traces2,layout=layout2)
    
    traces3=[]
    traces3.append(go.Table(header=dict(values=data_bar.columns.tolist(), font=dict(size=10, color="#fff"),
                                                 align="left", fill_color='#222'),
                                     cells=dict(values=[data_bar[k].tolist() for k in data_bar.columns.tolist()],
                                                fill_color='grey', font=dict(color='white'),
                                                align="left")))
    table=go.Figure(data=traces3,layout=go.Layout(title='descriptive analysis for stocks {}'.format(stock_ticker)))
    return ts,box,bar,table


if __name__ == '__main__':
    app.run_server()

