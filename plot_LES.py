#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Template plotting script 
"""
# imports
import os
import netCDF4 as nc
import numpy as np
import plot2D as pl
#
########################## run options
#
# set project path
projDir = ''
# list of paths for files to plot
## for average by height
htFiles = [ 'firstFileName.nc',
            'secondFileName.nc', ]
## for time-series
tsFiles = [ 'firstFileName.nc', 
            'secondFileName.nc', ]
# height-averaging times, indices
timeIs = [12,13,14,15,16,17,18,19,20,21,22,23] # last 12 hrs
# x-axis extent of time-series plots [hr]
ts_xAxis = (4,24)
# chart styling
lineStyles = ['solid','dashed']
lineColors = ['k',]
lineWidths = [1.0,]
zOrders = [i for i in range(len(htFiles),-1,-1)] # plotting priority
legendLabels = ['First','Second']
# figure saving
saveOption = True        # option to save all figures on run
savePath   = None         # path to save figures, None means relative path
groupName  = 'GroupName_' # start of all figure filenames
#
##########################
#
# open netCDF datasets to list
htNCs = [nc.Dataset(fileName, 'r') for fileName in htFiles]
tsNCs = [nc.Dataset(fileName, 'r') for fileName in tsFiles]
# get dimensions
## hourly average
htTimes   = [NC.variables['time'][:] for NC in htNCs] # [s]
htHeights = [NC.variables['z'][:] for NC in htNCs]    # [m]
htHeightsKm = [height*1e-3 for height in htHeights]  # [km]
## timeseries
tsTimes   = [NC.variables['time'][:] for NC in tsNCs] # [s]
tsTimesHr = [times/3600 for times in tsTimes]         # [hr]
# get variables
rho_a = htNCs[0].variables['RHO'] # air density, [kg m-3]
rho_a_srf = float( htNCs[0].variables['RHO'][0,0] ) # [kg m-3]
#
### lists of dictionaries of all variables from each netCDF
##... careful if uncommenting, this will unpackage everything
#htVars =[{key:value[:] for key,value in NC.variables.items()} for NC in htNCs]
#tsVars =[{key:value[:] for key,value in NC.variables.items()} for NC in tsNCs]
###
#
## average by height
CLDs    = [NC.variables['CLD'][:] for NC in htNCs]    # [fraction]
PRECIPs = [NC.variables['PRECIP'][:] for NC in htNCs] # [mm/d]
TVFLUXs = [NC.variables['TVFLUX'][:] for NC in htNCs] # [W m-2]
THETALs = [NC.variables['THETAL'][:] for NC in htNCs] # [K]
QTs     = [NC.variables['QT'][:] for NC in htNCs]     # [g/kg]
QCs     = [NC.variables['QC'][:] for NC in htNCs]     # [g/kg]
W2s     = [NC.variables['W2'][:] for NC in htNCs]     # [m2 s-2]
WSKEWs  = [NC.variables['WSKEW'][:] for NC in htNCs]  # [?]
## timeseries
prec_srfs = [NC.variables['prec_srf'][:] for NC in tsNCs] # [kg/kg m/s]
Ncs       = [NC.variables['Nc'][:] for NC in tsNCs]       # [cm-3]
LWPs      = [NC.variables['LWP'][:] for NC in tsNCs]      # [g m-2]
lhfs      = [NC.variables['lhf'][:] for NC in tsNCs]      # [kg/kg m/s]
tkes      = [NC.variables['tke'][:] for NC in tsNCs]      # [m3 s-2]
ccs       = [NC.variables['cc'][:] for NC in tsNCs]       # [fraction]
# close files
for NC in htNCs+tsNCs:
    NC.close()
# calculate plot values
## hourly averages by height
### CLD
CLD_tAvg = np.array([ [np.sum(CLDs[i][timeIs,z])/np.size(CLDs[i][timeIs,z]) \
                       for z in range(np.size(htHeightsKm[i]))] \
                       for i in range(len(CLDs)) ]) # [fraction]
### PRECIP
PRECIP_tAvg = np.array([ [np.sum(PRECIPs[i][timeIs,z])/ \
                          np.size(PRECIPs[i][timeIs,z]) \
                          for z in range(np.size(htHeightsKm[i]))] \
                          for i in range(len(PRECIPs)) ]) # [mm/d]
### TVFLUX
TVFLUX_tAvg = np.array([ [np.sum(TVFLUXs[i][timeIs,z])/ \
                          np.size(TVFLUXs[i][timeIs,z]) \
                          for z in range(np.size(htHeightsKm[i]))] \
                          for i in range(len(TVFLUXs)) ]) # [W m-2]
### THETAL
THETAL_tAvg = np.array([ [np.sum(THETALs[i][timeIs,z])/ \
                          np.size(THETALs[i][timeIs,z]) \
                          for z in range(np.size(htHeightsKm[i]))] \
                          for i in range(len(THETALs)) ]) # [K]
### QT
QT_tAvg = np.array([ [np.sum(QTs[i][timeIs,z])/np.size(QTs[i][timeIs,z]) \
                      for z in range(np.size(htHeightsKm[i]))] \
                      for i in range(len(QTs)) ]) # [g/kg]
### QC
QC_tAvg = np.array([ [np.sum(QCs[i][timeIs,z])/np.size(QCs[i][timeIs,z]) \
                      for z in range(np.size(htHeightsKm[i]))] \
                      for i in range(len(QCs)) ]) # [g/kg]
### W2
W2_tAvg = np.array([ [np.sum(W2s[i][timeIs,z])/np.size(W2s[i][timeIs,z]) \
                      for z in range(np.size(htHeightsKm[i]))] \
                     for i in range(len(W2s)) ]) # [m+2 s-2]
### WSKEW
WSKEW_tAvg = np.array([ [np.sum(WSKEWs[i][timeIs,z])/ \
                         np.size(WSKEWs[i][timeIs,z]) \
                         for z in range(np.size(htHeightsKm[i]))] \
                         for i in range(len(W2s)) ]) # [m+2 s-2]
## timeseries
### constants
rho_r = 1000 # liquid water density: [kg m-3]
L_v   = 2.5104e+6 # latent heat of vaporization, water: [J/kg] 
### convert prec_srfs to [mm/d]
#... get air density at surface
#... prec_srf: [kg_w/kg_a * m/s]*(kg_a m-3 / kg_w m-3)*(s/d)*(mm/m) = [mm/d]
prec_srfs_mmd = [prec_srf * (rho_a_srf/rho_r) * 86400*1000 
                 for prec_srf in prec_srfs] # [mm/d]
### calculate accumulated surface precipitation for timeseries
prec_srfs_accums = [] # set list
for series in prec_srfs_mmd: # iterate for each prec_srf
    prec_srf_accum = []; accum = 0 # set list; set for sum
    for n in range(len(series)): # iterate over prec_srf
        accum += ( series[n]*(60/86400) ) # add to accum [mm]
        prec_srf_accum.append( accum ) # append each accum
    prec_srfs_accums.append( prec_srf_accum ) # append each list
### convert lhfs to [W m-2]
#... lhf: [kg_w/kg_a * m/s]*(kg_a m-3 / kg_w m-3)*(J/kg_w) = [W m-2]
lhfs_Wm2 = [lhf *(rho_a_srf/rho_r)*L_v for lhf in lhfs]
#
# plots
#
## average by height
### CLD
CLD_plot = [(CLD_tAvg[i],htHeightsKm[i]) for i in range(len(CLD_tAvg))]
pl.plot2D( CLD_plot,
          chartStyle=['line',],
          zOrders=zOrders,
          lineStyle=lineStyles,
          lineColor=lineColors,
          lineWidth=lineWidths,
          figSize=(5,5),
          title=None,
          xTitle='Cloud cover fraction [ratio]',
          yTitle='Height [km]',
          xLimit=(0,0.1),
          yLimit=(0,4),
          spineVis=(True,True,True,True),
          spineMajorTicks=(True,True,True,True),
          spineMinorTicks=(True,True,True,True),
          tickLengths=(6,3),
          tickDirections=('out','out'),
          spineLabels=(False,False,True,True),
          majorSpace=(0.02,0.5),
          minorSpace=(None,None),
          minorLabels=False,
          fontSize=(12,14,14,10),
          legendLabels=legendLabels,
          legendLoc='best',
          save=saveOption,
          path=savePath,
          fileName=groupName+'CLD',
          fileFormat='png',
          quality=300 
          )
### PRECIP
PRECIP_plot = [(PRECIP_tAvg[i],htHeightsKm[i]) \
               for i in range(len(PRECIP_tAvg))]
pl.plot2D( PRECIP_plot,
          chartStyle=['line',],
          zOrders=zOrders,
          lineStyle=lineStyles,               
          lineColor=lineColors,
          lineWidth=lineWidths,
          figSize=(5,5),
          title=None,
          xTitle=r'Precipitation flux [mm $\mathregular{d^{-1}}$]',
          yTitle='Height [km]',
          xLimit=(0,2),
          yLimit=(0,4),
          spineVis=(1,1,True,True),
          spineMajorTicks=(1,1,True,True),
          spineMinorTicks=(1,1,True,True),
          tickLengths=(6,3),
          tickDirections=('out','out'),
          spineLabels=(False,False,True,True),
          majorSpace=(0.5,0.5),
          fontSize=(12,14,14,10),
          legendLabels=legendLabels,
          legendLoc='best',
          save=saveOption,
          path=savePath,
          fileName=groupName+'PRECIP',
          fileFormat='png',
          quality=300 
          )
### TVFLUX
TVFLUX_plot = [(TVFLUX_tAvg[i],htHeightsKm[i]) \
               for i in range(len(TVFLUX_tAvg))]
vertZero = ( np.zeros_like(htHeightsKm[0]), htHeightsKm[0] )
pl.plot2D( [vertZero,] + TVFLUX_plot,
          chartStyle=['line',],
          zOrders=[0,]+zOrders,
          lineStyle= ['solid',] + lineStyles,
          lineColor= ['0.5'] + lineColors,
          lineWidth= [1.0] + lineWidths,
          figSize=(5,5),
          title=None,
          xTitle=r'Buoyancy flux [W $\mathregular{m^{-2}}$]',
          yTitle='Height [km]',
          xLimit=(-20,40),
          yLimit=(0,4),
          spineVis=(1,1,1,1),
          spineMajorTicks=(1,1,1,1),
          spineMinorTicks=(1,1,1,1),
          tickLengths=(6,3),
          tickDirections=('out','out'),
          spineLabels=(False,False,1,True),
          majorSpace=(10,0.5),
          fontSize=(12,14,14,10),
          legendLabels=['_',]+legendLabels,
          legendLoc='best',
          save=saveOption,
          path=savePath,
          fileName=groupName+'TVFLUX',
          fileFormat='png',
          quality=300 
          )
### THETAL
THETAL_plot = [(THETAL_tAvg[i],htHeightsKm[i]) \
               for i in range(len(THETAL_tAvg))]
pl.plot2D( THETAL_plot,
          chartStyle=['line',],
          zOrders=zOrders,
          lineStyle=lineStyles,                
          lineColor=lineColors,
          lineWidth=lineWidths,
          figSize=(5,5),
          title=None,
          xTitle='Liquid water potential temperature [K]',
          yTitle='Height [km]',
          xLimit=(295,325),
          yLimit=(0,4),
          spineVis=(1,1,True,True),
          spineMajorTicks=(1,1,True,True),
          spineMinorTicks=(1,1,True,True),
          tickLengths=(6,3),
          tickDirections=('out','out'),
          spineLabels=(False,False,True,True),
          majorSpace=(10,0.5),
          minorSpace=(None,None),
          fontSize=(12,14,14,10),
          legendLabels=legendLabels,
          legendLoc='best',
          save=saveOption,
          path=savePath,
          fileName=groupName+'THETAL',
          fileFormat='png',
          quality=300 
          )
### QT
QT_plot = [(QT_tAvg[i],htHeightsKm[i]) for i in range(len(QT_tAvg))]
pl.plot2D( QT_plot,
          chartStyle=['line',],
          zOrders=zOrders,
          lineStyle=lineStyles,                
          lineColor=lineColors,
          lineWidth=lineWidths,
          figSize=(5,5),
          title=None,
          xTitle=r'Total water [g $\mathregular{kg^{-1}}$]',
          yTitle='Height [km]',
          xLimit=(0,20),
          yLimit=(0,4),
          spineVis=(1,1,1,True),
          spineMajorTicks=(1,1,1,True),
          spineMinorTicks=(1,1,1,True),
          tickLengths=(6,3),
          tickDirections=('out','out'),
          spineLabels=(False,False,1,True),
          majorSpace=(2,0.5),
          fontSize=(12,14,14,10),
          legendLabels=legendLabels,
          legendLoc='best',
          save=saveOption,
          path=savePath,
          fileName=groupName+'QT',
          fileFormat='png',
          quality=300 
          )
### QC
QC_plot = [(QC_tAvg[i],htHeightsKm[i]) for i in range(len(QC_tAvg))]
pl.plot2D( QC_plot,
          chartStyle=['line',],
          zOrders=zOrders,
          lineStyle=lineStyles,                
          lineColor=lineColors,
          lineWidth=lineWidths,
          figSize=(5,5),
          title=None,
          xTitle=r'Cloud water [g $\mathregular{kg^{-1}}$]',
          yTitle='Height [km]',
          xLimit=(0,0.05),
          yLimit=(0,4),
          spineVis=(1,1,1,1),
          spineMajorTicks=(1,1,1,True),
          spineMinorTicks=(1,1,1,True),
          tickLengths=(6,3),
          tickDirections=('out','out'),
          spineLabels=(False,False,1,True),
          majorSpace=(0.01,0.5),
          fontSize=(12,14,14,10),
          legendLabels=legendLabels,
          legendLoc='best',
          save=saveOption,
          path=savePath,
          fileName=groupName+'QC',
          fileFormat='png',
          quality=300 
          )
### W2
W2_plot = [(W2_tAvg[i],htHeightsKm[i]) for i in range(len(W2_tAvg))]
pl.plot2D( W2_plot,
          chartStyle=['line',],
          zOrders=zOrders,
          lineStyle=lineStyles,               
          lineColor=lineColors,
          lineWidth=lineWidths,
          figSize=(5,5),
          title=None,
          xTitle=r'Variance of vertical velocity [$\mathregular{m^{2}s^{-2}}$]',
          yTitle='Height [km]',
          xLimit=(0,0.3),
          yLimit=(0,4),
          spineVis=(1,1,1,1),
          spineMajorTicks=(1,1,1,1),
          spineMinorTicks=(1,1,1,1),
          tickLengths=(6,3),
          tickDirections=('out','out'),
          spineLabels=(0,0,1,1),
          majorSpace=(0.1,0.5),
          fontSize=(12,14,14,10),
          legendLabels=legendLabels,
          legendLoc='best',
          save=saveOption,
          path=savePath,
          fileName=groupName+'W2',
          fileFormat='png',
          quality=300 
          )
### WSKEW
WSKEW_plot = [(WSKEW_tAvg[i],htHeightsKm[i]) for i in range(len(WSKEW_tAvg))]
vertZero = ( np.zeros_like(htHeightsKm[0]), htHeightsKm[0] )
pl.plot2D( [vertZero,] + WSKEW_plot,
          chartStyle=['line',],
          zOrders=[0,]+zOrders,
          lineStyle= ['solid'] + lineStyles,
          lineColor= ['0.5'] + lineColors,
          lineWidth= [1.0,] + lineWidths,
          figSize=(5,5),
          title=None,
          xTitle='Vertical velocity skewness',
          yTitle='Height [km]',
          xLimit=(-1,1),
          yLimit=(0,4),
          spineVis=(1,1,1,1),
          spineMajorTicks=(1,1,1,1),
          spineMinorTicks=(1,1,1,1),
          tickLengths=(6,3),
          tickDirections=('out','out'),
          spineLabels=(0,0,1,1),
          majorSpace=(0.5,0.5),
          fontSize=(12,14,14,10),
          legendLabels=['_',]+legendLabels,
          legendLoc='best',
          save=saveOption,
          path=savePath,
          fileName=groupName+'WSKEW',
          fileFormat='png',
          quality=300 
          )
## timeseries
### prec_srf
prec_srf_plot = [(tsTimesHr[i],prec_srfs_mmd[i]) \
                 for i in range(len(prec_srfs_mmd))]
pl.plot2D( prec_srf_plot,
          chartStyle=['line',],
          zOrders=zOrders,
          lineStyle=lineStyles,                
          lineColor=lineColors,
          lineWidth=lineWidths,
          figSize=(12,4),
          title='Surface precipitation rate',
          xTitle='Time [hr]',
          yTitle='Precip. rate [mm $\mathregular{d^{-1}}$]',
          xLimit=ts_xAxis,
          yLimit=(0,10),
          spineVis=(1,1,1,1),
          spineMajorTicks=(1,1,True,True),
          spineMinorTicks=(1,1,True,True),
          tickLengths=(6,3),
          tickDirections=('out','out'),
          spineLabels=(False,False,True,True),
          majorSpace=(4,None),
          fontSize=(12,14,14,10),
          legendLabels=legendLabels,
          legendLoc='best',
          save=saveOption,
          path=savePath,
          fileName=groupName+'ts_precip_srf',
          fileFormat='png',
          quality=600 
          )
### prec_srf_accum
prec_srfs_accums_plot = [(tsTimesHr[i],prec_srfs_accums[i]) \
                         for i in range(len(prec_srfs_accums))]
pl.plot2D( prec_srfs_accums_plot,
          chartStyle=['line',],
          zOrders=zOrders,
          lineStyle=lineStyles,
          lineColor=lineColors,
          lineWidth=lineWidths,
          figSize=(12,4),
          title='Surface precipitation accumulation',
          xTitle='Time [hr]',
          yTitle='Accumulation [mm]',
          xLimit=ts_xAxis,
          yLimit=(0,0.5),
          spineVis=(1,1,1,1),
          spineMajorTicks=(1,1,True,True),
          spineMinorTicks=(1,1,True,True),
          tickLengths=(6,3),
          tickDirections=('out','out'),
          spineLabels=(False,False,True,True),
          majorSpace=(4,0.1),
          fontSize=(12,14,14,10),
          legendLabels=legendLabels,
          legendLoc='upper left',
          save=saveOption,
          path=savePath,
          fileName=groupName+'ts_precip_srf_accum',
          fileFormat='png',
          quality=600 
          )
### Nc
Nc_plot = [(tsTimesHr[i],Ncs[i]) for i in range(len(Ncs))]
pl.plot2D( Nc_plot,
          chartStyle=['line',],
          zOrders=zOrders,
          lineStyle=lineStyles,                
          lineColor=lineColors,
          lineWidth=lineWidths,
          figSize=(12,4),
          title='Mean cloud droplet concentration',
          xTitle='Time [hr]',
          yTitle='Concentration [$\mathregular{cm^{-3}}$]',
          xLimit=ts_xAxis,
          yLimit=(0,100),
          spineVis=(1,1,1,1),
          spineMajorTicks=(1,1,True,True),
          spineMinorTicks=(1,1,True,True),
          tickLengths=(6,3),
          tickDirections=('out','out'),
          spineLabels=(False,False,True,True),
          majorSpace=(4,None),
          fontSize=(12,14,14,10),
          legendLabels=legendLabels,
          legendLoc='best',
          save=saveOption,
          path=savePath,
          fileName=groupName+'ts_Nc',
          fileFormat='png',
          quality=600 
          )
### LWP
LWP_plot = [(tsTimesHr[i],LWPs[i]) for i in range(len(LWPs))]
pl.plot2D( LWP_plot,
          chartStyle=['line',],
          zOrders=zOrders,
          lineStyle=lineStyles,                
          lineColor=lineColors,
          lineWidth=lineWidths,
          figSize=(12,4),
          title='Mean liquid water path',
          xTitle='Time [hr]',
          yTitle='LWP [g $\mathregular{m^{-2}}$]',
          xLimit=ts_xAxis,
          yLimit=(0,100),
          spineVis=(1,1,1,1),
          spineMajorTicks=(1,1,True,True),
          spineMinorTicks=(1,1,True,True),
          tickLengths=(6,3),
          tickDirections=('out','out'),
          spineLabels=(False,False,True,True),
          majorSpace=(4,None),
          fontSize=(12,14,14,10),
          legendLabels=legendLabels,
          legendLoc='best',
          save=saveOption,
          path=savePath,
          fileName=groupName+'ts_LWP',
          fileFormat='png',
          quality=600 
          )
### lhf
lhf_plot = [(tsTimesHr[i],lhfs_Wm2[i]) for i in range(len(lhfs_Wm2))]
pl.plot2D( lhf_plot,
          chartStyle=['line',],
          zOrders=zOrders,
          lineStyle=lineStyles,
          lineColor=lineColors,
          lineWidth=lineWidths,
          figSize=(12,4),
          title=None,
          xTitle='Time [hr]',
          yTitle='Latent heat flux [W $\mathregular{m^{-2}}$]',
          xLimit=ts_xAxis,
          yLimit=(0.14,0.2),
          spineVis=(1,1,1,1),
          spineMajorTicks=(1,1,True,True),
          spineMinorTicks=(1,1,True,True),
          tickLengths=(6,3),
          tickDirections=('out','out'),
          spineLabels=(False,False,True,True),
          majorSpace=(4,0.005),
          fontSize=(12,14,14,10),
          legendLabels=legendLabels,
          legendLoc='upper left',
          save=saveOption,
          path=savePath,
          fileName=groupName+'ts_lhf',
          fileFormat='png',
          quality=600 
          )
### tke
tke_plot = [(tsTimesHr[i],tkes[i]) for i in range(len(tkes))]
pl.plot2D( tke_plot,
          chartStyle=['line',],
          zOrders=zOrders,
          lineStyle=lineStyles,                
          lineColor=lineColors,
          lineWidth=lineWidths,
          figSize=(12,4),
          title='Turbulent kinetic energy',
          xTitle='Time [hr]',
          yTitle='TKE [$\mathregular{m^{3}s^{-2}}$]',
          xLimit=ts_xAxis,
          yLimit=(0.0,1600),
          spineVis=(1,1,1,1),
          spineMajorTicks=(1,1,True,True),
          spineMinorTicks=(1,1,True,True),
          tickLengths=(6,3),
          tickDirections=('out','out'),
          spineLabels=(False,False,True,True),
          majorSpace=(4,300),
          fontSize=(12,14,14,10),
          legendLabels=legendLabels,
          legendLoc='upper left',
          save=saveOption,
          path=savePath,
          fileName=groupName+'ts_tke',
          fileFormat='png',
          quality=600 
          )
# cc
cc_plot = [(tsTimesHr[i],ccs[i]) for i in range(len(ccs))]
pl.plot2D( cc_plot,
          chartStyle=['line',],
          zOrders=zOrders,
          lineStyle=lineStyles,                
          lineColor=lineColors,
          lineWidth=lineWidths,
          figSize=(12,4),
          title=None,
          xTitle='Time [hr]',
          yTitle='Cloud cover [ratio]',
          xLimit=ts_xAxis,
          yLimit=(0.0,0.5),
          spineVis=(1,1,1,1),
          spineMajorTicks=(1,1,True,True),
          spineMinorTicks=(1,1,True,True),
          tickLengths=(6,3),
          tickDirections=('out','out'),
          spineLabels=(False,False,True,True),
          majorSpace=(4,0.1),
          fontSize=(12,14,14,10),
          legendLabels=legendLabels,
          legendLoc='best',
          save=saveOption,
          path=savePath,
          fileName=groupName+'ts_cc',
          fileFormat='png',
          quality=600 
          )
#
##########################