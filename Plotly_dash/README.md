# Python Interactive Visualization project 
This repository includes python interactive visualization methonds by using plotly and dash package. Please feel free to check code [here](https://github.com/JasmineYuer/jasmineyuer.github.io/tree/master/Plotly_dash/code)

Plot types include line chart, radar chart, map, etc. 

Features include automatically refresh in given time, get data from database daily and live updating, hover around map to get detailed data, and connect with mapbox api to have a fancier visualization

The plot has generic feature, basically for the same type of plot, we just change the data source and apply some basic panads function then it works fine with a new plot. AKA template. 

This repository is for personal use and create by a group of students. For details, please see the list of contributors. 
## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Python 3 environment 
```

### Installing

The main packages drawing the graph is plotly and dash, we read https://dash.plot.ly/ as reference 
To install, simply type 

```
pip install dash
pip install plotly
```
To import, one thing might be different is 

```
import plotly.graph_objs as go
```
sometimes work but sometimes doesn't work on some computer, try
```
import plotly.graph_objects as go
```
instead 


## Deployment
We follow the tutorial on this document: https://docs.google.com/document/d/1DjWL2DxLiRaBrlD3ELyQlCBRu7UQuuWfgjv9LncNp_M/edit.
All of our code is deployed on heroku.


## Result of deployment and sample pic

***Notice: Please wait for 30 seconds after click on the link, cause the code need to be launched on a remote server on heroku, it takes time.
If nothing show up initially, try to play with the bars and hit submit, then your are good to go. You can hover on the graph to find more insights about out data.***


**1.Yahoo Finanace stock Ticker :** [Click me to view from Heroku](https://fairyjump.herokuapp.com/)
![image](/Plotly_dash/image/img.PNG)

This project will automatically grab daily stock data from [yahoo finance](https://finance.yahoo.com) and plot it's closing price and return in different form of visualization. The tickers include more than 2000 number of stocks in the dropdown menu. It also includes simple analysis for selected stocks like mean of return and standard deviation of return.

**2.Macro CISS:** [Click me to view from Heroku](https://cissploty.herokuapp.com)

![image](/Plotly_dash/image/img1.png)

**3.World bank:** [Click me to view from Heroku](https://shuyidashapp.herokuapp.com)  

![image](/Plotly_dash/image/img2.png)


## Comments
Even though this is much more work to do compare with Power BI and tableau, and it is not visual friendly, but those charts are apps that can run automatically with little governance. Since it is programming in python, those programs can leverage the python packages like _pandas_, _numpy_, _sklearn_ more easily, thus it can be enriched in functionality more easily


## Authors

* **Jasmine Yu** - *Initial work* - [GitHub](https://github.com/Jasminejump) | [LinkedIn](https://www.linkedin.com/in/jasmine-yu-214712192/)

See also the list of [contributors](/Plotly_dash/Contributor.md) who participated in this project.

