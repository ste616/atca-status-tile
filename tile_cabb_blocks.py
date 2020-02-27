# coding=utf-8
# tile_cabb_blocks.py
# Author: Jamie Stevens
# This file contains all the code necessary to make one of
# the tiles into a CABB block status indicator.

from atca_status_tile import MoniCAPoint, StatusIndicator

## Routine to turn a block status into a colour.
def blockStatusColour(blockStatus=None):
  #print ("DEBUG: the block status is %s" % blockStatus)
  if (blockStatus is not None):
    if (blockStatus == "ONLINE"):
      return [ ( 0, 255, 0 ) ]
    else:
      return [ ( 255, 0, 0 ) ]
  return [ ( 0, 0, 0 ) ]

## This routine takes a tile argument and puts all the CABB block
## status indicators on it.
## Arguments:
##    tile = the LiFX tile master instance
##    monica = the MoniCA server instance
def cabbBlockTile(tile=None, monica=None):
  for i in range(1, 37):
    if (i > 16 and i < 21):
      continue
    pointName = "caccc.cabb.correlator.Block%02d" % i
    block = MoniCAPoint(pointName=pointName,
                        monicaServer=monica)
    blockIndicator = StatusIndicator(computeFunction=block.getValue,
                                     colourFunction=blockStatusColour)
    offblock = 0
    ylevel = 0
    if i < 9:
      offblock = 1
      ylevel = 0
    elif i < 17:
      offblock = 9
      ylevel = 2
    elif i < 29:
      offblock = 21
      ylevel = 4
    else:
      offblock = 29
      ylevel = 6
    x = [ i - offblock, i - offblock ]
    y = [ ylevel, ylevel + 1 ]
    tile.addIndicator(indicator=blockIndicator,
                      x=x, y=y)
