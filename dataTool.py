import numpy as np
import requests
import json
import csv

class dataTool:
    def __init__(self, name):

        self.url = "https://stormy-mesa-57066.herokuapp.com/"
        self.data = requests.get(self.url + name + "?timeframe=1d&range=500")
        self.data_close = self.data.json()[0]['data']['intervals']
        
    def get_data_close(self):
        return self.data_close

    def iterate_patterns(self):
        data = []
        for i in range(0, len(self.data_close) - 9):
            data.append(self.find_pattern(i))
            
        return data       

    def find_pattern(self, index):
        json_line = [len(self.data_close) - index , self.data_close[index]['last']]
        # Appends the next 9 points to the lists
        for i in range(index + 1, index + 10):
            json_line.append(self.data_close[i]['last'])
        return json_line