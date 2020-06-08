# coding=utf-8
# tile_observing.py
# Author: Jamie Stevens
# This file contains all the code necessary to make one of the
# tiles into an indicator of the observing status.

from atca_status_tile import MoniCAPoint, StatusIndicator

## Routine to return a colour depending on the status of the servo.
def servoStatusColour(servoStatus=None):
  if ((servoStatus == "STOWED") or
      (servoStatus == "PARKED")):
    ## Antenna is stowed, white.
    return [ ( 255, 255, 255 ) ]
  if (servoStatus == "SLEWING"):
    ## Antenna is slewing, yellow.
    return [ ( 255, 255, 0 ) ]
  if (servoStatus == "TRACKING"):
    ## Antenna is tracking, green.
    return [ ( 0, 255, 0 ) ]
  if (servoStatus == "DRIVE_ERROR"):
    ## Antenna has a drive error, red.
    return [ ( 255, 0, 0 ) ]
  return [ ( 0, 0, 0 ) ]

## This routine takes a tile argument and puts all the
## observing indicators on it.
## Arguments:
##    tile = the LiFX tile master instance
##    monica = the MoniCA server instance
def observingTile(tile=None, monica=None):

  ## We monitor per antenna, so we loop over those.
  ants = [ "ca01", "ca02", "ca03", "ca04", "ca05", "ca06" ]
  for i in range(0, len(ants)):
    pointName = "%s.%s" % (ants[i], "servo.State")
    servoStatus = MoniCAPoint(pointName=pointName, monicaServer=monica)
    servoIndicator = StatusIndicator(computeFunction=servoStatus.getValue,
                                     colourFunction=servoStatusColour)
    tile.addIndicator(indicator=servoIndicator,
                      x=[ (2 + i) ], y = [ 0 ])
    
