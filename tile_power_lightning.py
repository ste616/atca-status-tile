# coding=utf-8
# tile_power_lightning.py
# Author: Jamie Stevens
# This file contains all the code necessary to make one of the
# tiles into an indicator of nearby lightning and the power situation.

from atca_status_tile import MoniCAPoint, StatusIndicator
import atca_status_tile.colours as colours

## Routine to take a lightning count and turn it into
## the appropriate colour.
def lightningColour(lightningStatus=None):
  if (lightningStatus is not None):
    count = int(lightningStatus)
    if count < 1:
      ## No lightning, blank.
      return colours.BLANK
    if count < 3:
      ## Some lightning, yellow.
      return colours.YELLOW
    if count < 10:
      # Quite a few strikes, orange.
      return colours.ORANGE
    ## Lots of strikes, red.
    return colours.RED
  return colours.BLANK

## Routine to take the lightning threat level and
## turn it into the appropriate colour.
def threatLevelColour(threatStatus=None):
  if (threatStatus is not None):
    threatLevel = int(threatStatus)
    if threatLevel == 0:
      ## No lightning, green.
      return colours.GREEN
    if threatLevel == 1:
      ## Some lightning, blue.
      return colours.BLUE
    if threatLevel == 2:
      ## Consider generators, yellow.
      return colours.YELLOW
    if threatLevel == 3:
      ## Enable generators, orange.
      return colours.ORANGE
    if threatlevel == 4:
      ## Storm stow, red.
      return colours.RED
    return colours.BLANK

## Routine that determines if mains is available and
## colours this state.
def powerStatusColour(powerStatus=None):
  if (powerStatus is not None):
    if powerStatus == "true":
      ## Mains is available, green.
      return colours.GREEN
    ## Mains is not available, red.
    return colours.RED
  return colours.BLANK

## Routine to return a colour depending on whether
## the generator is running or has experienced a
## critical error.
def generatorStatusColour(generatorStatus=None):
  #print ("DEBUG: generator status called")
  #print (generatorStatus)
  powerSource = generatorStatus[0]
  generatorFailed = generatorStatus[1]
  if generatorFailed == "true":
    ## Generator has a critical error, red.
    return colours.RED
  if powerSource == "GENERATOR":
    ## Running on generator, blue.
    return colours.BLUE
  if powerSource == "mains":
    ## Running on mains, green.
    return colours.GREEN
  if powerSource == "SHARED_LOAD":
    ## Going between mains and generator, yellow.
    return colours.YELLOW
  return colours.BLANK

## This routine takes a tile argument and puts all the
## indicators for power and lightning on it.
## Arguments:
##    tile = the LiFX tile master instance
##    monica = the MoniCA server instance
def powerLightningTile(tile=None, monica=None):

  ## Begin by making a radial plot on the top of the tile
  ## which illustrates if lightning is around and where
  ## it is.
  pointPrefix = "site.environment.lightning"
  lightningPoints = [
    { 'name': 'far_N', 'x': [ 1, 6 ], 'y': [ 0, 0 ] },
    { 'name': 'far_NW', 'x': [ 0 ], 'y': [ 0 ] },
    { 'name': 'far_W', 'x': [ 0, 0 ], 'y': [ 1, 2 ] },
    { 'name': 'far_SW', 'x': [ 0 ], 'y': [ 3 ] },
    { 'name': 'far_S', 'x': [ 1, 6 ], 'y': [ 3, 3 ] },
    { 'name': 'far_SE', 'x' : [ 7 ], 'y' : [ 3 ] },
    { 'name': 'far_E', 'x': [ 7, 7 ], 'y': [ 1, 2 ] },
    { 'name': 'far_NE', 'x' : [ 7 ], 'y': [ 0 ] },
    { 'name': 'near_N', 'x': [ 3, 4 ], 'y': [ 0, 0 ] },
    { 'name': 'near_NW', 'x': [ 2 ], 'y': [ 0 ] },
    { 'name': 'near_W', 'x': [ 1, 1 ], 'y': [ 1, 2 ] },
    { 'name': 'near_SW', 'x': [ 2 ], 'y': [ 3 ] },
    { 'name': 'near_S', 'x': [ 3, 4 ], 'y': [ 3, 3 ] },
    { 'name': 'near_SE', 'x': [ 5 ], 'y': [ 3 ] },
    { 'name': 'near_E', 'x': [ 6, 6 ], 'y': [ 1, 2 ] },
    { 'name': 'near_NE', 'x': [ 5 ], 'y': [ 0 ] },
    { 'name': 'overhead', 'x': [ 2, 3, 4, 5, 2, 3, 4, 5 ],
      'y': [ 1, 1, 1, 1, 2, 2, 2, 2 ] }
    ]
  for i in range(0, len(lightningPoints)):
    pointName = "%s.%s" % (pointPrefix, lightningPoints[i]['name'])
    lstatus = MoniCAPoint(pointName=pointName, monicaServer=monica)
    lightningIndicator = StatusIndicator(computeFunction=lstatus.getValue,
                                         colourFunction=lightningColour)
    tile.addIndicator(indicator=lightningIndicator,
                      x=lightningPoints[i]['x'],
                      y=lightningPoints[i]['y'])
  ## Put the lightning threat level on the bottom half on the left.
  threatName = "%s.threat_int" % pointPrefix
  threatStatus = MoniCAPoint(pointName=threatName, monicaServer=monica)
  threatIndicator = StatusIndicator(computeFunction=threatStatus.getValue,
                                    colourFunction=threatLevelColour)
  tile.addIndicator(indicator=threatIndicator,
                    x=[ 0, 0, 0, 0 ], y=[ 4, 5, 6, 7 ])

  ## The other part of this bottom half of this tile shows the power
  ## and generator states.
  for i in range(0, 7):
    name = "ca"
    if i > 0:
      name = "ca%02d" % i
    pointName = "%s.power.genset.LS4.MainsStatus" % name
    powerStatus = MoniCAPoint(pointName=pointName, monicaServer=monica)
    powerIndicator = StatusIndicator(computeFunction=powerStatus.getValue,
                                     colourFunction=powerStatusColour)
    tile.addIndicator(indicator=powerIndicator,
                      x=[ 1 + i, 1 + i ], y = [ 6, 7 ])
    powerName = "%s.power.powerSource" % name
    sourceStatus = MoniCAPoint(pointName=powerName, monicaServer=monica)
    alarmName = "%s.power.genset.GCP31.CriticalAlarm" % name
    alarmStatus = MoniCAPoint(pointName=alarmName, monicaServer=monica)
    generatorIndicator = StatusIndicator(
      computeFunction=[ sourceStatus.getValue, alarmStatus.getValue ],
      colourFunction=generatorStatusColour)
    tile.addIndicator(indicator=generatorIndicator,
                      x=[ 1 + i, 1 + i ], y=[ 4, 5 ])

