import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
import pathlib
import scipy.stats

PDP = pathlib.Path(__file__).parents[0]
LISBON_COORDINATES_DICT = {'lon_left': -9.5361328125, 'lon_right': -7.789306640625, 'lat_up': 39.55911824217184, 'lat_down': 37.792422407988575}
GND_SAT_DATA = pathlib.Path(__file__).parents[1].joinpath('preprocessing/data/Lisbon/Gnd_Sat_merge_v2_finale.csv')
GND_STATIONS = pathlib.Path(__file__).parents[1].joinpath('preprocessing/data/Lisbon/gnd/Lisbon_Samp_Points.csv')
RAW_SAT_DATA = pathlib.Path(__file__).parents[1].joinpath('preprocessing/data/Lisbon/sat/Ozone_S5P.csv')
RAW_GND_DATA = pathlib.Path(__file__).parents[1].joinpath('preprocessing/data/Lisbon/gnd/Lisbon_GND_2019_All_with_TW.csv')

def linearRegression():
    # read CSV file with fitted data (satellite date to ground stations data)
    gnd_sat_df = pd.read_csv(GND_SAT_DATA)
    # divide data per ground station (SamplingPoint) and create list of DFs
    df_list = [df for _, df in gnd_sat_df.groupby(['SamplingPoint'])]
    # for every ground station
    for df in df_list:
        # create scikit learn linear regression object
        reg = linear_model.LinearRegression()
        # calculate linear regression (ground measurement - Independent var, satellite data - dependent var)
        reg.fit(df[['GND_mea_val']], df.SAT_mea_val)
        # calculate R2 value (compare distance between actual values and mean (actual - mean) with estimated values with the mean (estimated - mean)
        rsq = reg.score(df[['GND_mea_val']], df.SAT_mea_val)
        # calculate mean squared error
        mse = mean_squared_error(df[['GND_mea_val']], df.SAT_mea_val)
        # calculate root mean squared error
        rmse = np.sqrt(mse)
        # calculate Pearson's correlation
        p_c, p_p = scipy.stats.pearsonr(list(df['GND_mea_val']), list(df['SAT_mea_val']))
        # calculate Spearman’s correlation
        s_c, s_p = scipy.stats.spearmanr(list(df['GND_mea_val']), list(df['SAT_mea_val']))
        # print those values
        print(f"#----------------GROUND STATION: {df['SamplingPoint'].iloc[0]}----------------#")
        print("LINEAR REGRESSION STATS:")
        print(f"R^2: {rsq}")
        print(f"MSE: {mse}")
        print(f"RMSE: {rmse}")
        print("CORRELATION STATS:")
        print(f"Pearson's correlation: Pearson’s correlation coefficient: {p_c},\t p-value: {p_p}")
        print(f"Spearman’s correlation: Spearman’s correlation coefficient: {s_c},\t p-value: {s_p}\n")
        # plot ground measurements vs satellite measurements on scatter plot
        plt.scatter(df.GND_mea_val, df.SAT_mea_val, color="c", marker=".")
        # draw regression line
        plt.plot(list(df['GND_mea_val']), reg.predict(df[['GND_mea_val']]), "r:", label=f"y={round(reg.coef_[0], 5)}x+{round(reg.intercept_, 5)}")
        # add plot title
        plt.title(df['SamplingPoint'].iloc[0])
        # add axes labels
        plt.ylabel("TROPOMI [$mol/m^2$]")
        plt.xlabel("Stacja Naziemna [$µg/m^3$]")
        # display legend
        plt.legend()
        # show chart
        plt.show()

def rawDataLinReg():
    # read CSVs
    sat_df = pd.read_csv(RAW_SAT_DATA)
    gnd_df = pd.read_csv(RAW_GND_DATA)
    print(f"readed sat data shape: {sat_df.shape[0]}")
    print(f"readed gnd data shape: {gnd_df.shape[0]}")
    print(f"Nulls within sat data: {sat_df['total ozone column (mol m-2)'].isnull().sum()}")
    print(f"Nulls within gnd data {gnd_df['Concentration'].isnull().sum()}")
    sat_df = sat_df[sat_df['total ozone column (mol m-2)'].notna()]
    gnd_df = gnd_df[gnd_df['Concentration'].notna()]
    print(f"sat data shape without nulls: {sat_df.shape[0]}")
    print(f"gnd data shape without nulls: {gnd_df.shape[0]}")
    sat_df = sat_df.loc[sat_df['data quality value (1)'] >= 0.5]
    gnd_df = gnd_df.loc[gnd_df['Validity'] == 1]
    print(f"range of sat data quality values: {sat_df['data quality value (1)'].unique()}")
    print(f"range of gnd data quality values: {gnd_df['Validity'].unique()}")
    print(f"sat data shape with proper quality: {sat_df.shape[0]}")
    print(f"gnd data shape with proper quality: {gnd_df.shape[0]}")

    reg = linear_model.LinearRegression()
    reg.fit(gnd_df[['Concentration']], sat_df['total ozone column (mol m-2)'])




if __name__ == "__main__":
    linearRegression()
    # rawDataLinReg()

