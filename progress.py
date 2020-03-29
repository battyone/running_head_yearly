# standard library imports
import datetime as dt

import dateutil.parser
import lxml.etree as ET
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set()

class YearlyProgress(object):

    def __init__(self, filename):
        self.filename = filename

    def run(self):

        self.parse_xml()

        self.plot()

    def plot(self):
        fig, ax = plt.subplots()

        handles = []
        labels = []
        for idx, df in self.df.groupby(self.df.date.dt.year):
            if idx < 2016:
                continue

            df = df.copy()

            df['dayofyear'] = df.date.dt.dayofyear
            df['cumdist'] = df.distance.cumsum()
            label = str(idx)
            x = df.plot.line(x='dayofyear', y='cumdist', ax=ax, label=label)

            labels.append(label)

            ch = x.get_children()
            handle = [h for h in ch if h.get_label() == label]
            handles.extend(handle)

        days_of_year = np.arange(0, 367)
        for pace_per_week in [60, 55, 50, 45, 40, 35, 30, 25]:

            total_miles = pace_per_week / 7 * days_of_year
            h, = ax.plot(days_of_year, total_miles, linestyle='-.', zorder=0)
            label = f'{pace_per_week}/wk'

            handles.append(h)
            labels.append(label)

        ax.legend(handles, labels)
        plt.show()

    def parse_xml(self):

        tree = ET.parse(self.filename)

        records = []

        events = tree.xpath('EventCollection/Event[@type="10"]')
        for event in events:
            date = dateutil.parser.parse(event.attrib['time'], ignoretz=True)

            if date.year < 1900:
                continue

            distance = float(event.xpath('Distance/text()')[0])
            record = {
                'date': date,
                'distance': distance
            }
            records.append(record)

        self.df = pd.DataFrame(records)

if __name__ == '__main__':

    o = YearlyProgress('log.xml')
    o.run()
