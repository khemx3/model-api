from sklearn import preprocessing
import matplotlib.pyplot as plt
import csv
import numpy as np


import sys
sys.path.append(".") 
from model import model


ml_model = model(20, 12)
ml_model.restore_model("models/model_10_weights")
def backtrack():
        # Splits the file into rows and each row into cells
        with open('backtrack/data_1d.csv') as file:
            lists = [line.split(',') for line in file]

        header = lists.pop(0)
        del header[0]

        for lis in lists[:]:
            lis[-1] = lis[-1].strip()
            number = lis[:]
            float_list = [float(i) for i in lis[1:]]


            input_window = ml_model.prepare_prediction_data(float_list)
            pattern = ml_model.predict_pattern(input_window)
            # print(number)
            max_index = np.argmax(pattern[0].tolist())
            # # Initializes a line that will be appended to the csv file
            csv_line = [number[0], max_index + 1, pattern[0].tolist()[max_index] * 100]

            with open('backtrack/output.csv', 'a', newline='') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(csv_line)
                csvFile.close()
            
        
backtrack()