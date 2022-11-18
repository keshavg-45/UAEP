from flask import Flask, render_template, request
from flask_cors import CORS
import numpy as np
import pickle
import pandas
import os
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "5krRUFWdHgYbO4G9dm85TYoeeTlXRfJtTPcF5wo6ZrPF"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app=Flask (__name__)
CORS(app)  
@app.route('/') # rendering the html template 
def form1(): 
    return render_template('form1.html')
@app.route('/prediction',methods=["POST","GET"])  


@app.route('/predict', methods = [ "POST","GET"])# route to show the predictions in a web UI def 
def predict():
   input_feature=[float(x) for x in request.form.values() ]
    #input_feature = np.transpose(input_feature)
   input_feature=[np.array(input_feature)]
   print(input_feature)
   def predictSpecies():
     GRE_SCORE = float(request.form['GRE SCORE'])
     TOFEL_SCORE = float(request.form['TOFEL SCORE'])
     SOP_SCORE = float(request.form['SOP SCORE'])
     LOR_SCORE = float(request.form['LOR SCORE'])
     CGPA = float(request.form['CGPA'])
     RESEARCH_PAPER = float(request.form['RESEARCH PAPER'])
     UNIVERSITY_RANK = float(request.form['UNIVERSITY RANK'])
     X = [[GRE_SCORE, TOFEL_SCORE, SOP_SCORE, LOR_SCORE,CGPA,RESEARCH_PAPER,UNIVERSITY_RANK]]
   #data_scaled = scale.fit_transform(data) #data = pandas.DataFrame(, columns=names)
   # predictions using the loaded model file prediction=model.predict(data)
     payload_scoring = {"input_data": [{"fields": ['GRE SCORE', 'TOFEL SCORE', 'SOP SCORE', 'LOR SCORE', 'CGPA', 'RESEARCH PAPER', 'UNIVERSITY RANK'], "values": X}]}
     response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/776e4e48-19ec-4dc8-81b8-333f4fc115d6/predictions?version=2022-11-18', json=payload_scoring,headers={'Authorization': 'Bearer ' + mltoken})
     print(response_scoring)
     predict = response_scoring.json()['predictions'][0]['values'][0][0]
     print("Final prediction :",predict)
     return predict

   if (predict >= 60):
        return render_template("sucess.html", prediction_text = predict)
   else:
    #showing the prediction results in a UI
        return render_template("failure.html",  prediction_text = predict)

  
    
  
if __name__=="__main__":
# app.run(host='0.0.0.0', port=8000, debug=True) 
  port=int(os.environ.get('PORT',5000)) 
  app.run(debug=False)
  