"""A script to plot time series data given a start and end time"""
"""Tom Waldin 18/08/2021"""

# import supporting packages
import numpy as np
from numpy.core.arrayprint import str_format
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
from matplotlib.dates import DateFormatter

# global inputs
TREMOR = "C:/Users/user/OneDrive/Documents/FYP/ruapehu/data/FWVZ_tremor_data.csv"
RAINFALL = "C:/Users/user/OneDrive/Documents/FYP/ruapehu/data/chateau_rain_all.txt"
STORMS = [('2006-04-17 00:00:00', '2006-04-19 00:00:00'),
          ('2006-05-26 00:00:00', '2006-05-28 00:00:00'),
          ('2008-04-14 00:00:00', '2008-04-16 00:00:00'),
          ('2009-04-26 00:00:00', '2009-05-01 00:00:00'),
          ('2010-04-29 00:00:00', '2010-05-01 00:00:00'),
          ('2010-06-05 00:00:00', '2010-06-08 00:00:00'),
          ('2010-12-27 00:00:00', '2010-12-29 00:00:00'),
          ('2011-01-17 00:00:00', '2011-01-20 00:00:00'),
          ('2011-05-25 00:00:00', '2011-05-28 00:00:00'),
          ('2012-03-11 00:00:00', '2012-03-13 00:00:00'),
          ('2014-03-14 00:00:00', '2014-03-18 00:00:00'),
          ('2014-08-01 00:00:00', '2014-08-04 00:00:00'),
          ('2015-02-05 00:00:00', '2015-02-07 00:00:00'),
          ('2015-03-07 00:00:00', '2015-03-09 00:00:00'),
          ('2016-02-16 00:00:00', '2016-02-20 00:00:00'),
          ('2016-03-23 00:00:00', '2016-03-25 00:00:00'),
          ('2017-05-10 00:00:00', '2017-05-13 00:00:00'),
          ('2018-04-15 00:00:00', '2018-04-17 00:00:00'), 
          ('2019-03-31 00:00:00', '2019-04-02 00:00:00')]

def get_data():
    """Function to read csv files and convert relevent columns to datetime objects"""
    tremor_data = pd.read_csv(TREMOR)
    rainfall_data = pd.read_csv(RAINFALL)
    tremor_data['time'] =  pd.to_datetime(tremor_data['time'])  
    rainfall_data['Date(NZST)'] = pd.to_datetime(rainfall_data['Date(NZST)'], format='%Y%m%d:%H%M')
    return tremor_data, rainfall_data

def assign_label_vectors(tremor_data):
    """A function to create label vectors for storm events based on a 20% and 5% threshold of maximum"""

    # create label vector of zeros and empty list of dates
    label_vector_20 = np.zeros(len(tremor_data))
    dates = []

    # for each storm update label vectors
    for start_string, end_string in STORMS:
        
        # convert strings to datetime objects
        storm_start = pd.to_datetime(start_string)
        storm_end = pd.to_datetime(end_string)

        # find max hfF within range and caculate 20% threshold
        tremor_window = tremor_data[(tremor_data['time'] > storm_start) & (tremor_data['time'] < storm_end)]
        max_hfF = tremor_window['hfF'].max()
        percent20 = 0.2 * max_hfF

        # obtain datetimes of 20% storm and update label vector
        window20 = tremor_window[(tremor_window['hfF'] > percent20)]
        idx20 = window20.index
        label_vector_20[idx20] = 1
        
        # create an array of the actual start and end times
        act_start = window20.at[idx20[0], 'time'] 
        act_end = window20.at[idx20[-1], 'time']
        dates.append((act_start, act_end))  

    return label_vector_20, dates

