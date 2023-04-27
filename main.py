import os
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate

DATA_DIR = "data/"

WIDTH = 10
HEIGHT = 5

keep = ['Project', 'Start date', 'Start time', 'End date', 'End time', 'Duration', 'Tags']
def create_df(path):
    # creates empty dataframe
    data_frame = pd.DataFrame(columns=keep)

    # gets complete path to directory of excel files
    dirname = os.getcwd()
    directory = os.path.join(dirname, path)
    for filename in os.listdir(directory):
        # ignores hidden and temp
        if not filename.startswith('.') and not filename.startswith('~'):
            # complete path to excel file
            f = os.path.join(directory, filename)
            if os.path.isfile(f):
                
                # saves current excel sheet as dataframe
                current_sheet = pd.DataFrame(pd.read_csv(f))
                current_sheet = current_sheet[keep]

                # adds current sheet to final data frame
                data_frame = pd.concat([data_frame, current_sheet], ignore_index=True)
                print(data_frame)
                data_frame['Start date'] = pd.to_datetime(data_frame['Start date'])
                data_frame['Start time'] = pd.to_datetime(data_frame['Start time'], format='%H:%M:%S')
                data_frame['End date'] = pd.to_datetime(data_frame['End date'])
                data_frame['End time'] = pd.to_datetime(data_frame['End time'], format='%H:%M:%S')


    return data_frame


# instantiate argument parser
parser = argparse.ArgumentParser()

# define arguments
parser.add_argument("--heatmap", help="output heatmap of time entries", action="store_true")
args = parser.parse_args()

# create dataframe from excel files in \data directory
df = create_df(DATA_DIR)


if args.heatmap:
    show_heatmap(df)

print(df.info())

plt.show()
