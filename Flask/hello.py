from flask import Flask, request, render_template, session, redirect
import pandas as pd
import numpy as np

app = Flask(__name__)

data=pd.read_csv(r'/Users/kazba1/Desktop/RE valuation modelling/11_23_2.csv')
df=pd.DataFrame(data)
df=df.drop("Unnamed: 0", axis=1)
df=df.replace(" ",np.nan)
df=df.reset_index(drop=True)

#Here I decrease the scope of data set and transform it into a dictionary
cf=df.iloc[0:10,2:8]
items=[]
for i in range(len(cf.index)):
    items+= [dict(Appartment_Address=df.iloc[i,0],Boligtype=df.iloc[i,1])]
headers = ['Appartment_Address','Boligtype']

@app.route("/", methods=["GET","POST"])
def index():
    return render_template('index.html')

#This is temporary section to post the data, using simple html we build the table
@app.route("/result")
def result():
    return render_template('simple.html', headers = headers, objects = items)
