# coding=utf-8
# status_indicator.py
# Author: Jamie Stevens
# This file contains a StatusIndicator class which computes some colours
# based on some function.

from .errors import FunctionError
import types

class StatusIndicator:
  def __init__(self, computeFunction=None, colourFunction=None):
    self.computeFunction = computeFunction
    self.colourFunction = colourFunction
    self.state = None
    self.colour = None

  def refresh(self):
    # Work out the current state and new colour.
    if (self.computeFunction is not None and self.colourFunction is not None):
      if isinstance(self.computeFunction, list):
        newState = list(map(lambda x: x(), self.computeFunction))
      else:
        newState = self.computeFunction()
      self.state = newState

      newColour = self.colourFunction(self.state)
      self.colour = newColour
    else:
      if (self.computeFunction is None):
        raise FunctionError("StatusIndicator.refresh", "computeFunction",
                            "No compute function supplied")
      elif (self.colourFunction is None):
        raise FunctionError("StatusIndicator.refresh", "colourFunction",
                            "No colour function supplied")
    return self

  def getColours(self):
    return self.colour
  
