import os
import pandas as pd
import pathlib
import datetime

PDP = pathlib.Path(__file__).parents[0]
METADATA = pathlib.Path(__file__).parents[1].joinpath('download/data/Lisbon/gnd/Metadata_EEA_gnd_stations.csv')
LISBON_GND_FILE_PATH = pathlib.Path(__file__).parents[1].joinpath('download/data/Lisbon/gnd/2019/')
MEASUREMENTS_TIME_WINDOW = {'tw_begin': 12, 'tw_end': 14}
MEASUREMENTS_TIME_WINDOW_WITH_BUFFER = {'tw_begin': 10, 'tw_end': 16}

"""
Reading ozone data from ground stations and merge with ground stations metadata 
"""
def eeaFilesPerProc():
    """
    EEA Ground Stations METADATA
    """
    # read csv file
    metDf = pd.read_csv(METADATA, usecols=['SamplingPoint', 'Longitude', 'Latitude', 'BuildingDistance'])
    # remove duplicates records
    uniqMetDf = metDf.drop_duplicates(subset='SamplingPoint', keep='first')
    """
    Lisbon Ground Stations Files
    """
    # list of dataframes
    dfl = []
    # for filename in gndLisbonFiles:
    for filename in os.listdir(LISBON_GND_FILE_PATH):
        # read each file and select desired columns
        stationDf = pd.read_csv(LISBON_GND_FILE_PATH.joinpath(filename), usecols=['SamplingPoint', 'AirPollutant', 'Concentration', 'UnitOfMeasurement',
                                                   'DatetimeBegin', 'DatetimeEnd', 'Validity'], index_col=None, header=0)
        # convert datetimes to UTC and remove timezone info
        stationDf['DatetimeBegin'] = pd.to_datetime(stationDf['DatetimeBegin'], utc=True).astype(str).str[:-6]
        stationDf['DatetimeEnd'] = pd.to_datetime(stationDf['DatetimeEnd'], utc=True).astype(str).str[:-6]
        # append to dfs to list
        dfl.append(stationDf)
    # concatenate data frames into single one
    gndDf = pd.concat(dfl, axis=0)
    """
    Merge Metadata and Ground Station data
    """
    # merge ground station data with metadata
    mergedDf = gndDf.merge(uniqMetDf, how='left', on='SamplingPoint')
    # write data to csv file
    mergedDf.to_csv(PDP.joinpath('data/Lisbon/gnd/Lisbon_GND_2019_All.csv'))

"""
Reading ozone data from ground stations in selected time window 
"""
def eeaFilesPerProcTW():
    """
    EEA Ground Stations METADATA
    """
    # read csv file
    metDf = pd.read_csv(METADATA, usecols=['SamplingPoint', 'Longitude', 'Latitude', 'BuildingDistance'])
    # remove duplicates records
    uniqMetDf = metDf.drop_duplicates(subset='SamplingPoint', keep='first')
    """
    Lisbon Ground Stations Files
    """
    # list of dataframes
    dfl = []
    # for filename in gndLisbonFiles:
    for filename in os.listdir(LISBON_GND_FILE_PATH):
        # read each file and select desired columns
        stationDf = pd.read_csv(LISBON_GND_FILE_PATH.joinpath(filename), usecols=['SamplingPoint', 'AirPollutant', 'Concentration', 'UnitOfMeasurement',
                                                   'DatetimeBegin', 'DatetimeEnd', 'Validity'], index_col=None, header=0)
        # convert datetimes to UTC and remove timezone info
        stationDf['DatetimeBegin'] = pd.to_datetime(stationDf['DatetimeBegin'], utc=True).astype(str).str[:-6]
        stationDf['DatetimeEnd'] = pd.to_datetime(stationDf['DatetimeEnd'], utc=True).astype(str).str[:-6]
        # convert DatetimeBegin from "object" type to "DataFrame" type
        stationDf.DatetimeBegin = pd.to_datetime(stationDf.DatetimeBegin)
        # set start and end hour of time window
        begin = datetime.time(MEASUREMENTS_TIME_WINDOW['tw_begin'])
        end = datetime.time(MEASUREMENTS_TIME_WINDOW['tw_end'])
        # set index for data frame (required for method: between_time)
        stationDf = stationDf.set_index(['DatetimeBegin'])
        # create new dataframe with data from time window
        nd = stationDf.between_time(begin, end)
        # reset index of new dataframe (allows to concat data frames with 'DatetimeBegin' column)
        nd = nd.reset_index()
        # append reduced data frame to list of data frames
        dfl.append(nd)

    # concatenate data frames into single one
    gndDf = pd.concat(dfl, axis=0)
    # print(gndDf['DatetimeBegin'])
    """
    Merge Metadata and Ground Station data
    """
    # merge ground station data with metadata
    mergedDf = gndDf.merge(uniqMetDf, how='left', on='SamplingPoint')
    # write data to csv file
    mergedDf.to_csv(PDP.joinpath('data/Lisbon/gnd/Lisbon_GND_2019_All_with_TW.csv'))

if __name__ == "__main__":
    print("Hello")
    # eeaFilesPerProc()
    eeaFilesPerProcTW()




