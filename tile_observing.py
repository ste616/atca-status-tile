# coding=utf-8
# tile_observing.py
# Author: Jamie Stevens
# This file contains all the code necessary to make one of the
# tiles into an indicator of the observing status.

from atca_status_tile import MoniCAPoint, StatusIndicator
import atca_status_tile.colours as colours
import re

## Routine which returns a colour if the antenna is stowed or parked.
def antennaStowedParked(servoStatus=None, parentTile=None):
  if (servoStatus == "STOWED"):
    ## Return yellow.
    return colours.YELLOW
  if (servoStatus == "PARKED"):
    ## Return orange.
    return colours.ORANGE
  ## Return blank.
  return colours.BLANK

## Routine which returns a colour if the antenna is slewing.
def antennaSlewing(servoStatus=None, parentTile=None):
  if (servoStatus == "SLEWING"):
    ## Return yellow.
    return colours.YELLOW
  ## Return blank.
  return colours.BLANK

## Routine which returns a colour if the antenna is tracking.
def antennaTracking(servoStatus=None, parentTile=None):
  if (servoStatus == "TRACKING"):
    ## Return green.
    return colours.GREEN
  ## Return blank.
  return colours.BLANK

## Routine which returns a colour if the antenna has a drive error.
def antennaError(servoStatus=None, parentTile=None):
  if (servoStatus == "DRIVE_ERROR"):
    ## Return red.
    if (parentTile is not None):
      parentTile.callForAttention()
    return colours.RED
  ## Return blank.
  return colours.BLANK

## Routine which returns a colour based on the current antenna wrap.
def antennaWrap(servoStatus=None, parentTile=None):
  if (servoStatus == "SOUTH"):
    ## Return blue.
    return colours.BLUE
  if (servoStatus == "NORTH"):
    ## Return yellow.
    return colours.YELLOW
  ## Return blank.
  return colours.BLANK

## Routine to return a colour depending on the status of the servo.
def caobsStatusColour(caobsStatus=None, parentTile=None):
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
    ## Call for attention.
    if (parentTile is not None):
      parentTile.callForAttention()
    return colours.BLUE
  
  return colours.BLANK

def degStringToFloat(degString):
  els = re.split('[Â°\'\"]+', degString)
  neg = 1
  if (degString[0] == '-'):
    neg = -1
  deg = float(els[0]) * neg
  minute = float(els[1])
  sec = float(els[2]) + float(els[3])
  rv = neg * (deg + minute / 60. + sec / 3600.)
  return rv

def slewingErrorColour(err):
  ## Translate a distance in degrees to a colour.
  if (err > 100):
    return colours.RED[0]
  if (err > 20):
    return colours.ORANGE[0]
  if (err > 1):
    return colours.BLUE[0]
  return colours.GREEN[0]

def positionErrorStatusColour(positionErrors=None, parentTile=None):
  azError = positionErrors[0]
  elError = positionErrors[1]
  rmsError = float(positionErrors[2])
  servoState = positionErrors[3]

  if (servoState == "SLEWING"):
    ## The position error is az and el.
    azDegError = degStringToFloat(azError)
    elDegError = degStringToFloat(elError)
    return [ slewingErrorColour(azDegError),
             slewingErrorColour(elDegError) ]
  if (servoState == "TRACKING"):
    ## The position error is from the RMS (in arcsec).
    if (rmsError > 10):
      return colours.RED
    if (rmsError > 2):
      return colours.ORANGE
    return colours.GREEN

  return colours.BLANK

def cycleColour(cycleNumber=None, parentTile=None):
  ## We simply light up each pixel based on its
  ## binary representation.
  ncyc = int(cycleNumber.replace("cyc", ""))
  ## We have 16 pixels to fill.
  ncycBinary = format(ncyc, 'b').zfill(16)
  rv = []
  for i in range(15, -1, -1):
    if (ncycBinary[i] == "1"):
      rv.append(colours.WHITE[0])
    else:
      rv.append(colours.BLACK[0])
  return rv

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
    ## Seventh and eight rows are the position errors.
    azimuthErrorPointName = "%s.servo.AzError" % ants[i]
    elevationErrorPointName = "%s.servo.ElError" % ants[i]
    rmsErrorPointName = "%s.servo.RMSError" % ants[i]
    azimuthError = MoniCAPoint(pointName=azimuthErrorPointName,
                               monicaServer=monica)
    elevationError = MoniCAPoint(pointName=elevationErrorPointName,
                                 monicaServer=monica)
    rmsError = MoniCAPoint(pointName=rmsErrorPointName,
                           monicaServer=monica)
    positionErrorIndicator = StatusIndicator(
      computeFunction=[ azimuthError.getValue, elevationError.getValue,
                        rmsError.getValue, servoStatus.getValue ],
      colourFunction=positionErrorStatusColour)
    tile.addIndicator(indicator=positionErrorIndicator,
                      x=[ (2 + i), (2 + i) ],
                      y=[ 6, 7 ])
    
  ## The side of the panel is a binary representation of the
  ## number of cycles on the current scan. The idea is that if it
  ## gets too high, you may have typed track...
  cyclePointName = "site.misc.obs.cycleNum"
  cycleStatus = MoniCAPoint(pointName=cyclePointName, monicaServer=monica)
  cycleIndicator = StatusIndicator(computeFunction=cycleStatus.getValue,
                                   colourFunction=cycleColour)
  tile.addIndicator(indicator=cycleIndicator,
                    x=[ 0, 1, 0, 1, 0, 1, 0, 1,
                        0, 1, 0, 1, 0, 1, 0, 1 ],
                    y=[ 0, 0, 1, 1, 2, 2, 3, 3,
                        4, 4, 5, 5, 6, 6, 7, 7 ])
