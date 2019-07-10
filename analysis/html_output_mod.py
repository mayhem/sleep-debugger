import pandas as pd
from pandas import DataFrame
import bokeh.charts
import numpy as np

class Produce_html_files(object):
    """Class that prduces html format report files"""

    def __init__(self, dataframe=None, x=None, y=None,
                title=None, xlabel=None, ylabel=None,
                directory=None, filename=None):
        self.dataframe = dataframe
        self.x = x
        self.y = y
        self.title =title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.directory = directory
        self.filename = filename

    def plotscatter(self, dataframe, x, y, title, xlabel,
                    ylabel, directory, filename):
        """Function to plot and export Scatter Chart to html"""
        filename = directory+filename
        plot = bokeh.charts.Scatter(dataframe, x=x, y=y,
                                    title = title, xlabel=xlabel,
                                    ylabel=ylabel)
        bokeh.charts.output_file(filename)

    def plotline(self, dataframe, x, y, title, xlabel,
                 ylabel, directory, filename):
        """Function to plot and export Line Chart to html"""
        filename = directory+filename
        plot = bokeh.charts.Line(dataframe, x=x, y=y,
                                 title = title, xlabel=xlabel,
                                 ylabel=ylabel)
        bokeh.charts.output_file(filename)

    def WritetoHTML(self, dataframe, directory, filename):
        """Writes reports to html"""
        filename = directory+filename
        html_str= dataframe.to_html()
        html_file = open(filename, 'w')
        html_file.write(html_str)
        html_file.close()