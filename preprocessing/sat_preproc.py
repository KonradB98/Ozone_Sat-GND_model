import numpy as np
import netCDF4 as nc
import os
import pandas as pd
import pathlib
from datetime import datetime

PDP = pathlib.Path(__file__).parents[0]
LISBON_COORDINATES_DICT = {'lon_left': -9.5361328125, 'lon_right': -7.789306640625, 'lat_up': 39.55911824217184, 'lat_down': 37.792422407988575}
FILE_PATH_LISBON = pathlib.Path(__file__).parents[1].joinpath('download/data/Lisbon/sat/')

def readNetCDFLisbon():
    for f in os.listdir(FILE_PATH_LISBON):
        print(f)
        ds = nc.Dataset(FILE_PATH_LISBON.joinpath(f), mode='r')
        # latitudes
        lat = np.array(ds.groups['PRODUCT'].variables['latitude'][0])
        # longitudes
        lon = np.array(ds.groups['PRODUCT'].variables['longitude'][0])
        # range of indexes where data regarding Lisbon occurs
        xRange, yRange = np.where(
            (lon >= LISBON_COORDINATES_DICT['lon_left']) & (lon <= LISBON_COORDINATES_DICT['lon_right']) & \
            (lat >= LISBON_COORDINATES_DICT['lat_down']) & (lat <= LISBON_COORDINATES_DICT['lat_up']))
        t = ds.groups['PRODUCT'].variables['time_utc']
        # print(f"Min xRange: {min(xRange)}, Max xRange: {max(xRange)}")
        print('time_utc:')
        print(t[0, min(xRange):max(xRange)])

def s5pSingleFilePreProc():
    """
    Read single file
    """
    print(FILE_PATH_LISBON)
    fn = os.listdir(FILE_PATH_LISBON)[1]
    ds = nc.Dataset(FILE_PATH_LISBON.joinpath(fn), mode='r')
    print(fn)
    print(ds.time_coverage_start)
    """
    PRODUCTS VARIABLES
    """
    # latitudes
    lat = np.array(ds.groups['PRODUCT'].variables['latitude'][0])
    # longitudes
    lon = np.array(ds.groups['PRODUCT'].variables['longitude'][0])
    # range of indexes where data regarding Lisbon occurs
    xRange, yRange = np.where((lon >= LISBON_COORDINATES_DICT['lon_left']) & (lon <= LISBON_COORDINATES_DICT['lon_right']) & \
                             (lat >= LISBON_COORDINATES_DICT['lat_down']) & (lat <= LISBON_COORDINATES_DICT['lat_up']))
    # ozone measurements - Total Ozone Column (TOC)
    o3 = np.array(ds.groups['PRODUCT'].variables['ozone_total_vertical_column'][0])
    # ozone measurements precision
    o3_prec = ds.groups['PRODUCT'].variables['ozone_total_vertical_column_precision'][0]
    # data quality value
    qa = ds.groups['PRODUCT'].variables['qa_value'][0]
    # dictionary for desired variables for preprocessing
    LisboaDict = {'longitude': [], 'latitude':[], 'qa_value':[], 'ozone_total_vertical_column': [], 'ozone_total_vertical_column_precision': [], 'x': [], 'y':[]}
    # range of indexes where data regarding Lisbon occurs
    xRange, yRange = np.where((lon >= LISBON_COORDINATES_DICT['lon_left']) & (lon <= LISBON_COORDINATES_DICT['lon_right']) & \
                             (lat >= LISBON_COORDINATES_DICT['lat_down']) & (lat <= LISBON_COORDINATES_DICT['lat_up']))
    for i in range(min(xRange), max(xRange)+1):
        for j in range(min(yRange), max(yRange)+1):
            if lon[i, j] >= LISBON_COORDINATES_DICT['lon_left'] and lon[i, j] <= \
                            LISBON_COORDINATES_DICT['lon_right'] and lat[i, j] >= LISBON_COORDINATES_DICT[
                        'lat_down'] and lat[i, j] <= LISBON_COORDINATES_DICT['lat_up']:
                LisboaDict['longitude'].append(lon[i, j])
                LisboaDict['latitude'].append(lat[i, j])
                LisboaDict['ozone_total_vertical_column'].append(o3[i, j])
                LisboaDict['ozone_total_vertical_column_precision'].append(o3_prec[i, j])
                LisboaDict['qa_value'].append(qa[i, j])
                LisboaDict['x'].append(i)
                LisboaDict['y'].append(j)
    vars_df = pd.DataFrame.from_dict(LisboaDict)
    vars_df.to_csv(PDP.joinpath('data/Lisbon/sat/test_Lisbon.csv'))

if __name__ == "__main__":
    readNetCDFLisbon()
    # s5pSingleFilePreProc()



