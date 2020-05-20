import tensorflow.compat.v1 as tf
from keras.layers import Dense
import numpy as np
import pandas as pd
from keras import backend as K
import random

tf.disable_eager_execution()


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

        # # Splits the dataframe into test and training dataframes
        self.test_df = self.df[-3000:]
        self.test_labels = self.df_labels[-3000:]

        self.df = self.df[:]
        self.df_labels = self.df_labels[:]

        # The correct labels
        self.labels = tf.placeholder(tf.float32, [None, output_dimension])

        # The neural network, with the architecture described in the research paper
        # 20 units in the input layer
        # 16 units in the hidden layer
        # 12 units in the output layer
        # Fully connected
        # Sigmoid activation

        # The output of the neural network is a value for each specific pattern, the higher the value,
        # the more similar the neural network sees the input as that pattern
        self.input_layer = tf.placeholder(tf.float32, [None, input_dimension])
        self.layer = Dense(16, activation='sigmoid')(self.input_layer)
        self.output = Dense(output_dimension, activation="sigmoid")(self.layer)

        # Loss function as described in formula 3
        self.loss = tf.reduce_sum(tf.square(self.labels - self.output))

        # Learning rate as input to the train step
        self.learning_rate = tf.placeholder(tf.float32, shape=[])

        # The optimizer is gradient descent
        self.train = tf.train.GradientDescentOptimizer(learning_rate=self.learning_rate).minimize(self.loss)

        # Initialize the session
        self.sess = tf.Session()

        K.set_session(self.sess)
        # Used to save and restore the model
        self.saver = tf.train.Saver ()

        # Initialize all tensorflow variables
        self.sess.run(tf.global_variables_initializer())

    # Predict a pattern given an input
    def predict_pattern(self, input_layer):
        return self.sess.run(
            self.output,
            feed_dict={self.input_layer: input_layer}
        )

    # Run a training session
    def train_model(self):

        # For all the step sizes
        for i in range(len(self.steps)):
            step_size = self.steps[i]
            for step in range(step_size):

                # # Every 100 iterations we test the model on the test set
                if (step + 1) % 100 == 0:

                    # Clear the lists
                    prediction = []
                    actual_labels = []

                    # Predict the pattern for all the samples in the test set
                    for j in range(len(self.test_df)):
                        input_data, list_label = self.prepare_test_data(j)
                        output = self.output.eval(session=self.sess, feed_dict={
                            self.learning_rate: self.learning_rates[i],
                            self.input_layer: input_data,
                            self.labels: list_label
                        })
                        prediction.append(np.argmax(output[0]) + 1)
                        actual_labels.append(np.argmax(list_label[0]) + 1)

                    # Computes and prints the accuracy of the model on the train set
                    print("Accuracy: %f" % (sum(1 for x, y in zip(prediction, actual_labels) if x == y) / float(len(prediction))))

                # Picks a random data point to train on
                random_number = random.randint(1, len(self.df) - 1)
                input_data, list_label = self.prepare_data(random_number)

                # Runs a train step
                self.sess.run(
                    self.train,
                    feed_dict={self.learning_rate: self.learning_rates[i],
                               self.input_layer: input_data,
                               self.labels: list_label}
                )

    # Prepares the data so it can be used as input by the machine learning model
    def prepare_data(self, index):
        input_data = self.df.iloc[[index]].values.tolist()[0]
        self.add_complements(input_data)
        input_data = [input_data]
        label = self.df_labels.iloc[[index]]
        list_label = self.create_label_list(label)
        list_label = [list_label]
        return input_data, list_label

    # Prepares the test data so it can be used as input by the machine learning model
    def prepare_test_data(self, index):
        input_data = self.test_df.iloc[[index]].values.tolist()[0]
        self.add_complements(input_data)
        input_data = [input_data]
        label = self.test_labels.iloc[[index]]
        list_label = self.create_label_list(label)
        list_label = [list_label]
        return input_data, list_label

    # Prepares the data in order to predict its pattern
    def prepare_prediction_data(self, pattern):
        self.add_complements(pattern)
        pattern = [pattern]
        return pattern

    # Creates a list out of the label
    def create_label_list(self, label):
        list_label = np.zeros(12)
        list_label[label - 1] = 1
        return list_label

    # Normalizes the input
    def normalize_pattern(self, pattern):
        mini = min(pattern)
        maxi = max(pattern)
        diff = maxi - mini

        for i in range(len(pattern)):
            pattern[i] = (pattern[i] - mini)/diff

    # Adds the complements to 1 of the 10 points to the list
    def add_complements(self, line):
        length = len(line)
        for i in range(length):
            line.append(1 - line[i])

    # Save model to a file
    def save_model(self, file_path):
        self.saver.save(self.sess, file_path)

    # Restore model from a file
    def restore_model(self, file_path):
        self.saver.restore(self.sess, file_path)


ml_model = model(20, 12)
# ml_model.train_model()
# ml_model.save_model("models/model_1_weights")
