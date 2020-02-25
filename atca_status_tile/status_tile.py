# coding=utf-8
# status_tile.py
# Author: Jamie Stevens
# This file contains a StatusTile class which can be used to wrap a number of
# indicators.

from .errors import ArgumentError, PixelError

## A mapper between (x,y) and pixel number.
def xy2pix(x=0, y=0):
  p = x + 8 * y
  return p

## Conversion between RGB and HSV.
def rgb2hsv(r, g, b):
  ## Change to fractional values.
  rf = r / 255.
  gf = g / 255.
  bf = b / 255.

  ## Get the maximum and minimum colour values.
  cmax = max(rf, gf, bf)
  cmin = min(rf, gf, bf)
  cdelta = cmax - cmin

  ## Calculate the hue.
  h = 0
  if cdelta > 0:
    if cmax == rf:
      h = 60. * (((gf - bf) / cdelta) % 6)
    elif cmax == gf:
      h = 60. * (((bf - rf) / cdelta) + 2.)
    elif cmax == bf:
      h = 60. * (((rf - gf) / cdelta) + 4.)
  ## Calculate the saturation.
  s = 0
  if cmax != 0:
    s = cdelta / cmax
  ## Calculate the fractional brightness (value).
  v = cmax
  return (h, s, v)
  
class StatusTile:
  def __init__(self, tile=None, tileNumber=None):
    self.tileMaster = tile
    self.tileNumber = tileNumber
    self.indicators = []
    self.colours = [ ( 0, 0, 0, 0 ) ] * 64
    self.pixelsUsed = [ False ] * 64
    self.lastBrightness = 65535 ## Full brightness.
    self.lastTemperature = 3500 ## Default colour temperature.

  def addIndicator(self, indicator=None, x=[], y=[]):
    p = []
    if indicator is None:
      raise ArgumentError(
        routine="StatusTile.addIndicator",
        arg="indicator",
        message="must be an StatusIndicator object"
        )
    if ((len(x) == 0) or (len(y) == 0) or (len(x) != len(y))):
      raise ArgumentError(
        routine="StatusTile.addIndicator",
        arg="x/y",
        message="must be equal length lists of pixel coordinates"
        )
    for i in range(0, len(x)):
      if (x[i] < 0 or x[i] > 7 or y[i] < 0 or y[i] > 7):
        raise PixelError(
          routine="StatusTile.addIndicator",
          x=x[i], y=y[i],
          message="pixel value out of range 0 <= v < 8"
          )
      tp = xy2pix(x[i], y[i])
      if (self.pixelsUsed[tp] == True):
        raise PixelError(
          routine="StatusTile.addIndicator",
          x=x[i], y=y[i],
          message="pixel already allocated to another indicator"
          )
      p.append(tp)
    ## If we get here, this indicator can be added to our list.
    self.indicators.append({
      "indicator": indicator,
      "pixels": p
      })
    for i in p:
      self.pixelsUsed[i] = True
    return self

  def refresh(self, brightness=None, temperature=None):
    print("DEBUG: tile %d being refreshed" % self.tileNumber)
    ## Called to update the pixel values.
    if brightness is None:
      brightness = self.lastBrightness
    else:
      self.lastBrightness = brightness
    if temperature is None:
      temperature = self.lastTemperature
    else:
      self.lastTemperature = temperature
      
    for i in range(0, len(self.indicators)):
      self.indicators[i]["indicator"].refresh()
      pixelColours = self.indicators[i]["indicator"].getColours()
      if len(pixelColours) == 1:
        # Just one colour for all the pixels.
        # Convert RGB to HS.
        (hue, saturation, value) = rgb2hsv(*pixelColours[0])
        # Set the pixels.
        for j in range(len(self.indicators[i]["pixels"])):
          self.colours[self.indicators[i]["pixels"][j]] = (
            (hue / 360) * 65535, 65535 * saturation,
            brightness * value, temperature )

    ## Blank out all the pixels that aren't used.
    for i in range(0, len(self.pixelsUsed)):
      if (self.pixelsUsed[i] == False):
        self.colours[i] = ( 0, 0, 0, self.lastTemperature )
          
    # Now update the tile.
    print ("DEBUG: tile %d colours is now:", self.tileNumber)
    print (self.colours)
    self.tileMaster.setTileColours(tileNumber=self.tileNumber,
                                   colours=self.colours)
    
    
