import os
from flask import Flask, request, render_template, session, redirect
import pandas as pd
import numpy as np

app = Flask(__name__, instance_relative_config=True)

data=pd.read_csv(r'/Users/kazba1/Desktop/RE valuation modelling/11_23_2.csv')
df=pd.DataFrame(data)
df=df.drop("Unnamed: 0", axis=1)
df=df.replace(" ",np.nan)
df=df.reset_index(drop=True)

#Here I decrease the scope of data set and transform it into a dictionary
cf=df.iloc[0:5,2:8]
items=[]
for i in range(len(cf.index)):
    items+= [dict(Appartment_Address=cf.iloc[i,0],Boligtype=cf.iloc[i,1])]
headers = ['Appartment_Address','Boligtype']

@app.route("/", methods=["GET","POST"])
def index():
    return render_template('index.html')

@app.route("/result", methods=["POST"])
def result():
    if request.method == 'POST':
        apartment = request.form.get('apartment')
        room = request.form.get('room')
        villa = request.form.get('villa')
        university_selection=request.form.get('university_selection')
        min_price = request.form.get('min_price')
        max_price = request.form.get('max_price')
        min_room = request.form.get('min_room')
        max_room = request.form.get('max_room')
        pets_allowed = request.form.get('pets_allowed')
        furnished = request.form.get('furnished')
        rent_period = request.form.get('rent_period')
        price = request.form.get('price')
        location = request.form.get('location')
        other = request.form.get('other')
        global df
        return render_template('result.html',university_selection=university_selection , df=df)

#This is temporary section to post the data, using simple html we build the table
#@app.route("/result", methods=["POST"])
#def result():
    #if request.method == 'POST':
       # return render_template('simple.html', headers = headers, objects = items)

if __name__ == '__main__':
    app.run()