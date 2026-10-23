from flask import Flask, request
import pickle

import numpy as np
import os
_dir = os.path.dirname(os.path.abspath(__file__))
local_classifier = pickle.load(open(os.path.join(_dir, '../../section 2/ml_classification/classifier.pickle'), 'rb'))
local_scaler     = pickle.load(open(os.path.join(_dir, '../../section 2/ml_classification/sc.pickle'), 'rb'))

app = Flask(__name__)

@app.route('/model',methods=['POST'])
def hello_world():
    request_data = request.get_json(force=True)
    age = request_data['age']
    salary = request_data['salary']
    print(age)
    print(salary)
    pred_proba = local_classifier.predict_proba(local_scaler.transform(np.array([[age,salary]])))[:,1]
    return "The prediction is {}".format(pred_proba)

if __name__ == "__main__":
    app.run(port=8005, debug=True)



