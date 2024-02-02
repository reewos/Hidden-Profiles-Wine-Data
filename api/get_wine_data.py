from flask import Flask, jsonify
import warnings

# Ignore all deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import pandas as pd
import os

app = Flask(__name__)

@app.route('/get_wine_data', methods=['GET'])
def get_wine_data():
    #Load dataset
    try:
        #"The dataset is obtained directly from the link.
        wine_data = pd.read_csv("https://storage.googleapis.com/the_public_bucket/wine-clustering.csv")
    except:
        #If it's not available, the local dataset is retrieved.
        try:
            wine_data = pd.read_csv("./datasets/wine-clustering.csv")
        except:
            wine_data = {}
        
    #Return dataset as json
    wine_data_dict = wine_data.to_dict(orient='records')
    return jsonify({"wine_data": wine_data_dict})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
