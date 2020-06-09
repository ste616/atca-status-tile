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
    