def plot_window(tremor_data, rainfall_data, label_vector, dates):
    """A function to plot time series graphs
    of input data within the relevant time window
    """

    for START, END in dates:
        
        # add 12 hours either side of the start and end
        START -= dt.timedelta(hours=12)
        END += dt.timedelta(hours=12)
        
        # filter the data to the specified time window
        tremor_window = tremor_data[(tremor_data['time'] > START) & (tremor_data['time'] < END)]

        # set font size and date form
        plt.rc('font', size=12) 
        date_form = DateFormatter("%d/%m")
        ticks = pd.date_range(START, END)

        # create plots
        f,axs=plt.subplots(3,1)
        ax1,ax2,ax3=axs

        # dsar plot
        ax1.set_title('{}'.format(str(START)[:4]))
        ax1.plot(tremor_window['time'], tremor_window['dsar'], 'm-', label='dsar', linewidth=0.5)
        ax1.plot(tremor_window['time'], tremor_window['dsarF'], 'r-', label='dsarF', linewidth=0.5)
        ax1.set_ylabel('dsar (\u03bcm/s)')
        ax1.legend(loc='upper left')
        ax1.set_xlim(START, END)
        ax1t = ax1.twinx()
        ax1t.plot(rainfall_data['Date(NZST)'] - dt.timedelta(hours=12), rainfall_data['Amount(mm)'], 'b-', label='rainfall', linewidth=0.5)
        ax1t.plot(tremor_data['time'], 10000*label_vector - 10, 'k--', label='storm bounds',linewidth=0.5)
        ax1t.set_ylabel('rainfall (mm)')    
        ax1t.legend(loc='upper right')
        ax1t.set_ylim(0, 10)
        ax1.set_xticks(ticks)
        ax1.xaxis.set_major_formatter(date_form)

        # high and medium frequency plots
        ax2.plot(tremor_window['time'], tremor_window['hfF'], 'g-', label='hfF', linewidth=0.5)   
        ax2.plot(tremor_window['time'], tremor_window['mfF'], 'r-', label='mfF', linewidth=0.5)
        ax2.set_ylabel('hf and mf (\u03bcm/s)')
        ax2.legend(loc='upper left')
        ax2.set_xlim(START, END)
        ax2t = ax2.twinx()
        ax2t.plot(rainfall_data['Date(NZST)'] - dt.timedelta(hours=12), rainfall_data['Amount(mm)'], 'b-', label='rainfall', linewidth=0.5)
        ax2t.plot(tremor_data['time'], 10000*label_vector - 10, 'k--', label='storm bounds',linewidth=0.5)
        ax2t.set_ylabel('rainfall (mm)')    
        ax2t.legend(loc='upper right')
        ax2t.set_ylim(0, 10)
        ax2.set_xticks(ticks)
        ax2.xaxis.set_major_formatter(date_form)

        # rsam plot
        ax3.plot(tremor_window['time'], tremor_window['rsam'], 'm-', label='rsam', linewidth=0.5)
        ax3.plot(tremor_window['time'], tremor_window['rsamF'], 'r-', label='rsamF', linewidth=0.5)
        ax3.set_ylabel('rsam (\u03bcm/s)')
        ax3.legend(loc='upper left')
        ax3.set_xlim(START, END)
        ax3t = ax3.twinx()
        ax3t.plot(rainfall_data['Date(NZST)'] - dt.timedelta(hours=12), rainfall_data['Amount(mm)'], 'b-', label='rainfall', linewidth=0.5)
        ax3t.plot(tremor_data['time'], 10000*label_vector - 10, 'k--', label='storm bounds',linewidth=0.5)
        ax3t.set_ylabel('rainfall (mm)')    
        ax3t.legend(loc='upper right')
        ax3t.set_ylim(0, 10)
        ax3.set_xticks(ticks)
        ax3.xaxis.set_major_formatter(date_form)

        # display and save
        plt.tight_layout()
        #plt.savefig('search {}.png'.format(str(i)),dpi=400)
        #plt.savefig('Eruption {}.png'.format(str(START)[:10]),dpi=400)
        plt.show()
        break

def main():
    """Main function to call other functions"""
    tremor_data, rainfall_data = get_data()
    label_vector, dates = assign_label_vectors(tremor_data)
    plot_window(tremor_data, rainfall_data, label_vector, dates)

main()