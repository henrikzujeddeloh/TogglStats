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

# specifies which columns of csv file to keep
keep = ['Project', 'Start date', 'Start time', 'End date', 'End time', 'Duration', 'Tags']



def create_df(path):
    # creates empty dataframe
    data_frame = pd.DataFrame(columns=keep)

    # gets complete path to directory of csv files
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

    # formats start and end dates and times as well as duration in minutes
    data_frame['Start date'] = pd.to_datetime(data_frame['Start date'])
    data_frame['Start time'] = pd.to_datetime(data_frame['Start time'], format='%H:%M:%S')
    data_frame['End date'] = pd.to_datetime(data_frame['End date'])
    data_frame['End time'] = pd.to_datetime(data_frame['End time'], format='%H:%M:%S')
    data_frame['Duration'] = data_frame['Duration'].str.split(':').apply(lambda x: int(x[0]) * 60 + int(x[1]))
    return data_frame




def show_heatmap(data_frame):
    # creates new dataframe hours and weekdays of time entries for every day
    weekday_hour = pd.DataFrame(columns=('date', 'weekday', 'hour'))
    
    # loops through every time entry
    for index, row in data_frame.iterrows():
        weekday = row['Start date'].day_name()
        # if time entry starts and ends in same hour it just adds one entry
        if row['Start time'].hour == row['End time'].hour:
            hour = row['Start time'].hour
            new_row = [row['Start date'], weekday, hour]
            weekday_hour.loc[len(weekday_hour.index)] = new_row

        # if time entry spans over multiple hours, it creates multiple entries
        else:
            # adds new row for each hour of time entry
            for h in range(row['Start time'].hour, row['End time'].hour+1):
                #print("multiple hours! " + "Start Hour: " + str(row['Start time'].hour) + " End Hour: " + str(row['End time'].hour) + " Hour Added: " + str(h))
                new_row = [row['Start date'], weekday, h]
                weekday_hour.loc[len(weekday_hour.index)] = new_row
    
    # removes double entries per hour for one day
    weekday_hour = weekday_hour.drop_duplicates()
    
    # sorts dataframe by day of week
    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday_hour['weekday'] = pd.Categorical(weekday_hour['weekday'], categories=week_days, ordered=True)
    weekday_hour = weekday_hour.sort_values('weekday')
    weekday_hour = weekday_hour.groupby(["weekday", "hour"]).size().unstack()

    # outpus heatmap
    fig_heatmap, axs_heatmap = plt.subplots(figsize=[WIDTH,HEIGHT])
    sns.heatmap(weekday_hour, cmap="Blues", ax=axs_heatmap)
    axs_heatmap.set_title("Focus Heatmap")





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
