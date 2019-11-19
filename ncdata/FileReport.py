#! /usr/bin/python
# coding: utf-8
#
# License
#

import os
import fnmatch
import pickle
from .DataFile import DataFile
from .tools import printProgressBar


from pathlib import Path

def realpath(fileList):
    return list(set([os.path.realpath(f) 
        for f in fileList if os.path.isfile(f)]))

def is_file(fileList):
    result = []
    print('Checking valid files...')
    l = len(fileList)
    printProgressBar(0, l, prefix = 'Checking valid files, Progress:', suffix = 'Complete', length = 50)
    for i,f in enumerate(fileList):
        if os.path.isfile(f): result.append(f)
        printProgressBar(i + 1, l, prefix = 'Progress:', \
                         suffix = 'Complete', length = 50)
    return result
#    return [f for f in fileList if os.path.isfile(f)] 
    
def filter(fileList, match='*'):
    return fnmatch.filter(fileList, match)

def suffix_dict(fileList):
    result = {}
    print('Creating suffix overview...')
    l = len(fileList)
    printProgressBar(0, l, prefix = 'Suffix Scan, Progress:', suffix = 'Complete', length = 50)
    for i,filename_str in enumerate(fileList):
        printProgressBar(i + 1, l, prefix = 'Progress:', \
                         suffix = 'Complete', length = 50)
        suffix = Path(filename_str).suffix
        if not suffix:
            if 'no suffix' in result:
                result['no suffix'].append(filename_str)
            else:
                result['no suffix'] = [filename_str]
        elif suffix in result:
            result[suffix].append(filename_str)
        else:
            result[suffix] = [filename_str]
    return result


def sort_by_attrs(datafiles, attrs):
    if not attrs: 
        return datafiles
    result = {}
    attr = attrs[0]
    sorted_datafiles = sort_by_attr(datafiles, attr)
    for attr_value, datafile_list in sorted_datafiles.items():
        result[attr_value] = sort_by_attrs(datafile_list, attrs[1:])
    return result


def filter_by_filename(datafiles, matches):
    result = []
    for df in datafiles:
        for match in matches:
            if fnmatch.fnmatch(df.filename_str,match):
                result.append(df)
            else:
                break
    return result


def filter_by_attrs(datafiles, **kwargs):
    result = []
    for datafile in datafiles:
        found = []
        for attr, value in kwargs.items():
            if attr in datafile.ncdict:
                if datafile.ncdict[attr] == value:
                    found.append(True)
                else: 
                    found.append(False)
            else:
                found.append(False)
        if all(found):
            result.append(datafile)
    return result


def sort_by_attr(datafiles, attr):
    result = {}
    missing_key = 'no {}'.format(attr)
    for datafile in datafiles:
        if attr in datafile.ncdict:
            value = datafile.ncdict[attr]
            if value in result:
                result[value].append(datafile)
            else:
                result[value] = [datafile]
        else:
            if missing_key in result:
                result[missing_key].append(datafile)
            else:
                result[missing_key] = [datafile]
    return result


def symlink(fileList):
    valid   = []
    missing = []
    print('Scanning for Symlinks...')
    l = len(fileList)
    printProgressBar(0, l, prefix = 'Scanning symlinks Progress:', suffix = 'Complete', length = 50)
    for i,f in enumerate(fileList):
        printProgressBar(i + 1, l, prefix = 'Progress:', \
                         suffix = 'Complete', length = 50)
        if os.path.islink(f):
            if os.path.isfile(f):
                valid.append(f)
            else:
                missing.append(f)
    return (valid, missing)

def scan(rootDir, match='*'):
    result = []
    for dirName, subdirList, fileList in os.walk(rootDir):
       print('\rScanning: %s                      ' % dirName, end='')
       if len(fileList) > 0:
           filenames = [os.path.join(dirName,filename) for filename in fileList \
                        if fnmatch.fnmatch(filename, match)]
           result += filenames
    return result


def scan_ncattrs(fileList):
    print('Scanning for NetCDF Attributes...')
    dataFileList = []
    l = len(fileList)
    printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
    for i, filename_str in enumerate(fileList):
        dataFileList.append(DataFile(filename_str))
        printProgressBar(i + 1, l, prefix = 'Progress:', \
                         suffix = 'Complete', length = 50)
    return dataFileList
    #return [DataFile(filename_str) for filename_str in fileList]


class FileReport(object):

    def __init__(self, rootDir, match='*'):
        self.rootDir  = rootDir
        self.match    = match
        self.fileList = []
        self.valid    = []
        self.symlink  = []
        self.missing  = []
        self.suffix   = {}

    def __getitem__(self, suffix):
        return self.suffix[suffix]

    def __iter__(self):
        return iter(self.valid)

    def __str__(self):
        output  = '\n'
        output += 'FileReport of {}\n'.format(self.rootDir)
        output += '\n'
        output += ' Number of Files               : {}\n'.format(len(self.fileList))
        output += ' Number of valid Files         : {}\n'.format(len(self.valid))
        output += ' Number of Symlinks            : {}\n'.format(len(self.symlink))
        output += ' Number of missing Symlinks    : {}\n'.format(len(self.missing))
        output += ' \n'
        output += ' Number of Suffixes            : {}\n'.format(len(self.suffix.keys()))
        for suffix,fileList in self.suffix.items():
            output += '               {:<12}    : {}\n'.format(suffix,len(fileList))
        return output

    def report(self):
        if not self.fileList:
            self.scan()
        print('finished scan')
        print('Found {} files'.format(len(self.fileList)))
        (self.symlink, self.missing) = symlink(self.fileList)
        self.valid    = is_file(self.fileList)
        #self.realpath = realpath(self.valid)
        self.suffix   = suffix_dict(self.valid)

    def scan(self):
        self.fileList = scan(self.rootDir, match=self.match)

    def write(self, filename):
        self.filename = filename
        pickle.dump(self, open(filename,'wb'))

    @staticmethod
    def read(filename):
        return pickle.load(open(filename,'rb'))



class NCFileReport(FileReport):

    def __init__(self):
        FileReport.__init__(self)
        self.match    = ['*.nc']


    




