import pandas as pd
from pandas import DataFrame
import numpy as np


class SleepReportAnalysis(object):
    """A Class to Produce a morning Sleep Report"""

    def __init__(self, data=None, dataframe=None, frame1=None, frame2=None):
        self.data = data
        self.dataframe = dataframe
        self.frame1 = frame1
        self.frame2 = frame2

    def ProduceDataFrame(self, data):
        """Function to produce dataframe"""
        df = pd.read_csv(self.data, header=None, names=['Timestamp',
                                                        'Magnitude'])
        df = df.dropna()
        df['Timestamp'] = df['Timestamp'].astype(np.datetime64)
        return df
    
    def DataOverview(self, dataframe):
        """Function to provide top level overview of data"""
        return dataframe.describe()

    def HighestPeaks(self, dataframe):
        """Fucntion to ID highest peaks in data"""
        dfsorted1= dataframe.sort_values('Magnitude', axis=0,
                                         ascending=False).head(n=150)
        dfsorted2= dfsorted1.sort_values('Timestamp', axis=0, ascending=True)
        return dfsorted2

    def CalcDiff(self, dataframe):
        """Function to calculate the time span between readings"""
        difference = dataframe.diff(periods=1, axis=0)
        difference2 = difference[difference.Timestamp >= '00:10:00']
        #update the timestamp to desired length of time span
        return difference2

    def ProduceSleepReport(self, frame1, frame2):
        """Function to produce the Sleep Report,
        Frame1 should be CalcDiff Output"""
        frames = [frame1, frame2]
        result = pd.concat(frames, axis=1).dropna().drop('Magnitude', axis=1)
        cols=['Length Between Peak', 'Timestamp of Peak']
        result.columns = cols
        return result
