
import os
import numpy as np
import glob
import sys

from cdo import *
cdo = Cdo()

# Definition of valid ranges for different variables and conditions
trange='173,373'
prrange='0,10000'
wetdays='1,10000'
drydays='-0.01,1'



class ClimateIndex(object):
    """The ClimateIndex Base Class.

    Implements common attributes and functions.

    """
    def __init__(self):
        self.name      = 'UNKNOWN'
        self.timerange = (1950,2100) 

    def compute(self):
        raise NotImplementedError


def tas_trans(ClimateIndex):
    """Annual mean temperature.
    """
    def __init__(self):
        ClimateIndex.__init__(self)
        self.name = 'tas_trans'

    def compute(self):
        """Annual mean temperature.

        **Arguments:**
            *data:* 
                Data file should contain daily temperature values in [K].
        """
        options = '-f nc -f'
        input   = '-setvrange,{} -selyear,{} {}'.format(self.timerange,inputfile)
        output  = ofile
        output  = cdo.yearmean(options=options, input=input, output=output)
        #os.system('cdo -f nc -s yearmean -setvrange,'+trange+' -selyear,1950/2100 '+data+' '+ofile)

        return ofile

def pr_pctl_days_trans(ClimateIndex):
    """Annual number of days exceeding the <thr>-percentile of precipitation sum of the reference period 1971-2000.
    """
    def __init__(self):
        ClimateIndex.__init__(self)
        self.name = 'pr_pctl_days_trans'

    def compute(data,rdata,ofile,thr):
        """Annual number of days exceeding the <thr>-percentile of precipitation sum of the reference period 1971-2000.
    
        **Arguments:**
            *data:* 
                Data file should contain daily precipitation sum in [kgm-2s-1].
            *thr:*
                Threshold depics a dimensionless percentile value (e.g. 95 for p95).
        """
        os.system('cdo -f nc -s selyear,1971/2000 -setvrange,'+wetdays+'  -mulc,86400 '+rdata+' FIN')
        os.system('cdo -s runmean,30 -yearpctl,'+str(thr)+' FIN -yearmin FIN -yearmax FIN REF')
        os.system('cdo -s yearsum -lt -setmissval,$CD_MISSVAL REF -setmissval,$CD_MISSVAL -selyear,1950/2100 -setvrange,'+wetdays+' -mulc,86400 '+data+' '+ofile)
        os.system('rm FIN')
        os.system('cp REF '+ofile.replace('.nc','_REF.nc'))
        os.system('rm REF')
    
        return ofile


