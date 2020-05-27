import csv
import numpy as np
from model import model
from dataTool import *

ml_model = model(20, 12)
ml_model.restore_model("models/model_10_weights")

def backtrack(name):
        json_line = []
        lists = dataTool(name).iterate_patterns()

        for lis in lists[:]:
            number = lis[0]
            float_list = [float(i) for i in lis[1:]]
            pattern = model_input(float_list)
            max_index = np.argmax(pattern[0].tolist())
            percentage = pattern[0].tolist()[max_index] * 100
            if(percentage >= 90):
                json_line.append({
                    'index':number, 
                    'pattern':int(max_index)+1, 
                    'percentage':percentage
                })
            
            
        return json_line
def model_input(data):
    input_window = ml_model.prepare_prediction_data(data)
    pattern = ml_model.predict_pattern(input_window)

    return pattern