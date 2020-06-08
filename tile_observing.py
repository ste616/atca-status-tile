# coding=utf-8
# tile_observing.py
# Author: Jamie Stevens
# This file contains all the code necessary to make one of the
# tiles into an indicator of the observing status.

from atca_status_tile import MoniCAPoint, StatusIndicator
import atca_status_tile.colours as colours

## Routine which returns a colour if the antenna is stowed or parked.
def antennaStowedParked(servoStatus=None):
  if (servoStatus == "STOWED"):
    ## Return yellow.
    return colours.YELLOW
  if (servoStatus == "PARKED"):
    ## Return orange.
    return colours.ORANGE
  ## Return blank.
  return colours.BLANK

## Routine which returns a colour if the antenna is slewing.
def antennaSlewing(servoStatus=None):
  if (servoStatus == "SLEWING"):
    ## Return yellow.
    return colours.YELLOW
  ## Return blank.
  return colours.BLANK

## Routine which returns a colour if the antenna is tracking.
def antennaTracking(servoStatus=None):
  if (servoStatus == "TRACKING"):
    ## Return green.
    return colours.GREEN
  ## Return blank.
  return colours.BLANK

## Routine which returns a colour if the antenna has a drive error.
def antennaError(servoStatus=None):
  if (servoStatus == "DRIVE_ERROR"):
    ## Return red.
    return colours.RED
  ## Return blank.
  return colours.BLANK

## Routine which returns a colour based on the current antenna wrap.
def antennaWrap(servoStatus=None):
  if (servoStatus == "SOUTH"):
    ## Return blue.
    return colours.BLUE
  if (servoStatus == "NORTH"):
    ## Return yellow.
    return colours.YELLOW
  ## Return blank.
  return colours.BLANK

## Routine to return a colour depending on the status of the servo.
def caobsStatusColour(caobsStatus=None):
  if ((caobsStatus == "STOWED") or
      (caobsStatus == "PARKED")):
    ## Antenna is stowed, white.
    return colours.WHITE
  if (caobsStatus == "SLEWING"):
    ## Antenna is slewing, yellow.
    return colours.YELLOW
  if (caobsStatus == "TRACKING"):
    ## Antenna is tracking, green.
    return colours.GREEN
  if (caobsStatus == "DRIVE_ERROR"):
    ## Antenna has a drive error, red.
    return colours.RED
  if (caobsStatus == "DISABLED"):
    ## Antenna isn't active, turquoise.
    return colours.TURQUOISE
  if (caobsStatus == "OFF-LINE"):
    ## Antenna isn't connected, orange.
    return colours.ORANGE
  if (caobsStatus == "IDLE"):
    ## Antenna isn't moving, blue.
    return colours.BLUE
  
  return colours.BLANK

## This routine takes a tile argument and puts all the
## observing indicators on it.
## Arguments:
##    tile = the LiFX tile master instance
##    monica = the MoniCA server instance
def observingTile(tile=None, monica=None):

  ## We monitor per antenna, so we loop over those.
  ants = [ "ca01", "ca02", "ca03", "ca04", "ca05", "ca06" ]
  for i in range(0, len(ants)):
    xant = [ ( 2 + i ) ]
    pointName = "%s.servo.State" % ants[i]
    ## Top row lights up if the antenna is stowed or parked.
    servoStatus = MoniCAPoint(pointName=pointName, monicaServer=monica)
    stowIndicator = StatusIndicator(computeFunction=servoStatus.getValue,
                                    colourFunction=antennaStowedParked)
    tile.addIndicator(indicator=stowIndicator,
                      x=xant, y=[ 0 ])
    caobsPointName = "%s.misc.obs.caobsAntState" % ants[i]
    ## Second row lights up different colours depending on the
    ## caobs reported state.
    caobsStatus = MoniCAPoint(pointName=caobsPointName, monicaServer=monica)
    caobsIndicator = StatusIndicator(computeFunction=caobsStatus.getValue,
                                     colourFunction=caobsStatusColour)
    tile.addIndicator(indicator=caobsIndicator,
                      x=xant, y=[ 1 ])
    ## Third row lights up if the antenna is slewing.
    slewingIndicator = StatusIndicator(computeFunction=servoStatus.getValue,
                                       colourFunction=antennaSlewing)
    tile.addIndicator(indicator=slewingIndicator,
                      x=xant, y=[ 2 ])
    ## Fourth row lights up if the antenna is tracking.
    trackingIndicator = StatusIndicator(computeFunction=servoStatus.getValue,
                                        colourFunction=antennaTracking)
    tile.addIndicator(indicator=trackingIndicator,
                      x=xant, y=[ 3 ])
    ## Fifth row lights up if the antenna has a drive error.
    errorIndicator = StatusIndicator(computeFunction=servoStatus.getValue,
                                     colourFunction=antennaError)
    tile.addIndicator(indicator=errorIndicator,
                      x=xant, y=[ 4 ])
    wrapPointName = "%s.servo.AzWrap" % ants[i]
    ## Sixth row lights up depending on the antenna wrap.
    wrapStatus = MoniCAPoint(pointName=wrapPointName, monicaServer=monica)
    wrapIndicator = StatusIndicator(computeFunction=wrapStatus.getValue,
                                    colourFunction=antennaWrap)
    tile.addIndicator(indicator=wrapIndicator,
                      x=xant, y=[ 5 ])
