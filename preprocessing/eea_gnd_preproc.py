import os
import pandas as pd
import pathlib

PDP = pathlib.Path(__file__).parents[0]
METADATA = pathlib.Path(__file__).parents[1].joinpath('download/data/Lisbon/gnd/Metadata_EEA_gnd_stations.csv')
LISBON_GND_FILE_PATH = pathlib.Path(__file__).parents[1].joinpath('download/data/Lisbon/gnd/2019/')

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
    gndDf = pd.concat(dfl, axis=0, ignore_index=True)
    # print(gndDf['DatetimeBegin'])
    """
    Merge Metadata and Ground Station data
    """
    # merge ground station data with metadata
    mergedDf = gndDf.merge(uniqMetDf, how='left', on='SamplingPoint')
    # write data to csv file
    mergedDf.to_csv(PDP.joinpath('data/Lisbon/gnd/Lisbon_GND_2019_All.csv'))

if __name__ == "__main__":
    eeaFilesPerProc()




