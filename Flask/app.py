import os
from flask import Flask, request, render_template, session, redirect
import pandas as pd
import numpy as np

app = Flask(__name__, instance_relative_config=True)

data=pd.read_csv(r'/Users/kazba1/Desktop/RE valuation modelling/data_01_01.csv')
df=pd.DataFrame(data)
df=df.drop("Unnamed: 0", axis=1)
df=df.replace(" ",np.nan)
df=df.reset_index(drop=True)
df["links_image1_url"]=df["links_image1_url"][:][:-5]
df["links_image2_url"]=df["links_image2_url"][:][:-5]
df["links_image3_url"]=df["links_image3_url"][:][:-5]

for i in range(30,48):
    df.iloc[:,i]=round(df.iloc[:,i],2)

#Here I decrease the scope of data set and transform it into a dictionary
cf=df.iloc[0:5,2:8]
items=[]
for i in range(len(cf.index)):
    items+= [dict(Appartment_Address=cf.iloc[i,0],Boligtype=cf.iloc[i,1])]
headers = ['Appartment_Address','Boligtype']

@app.route("/", methods=["GET","POST"])
def index():
    return render_template('index.html')

@app.route("/result", methods=["GET","POST"])
def result():
        global df, university_selection, apartment, pets_allowed, price, location
        min_price=0
        max_price=0
        min_room=0
        max_room=0
        apartment = request.form.get('apartment')
        room = request.form.get('room')
        villa = request.form.get('villa')
        terraced = request.form.get('terraced')
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
        if apartment!="on":
            df=df[df['links_Appartment_Boligtype']!="Lejlighed"]
        if terraced!="on":
            df=df[df['links_Appartment_Boligtype']!="Rækkehus"]
        if room!="on":
            df=df[df['links_Appartment_Boligtype']!="Værelse"]
        if villa!="on":
            df=df[df['links_Appartment_Boligtype']!="Villa"]
        try:
            if min_price!='':
                df=df[df['links_rent_aconto_monthly']>int(min_price)]
        except:
            TypeError
        try:
            if max_price!='':
                df=df[df['links_rent_aconto_monthly']<int(max_price)]
        except:
            TypeError
        try:
            if min_room!='':
                df=df[df["links_Appartment_Rooms"]>int(min_room)]
        except:
            TypeError
        try:
            if max_room!='':
                df=df[df["links_Appartment_Rooms"]<int(max_room)]
        except:
            TypeError
            if pets_allowed=="1":
                df=df[df["links_Appartment_Pets_allowed"]=="Ja"]
            if furnished=="1":
                df=df[df["links_Appartment_Furnished"]=="Ja"]
        try:
            university_selection_score=university_selection+" score"
            df.loc[:,"Sorter"]=int(location)*df.loc[:,university_selection_score]+int(price)*df.loc[:,"Price_score"]
            df=df.sort_values(by=['Sorter'], ascending=False)
            df=df.reset_index(drop=True)
        except:
            TypeError

        
        return render_template('result.html',university_selection=university_selection , df=df)
        

@app.route("/result2", methods=["GET","POST"])
def result2():
    return render_template('result2.html', university_selection=university_selection, df=df)

@app.route("/result3", methods=["GET","POST"])
def result3():
    return render_template('result3.html', university_selection=university_selection, df=df)


#This is temporary section to post the data, using simple html we build the table
#@app.route("/result", methods=["POST"])
#def result():
    #if request.method == 'POST':
       # return render_template('simple.html', headers = headers, objects = items)

if __name__ == '__main__':
    app.run()