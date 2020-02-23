import atca_status_tile as atca

## Routine to turn a block status into a colour.
def blockStatusColour(blockStatus=None):
  if (blockStatus is not None):
    if (blockStatus == "ONLINE"):
      return ( 0, 255, 0 )
    else:
      return ( 255, 0, 0 )
  return ( 0, 0, 0 )


## Let's get the status of block 1.
server = atca.initialiseServerInstance()
server.addPoint(pointName="caccc.cabb.correlator.Block01")
block1 = server.getPointByName("caccc.cabb.correlator.Block01")
server.updatePoints()
val = block1.getValue()
print (blockStatusColour(val))
