import numpy as np
import pandas as pd
import os
import pathlib
import netCDF4 as nc
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

"""
For this program Basemap library is required which ia available on Anaconda environment
"""

PDP = pathlib.Path(__file__).parents[0]
SAT_DIR = PDP.joinpath('data\Lisbon\sat')
LISBON_COORDINATES_DICT = {'lon_left': -9.5361328125, 'lon_right': -7.789306640625, 'lat_up': 39.55911824217184, 'lat_down': 37.792422407988575}
GND_SAT_DATA = pathlib.Path(__file__).parents[1].joinpath('preprocessing/data/Lisbon/Gnd_Sat_merge_v2_finale.csv')
GND_STATIONS = pathlib.Path(__file__).parents[1].joinpath('preprocessing/data/Lisbon/gnd/Lisbon_Samp_Points.csv')

"""
This function creates colorful map of Lisbon based on satelite measurements
"""
def satDataMap():
    # list of all satellite data files within folder
    files = os.listdir(SAT_DIR)
    # .nc files with the absolute path
    fwp = [str(SAT_DIR)+"/"+file for file in files]
    # specify file
    fn = fwp[0]
    # read netcdf
    ds = nc.Dataset(fn, mode='r')
    # latitudes
    lats = np.array(ds.groups['PRODUCT'].variables['latitude'][0])
    # longitudes
    lons = np.array(ds.groups['PRODUCT'].variables['longitude'][0])
    # range of indexes where Lisbon data occurs
    xRange, yRange = np.where((lons >= LISBON_COORDINATES_DICT['lon_left']) & (lons <= LISBON_COORDINATES_DICT['lon_right']) & \
                             (lats >= LISBON_COORDINATES_DICT['lat_down']) & (lats <= LISBON_COORDINATES_DICT['lat_up']))
    # take only latitudes from calculated range of indexes (latitudes from Lisbon area)
    lats = lats[min(xRange):max(xRange)+1, min(yRange):max(yRange)+1]
    # take only longitudes from calculated range of indexes (longitudes from Lisbon area)
    lons = lons[min(xRange):max(xRange)+1, min(yRange):max(yRange)+1]
    # take only ozone data from calculated range of indexes (ozone data from Lisbon area)
    o3 = ds.groups['PRODUCT'].variables['ozone_total_vertical_column'][0][min(xRange):max(xRange)+1, min(yRange):max(yRange)+1]
    # define satellite measurements units
    o3_units = "DU"

    print(len(lons), len(lats))
    # calculate average of longitudes and latitudes (middle point of the map)
    lon_0 = lons.mean()
    lat_0 = lats.mean()

    # create map from Basemap library
    m = Basemap(projection='stere',
                 llcrnrlon=LISBON_COORDINATES_DICT['lon_left'],
                 llcrnrlat=LISBON_COORDINATES_DICT['lat_down'],
                 urcrnrlon=LISBON_COORDINATES_DICT['lon_right'],
                 urcrnrlat=LISBON_COORDINATES_DICT['lat_up'],
                 resolution='i',
                 lat_0=lat_0, lon_0=lon_0)

    xi, yi = m(lons, lats)

    # plot colorful map (color of pixel is based on measurement)
    cs = m.pcolor(xi, yi, np.squeeze(o3), cmap='jet')
    # add coastlines, countries and states
    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()

    # add legend (colorbar)
    cbar = m.colorbar(cs, location='right')
    cbar.set_label(f"$O_3$ [${o3_units}$]")

    # plot chart
    plt.title("Pomiary satelitarne ozonu")
    plt.show()

"""
This function creates map of colorful points which represents o3 measurements of each ground station
"""
def gndDataMap():
    # read CSV file with fitted data (satellite date to ground stations data), merge with metadata file with ground stations coordinates
    gnd_sat_df = pd.read_csv(GND_SAT_DATA)
    sp_df = pd.read_csv(GND_STATIONS)
    gnd_sat_df = pd.merge(gnd_sat_df, sp_df, on='SamplingPoint')
    # divide data per ground station (SamplingPoint) and create list of DFs
    df_list = [df for _, df in gnd_sat_df.groupby(['SamplingPoint'])]
    # create lists of longitudes, latitudes and ozone data
    lons = []
    lats = []
    o3 = []
    # for every ground station in list
    for station in df_list:
        # convert "object" data type to datetime type
        station['SAT_time'] = pd.to_datetime(station['SAT_time'], format='%Y-%m-%d %H:%M:%S')
        # take data (rows of data) only from specified period of time
        filtered_df = station.loc[(station['SAT_time'] >= '2019-08-01') & (station['SAT_time'] < '2019-08-08')]
        # take longitude, latitude of ground station
        lons.append(filtered_df['Longitude'].iloc[0])
        lats.append(filtered_df['Latitude'].iloc[0])
        # calculate average value of o3 measurements within specified time window
        o3.append(filtered_df['GND_mea_val'].mean())
    # convert lists into numpy arrays
    lons = np.array(lons)
    lats = np.array(lats)
    o3 = np.array(o3)
    # define ground measurements units
    o3_units = "µg/m3"

    # calculate average of longitudes and latitudes (middle point of the map)
    lon_0 = lons.mean()
    lat_0 = lats.mean()

    # create map from Basemap library
    m = Basemap(projection='stere',
                 llcrnrlon=LISBON_COORDINATES_DICT['lon_left'],
                 llcrnrlat=LISBON_COORDINATES_DICT['lat_down'],
                 urcrnrlon=LISBON_COORDINATES_DICT['lon_right'],
                 urcrnrlat=LISBON_COORDINATES_DICT['lat_up'],
                 resolution='i',
                 lat_0=lat_0, lon_0=lon_0)

    # plot colorful points on the map (one point for one ground station)
    cs = m.scatter(lons, lats, latlon=True,
                   c=o3, cmap='jet')

    # add coastlines, countries and states
    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()

    # add legend (colorbar)
    cbar = m.colorbar(cs, location='right')
    cbar.set_label(f"$O_3$ [${o3_units}$]")

    # plot chart
    plt.title("Pomiary naziemne ozonu")
    plt.show()


if __name__ == "__main__":
    satDataMap()
    # gndDataMap()

