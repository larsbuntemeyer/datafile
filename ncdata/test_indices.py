#! /usr/bin/env python
# coding: utf-8
# Copyright (C) 2010-2014 REMO Group

"""Executable script for testing calculation of time series for specific climate indices for EURO-CORDEX 0.11.

**Externals:**
    *calculate_indices.py*

Written by Thomas Remke
"""

import os
import glob
from calculate_indices import * 

def calc_indice(data,ofile,indice,thr=None):
    """Calculation of climate indices through external routines.

    **Arguments:**
        *data:*
            Filename of the data file to be used for climate index calculation.
        *ofile:*
            Filename of the output file.
        *indice:*
            Index to be calculated.
        *thr:*
            Threshold to be specified if needed by the external routine.
    """
    if indice_dic[indice]['indice'] == 'pr-pctl-days-trans':
        for thr in indice_dic[indice]['thr']:
            rdata = data.replace(os.path.basename(data).split('_')[3],'historical')
            outfile = ofile.replace(os.path.basename(ofile).split('_')[0],os.path.basename(ofile).split('_')[0].replace('pctl','p'+thr))
            pr_pctl_days_trans(data,rdata,outfile,thr)
    elif indice_dic[indice]['indice'] == 'pr-thr-trans':
        for thr in indice_dic[indice]['thr']:
            outfile = ofile.replace(os.path.basename(ofile).split('_')[0],os.path.basename(ofile).split('_')[0].replace('thr',thr+'mm'))
            pr_thr_trans(data,outfile,thr)

# Path to EURO-CORDEX data from ESGF
file_path = '/eddy/pool/sims/cordex/testlab/data/EUR-11/{}/'
out_path = '/eddy/pool/sims/cordex/testlab/indices_lars/'
ystart = 1971
yend = 2000

# Indice dictionary
indice_dic = { 'pr-pctl-days': { 'indice' : 'pr-pctl-days-trans','var' : 'pr',     'thr' : ['95','99'] },
               'pr-thr'      : { 'indice' : 'pr-thr-trans',      'var' : 'pr',     'thr' : ['10','20'] }
             }

for indice in indice_dic:

    # Merge time slices
    file_list = [f for f in glob.glob(file_path.format(indice_dic[indice]['var'])+'*.nc') if 'historical' in os.path.basename(f)]
    join_list = []
    for file in file_list:
        if int(os.path.basename(file).split('_')[-1].split('-')[0][0:4]) >= ystart and\
           int(os.path.basename(file).split('_')[-1].split('-')[1][0:4]) <= yend:
            join_list.append(file)
    join_list.sort()
    ofile = out_path+'_'.join(os.path.basename(join_list[0]).split('_')[0:-1])+'_'+\
            os.path.basename(join_list[0]).split('_')[-1].split('-')[0][0:8]+'-'+\
            os.path.basename(join_list[-1]).split('_')[-1].split('-')[1][0:8]+'.nc'
    if not os.path.isfile(ofile): 
        print 'merging time slice files to \033[1m'+os.path.basename(ofile)+'\033[1m'
        os.system('cdo -f nc mergetime '+' '.join(join_list)+' '+ofile)
    else:
        print 'merged file \033[1m'+os.path.basename(ofile)+'\033[1m found'

    print 'working on file \033[1m'+os.path.basename(ofile)+'\033[0m'

    # Compute indice
    print 'computing \033[1m'+indice+'\033[1m'
    ofile = calc_indice(ofile,ofile.replace(indice_dic[indice]['var'],indice_dic[indice]['indice']),indice)

    print 'done \n'
