# coding=utf-8
# monica_point.py
# Author: Jamie Stevens
# This file contains a MoniCAPoint class which allows for easy
# management and value queries of a MoniCA point.

class MoniCAPoint:
  def __init__(self, pointName=None, monicaServer=None,
               isTimeSeries=False, startTime=None, interval=None):
    self.pointName = pointName
    self.monicaServer = monicaServer
    if (self.pointName is not None and
        self.monicaServer is not None):
      if (isTimeSeries == False):
        self.monicaServer.addPoint(pointName=self.pointName)
      else:
        self.monicaServer.addTimeSeries(pointName=self.pointName,
                                        interval=interval,
                                        startTime=startTime)

  def getValue(self, parentTile=None):
    if (self.pointName is not None and
        self.monicaServer is not None):
      point = self.monicaServer.getPointByName(self.pointName)
      return point.getValue()

  def getSeries(self, parentTile=None):
    if (self.pointName is not None and
        self.monicaServer is not None):
      series = self.monicaServer.getTimeSeriesByName(self.pointName)
      return series.getSeries()
    
  def getErrorState(self, parentTile=None):
    if (self.pointName is not None and
        self.monicaServer is not None):
      point = self.monicaServer.getPointByName(self.pointName)
      return point.getErrorState()
  
