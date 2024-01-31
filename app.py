from flask import Flask, request, jsonify
import numpy as np
import math
import pandas as pd
import json
from new_utils import get_preds
import logging

app = Flask(__name__)

#logging.basicConfig(filename='app.log', level=logging.ERROR)

@app.route('/predict', methods=['POST'])
def predict():

    data = request.json['Symbol']  # Assuming you send the past stock prices as JSON data
    #data = np.array(data)  # Convert JSON data to a numpy array

    data = str(data)

    final_res = get_preds(data)

    my_res = 0
    if(final_res==2):
        my_res = "SELL"
    if(final_res==1):
        my_res = "BUY"
    if(final_res==0):
        my_res = "NOTHING"
    #print()

    #print(data["Datetime"][len(data)-1])
    #print(data["Close"][len(data)-1])
    #print(data["Open"][len(data)-1])

    #print(data[0])


   # prediction = model.predict(np.expand_dims(data, axis=0))  # Make a prediction
    return jsonify({'prediction': my_res})

if __name__ == '__main__':
    app.run(debug=True)