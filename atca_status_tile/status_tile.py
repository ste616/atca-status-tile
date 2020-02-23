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

class StatusTile:
  def __init__(self, tileNumber=None):
    self.tileNumer = tileNumber
    self.indicators = []
    self.pixelsUsed = [ False ] * 64
    self.lastBrightness = 32768

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
      if (self.pixelsUsed[p] == True):
        raise PixelError(
          routine="StatusTile.addIndicator",
          x=x[i], y=y[i],
          message="pixel already allocated to another indicator"
          )
      p.append(tp)
    ## If we get here, this indicator can be added to our list.
    self.indicators.append({
      indicator: indicator,
      pixels: tp
      })
    for i in p:
      pixelsUsed[i] = True
    return self

  def refresh(self, brightness=None):
    ## Called to update the pixel values.
    if brightness is None:
      brightness = self.lastBrightness
    else:
      self.lastBrightness = brightness
      
    for i in range(0, len(self.indicators)):
      self.indicators[i].indicator.refresh()
      pixelColours = self.indicators[i].indicator.getColours()
      if len(pixelColours) == 1:
        # Just one colour for all the pixels.
        # Convert RGB to HS.
        ( hue, saturation ) = ( 1, 1 )
        # Set the pixels.
        for j in range(len(self.indicators[i].pixels)):
          self.indicators[i].pixels[j] = ( hue, saturation, brightness, kelvin )

    # Now update the tile.
    set_tile_colours()
    
    
