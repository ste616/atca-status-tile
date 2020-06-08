#!/usr/bin/env python3
# coding=utf-8
# monitor1.py
# Author: Jamie Stevens
# This is monitor layout 1.
# This main routine imports all the required routines from other
# files and the library, and sets up the tiles in the required
# pattern.

from lifxlan import *
from atca_status_tile import TileMaster, initialiseServerInstance
from time import sleep
from tile_cabb_blocks import cabbBlockTile
from tile_power_lightning import powerLightningTile
from tile_cryogenics import cryogenicsTile
from tile_observing import observingTile

def main():
  ## Get the tile we want to control.
  lan = LifxLAN()
  atcaTile = lan.get_tilechain_lights()[0]

  ## Initialise the tile master.
  master = TileMaster(lifxTile=atcaTile,
                      refreshTime=2)
  ## Switch on the tiles.
  master.powerOn()

  ## Start the MoniCA machinery.
  server = initialiseServerInstance()
  
  ## Tile 1: CABB block indicators.
  tile1 = master.addTile(tileNumber=0)
  cabbBlockTile(tile=tile1, monica=server)
  
  ## Tile 2: Lightning and power tile.
  tile2 = master.addTile(tileNumber=1)
  powerLightningTile(tile=tile2, monica=server)

  ## Tile 3: Cryogenics.
  tile3 = master.addTile(tileNumber=2)
  cryogenicsTile(tile=tile3, monica=server)
  
  ## Tile 5: Observing status.
  tile5 = master.addTile(tileNumber=4)
  observingTile(tile=tile5, monica=server)
  
  ## Sit here and let the master do its work.
  try:
    while(True):
      server.updatePoints()
      sleep(2)
      
  finally:
    master.stop()
      
if __name__ == "__main__":
  main()
