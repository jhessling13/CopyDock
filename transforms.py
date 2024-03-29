# =================================================================================================
# Transforms
#
# Define transform functions on string/clipboard items.
# 
# Evolve!
# =================================================================================================

def sep(psyduck, delimiter="\n", separator=','):
   golduck = psyduck.rstrip().replace(delimiter, separator)
   return golduck

def wrapSep(squirtle, delimiter="\n", separator=',', wrapper="'"):
   wartortle = squirtle.rstrip().replace(delimiter, wrapper + separator + wrapper)
   blastoise = wrapper + wartortle + wrapper
   return blastoise

def fixPattern(ditto):
   if ditto == "^n":
      ditto = '\n'
   elif ditto == "^t":
      ditto = '\t'
   return ditto

def getPassword():
   return "XXXXXXXXX"

# TODO - Add a transform here to pull out values from the FxE for PW Troubleshooter, connect to a button somewhere....