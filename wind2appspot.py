#!/usr/bin/env python
# author: cyril: cyrilbiz@gmail.com
# parses the file cscVantageLoop.csv generated by the csv extension installed on weewx (see https://github.com/weewx/weewx/wiki/csv) 
# and writes the cscWind.txt to be pushed to appspot

import datetime
import os
import time

vantageLoopFilePath = '/home/admin/wind2web/data/cscVantageLoop.csv'
appspotFilePath     = "/home/admin/wind2web/data/cscWind.txt"

# read vantageLoop lines
with open(vantageLoopFilePath) as fp:
    line0 = fp.readline()
    line1 = fp.readline()
    
# split commas
keys = line0.split (",")
vals = line1.split(",")
    
# indexes
dateTimeIdx    = keys.index('# dateTime')
windSpeed10Idx = keys.index('windSpeed10')
windDirDegIdx  = keys.index('windDir')
windGustIdx    = keys.index('windGust')
    
# get data from  list
dateTime      = str(datetime.datetime.fromtimestamp(float(vals[dateTimeIdx] ) ))
dateTimeUnix  = vals[dateTimeIdx] 
dateTimeIso   = str(datetime.datetime.fromtimestamp( float(vals[dateTimeIdx]) ).isoformat()) + 'UTC-7 hours'

    
windSpeed10     = vals[windSpeed10Idx] # wind average in the past 10 seconds (as per vantage doc regarding Loop data)
windDirDeg      = vals[windDirDegIdx] # wind direction in degrees
    

if (windDirDeg != 'None'):
    windDirDegFloat    = float(windDirDeg) # convert to float in order to do proper division for the "degrees to sector conversion"
else:
    windDirDegFloat = 0 # in case there is no wind direction in this frame set it to 0 degree (weewx content varies from frame to frame)

# convert angles to sectors 
windGust        = vals[windGustIdx]
sectors         =  ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW","N"]
windDirSec      = sectors[int(windDirDegFloat/22.5)] # degrees to sector conversion

# build the strings
windSpeedStr    =  ' wind speed | ' + windSpeed10 + ' | knots | ' + dateTimeUnix + '\n'
windDirDegStr   = ' wind direction | ' + windDirDeg + ' | degrees | ' + dateTimeUnix + '\n'
windDirSecStr   = ' wind direction | ' +  windDirSec + ' | sector | ' + dateTimeUnix + '\n'
windGustStr     =  ' wind gust speed | ' + windGust + ' | knots | ' + dateTimeUnix + '\n'
    
# write the strings to the txt file that will be uploaded to appspot
with open(appspotFilePath,'w') as fp:
    fp.write( windSpeedStr )
    fp.write( windDirDegStr )
    fp.write( windDirSecStr )
    fp.write( windGustStr )






