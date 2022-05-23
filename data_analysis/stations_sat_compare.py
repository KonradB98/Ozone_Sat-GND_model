import numpy as np
import os
import pandas as pd
import pathlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

PDP = pathlib.Path(__file__).parents[0]
GND_SAT_DATA = pathlib.Path(__file__).parents[1].joinpath('preprocessing/data/Lisbon/Gnd_Sat_merge_v2_finale.csv')

def plotRawDataforSingleStation():
    # read CSV file with fitted data (satellite date to ground stations data)
    gnd_sat_df = pd.read_csv(GND_SAT_DATA)
    # divide data per ground station (SamplingPoint) and create list of DFs
    df_list = [df for _, df in gnd_sat_df.groupby(['SamplingPoint'])]
    # for every ground station (SamplingPoint) in the list
    for station in df_list:
        # convert 'SAT_time' (object) field to datatime field
        station['SAT_time'] = pd.to_datetime(station['SAT_time'])
        # set index based on measure time
        station = station.set_index('SAT_time')
        # create multiple plots on one figure
        fig, ax1 = plt.subplots()
        # plot ground measurements data
        l1 = ax1.plot(station['GND_mea_val'], label='Stacja Naziemna', color='tab:blue')
        # create twin axes (one for ground measurements, one for satellite measurements) -> different units for both
        ax2 = ax1.twinx()
        # plot satellite data
        l2 = ax2.plot(station['SAT_mea_val'], label='TROPOMI', color='tab:red')
        # add those two lines
        lines = l1 + l2
        # get labels of this lines
        labels = [l.get_label() for l in lines]
        # add labels to the legend
        ax1.legend(lines, labels, loc=0)
        # set X axis label
        ax1.set_xlabel('Data')
        # set label of 1st Y axis (ground measurements)
        ax1.set_ylabel('$O_3$ µg/m3', color='tab:blue')
        # color 1st Y axis
        ax1.tick_params(axis='y', labelcolor='tab:blue')
        # set label of 2nd Y axis (satellite measurements)
        ax2.set_ylabel('$O_3$ mol/m2', color='tab:red')
        # color 2nd Y axis
        ax2.tick_params(axis='y', labelcolor='tab:red')
        # set title of the chart as ground station name (ID)
        plt.title(station['SamplingPoint'].iloc[0])
        # save figure in proper location
        plt.savefig(PDP.joinpath(f"one_to_one_compare/{station['SamplingPoint'].iloc[0]}_1to1.png"), dpi=200)

def calculateStatistics():
    # read CSV file with fitted data (satellite date to ground stations data)
    gnd_sat_df = pd.read_csv(GND_SAT_DATA)
    # divide data per ground station (SamplingPoint) and create list of DFs
    df_list = [df for _, df in gnd_sat_df.groupby(['SamplingPoint'])]
    # for every ground station (SamplingPoint) in the list
    for station in df_list:
        d = {'Statistic name': ['mean', 'variance', 'std', 'relative std [%]', 'min', 'max', 'skewness'],
             'Satellite measurements':
            [station['SAT_mea_val'].mean(), station['SAT_mea_val'].var(), station['SAT_mea_val'].std(), (station['SAT_mea_val'].std()/station['SAT_mea_val'].mean()*100),
             station['SAT_mea_val'].min(), station['SAT_mea_val'].max(), station['SAT_mea_val'].skew()],
             'Ground stations measurements':
                 [station['GND_mea_val'].mean(), station['GND_mea_val'].var(), station['GND_mea_val'].std(), (station['GND_mea_val'].std()/station['GND_mea_val'].mean()*100),
                  station['GND_mea_val'].min(), station['GND_mea_val'].max(), station['GND_mea_val'].skew()]
             }
        df = pd.DataFrame(data=d)
        print(f"{station['SamplingPoint'].iloc[0]}\n")
        print(f"{df}\n")

if __name__ == "__main__":
    # plotRawDataforSingleStation()
    calculateStatistics()
