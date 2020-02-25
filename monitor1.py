#!/usr/bin/env python3

from lifxlan import *
import atca_status_tile as atca
from time import sleep

## Routine to turn a block status into a colour.
def blockStatusColour(blockStatus=None):
  if (blockStatus is not None):
    if (blockStatus == "ONLINE"):
      return ( 0, 255, 0 )
    else:
      return ( 255, 0, 0 )
  return ( 0, 0, 0 )

def main():
  ## Get the tile we want to control.
  lan = LifxLAN()
  atcaTile = lan.get_tilechain_lights()[0]

  ## Initialise the tile master.
  master = atca.TileMaster(lifxTile=atcaTile)
  ## Switch on the tiles.
  master.powerOn()

  ## Tile 1: CABB block indicators.
  tile1 = master.addTile(tileNumber=0)
  

  ## Sit here and let the master do its work.
  try:
    while(True):
      sleep(100)
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
