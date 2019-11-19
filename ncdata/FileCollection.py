

from .DataFile import DataFile
import pandas as pd
from pandas import Series


class DataFileSet(object):

    def __init__(self, datafiles):
        self.datafiles = datafiles

    @property
    def filenames(self):
        return [df.filename_str for df in self.datafiles]

@property
    def _constructor(self):
                return SubclassedSeries

                @property
                    def _constructor_expanddim(self):
                                return SubclassedDataFrame

class TimeSeries(Series):

    @property
    def _constructor(self):
        dates = [df.taxis.dates[0] for df in self.datafiles]
        Series(datafiles, index=dates)
        self._init()

    def _init(self):
        pass 


