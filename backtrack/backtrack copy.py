from sklearn import preprocessing
import matplotlib.pyplot as plt
import csv
import numpy as np

from silverOhlcv import silverOhlcv


class dataToolkit:
    def __init__(self):
        self.db = silverOhlcv()
        self.data = self.db.read_all_data("1d").copy()
        self.data_close = self.data['close']

    # Iterates over all the available patterns in the database
    def iterate_patterns(self):
        for i in range(len(self.data.index) - 1, 0, -1):
            if i - 9 >= 0:
                self.find_pattern(i)

    # Finds a pattern formed by local minimums and maximums and plots it onto a graph
    def find_pattern(self, index):

        # Initializes a line that will be appended to the csv file
        csv_line = [index, self.data_close[index]]

        # Initializes the pattern and pattern index lists with the first element of the list
        pattern = [self.data_close[index]]
        pattern_index = [self.data.index[index]]

        # Appends the next 9 points to the lists
        for i in range(index - 1, index - 10, -1):
            pattern_index.append(self.data.index[i])
            pattern.append(self.data_close[i])
            csv_line.append(self.data_close[i])

        # Writes the line to the csv file
        with open('data_1d.csv', 'a', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(csv_line)
            csvFile.close()

        # Normalizes the pattern in order to create the plot
        self.normalize_pattern(pattern)
        plt.plot(range(10), pattern)
        plt.yticks(np.arange(0, 1.1, step=0.1))
        plt.xticks(np.arange(0, 11, step=1))
        plt.grid(True)
        plt.xlabel(str(pattern_index[0]) + ' - ' + str(pattern_index[len(pattern_index) - 1]))
        plt.savefig(str(index)+'.png')
        plt.cla()
        plt.clf()

    # Normalizes the pattern so it is contained within the (0, 1) interval
    # Same as formula 6 in the research paper
    def normalize_pattern(self, pattern):
        mini = min(pattern)
        maxi = max(pattern)
        diff = maxi - mini

        for i in range(len(pattern)):
            pattern[i] = (pattern[i] - mini)/diff

    # Creates the training set that will be used by the machine learning model, using the csv file with labeled data
    def create_training_set(self):

        # Splits the file into rows and each row into cells
        with open('data_1d.csv') as file:
            lists = [line.split(',') for line in file]

        # Cleans the header of the csv
        header = lists.pop(0)
        del header[0]
        header[len(header) - 1] = header[len(header) - 1].rstrip('\n')

        # Adds the header to the csv file
        with open('model_1d_data.csv', 'a', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(header)
            csvFile.close()

        # Iterates over all the rows
        for lis in lists:

            # Removes trailing new lines
            lis[len(lis) - 1] = lis[len(lis) - 1].rstrip('\n')

            # Removes the index the pattern was found at, as it is not needed
            del lis[0]

            # Filters the labeled data from the not labeled one
            if len(lis[len(lis) - 1]) > 0:

                # Removes the 'P' in the label
                label = lis.pop(len(lis) - 1)[1:]

                float_list = [float(i) for i in lis]
                self.normalize_pattern(float_list)
                float_list.append(label)
                with open('model_1d_data.csv', 'a', newline='') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow(float_list)
                    csvFile.close()

#
dataToolkit = dataToolkit()
dataToolkit.iterate_patterns()
# dataToolkit.create_training_set()