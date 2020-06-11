# coding=utf-8
# monica.py
# Author: Jamie Stevens
# This is a connection to a MoniCA server.

from requests import Session
import requests
import json

class monicaPoint:
  def __init__(self, info={}):
    self.value = None
    self.timeValue = None
    self.description = None
    self.pointName = None
    self.updateTime = None
    self.errorState = None
    self.timeSeries = False
    self.startTime = None
    self.interval = None
    if "value" in info:
      self.setValue(info['value'])
    if "description" in info:
      self.setDescription(info['description'])
    if "pointName" in info:
      self.pointName = info['pointName']
    if "updateTime" in info:
      self.setUpdateTime(info['updateTime'])
    if "errorState" in info:
      self.setErrorState(info['errorState'])
    if "isTimeSeries" in info:
      self.setTimeSeries(info['isTimeSeries'])
    if "startTime" in info:
      self.setStartTime(info['startTime'])
    if "interval" in info:
      self.setInterval(info['interval'])

  def getPointName(self):
    return self.pointName
          
  def setValue(self, value=None):
    if value is not None:
      self.value = value
    return self

  def getValue(self):
    if self.timeSeries == False:
      return self.value
    else:
      ## We can return just the latest value.
      return self.value[-1]

  def setSeries(self, values=None):
    ## Fill this in when we know how to do this.
    print(values)
    return self
  
  def getSeries(self):
    return { "times": self.timeValue, "values": self.value }

  def setDescription(self, description=None):
    if description is not None:
      self.description = description
    return self

  def getDescription(self):
    return self.description
  
  def setUpdateTime(self, updateTime=None):
    if updateTime is not None:
      self.updateTime = updateTime
    return self

  def getUpdateTime(self):
    return self.updateTime
  
  def setErrorState(self, errorState=None):
    if errorState is not None:
      self.errorState = errorState
    return self

  def getErrorState(self):
    return self.errorState

  def setTimeSeries(self, isTimeSeries=False):
    if (isTimeSeries == True):
      self.timeSeries = True
    else:
      self.timeSeries = False
    return self

  def isTimeSeries(self):
    return self.timeSeries

  def setStartTime(self, startTime=None):
    if startTime is not None:
      if startTime < 0:
        ## Latest data.
        self.startTime = -1
      ## Later, we will add a way to get historical time.
    return self
  
  def getStartTime(self):
    if self.startTime == -1:
      return "-1"
    return self.startTime

  def setInterval(self, interval=None):
    if interval is not None:
      ## Interval is in minutes.
      if interval > 0:
        self.interval = interval
    return self

  def getInterval(self):
    return self.interval

class monicaServer:
  def __init__(self, info={}):
    self.serverName = "monhost-nar"
    self.protocol = "https"
    self.webserverName = "www.narrabri.atnf.csiro.au"
    self.webserverPath = "cgi-bin/obstools/web_monica/monicainterface_json.pl"
    self.points = []
    if "serverName" in info:
      self.serverName = info['serverName']
    if "protocol" in info:
      self.protocol = info['protocol']
    if "webserverName" in info:
      self.webserverName = info['webserverName']
    if "webserverPath" in info:
      self.webserverPath = info['webserverPath']

  def addPoint(self, pointName=None):
    if pointName is not None:
      npoint = monicaPoint({ 'pointName': pointName })
      self.points.append(npoint)
    return self
  
  def addPoints(self, points=[]):
    if len(points) > 0:
      for i in range(0, len(points)):
        self.addPoint(points[i])
    return self

  def addTimeSeries(self, pointName=None, interval=None, startTime=None):
    if pointName is not None and interval is not None:
      nseries = monicaPoint({ 'pointName': pointName,
                              'interval': interval,
                              'startTime': startTime })
      self.points.append(nseries)
    return self
  
  def getPointByName(self, pointName=None):
    if pointName is not None:
      for i in range(0, len(self.points)):
        if (self.points[i].getPointName() == pointName and
            self.points[i].isTimeSeries() == False):
          return self.points[i]
    return None

  def getTimeSeriesByName(self, pointName=None):
    if pointName is not None:
      for i in range(0, len(self.points)):
        if (self.points[i].getPointName() == pointName and
            self.points[i].isTimeSeries() == True):
          return self.points[i]
    return None
  
  def __comms(self, data=None):
    if data is None:
      return None

    session = Session()
    url = self.protocol + "://" + self.webserverName + "/" + self.webserverPath
    try:
      postResponse = session.post( url=url, data=data )
    except requests.exceptions.ConnectionError:
      print ("WHY YOU NO CONNECT?")
      return None
    try:
      rinfo = json.loads(postResponse.text)
    except json.decoder.JSONDecodeError:
      print ("Response from MoniCA not JSON this time")
      rinfo = None
    return rinfo

  def updatePoints(self):
    ##allPointNames = [ p.getPointName() for p in self.points ]
    allPointNames = []
    allSeriesNames = []
    success = False
    for i in range(0, len(self.points)):
      if self.points[i].isTimeSeries() == False:
        allPointNames.append(self.points[i].getPointName())
      else:
        allSeriesNames.append(
          "%s,%s,%d" % (self.points[i].getPointName(),
                        self.points[i].getStartTime(),
                        self.points[i].getInterval())
          )

    ## Start by getting just the regular point data.
    data = { 'action': "points", 'server': self.serverName,
             'points': ";".join(allPointNames) }
    response = self.__comms(data)
    if response is not None and "pointData" in response:
      for i in range(0, len(response['pointData'])):
        if response['pointData'][i]['pointName'] is not None:
          point = self.getPointByName(response['pointData'][i]['pointName'])
          point.setValue(response['pointData'][i]['value'])
          point.setUpdateTime(response['pointData'][i]['time'])
          point.setErrorState(not bool(response['pointData'][i]['errorState']))
      success = True
    ## And now get the time series data.
    data = { 'action': "intervals", 'server': self.serverName,
             'points': ";".join(allSeriesNames) }
    response = self.__comms(data)
    if response is not None and "intervalData" in response:
      for i in range(0, len(response['intervalData'])):
        if response['intervalData'][i]['name'] is not None:
          series = self.getSeriesByName(response['intervalData'][i]['name'])
          point.setSeries(response['intervalData'][i]['data'])
      success = True
    return success

serverInstance = None

def initialiseServerInstance(*args):
  global serverInstance
  if serverInstance is None:
    serverInstance = monicaServer()
  return serverInstance

def server():
  global serverInstance
  return serverInstance
