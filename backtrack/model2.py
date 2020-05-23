import pandas as pd
from tensorflow import keras
from keras.models import Sequential #used to initialize the NN
from keras.layers import Dense, Activation  #used to build the hidden Layers
from keras import losses

class model:
    def __init__(self, input_dimension, output_dimension):

        # 5000 steps with a learning rate of 0.5
        # 2000 steps with a learning rate of 0.1
        self.steps = [5000, 2000]
        self.learning_rates = [0.5, 0.1]

        # Loads the data into a dataframe, randomizes the order and splits it into data and labels
        self.df = pd.read_csv('model_data.csv')
        self.df = self.df.sample(frac=1)

        self.df_labels = pd.DataFrame()
        self.df_labels['Pattern'] = pd.Series(self.df['Pattern'])
        self.df = self.df.iloc[:, :-1]

        # Splitting the dataset into the Training set and Test set
        self.test_df = self.df[-3000:]
        self.test_labels = self.df_labels[-3000:]

        self.df = self.df[:]
        self.df_labels = self.df_labels[:]

        # The neural network, with the architecture described in the research paper
        # 20 units in the input layer
        # 16 units in the hidden layer
        # 12 units in the output layer
        # Fully connected
        # Sigmoid activation

        self.model = Sequential([
            Dense(16, input_shape=(10,)),
            Activation('sigmoid'),
            Dense(12),
            Activation('sigmoid'),
        ])

        self.model.compile(loss=losses.mean_squared_error, optimizer='sgd')
        print(self.model.outputs)

    def prepare_prediction_data(self, pattern):
        self.add_complements(pattern)
        pattern = [pattern]
        return pattern

    def prepare_test_data(self, index):
        input_data = self.test_df.iloc[[index]].values.tolist()[0]
        self.add_complements(input_data)
        input_data = [input_data]
        label = self.test_labels.iloc[[index]]
        list_label = self.create_label_list(label)
        list_label = [list_label]
        return input_data, list_label

    def add_complements(self, line):
        length = len(line)
        for i in range(length):
            line.append(1 - line[i])

A = model(20, 12)