####def tas_trans(data,ofile):
####    """Annual mean temperature.
####
####    **Arguments:**
####        *data:* 
####            Data file should contain daily temperature values in [K].
####    """
####    os.system('cdo -f nc -s yearmean -setvrange,'+trange+' -selyear,1950/2100 '+data+' '+ofile)
####
####    return ofile
####
####
####def tasmin_trans(data,ofile):
####    """Annual absolute minimum temperature.
####
####    **Arguments:**
####        *data:* 
####            Data file should contain daily minimum temperature values in [K].
####    """
####    os.system('cdo -f nc -s yearmin -setvrange,'+trange+' -selyear,1950/2100 '+data+' '+ofile)
####
####
####def tasmax_trans(data,ofile):
####    """Annual absolute maximum temperature.
####
####    **Arguments:**
####        *data:* 
####            Data file should contain daily maximum temperature values in [K].
####    """
####    os.system('cdo -f nc -s yearmax -setvrange,'+trange+' -selyear,1950/2100 '+data+' '+ofile)
####
####
####def tasmax_thr_trans(data,ofile,thr):
####    """Annual number of days with maximum temperature above or equal to <thr>.
####
####    **Arguments:**
####        *data:* 
####            Data file should contain daily maximum temperature values in [K].
####        *thr:*
####            Threshold temperature should contain a value in [degC].
####    """
####    os.system('cdo -f nc -s yearsum -gec,'+str(273.15+float(thr))+' -setvrange,'+trange+' -selyear,1950/2100 '+data+' '+ofile)
####
####
####def frostdays_trans(data,ofile):
####    """Annual number of frostdays (i.e. number of days with minimum temperature below 0 [degC]).
####
####    **Arguments:**
####        *data:* 
####            Data file should contain daily minimum temperature values in [K].
####    """
####    os.system('cdo -f nc -s yearsum -ltc,273.15 -setvrange,'+trange+' -selyear,1950/2100 '+data+' '+ofile)
####
####
####def icedays_trans(data,ofile):
####    """Annual number of icedays (i.e. number of days with maximum temperature below 0 [degC]).
####
####    **Arguments:**
####        *data:* 
####            Data file should contain daily maximum temperature values in [K].
####    """
####    os.system('cdo -f nc -s yearsum -ltc,273.15 -setvrange,'+trange+' -selyear,1950/2100 '+data+' '+ofile)
####
####
####def hwave_thr_trans(data,ofile,thr):
####    """Annual number and maximum length of heatwaves.
#### 
####    Heatwaves are defined as at least five consecutive days with daily maximum temperature exceeding <thr>.
####    The annual number of heatwaves depicts the annual number of occurrences. 
####    The maximum length depicts depicts the largest single event within a year.
####
####    **Arguments:**
####        *data:* 
####            Data file should contain daily maximum temperature values in [K].
####        *thr:*
####            Threshold temperature should contain a value in [degC].
####    
####    Heat wave if more than 5 consecutive days exceeding threshold (thr)     
####    """
####    # Occurrence per year
####    os.system('cdo -f nc -s consects -gtc,'+str(thr)+' -subc,273.15 -setvrange,'+trange+' -selyear,1950/2100 '+data+' FIN')
####    # Number of heat waves
####    os.system('cdo -s setmisstoc,0 -yearsum -gec,5 FIN '+os.path.dirname(ofile)+'N-'+os.path.basename(ofile))
####    # Maximum yearly duration of heat wave
####    os.system('cdo -s gec,5 FIN MASK')
####    os.system('cdo -s -yearmax -ifthen MASK FIN '+os.path.dirname(ofile)+'Dmax-'+os.path.basename(ofile))
####    os.system('rm FIN')
####    os.system('rm MASK')
####
####
####def pr_trans(data,ofile):
####    """Annual mean precipitation.
####
####    **Arguments:**
####        *data:* 
####            Data file should contain daily precipitation sum in [kgm-2s-1].
####    """
####    os.system('cdo -f nc -s yearmean -selyear,1950/2100 -setvrange,'+prrange+' -mulc,86400 '+data+' '+ofile)
####
####    return ofile
####
####
####def pr_seas_trans(data,ofile):
####    """Seasonal (DJF,MAM,JJA,SON) mean precipitation.
####
####    **Arguments:**
####        *data:* 
####            Data file should contain daily precipitation sum in [kgm-2s-1].
####    """
####    os.system('cdo -f nc -s seasmean -selyear,1950/2100 -setvrange,'+prrange+' -mulc,86400 '+data+' SEAS')
####    seas_dict={'2':'DJF','5':'MAM','8':'JJA','11':'SON'}
####    for seas in seas_dict:
####         os.system('cdo -s selmon,'+str(seas)+' SEAS '+ofile.replace(ofile.split('_')[0],ofile.split('_')[0].replace('seas',seas_dict[seas])))
####    os.system('rm SEAS')
####
####    return ofile
####
####
####def pr_pctl_trans(data,ofile,thr):
####    """Yearly <thr>-percentile of daily precipitation sum.
####
####    **Arguments:**
####        *data:* 
####            Data file should contain daily precipitation sum in [kgm-2s-1].
####        *thr:*
####            Threshold depics a dimensionless percentile value (e.g. 95 for p95).
####    """
####    os.system('cdo -f nc -s selyear,1950/2100 -setvrange,'+wetdays+'  -mulc,86400 '+data+' FIN')
####    os.system('cdo -s yearpctl,'+str(thr)+' FIN -yearmin FIN -yearmax FIN '+ofile)
####    os.system('rm FIN')
####
####    return ofile
####
####
####def pr_pctl_days_trans(data,rdata,ofile,thr):
####    """Annual number of days exceeding the <thr>-percentile of precipitation sum of the reference period 1971-2000.
####
####    **Arguments:**
####        *data:* 
####            Data file should contain daily precipitation sum in [kgm-2s-1].
####        *thr:*
####            Threshold depics a dimensionless percentile value (e.g. 95 for p95).
####    """
####    os.system('cdo -f nc -s selyear,1971/2000 -setvrange,'+wetdays+'  -mulc,86400 '+rdata+' FIN')
####    os.system('cdo -s runmean,30 -yearpctl,'+str(thr)+' FIN -yearmin FIN -yearmax FIN REF')
####    os.system('cdo -s yearsum -lt -setmissval,$CD_MISSVAL REF -setmissval,$CD_MISSVAL -selyear,1950/2100 -setvrange,'+wetdays+' -mulc,86400 '+data+' '+ofile)
####    os.system('rm FIN')
####    os.system('cp REF '+ofile.replace('.nc','_REF.nc'))
####    os.system('rm REF')
####
####    return ofile
####
####
####def pr_thr_trans(data,ofile,thr):
####    """Annual number of days with precipitation sum above or equal to <thr>.
####
####    **Arguments:**
####        *data:* 
####            Data file should contain daily precipitation sum in [kgm-2s-1].
####        *thr:*
####            Threshold precipitation should contain a value in [mmd-1].
####    """
####    os.system('cdo -f nc -s yearsum -gec,'+str(thr)+' -setvrange,'+prrange+' -mulc,86400 -selyear,1950/2100 '+data+' '+ofile)

