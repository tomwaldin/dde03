"""A script to analyse the rainfall data at Turoa in the last 12 months"""
"""Tom Waldin 3/08/2021"""

# import supporting packages
import pandas as pd
import matplotlib.pyplot as plt

# global inputs
FILENAME = "C:/Users/user/OneDrive/Documents/FYP/ruapehu/data/turoa_rainfall_data.csv"

def get_data():
    """Function to read csv file and filter to specified time window"""
    data = pd.read_csv(FILENAME, skiprows=1)
    data['Date'] = pd.to_datetime(data['Date'], dayfirst=True)
    #window = dataF[(dataF['time'] > START) & (dataF['time'] < END)]
    return data

def plot_data(data):
    """A function to plot time series graphs of input data"""
    #print(data.head())
    a = data['Date']
    plt.plot(data['Date'], data['Value'], 'k-')
    #plt.plot([i for i in range(len(data['Value']))], data['Value'], 'k-')
    plt.show()
    #plt.savefig('rainfall.png',dpi=400)

def main():
    """Main function"""
    data = get_data()
    plot_data(data)

main()

# change x axis to Dec-06, include year in graph title
# do full year and focusing around storms