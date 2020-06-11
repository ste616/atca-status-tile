# coding=utf-8
# tile_weather.py
# Author: Jamie Stevens
# This file contains all the code necessary to monitor the on-site
# weather conditions and ambient temperatures in the antennas.

from atca_status_tile import MoniCAPoint, StatusIndicator
import atca_status_tile.colours as colours

def ambientTemperatureColour(tempStatus=None):
  ## We simply look at whether the state is in error.
  if (tempStatus == "true"):
    return colours.RED
  return colours.GREEN

def pedestalTemperatureColour(tempStatus=None, parentTile=None):
  ## We use the ambient temperature colour translator, but we don't
  ## care if there's an error.
  return ambientTemperatureColour(tempStatus=tempStatus)

def vertexTemperatureColour(tempStatus=None, parentTile=None):
  ## We use the ambient temperature colour translator.
  rc = ambientTemperatureColour(tempStatus=tempStatus)
  ## If it comes back red, call for attention.
  if (rc == colours.RED):
    parentTile.callForAttention()
  return rc

def rainColour(rainTips=None, parentTile=None):
  ## Just turn the number of tips into a binary number.
  try:
    ntips = int(rainTips)
  except ValueError:
    ntips = 0
  ## We have 8 pixels to fill.
  ntipsBinary = format(ntips, 'b').zfill(8)
  rv = []
  for i in range(7, -1, -1):
    if (ntipsBinary[i] == "1"):
      rv.append(colours.BLUE[0])
    else:
      rv.append(colours.BLACK[0])
  return rv

def softWindColour(windState=None, parentTile=None):
  ## Is the wind-stow triggered?
  if (windState == "true"):
    parentTile.callForAttention()
    return colours.RED
  return colours.GREEN

def pmonWindColour(windState=None, parentTile=None):
  ## Is the wind-stow triggered?
  if (windState == "OK"):
    return colours.GREEN
  parentTile.callForAttention()
  return colours.RED

def siteWindColour(windSeries=None, parentTile=None):
  ## We have 7 columns of 4 pixels height to fill.
  ## The most recent wind is in the early part of the
  ## array we return, and each time needs four pixels.
  ## Low wind values have earlier pixels lit.
  pixelValues = [ colours.BLANK[0] ] * 28
  print(windSeries['times'])
  return pixelValues

## This routine takes a tile argument and puts all the weather
## indicators on it.
## Arguments:
##    tile = the LiFX tile master instance
##    monica = the MoniCA server instance
def weatherTile(tile=None, monica=None):

  ## Some of the points are per antenna, so we set those up first.
  ants = [ "ca01", "ca02", "ca03", "ca04", "ca05", "ca06" ]
  for i in range(0, len(ants)):
    xant = [ ( 2 + i ), ( 2 + i ) ]
    ## The bottom two rows are the pedestal temperature warnings.
    pedestalPointName = "%s.environment.ambient_temps.PedestalTemp" % ants[i]
    pedestalStatus = MoniCAPoint(pointName=pedestalPointName,
                                 monicaServer=monica)
    pedestalIndicator = StatusIndicator(
      computeFunction=pedestalStatus.getErrorState,
      colourFunction=pedestalTemperatureColour)
    tile.addIndicator(indicator=pedestalIndicator,
                      x=xant, y=[ 6, 7 ])
    ## The two rows above that are the vertex temperature warnings.
    vertexPointName = "%s.environment.ambient_temps.VertexTemp" % ants[i]
    vertexStatus = MoniCAPoint(pointName=vertexPointName,
                               monicaServer=monica)
    vertexIndicator = StatusIndicator(
      computeFunction=vertexStatus.getErrorState,
      colourFunction=vertexTemperatureColour)
    tile.addIndicator(indicator=vertexIndicator,
                      x=xant, y=[ 4, 5 ])
  ## On the left side of these bottom rows is a binary
  ## representation of tips of the rain gauge, filling up from
  ## the bottom.
  rainPointName = "site.environment.weather.RainTips"
  rainStatus = MoniCAPoint(pointName=rainPointName,
                           monicaServer=monica)
  rainIndicator = StatusIndicator(
    computeFunction=rainStatus.getValue,
    colourFunction=rainColour)
  tile.addIndicator(indicator=rainIndicator,
                    x=[ 0, 1, 0, 1, 0, 1, 0, 1 ],
                    y=[ 7, 7, 6, 6, 5, 5, 4, 4 ])
                        
  ## On the top left is the software and PMON wind-stow indicators.
  softWindName = "site.environment.weather.WindStowAlert"
  softWindStatus = MoniCAPoint(pointName=softWindName,
                               monicaServer=monica)
  softWindIndicator = StatusIndicator(
    computeFunction=softWindStatus.getValue,
    colourFunction=softWindColour)
  tile.addIndicator(indicator=softWindIndicator,
                    x=[ 0, 0 ], y=[ 0, 1 ])
  pmonWindName = "ca.misc.pmon.pmon_autostow"
  pmonWindStatus = MoniCAPoint(pointName=pmonWindName,
                               monicaServer=monica)
  pmonWindIndicator = StatusIndicator(
    computeFunction=pmonWindStatus.getValue,
    colourFunction=pmonWindColour)
  tile.addIndicator(indicator=pmonWindIndicator,
                    x=[ 0, 0 ], y=[ 2, 3 ])
  
  ## The time series of the wind speed are shown at the top
  ## right.
  siteWindName = "site.environment.weather.WindSpeed"
  siteWindStatus = MoniCAPoint(pointName=siteWindName,
                               monicaServer=monica,
                               isTimeSeries=True,
                               startTime=-1,
                               interval=30)
  siteWindIndicator = StatusIndicator(
    computeFunction=siteWindStatus.getSeries,
    colourFunction=siteWindColour)
  tile.addIndicator(indicator=siteWindIndicator,
                    x=[ 7, 7, 7, 7, 6, 6, 6, 6, 5, 5, 5, 5,
                        4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2,
                        1, 1, 1, 1 ],
                    y=[ 3, 2, 1, 0, 3, 2, 1, 0, 3, 2, 1, 0,
                        3, 2, 1, 0, 3, 2, 1, 0, 3, 2, 1, 0,
                        3, 2, 1, 0 ])
