# coding=utf-8
# tile_master.py
# Author: Jamie Stevens
# This file contains the TileMaster class which is the tile that is
# split into several StatusTiles.

class TileMaster:
  def __init__(self, lifxTile=None, refreshTime=10):
    self.lifxTile = lifxTile
    self.refreshTime = refreshTime
    self.temperature = None
    self.brightness = None
    self.colours = None

  def getStatus(self):
    ## This gets the current values of the tile pixels.
    if self.lifxTile is not None:
      self.colours = self.lifxTile.get_tilechain_colors()
    # Work out the temperature and brightness.
    if (self.colours is not None):
      for i in range(0, len(self.colours)):
        
    return self.colours

  def getTileValues(self, tileNumber=None):
    ## Return just the values for a specified tileNumber.
    self.getStatus()
    if tileNumber is not None and len(self.colours) > tileNumber:
      return self.colours[tileNumber]
    return None
