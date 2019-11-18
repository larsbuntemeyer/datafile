#! /usr/bin/python
# coding: utf-8
#
# License
#
"""This module provides a class to handle horizontal data used by :mod:`MapPlot`
classes.
"""

import os

from pathlib import Path
#from PyRemo.OoPlot.Netcdf4Read import NetcdfRead
from netCDF4 import Dataset
import time
import logging


##
# TODO:
# Climate Indices should follow CF conventions, this means:
# field dimensions need to be defined as netcdf variables, e.g., lat lon, etc...
# frequencies and scenarios should be consistent in the nc attributes
# indice names should appear in the field name and the standard names in the nc attributes.
#

# cmip5 naming convention: mrro_day_MPI-ESM-LR_rcp26_r1i1p1_20060101-20091231.nc
#                          varname_frequency_model_experiment_ensemble_startdate-enddate.suffix
#
# cmip6                    pr_day_MPI-ESM1-2-LR_historical_r1i1p1f1_gn_18500101-18691231.nc
#                          varname_frequency_model_experiment_ensemble_gridlabel_startdate-enddate.suffix

def get_cdo_command_from_line(line):
    command = ''
    pos = line.find('cdo')
    if pos > 0:
        command = line[pos:]
    return command



def get_cdo_history(datafile):
    history = datafile.history.splitlines()
    history.reverse()
    cdo_commands = []
    for line in history:
        if 'cdo' in line:
            cdo_commands.append(get_cdo_command_from_line(line))
    return cdo_commands




class FileReader(object):
    """Reads a NetCDF file, returns global and data field attributes.

    You can create a :class:`FileReader` object from scratch with this class.

    Written by Lars Buntemeyer  
    """

    def __init__(self, filename_str):
        """:class:`FileReader` constructor.
        
        **Arguments:**
            *filename_str:*
                The filename to read. 
        """
        self.filename_str = filename_str
        self.ignored_gridattrs = ['bounds', 'grid_mapping']
        self.ignored_variables = ['lat', 'lon', 'rlat', 'rlon']
        try:
            self.nc = Dataset(self.filename_str)
        except:
            raise Exception('could not read nc file: {}'.format(self.filename_str))

    def get_ncdict(self):
        """Returns a dictionary containing all global NetCDF attributes.
        """
        return {attr:self.nc.getncattr(attr) for attr in self.nc.ncattrs()}

    def get_varlist(self):
        """Returns a list of all NetCDF data fields. 
        """
        return self.nc.variables

    def get_cf_fields(self):
        """Returns a dictionary with all valid CF fields. NetCDF data fields
        that define a grid or mappring will be ignored.
        """
        fields = {} 
        return {varname: var for varname, var in self.nc.variables.items() \
                if varname not in self.get_ignored_nc_variables()}

    def get_ignored_nc_variables(self):
        """Returns a list of NetCDF data fields that should be ignored in
           the variable list of get_cf_fields.
        """
        ignored = self.ignored_variables
        metric  = []
        for varname, var in self.nc.variables.items():
            if varname in self.nc.dimensions:
                ignored.append(varname)
            metric += self.get_metric(varname)
        return ignored+metric

    def get_metric(self,varname):
        """Returns a list variable attributes that refers to
           grid attributes, e.g., grid mapping or bounds. 

        **Arguments:**
            *varname:*
                Name of the variable to check for attributes.

        """
        var     = self.nc.variables[varname]
        ncattrs = var.ncattrs()
        result = []
        for gridattr in self.ignored_gridattrs:
            if gridattr in ncattrs:
                result.append(var.getncattr(gridattr))
        return result
   
    def is_dimvar(self,varname):
        """Checks if a variable name refers to a NetCDF dimension.

        **Arguments:**
            *varname:*
                Name of the variable.

        """
        if varname in self.dimensions:
            return True
        else:
            return False
        


class DataFile(object):
    """Manages meta information of a file.

    You can create a :class:`DataFile` object from scratch with this class.

    Written by Lars Buntemeyer  
    """

    def __init__(self, filename_str, nc_meta=True):
        """:class:`DataFile` constructor.
        
        **Arguments:**
            *filename_str:*
                The filename to read. 
            *nc_meta:*
                Flag for reading NetCDF meta data at initialization. 
        """
        self.filename_str = filename_str
        self.filename     = Path(filename_str)
        self.mtime        = time.ctime(os.path.getmtime(filename_str))
        self.ctime        = time.ctime(os.path.getctime(filename_str))
        if nc_meta: self._init_nc_meta()

    def __str__(self):
        return self.filename_str

    def _init_nc_meta(self):
        """Initializes meta information and attributes of the 
        :class:`DataFile` object.

        """
        fr = FileReader(self.filename_str)
        cf_fields       = fr.get_cf_fields()
        self.ncdict     = fr.get_ncdict()
        varnames        = list(cf_fields.keys())
        if varnames:
            self.ncdict['varname'] = varnames[0]
        self._init_attributes()

    def _init_attributes(self):
        """Creates :class:`DataFile` attributes from global NetCDF 
        attributes (in the ncdict) for easy access.

        """
        for attr,value in self.ncdict.items():
            self.__setattr__(attr,value)



class CFDataFile(DataFile):
    def __init__(self, filename_str):
        DataFile.__init__(self, filename_str)
        self._validate_CF()

    def _validate_CF(self):
        if not hasattr(self, 'Conventions'):
            print('File has no  \'CF Conventions\' attribute')
            raise Exception('Can not init CFDataFile without \
                           \'Conventions\' global attribute. ')
        else:
            conv = self.Conventions
            if 'CF-' not in conv:
                raise Exception('Conventios not valid: {}'.format(conv))
            else:
                print('CF Conventions: {}'.format(conv))

    def _validate_project_id(self, expect=''):
        if not hasattr(self, 'project_id'):
            print('File has no \'project_id\' attribute')
            raise Exception('Can not init CordexDataFile without \
                           \'project_id\' global attribute. ')
        else:
            project_id = self.project_id
            if project_id != expect:
                raise Exception('project_id not valid: {}'.format(project_id))
            else:
                print('project_id: {}'.format(project_id))
        

class CordexDataFile(CFDataFile):
    def __init__(self, filename_str):
        CFDataFile.__init__(self, filename_str)
        self._validate_project_id('CORDEX')



class CMIP5DataFile(CFDataFile):
    def __init__(self, filename_str):
        CFDataFile.__init__(self, filename_str)
        self._validate_project_id('CMIP5')
