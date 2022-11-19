from flask import Flask, render_template, request
from flask_cors import CORS
import numpy as np
import pickle
import pandas
import os
import requests
import json

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = '5krRUFWdHgYbO4G9dm85TYoeeTlXRfJtTPcF5wo6ZrPF'
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


app = Flask(__name__, static_url_path='')
@app.route('/', methods=['GET','POST'])
def sendHomePage():
    return render_template('form1.html')


@app.route('/predict', methods = ['POST','GET'])# route to show the predictions in a web UI def 
def prediction():
    GRE_SCORE = float(request.form['gre'])
    TOFEL_SCORE = float(request.form['ielts'])
    SOP_SCORE = float(request.form['sop'])
    LOR_SCORE = float(request.form['lor'])
    CGPA = float(request.form['cgpa'])
    RESEARCH_PAPER = float(request.form['research paper'])
    UNIVERSITY_RANK = float(request.form['university rank'])
    X = [[GRE_SCORE, TOFEL_SCORE, SOP_SCORE, LOR_SCORE,CGPA,RESEARCH_PAPER,UNIVERSITY_RANK]]
   #data_scaled = scale.fit_transform(data) #data = pandas.DataFrame(, columns=names)
   # predictions using the loaded model file prediction=model.predict(data)
    payload_scoring = {"input_data": [{"fields": ['gre','ielts','sop','lor','cgpa','research paper','university rank'], "values": X}]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/776e4e48-19ec-4dc8-81b8-333f4fc115d6/predictions?version=2022-11-18', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    predictions = response_scoring.json()
    predict = predictions['predictions'][0]['values'][0][0]
   
    

    if (int(predict[0])>60):
      return render_template("sucess.html", prediction_text = predict)
    else:
    #showing the prediction results in a UI
      return render_template("failure.html",  prediction_text = predict)

    

     

     
  
    
if __name__ == '__main__' :
    app.run(debug= False)  

  