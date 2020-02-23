#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Plotting function, applies matplotlib
"""
# ensure modules
if 'np' not in dir(): import numpy as np
if 'plt' not in dir(): import matplotlib.pyplot as plt
#
def plot2D( dataSets,
           chartStyle=['scatter',],
           lineStyle=['solid',],                
           lineColor=['black',],
           lineWidth=[1.0,],
           zOrders=None,
           figSize=(8,5),
           title=None,
           xTitle=None,
           yTitle=None,
           xLimit=(None,None),
           yLimit=(None,None),
           xScaleLog=False,
           yScaleLog=False,
           spineVis=(True,True,True,True),
#           spineLoc=(None,None,None,None),
           spineMajorTicks=(True,True,True,True),
           spineMinorTicks=(True,True,True,True),
           tickLengths=(6,3),
           tickDirections=('out','out'),
           spineLabels=(False,False,True,True),
           majorSpace=(None,None),
           minorSpace=(None,None),
           xTicks=None,
           yTicks=None,
           xLabels=None,
           yLabels=None,
           grid=(False,False),
           labelRotation=(0,0),
           minorLabels=False,
           fontSize=(12,14,14,10),
           legendLabels=None,
           legendLoc='best',
           legendCols=1,
           legendShadow=False,
           textBox=False,
           save=False,
           path=None,
           fileName=None,
           fileFormat='png',
           quality=300 ):
    ''' 
    Draws a 2D plot from data given in sets of arrays.
    
     ... see all default arguments above ...
    
     dataSets (array): an array of tuples, one tuple per curve in the format
                       (<array of x-data>, <array of y-data>).
     chartStyle (str):
     lineStyle (str):
     lineColor (str):
     lineWidth (int/float):
     figSize (tuple):
     title (str): text appearing above the plot
     xTitle (str): text appearing below the x-axis
     yTitle (str): text appearing aside the y-axis
     spineVis (array): four bools representing the visibility of each 
                       spine in order (right, top, left, bottom).
     grid (bool): whether to show the grid.
     majorSpace (array):
     minorTicks (bool):
     minorSpace (array):
     xLabels (array):
     yLabels (array):
     labelRotation (array):
     minorLabels (array):
     fontSize (array-like,1D):
     grid (bool):
     legend (bool):
     textbox ():
     save (bool): option to save the output figures.
     path (str): directory to save images.
     fileName (str):
     quality (int): dots-per-inch of the saved image.  
        
    Returns None but outputs the figure to the console and can save.
    '''
    #
    '''
    ### <to do> ###
    '''
    #
    print('---')
    #
    ### check input data ###
    #
    # create figure and axes objects
    fig,ax = plt.subplots(figsize=figSize)
    ### twin axes
#    ax2.twinx()
    ###
    # make curves
    xMin=None; xMax=None; yMin=None; yMax=None # set holders
    if zOrders==None: zOrders = [i for i in range(len(dataSets)-1,-1,-1)]
    for i in range(len(dataSets)): # loop over given sets
        # ensure data as numpy arrays
        xCoords = np.array( dataSets[i][0] )
        yCoords = np.array( dataSets[i][1] )
        # track axes minimums and maximums
        if xMin is None: xMin = xCoords.min()
        elif xCoords.min() < xMin: xMin = xCoords.min()  
        if xMax is None: xMax = xCoords.max()
        elif xCoords.max() > xMax: xMax = xCoords.max()
        if yMin is None: yMin = yCoords.min()
        elif yCoords.min() < yMin: yMin = yCoords.min()
        if yMax is None: yMax = yCoords.max()
        elif yCoords.max() > yMax: yMax = yCoords.max()
        # set styles
        ### improve dynamic styling ###
        try: cStyle = chartStyle[i]    # if given
        except: cStyle = chartStyle[0] # else same as first
        try: zOrder = zOrders[i] # if given
        except: zOrder = 0       # else 0
        try: lColor = lineColor[i]
        except: lColor = lineColor[0]
        try: width = lineWidth[i]
        except: width = lineWidth[0]
        try: lStyle = lineStyle[i]
        except: lStyle = lineStyle[0]
        # make curve
        try:
            if cStyle == 'line':
                ax.plot( xCoords, yCoords, zorder=zOrder,
                        color=lColor,linewidth=width,linestyle=lStyle )
            elif cStyle == 'scatter':
                ax.scatter( xCoords, yCoords, zorder=zOrder,
                           color=lColor,linewidth=width,linestyle=lStyle )
            elif cStyle == 'bar':
                ax.bar( xCoords, yCoords, zorder=zOrder,
                       color=lColor,linewidth=width,linestyle=lStyle )
            else: # handle unknown style
                print('! Error: unknown chart style...plotting scatter.')
                ax.scatter( xCoords, yCoords, zorder=zOrder,
                           color=lColor,linewidth=width,linestyle=lStyle )
            #
        except: # report and return None
            # This error usually occurs because x and y data of different
            # shape given
            print('! Error: in chart styling ... returning None.')
            return None
    #
    # axis scales
    if xScaleLog: ax.set_xscale('log')
    if yScaleLog: ax.set_yscale('log')
#    if xScaleLog: plt.xscale('log')
#    if yScaleLog: plt.yscale('log')
    # axis limits
    if xLimit[0] is not None: xLimLo = xLimit[0] ## if custom
    else: xLimLo = xMin                          ## else from data
    if xLimit[1] is not None: xLimHi = xLimit[1]
    else: xLimHi = xMax
    if yLimit[0] is not None: yLimLo = yLimit[0]
    else: yLimLo = yMin
    if yLimit[1] is not None: yLimHi = yLimit[1]
    else: yLimHi = yMax
    # set axis limits
    ax.set_xlim(xLimLo,xLimHi)
    ax.set_ylim(yLimLo,yLimHi)
    # get axis lengths
    deltaX = xLimHi - xLimLo
    deltaY = yLimHi - yLimLo
    # spine visibilities
    ax.spines['right'].set_visible(spineVis[0])
    ax.spines['top'].set_visible(spineVis[1])
    ax.spines['left'].set_visible(spineVis[2])
    ax.spines['bottom'].set_visible(spineVis[3])
#    ###################### not working
#    ## spine locations
#    #### custom option not working
#    #### breaks log scale ability
#    ## by limits
##    ax.spines['right'].set_position(('data',xLimHi))
##    ax.spines['top'].set_position(('data',yLimHi))
##    ax.spines['left'].set_position(('data',xLimLo))
##    ax.spines['bottom'].set_position(('data',yLimLo))
#    ## with custom option
#    if spineLoc[0] is not None: 
#        ax.spines['right'].set_position(('data',spineLoc[0]))
#    else: ax.spines['right'].set_position(('data',xLimHi))
#    if spineLoc[1] is not None:
#        ax.spines['top'].set_position(('data',spineLoc[1]))
#    else: ax.spines['top'].set_position(('data',yLimHi))
#    if spineLoc[2] is not None:
#        ax.spines['left'].set_position(('data',spineLoc[0]))
#    else: ax.spines['left'].set_position(('data',xLimLo))
#    if spineLoc[3] is not None:
#        ax.spines['bottom'].set_position(('data',spineLoc[1]))
#    else: ax.spines['bottom'].set_position(('data',yLimLo))
#    ######################
    # major tick spacing and labels
    ## x-axis
    if majorSpace[0] is None: # spacing not given
        if xLabels is None:   # labels not given
            None              # neither given then set by matplotlib
        if xLabels is not None: # labels given
            xSpace = deltaX/(len(xLabels)-1) # calculate spacing from labels
            xTicks = [xLimLo + i*xSpace
                      for i in range(len(xLabels))] # set tick coords
    elif majorSpace[0] is not None:        # spacing given
        xTicks = [xLimLo + i*majorSpace[0] # set tick coords
                  for i in range(int(deltaX/majorSpace[0]+1.5))]
        if xLabels is None:             # labels not given
            xSpace = majorSpace[0]; n=0 # get given space and set counter
            while xSpace%1 != 0:        # determine proper decimal precision
                xSpace *= 10; n += 1    # increment scale and counter
            xLabels = [round(tick,n) for tick in xTicks] # get label list
        elif xLabels is not None: # labels given
            None                  # both given so no action
    if xLabels is not None:   # if labels set then run all-integer check
        xAllInts=True         # set flag
        for label in xLabels: # loop over labels
            if label%1 != 0: xAllInts=False # if non-integer label found
        if xAllInts:                        # if labels are all integers
            xLabels = [int(label) for label in xLabels] # reset labels as ints
    # set custom tick and labels
    if xTicks and xLabels: # if custom
        plt.xticks(xTicks,xLabels) # set x-axis ticks and labels
    ###################### old method
#    if majorSpace[0]: # custom x-axis tick spacing
#        xticks = [xLimLo + i*majorSpace[0] 
#                  for i in range(int(deltaX/majorSpace[0]+1.5))] # set coords
#        if not xLabels: # if x-axis labels not given
#            xSpace = majorSpace[0]; n=0 
#            while xSpace%1 != 0: # determine proper decimal precision
#                xSpace *= 10; n += 1
#            xLabels = [round(tick,n) for tick in xticks] # get label list
#    elif xLabels and not majorSpace[0]: # for labels given but not spacing
#        xSpace = deltaX/len(xLabels)
#        xticks = [origin[0] + i*xSpace
#                  for i in range(len(xLabels))] # set tick 
    ######################
    # repeat procedure for y axis
    if majorSpace[1]: # custom y-axis tick spacing
        yTicks = [yLimLo + i*majorSpace[1] 
                  for i in range(int(deltaY/majorSpace[1]+1.5))] # set coords
        if not yLabels: # if y-axis labels not given
            ySpace = majorSpace[1]; n=0 
            while ySpace%1 != 0: # determine proper decimal precision
                ySpace *= 10; n += 1
            yLabels = [round(tick,n) for tick in yTicks] # get label list
            ### remove padded zeros on decimal labels
#            fixLabels = []
#            for label in yLabels:
#                if type(label) == float and label < 1:
#                    newLabel = str(label)
#                    while newLabel[-1] == '0': newLabel = newLabel[:-1]
#                    fixLabels.append(newLabel)
#                else: fixLabels.append(label)
#            yLabels = fixLabels
            ###
    elif yLabels and not majorSpace[1]: # for labels given but not spacing
        ySpace = deltaY/(len(yLabels)-1)
        yTicks = [yLimLo + i*ySpace
                  for i in range(len(yLabels))] # set tick coords
    # if labels set then run all-integer check
    if yLabels is not None:
        yAllInts=True # set flag
        for label in yLabels: # run check
            if label%1 != 0: yAllInts=False
        if yAllInts: # if all integers
            yLabels = [int(label) for label in yLabels] # reset labels as ints
    if yTicks and yLabels: # if custom
        plt.yticks(yTicks,yLabels) # set y-axis spacing and labels
    # major ticks
    ax.tick_params(which='major', # set major
                   length=tickLengths[0],       # length
                   direction=tickDirections[0], # direction
                   right=spineMajorTicks[0],    # visibilities
                   top=spineMajorTicks[1],
                   left=spineMajorTicks[2],
                   bottom=spineMajorTicks[3])
    # minor ticks
    for entry in spineMinorTicks: # check if any custom minor
        if entry: # if custom entry found
            ax.minorticks_on() # turn on minor ticks
            ax.tick_params(which='minor', # set all custom minor
                           length=tickLengths[1],       # length
                           direction=tickDirections[1], # direction
                           right=spineMinorTicks[0],    # visibilities
                           top=spineMinorTicks[1],
                           left=spineMinorTicks[2],
                           bottom=spineMinorTicks[3])
            break # end check
    # label visibilities
    ax.tick_params(labelright=spineLabels[0],
                   labeltop=spineLabels[1],
                   labelleft=spineLabels[2],
                   labelbottom=spineLabels[3])
    # label rotaions
    ax.xaxis.set_tick_params(rotation=labelRotation[0])
    ax.yaxis.set_tick_params(rotation=labelRotation[1])
    # grid
    if grid[0] or grid[1]: # if either set both
        plt.grid( which='major', visible=grid[0] )
        plt.grid( which='minor', visible=grid[1] )
    ax.set_axisbelow(True) # ensure grid below data
    # titles and font sizes
    ax.tick_params(labelsize=fontSize[3])
    if title: plt.title(title,fontsize=fontSize[0],
                        pad=int(fontSize[3]*1.5) )
    if xTitle: ax.set_xlabel(xTitle,fontsize=fontSize[1])         
    if yTitle: ax.set_ylabel(yTitle,fontsize=fontSize[2])
    ########################## legend
    # legend
    if legend:
        ### simplify sloppy redundancies in block ###
        ## labels and location
        if legendLabels is None: 
            legendLabels = [str(i) for i in range(len(dataSets))]
            #
        if legendLoc is None: 
            legendLoc='best'
        else:
            # reference
            ### more custom locations ###
            customLocs = ['outside right',]
            references = ['upper center',]
            # placement
            ### custom placement ###
            bboxs = [(1.25,0.75),]
            if legendLoc in customLocs:
                finalLoc = references[customLocs.index(legendLoc)]
                bboxTA = bboxs[customLocs.index(legendLoc)]
                ax.legend(legendLabels,
                          loc=finalLoc,
                          bbox_to_anchor=bboxTA,
                          shadow=legendShadow,
                          ncol=legendCols
                          )
            else:
                ax.legend(legendLabels,
                          loc=legendLoc,
                          shadow=legendShadow,
                          ncol=legendCols
                          )
                    #
        ## legend formatting
    ##########################
    ### text box ###
    # save file
    if save:
        if 'os' not in dir(): import os # ensure module
        if not path: path = os.getcwd()+'\\' # path not given
        if not fileName: # filename not given
            import datetime # get current utc
            now = datetime.datetime.utcnow().strftime('%y%m%d%H%M%S')
            saveFileName = now[0:6]+'_'+now[6:] # set name from time
        else: saveFileName = fileName # filename given
        # prevent file overwrites
        if os.path.exists(path+saveFileName+f'.{fileFormat}'):
            saveIndex=1 # set index
            while os.path.exists(path+saveFileName+ # iterate index and check
                                 f'_{saveIndex}.{fileFormat}'): saveIndex+=1
            saveFileName += f'_{saveIndex}' # attach index
        # attach file format
        saveFileName += f'.{fileFormat}'
        plt.savefig( path + saveFileName, # save figure 
                    dpi=quality, 
                    format=fileFormat, 
                    transparent=False) 
        ### transparency options
        print(f'Figure saved as: ... \n {path+saveFileName}') # report
    ## show figure and return None
    '''
    '''
    plt.show()
    print('---')
    return None
#
##########################
if __name__ == '__main__':
    # 
    xData = np.arange(10)
    yData1 = np.arange(10)
    yData2 = np.arange(10,0,-1)
    #
    plot2D( [ (xData,yData1), 
              (xData,yData2) ],
           chartStyle=['scatter','line'],
           lineStyle=['solid','dashed'],                
           lineColor=['k','b'],
           lineWidth=[1.0,2.0],
           figSize=(8,5),
           title='Testing plot2D()',
           xTitle='x-axis',
           yTitle='y-axis',
           xLimit=(None,None),
           yLimit=(None,None),
           spineVis=(True,True,True,True),
           spineMajorTicks=(True,True,True,True),
           spineMinorTicks=(True,True,True,True),
           spineLabels=(False,False,True,True),
           majorSpace=(None,None),
           minorSpace=(None,None),
           xLabels=None,
           yLabels=None,
           xTicks=None,
           yTicks=None,
           labelRotation=(0,0),
           minorLabels=False,
           fontSize=(12,12,12,10),
           grid=(False,False),
           legend=False,
           textBox=False,
           save=False,
           path=None,
           fileName='test',
           fileFormat='png',
           quality=300 )
    #
#
##########################
