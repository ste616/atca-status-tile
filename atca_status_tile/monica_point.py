# coding=utf-8
# monica_point.py
# Author: Jamie Stevens
# This file contains a MoniCAPoint class which allows for easy
# management and value queries of a MoniCA point.

class MoniCAPoint:
  def __init__(self, pointName=None, monicaServer=None):
    self.pointName = pointName
    self.monicaServer = monicaServer
    if (self.pointName is not None and
        self.monicaServer is not None):
      self.monicaServer.addPoint(pointName=self.pointName)

  def getValue(self):
    if (self.pointName is not None and
        self.monicaServer is not None):
      point = self.monicaServer.getPointByName(self.pointName)
      return point.getValue()
