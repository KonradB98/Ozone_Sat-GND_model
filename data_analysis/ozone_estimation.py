import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
import pathlib

PDP = pathlib.Path(__file__).parents[0]
LISBON_COORDINATES_DICT = {'lon_left': -9.5361328125, 'lon_right': -7.789306640625, 'lat_up': 39.55911824217184, 'lat_down': 37.792422407988575}
GND_SAT_DATA = pathlib.Path(__file__).parents[1].joinpath('preprocessing/data/Lisbon/Gnd_Sat_merge_v2_finale.csv')
GND_STATIONS = pathlib.Path(__file__).parents[1].joinpath('preprocessing/data/Lisbon/gnd/Lisbon_Samp_Points.csv')

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
        # print those values
        print(f"R^2: {rsq}")
        print(f"MSE: {mse}")
        print(f"RMSE: {rmse}\n")
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


if __name__ == "__main__":
    linearRegression()

