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
    
