#!/usr/bin/env python3

from lifxlan import *
import atca_status_tile as atca
from time import sleep

## Routine to turn a block status into a colour.
def blockStatusColour(blockStatus=None):
  print ("DEBUG: the block status is %s" % blockStatus)
  if (blockStatus is not None):
    if (blockStatus == "ONLINE"):
      return [ ( 0, 255, 0 ) ]
    else:
      return [ ( 255, 0, 0 ) ]
  return [ ( 0, 0, 0 ) ]

def main():
  ## Get the tile we want to control.
  lan = LifxLAN()
  atcaTile = lan.get_tilechain_lights()[0]

  ## Initialise the tile master.
  master = atca.TileMaster(lifxTile=atcaTile)
  ## Switch on the tiles.
  master.powerOn()

  ## Start the MoniCA machinery.
  server = atca.initialiseServerInstance()
  
  ## Tile 1: CABB block indicators.
  tile1 = master.addTile(tileNumber=0)
  for i in range(1, 37):
    if (i > 16 and i < 21):
      continue
    pointName = "caccc.cabb.correlator.Block%02d" % i
    block = atca.MoniCAPoint(pointName=pointName,
                             monicaServer=server)
    blockIndicator = atca.StatusIndicator(computeFunction=block.getValue,
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
    tile1.addIndicator(indicator=blockIndicator,
                       x=x, y=y)

  ## Sit here and let the master do its work.
  try:
    while(True):
      server.updatePoints()
      sleep(2)
      
  finally:
    master.stop()
      
  ## Let's get the status of block 1.
  #server = atca.initialiseServerInstance()
  #server.addPoint(pointName="caccc.cabb.correlator.Block01")
  #block1 = server.getPointByName("caccc.cabb.correlator.Block01")
  #server.updatePoints()
  #val = block1.getValue()
  #print (blockStatusColour(val))

if __name__ == "__main__":
  main()
