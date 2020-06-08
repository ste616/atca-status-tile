# coding=utf-8
# tile_cyrogenics.py
# Author: Jamie Stevens
# This file contains all the code necessary to monitor the cryogenic
# temperatures and compressors on each of the antennas, and a PMON
# summary as well.

from atca_status_tile import MoniCAPoint, StatusIndicator
import atca_status_tile.colours as colours

def errorChecker(pointText=None, parentTile=None):
  ## Checking for problems with a cryo point is easy.
  ## Everything is OK if the text says "OK", otherwise we have a
  ## problem.
  if (pointText == "OK"):
    return colours.GREEN
  ## Call for attention.
  parentTile.callForAttention()
  return colours.RED

def stateChecker(pointState=None, parentTile=None):
  ## Checking for problems with the PMON state is also easy.
  ## Everything is OK if no point reports an error state,
  ## otherwise we have a problem.
  errorStateFound = False
  for i in range(0, len(pointState)):
    if (pointState[i] == "true"):
      errorStateFound = True
  if (errorStateFound):
    ## Call for attention.
    parentTile.callForAttention()
    return colours.RED
  ## Otherwise we're alright.
  return colours.GREEN

## This routine takes a tile argument and puts all the cryogenic
## indicators on it.
## Arguments:
##    tile = the LiFX tile master instance
##    monica = the MoniCA server instance
def cryogenicsTile(tile=None, monica=None):

  ## We monitor per antenna, so we loop over those.
  ants = [ "ca01", "ca02", "ca03", "ca04", "ca05", "ca06" ]
  for i in range(0, len(ants)):
    xant = [ ( 1 + i ) ]
    ## Top row is thermal summary, 16cm dewar.
    temp16Point = "%s.cryo.LS.Summary" % ants[i]
    temp16Status = MoniCAPoint(pointName=temp16Point, monicaServer=monica)
    temp16Indicator = StatusIndicator(computeFunction=temp16Status.getValue,
                                      colourFunction=errorChecker)
    tile.addIndicator(indicator=temp16Indicator,
                      x=xant, y=[ 0 ])
    ## Second row is compressor summary, 16cm system.
    comp16Point = "%s.cryo.compressor.system2.Summary" % ants[i]
    comp16Status = MoniCAPoint(pointName=comp16Point, monicaServer=monica)
    comp16Indicator = StatusIndicator(computeFunction=comp16Status.getValue,
                                      colourFunction=errorChecker)
    tile.addIndicator(indicator=comp16Indicator,
                      x=xant, y=[ 1 ])
    ## Third row is thermal summary, 4cm dewar.
    temp4Point = "%s.cryo.CX.Summary" % ants[i]
    temp4Status = MoniCAPoint(pointName=temp4Point, monicaServer=monica)
    temp4Indicator = StatusIndicator(computeFunction=temp4Status.getValue,
                                     colourFunction=errorChecker)
    tile.addIndicator(indicator=temp4Indicator,
                      x=xant, y=[ 2 ])
    ## Fourth row is compressor summary, 16cm system.
    comp4Point = "%s.cryo.compressor.system1.Summary" % ants[i]
    comp4Status = MoniCAPoint(pointName=comp4Point, monicaServer=monica)
    comp4Indicator = StatusIndicator(computeFunction=comp4Status.getValue,
                                     colourFunction=errorChecker)
    tile.addIndicator(indicator=comp4Indicator,
                      x=xant, y=[ 3 ])
    ## Fifth row is thermal summary, 15mm dewar.
    temp15Point = "%s.cryo.KQW.Summary" % ants[i]
    temp15Status = MoniCAPoint(pointName=temp15Point, monicaServer=monica)
    temp15Indicator = StatusIndicator(computeFunction=temp15Status.getValue,
                                      colourFunction=errorChecker)
    tile.addIndicator(indicator=temp15Indicator,
                      x=xant, y=[ 4 ])
    ## Sixth row is compressor summary, 15mm system.
    comp15Point = "%s.cryo.compressor.system3.Summary" % ants[i]
    comp15Status = MoniCAPoint(pointName=comp15Point, monicaServer=monica)
    comp15Indicator = StatusIndicator(computeFunction=comp15Status.getValue,
                                      colourFunction=errorChecker)
    tile.addIndicator(indicator=comp15Indicator,
                      x=xant, y=[ 5 ])

    ## The bottom two rows are a composite of all the PMON points.
    pmonPoints = [ "power_fail", "drive_disabled", "drive_fault",
                   "cryo_kq", "cryo_cx", "cryo_ls", "over_temp",
                   "fire", "ups_fault", "mains_fail", "genset_idle",
                   "estop", "unstowed" ]
    pmonStatus = []
    for j in range(0, len(pmonPoints)):
      pointName = "%s.misc.pmon.%s" % (ants[i], pmonPoints[j])
      pmonStatus.append(MoniCAPoint(pointName=pointName,
                                    monicaServer=monica))
    pmonComputeFunctions = list(map(lambda x: x.getErrorState, pmonStatus))
    pmonIndicator = StatusIndicator(
      computeFunction=pmonComputeFunctions,
      colourFunction=stateChecker)
    tile.addIndicator(indicator=pmonIndicator,
                      x=[ xant[0], xant[0] ], y=[ 6, 7 ])
