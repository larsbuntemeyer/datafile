#! /usr/bin/python
# coding: utf-8
#
# License
#


import os

# ESGF example
# pathstr     = '/eddy/pool/CORDEX-CORE/ESGF/
#               CORDEX/output/EUR-22/GERICS/ECMWF-ERAINT/evaluation/r0i0p0/GERICS-REMO2015/v1/fx/orog'

class NamingConvention():
    def __init__(self):
        pass


class FilePathConvention(NamingConvention):
    def __init__(self):
        NamingConvention.__init__(self)


class FileNameConvention(NamingConvention):
    def __init__(self):
        NamingConvention.__init__(self)


class FileConvention():
    def __init__(self,filepath_convention=None,filename_convention=None):
        self.filepath_convention = filepath_convention
        self.filename_convention = filename_convention



#institute_id            = 'GERICS'
#project_id              = 'CORDEX'
#CORDEX_domain           = 'EUR-22'
#product                 = 'output'
#driving_model_id        = 'ECMWF-ERAINT'
#driving_experiment_name = 'evaluation'
#ensemble                = 'r0i0p0'
#model_id                = 'GERICS-REMO2015'
#rcm_version_id          = 'v1'
#frequency               = 'fx'
#cf_name                 = 'orog'


class ESGF():
    def __init__(self):
        pass

    def path(): 

        return os.path.join(project_id, product, CORDEX_domain, institute_id,   \
                            driving_model_id, driving_experiment_name,ensemble, \
                            model_id,rcm_version_id,frequency,cf_name)







