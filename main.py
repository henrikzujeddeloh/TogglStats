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
    data_frame['Start date'] = pd.to_datetime(data_frame['Start date'])
    data_frame['Start time'] = pd.to_datetime(data_frame['Start time'], format='%H:%M:%S')
    data_frame['End date'] = pd.to_datetime(data_frame['End date'])
    data_frame['End time'] = pd.to_datetime(data_frame['End time'], format='%H:%M:%S')
    data_frame['Duration'] = data_frame['Duration'].str.split(':').apply(lambda x: int(x[0]) * 60 + int(x[1]))
    return data_frame

def show_heatmap(data_frame):
    length = len(data_frame.index)
    weekday_hour = pd.DataFrame(columns=('weekday', 'hour'))
    for index, row in data_frame.iterrows():
        weekday = row['Start date'].day_name()
        if row['Start time'].hour == row['End time'].hour:
            hour = row['Start time'].hour
            new_row = [weekday, hour]
            weekday_hour.loc[len(weekday_hour.index)] = new_row
        else:
            for h in range(row['Start time'].hour, row['End time'].hour+1):
                print("multiple hours! " + "Start Hour: " + str(row['Start time'].hour) + " End Hour: " + str(row['End time'].hour) + " Hour Added: " + str(h))
                new_row = [weekday, h]
                weekday_hour.loc[len(weekday_hour.index)] = new_row


    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday_hour['weekday'] = pd.Categorical(weekday_hour['weekday'], categories=week_days, ordered=True)
    weekday_hour = weekday_hour.sort_values('weekday')
    
    weekday_hour = weekday_hour.groupby(["weekday", "hour"]).size().unstack()
    print(weekday_hour)

    fig_heatmap, axs_heatmap = plt.subplots(figsize=[WIDTH,HEIGHT])
    sns.heatmap(weekday_hour, cmap="Blues", ax=axs_heatmap)
    axs_heatmap.set_title("Message Heatmap")

# instantiate argument parser
parser = argparse.ArgumentParser()

# define arguments
parser.add_argument("--heatmap", help="output heatmap of time entries", action="store_true")
args = parser.parse_args()

# create dataframe from excel files in \data directory
df = create_df(DATA_DIR)
print(df)

if args.heatmap:
    show_heatmap(df)

print(df.info())

plt.show()
