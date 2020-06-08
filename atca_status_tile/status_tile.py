# coding=utf-8
# status_tile.py
# Author: Jamie Stevens
# This file contains a StatusTile class which can be used to wrap a number of
# indicators.

from .errors import ArgumentError, PixelError
from .repeated_timer import RepeatedTimer

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
    self.testMode = False
    self.testTimer = None
    self.testPixel = 0
    self.testColours = [ ( 0, 0, 0, 3500 ) ] * 64
    self.attentionRequired = False

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

  def callForAttention(self):
    ## This method is called by a status indicator if the compute
    ## or colour routines decide that a point needs attention.
    self.attentionRequired = True
  
  def refresh(self, brightness=None, temperature=None):
    if self.testMode == True:
      return
    #print("DEBUG: tile %d being refreshed" % self.tileNumber)
    ## Called to update the pixel values.
    if brightness is None:
      brightness = self.lastBrightness
    else:
      self.lastBrightness = brightness
    if temperature is None:
      temperature = self.lastTemperature
    else:
      self.lastTemperature = temperature

    self.attentionRequired = False
    for i in range(0, len(self.indicators)):
      ## Make a run through all the indicators first to see if they
      ## need to call for attention.
      self.indicators[i]["indicator"].refresh(parentTile=self)

    ## Increase the brightness if attention is required.
    if (self.attentionRequired):
      brightness = 65535 ## Full brightness
    else:
      brightness = 16383 ## Quarter brightness

    ## Now run through the indicators again and set the pixels.
    for i in range(0, len(self.indicators)):
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
    #print ("DEBUG: tile %d colours is now:", self.tileNumber)
    #print (self.colours)
    self.tileMaster.setTileColours(tileNumber=self.tileNumber,
                                   colours=self.colours)
    
  def startTest(self):
    #print ("DEBUG: entering test mode for tile %d",
    #       self.tileNumber)
    if self.testMode == True:
      # Already running.
      return
    ## Blank the tile.
    self.tileMaster.setTileColours(tileNumber=self.tileNumber,
                                   colours=self.testColours)
    ## Set up the timer.
    self.testTimer = RepeatedTimer(1, self.test)
    self.testMode = True
    return self

  def test(self):
    if self.testPixel == 64:
      ## Test is finished.
      self.testMode = False
      self.testTimer.stop()
      ## Go back to the old colours.
      self.tileMaster.setTileColours(tileNumber=self.tileNumber,
                                     colours=self.colours)
    ## Unlight the previous pixel.
    if (self.testPixel > 0):
      self.testColours[self.testPixel - 1] = ( 0, 0, self.lastBrightness,
                                               self.lastTemperature )
    if (self.textPixel < 64):
      ## Light up the new pixel.
      self.testColours[self.testPixel] = ( 120, 65535, 65535,
                                           self.lastTemperature )
    self.tileMaster.setTileColours(tileNumber=self.tileNumber,
                                   colours=self.testColours)
    ## Increment the text pixel for next time.
    self.testPixel += 1
    
    
