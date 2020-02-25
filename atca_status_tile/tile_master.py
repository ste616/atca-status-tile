# coding=utf-8
# tile_master.py
# Author: Jamie Stevens
# This file contains the TileMaster class which is the tile that is
# split into several StatusTiles.

from .errors import NotFoundError, TileCommunicationError, ArgumentError, TileError
from .status_tile import StatusTile
from .repeated_timer import RepeatedTimer

class TileMaster:
  def __init__(self, lifxTile=None, refreshTime=10):
    self.lifxTile = lifxTile
    self.refreshTime = refreshTime
    self.temperature = None
    self.brightness = None
    self.colours = None
    self.tiles = None
    self.timer = RepeatedTimer(refreshTime, self.refresh)

  def getStatus(self):
    ## This gets the current values of the tile pixels.
    if self.lifxTile is not None:
      self.colours = self.lifxTile.get_tilechain_colors()
    else:
      raise NotFoundError(routine="TileMaster.getStatus",
                          expected="lifxTile",
                          message="No LiFX tileset was specified")
    ## Work out the temperature and brightness.
    ## We assume here that each pixel has the same brightness and
    ## temperature for simplicity.
    if self.colours is not None:
      self.temperature = self.colours[0][0][3]
      self.brightness = self.colours[0][0][2]
    else:
      raise TileCommunicationError(routine="TileMaster.getStatus",
                                   method="get_tilechain_colours",
                                   message="Could not get colours from tiles")
    ## If we're here for the first time, we initialise the
    ## tile list.
    self.tiles = [ None ] * len(self.colours)
    return self.colours
    
  def getTileValues(self, tileNumber=None):
    ## Return just the values for a specified tileNumber.
    self.getStatus()
    if tileNumber is not None and len(self.colours) > tileNumber:
      return self.colours[tileNumber]
    else:
      raise ArgumentError(routine="TileMaster.getTileValues",
                          arg="tileNumber",
                          message="argument was not supplied or is out of range")
    return None

  def powerOn(self):
    if self.lifxTile is not None:
      self.lifxTile.set_power(1)
    else:
      raise NotFoundError(routine="TileMaster.powerOn",
                          expected="lifxTile",
                          message="No LiFX tileset was specified")
    return self

  def powerOff(self):
    if self.lifxTile is not None:
      self.lifxTile.set_power(0)
    else:
      raise NotFoundError(routine="TileMaster.powerOn",
                          expected="lifxTile",
                          message="No LiFX tileset was specified")
    return self
  
  def addTile(self, tileNumber=None):
    if self.tiles is None:
      raise NotFoundError(routine="TileMaster.addTile",
                          expected="tiles",
                          message="No tiles configured in tile set")
    if (tileNumber is None or tileNumber < 0 or
        tileNumber > len(self.tiles)):
      raise ArgumentError(routine="TileMaster.addTile",
                          arg="tileNumber",
                          message="argument was not supplied or is out of range")
    if self.tile[tileNumber] is not None:
      raise TileError(routine="TileMaster.addTile",
                      tileNumber=tileNumber,
                      message="tile was already allocated")
    ## We can allocate this tile.
    self.tiles[tileNumber] = StatusTile(tile=self,
                                        tileNumber=tileNumber)
    return self.tiles[tileNumber]

  def refresh(self):
    print ("DEBUG: TileMaster is refreshing")
    if self.tiles is None:
      raise NotFoundError(routine="TileMaster.refresh",
                          expected="tiles",
                          message="No tiles configured in tile set")
    for i in range(0, len(self.tiles)):
      if self.tiles[i] is not None:
        self.tiles[i].refresh(brightness=self.brightness)

  def setTileColours(self, tileNumber=None, colours=None):
    if self.colours is None:
      raise NotFoundError(routine="TileMaster.setTileColours",
                          expected="colours",
                          message="no colours returned from tile set")
    if (tileNumber is None or tileNumber < 0 or
        tileNumber > len(self.tiles)):
      raise ArgumentError(routine="TileMaster.setTileColours",
                          arg="tileNumber",
                          message="argument was not supplied or is out of range")
    if colours is None or len(colours) != 64:
      raise ArgumentError(routine="TileMaster.setTileColours",
                          arg="colours",
                          message="argument was not supplied or is wrong size")
    ## We can set these colours.
    self.colours[tileNumber] = colours
    self.lifxTile.set_tile_colours(start_index=tileNumber,
                                   colors=self.colours[tileNumber],
                                   tile_count=1)

  def stop(self):
    ## Stop automatically updating.
    self.timer.stop()
