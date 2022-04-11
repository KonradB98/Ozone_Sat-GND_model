import numpy as np
import pandas as pd
import pathlib
from math import radians, cos, sin, asin, sqrt

PDP = pathlib.Path(__file__).parents[0]
SAT_DAT = PDP.joinpath('data/Lisbon/sat/Ozone_S5P.csv')
GND_DAT = PDP.joinpath('data/Lisbon/gnd/Lisbon_GND_2019_All.csv')
SAMP_DAT = PDP.joinpath('data/Lisbon/gnd/Lisbon_Samp_Points.csv')

"""
Function for calculating distance between 2 points on earth borrowed from:
https://www.geeksforgeeks.org/program-distance-two-points-earth/
"""
def calculateDistance(lon_x, lat_x, lon_y, lat_y):
    # convert longitudes and latitudes to radians
    lon_x = radians(lon_x)
    lat_x = radians(lat_x)
    lon_y = radians(lon_y)
    lat_y = radians(lat_y)
    # calculate distance between lon and lats (Haversine formula)
    d_lon = lon_y - lon_x
    d_lat = lat_y - lat_x
    x = sin(d_lat / 2)**2 + cos(lat_x) * cos(lat_y) * sin(d_lon / 2)**2
    c = 2 * asin(sqrt(x))
    # earth radius [km]
    r = 6371
    # convert output to km
    d_km = c * r
    return d_km

"""
Function for fitting satellite data (pixels) to Ground Stations coordinates
"""
def fitSatGndCoord():
    # read satellite data to data frame
    satDf = pd.read_csv(SAT_DAT)
    # read ground stations metadata (SamplePoint, Longitude, Latitude)
    sampDf = pd.read_csv(SAMP_DAT)
    # create dictionary for output data (
    fitDict = {'samplingpoint': [], 'time': [], 'lon_pix': [], 'lat_pix': [], 'total_ozone_column': [], \
               'total_ozone_column_prec': [], 'q_a': [], 'sp_distance_km': []}
    # for every ground station (SamplePoint)
    for i in range(len(sampDf)):
        # get coordinates of SamplePoint
        spLon = sampDf.loc[i, "Longitude"]
        spLat = sampDf.loc[i, "Latitude"]
        # for every row in satellite data
        for j in range(len(satDf)):
            # get coordinates of center pixel
            pxLon = satDf.loc[j, "pixel center longitude (degrees_east)"]
            pxLat = satDf.loc[j, "pixel center latitude (degrees_north)"]
            # calculate distance between SamplePoint and pixel
            d_sp_px = calculateDistance(spLon, spLat, pxLon, pxLat)
            # if calculated distance less than 7 km
            if d_sp_px <= 7:
                # write data to dictionary
                fitDict['samplingpoint'].append(sampDf.loc[i, "SamplingPoint"])
                fitDict['time'].append(satDf.loc[j, "Time"])
                fitDict['lon_pix'].append(pxLon)
                fitDict['lat_pix'].append(pxLat)
                fitDict['total_ozone_column'].append(satDf.loc[j, "total ozone column (mol m-2)"])
                fitDict['total_ozone_column_prec'].append(satDf.loc[j, "total ozone column random error (mol m-2)"])
                fitDict['q_a'].append(satDf.loc[j, "data quality value (1)"])
                fitDict['sp_distance_km'].append(d_sp_px)
    # convert dictionary to data frame
    fitDf = pd.DataFrame.from_dict(fitDict)
    # write to csv file
    fitDf.to_csv(PDP.joinpath('data/Lisbon/Gnd_Sat_fit.csv'))


if __name__ == "__main__":
    print("Hello")
    # fitSatGndCoord()



