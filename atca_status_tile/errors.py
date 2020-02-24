# coding=utf-8
# errors.py
# Author: Jamie Stevens
# Errors used throughout the classes.

# Our custom error.
class StatusError(Exception):
  ## Base class for exceptions in this module.
  pass

class ArgumentError(StatusError):
  ## Exception raised when the arguments passed to a function
  ## are not proper or sufficient.
  ## Attributes:
  ##     routine: the name of the routine called
  ##     arg: the argument specified incorrectly
  ##     message: explanation of what the argument should be
  def __init__(self, routine, arg, message):
    self.routine = routine
    self.arg = arg
    self.message = message

  def __str__(self):
    return ("ArgumentError: %s passed to %s invalid, %s" %
            (self.arg, self.routine, self.message))

class PixelError(StatusError):
  ## Exception raised when a pixel passed to a function is
  ## not valid in some way.
  ## Attributes:
  ##     routine: the name of the routine called
  ##     x: x value
  ##     y: y value
  ##     message: explanation of the problem
  def __init__(self, routine, x, y, message):
    self.routine = routine
    self.x = x
    self.y = y
    self.message = message

  def __str__(self):
    return ("PixelError: in routine %s, pixel (%d, %d), %s" %
            (self.routine, self.x, self.y, self.message))

class TileError(StatusError):
  ## Exception raised when a requested tile is already allocated.
  ## Attributes:
  ##     routine: the name of the routine called
  ##     tileNumber: the index of the tile (0 start)
  ##     message: explanation of the problem
  def __init__(self, routine, tileNumber, message):
    self.routine = routine
    self.tileNumber = tileNumber
    self.message = message

  def __str__(self):
    return ("TileError: tried to allocate tile %d in %s, %s" %
            (self.tileNumber, self.routine, self.message))
  
class FunctionError(StatusError):
  ## Exception raised when a function is supposed to be called
  ## but one was not supplied.
  ## Attributes:
  ##     routine: the name of the routine called
  ##     callback: which function was to be called
  ##     message: explanation of the problem
  def __init__(self, routine, callback, message):
    self.routine = routine
    self.callback = callback
    self.message = message

  def __str__(self):
    return ("FunctionError: could not call the %s callback from %s, %s" %
            (self.callback, self.routine, self.message))
    
class NotFoundError(StatusError):
  ## Exception raised when a tile or tileset is expected, but
  ## none is known.
  ## Attributes:
  ##     routine: the name of the routine called
  ##     expected: which variable isn't valid
  ##     message: explanation of the problem
  def __init__(self, routine, expected, message):
    self.routine = routine
    self.expected = expected
    self.message = message

  def __str__(self):
    return ("NotFoundError: %s not valid in %s, %s" %
            (self.expected, self.routine, self.message))

class TileCommunicationError(StatusError):
  ## Exception raised when a return value from a tile hasn't
  ## come back as expected.
  ## Attributes:
  ##     routine: the name of the routine called
  ##     method: the LiFX LAN method which didn't work
  ##     message: explanation of the problem
  def __init__(self, routine, method, message):
    self.routine = routine
    self.method = method
    self.message = message

  def __str__(self):
    return ("TileCommunicationError: call to %s did not work in %s, %s" %
            (self.method, self.routine, self.message))
  
