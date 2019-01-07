# Utility to re-create the jet id definition of the previous analysis 

def getBitDecision(x, n): # x is an integer
  return (x & 2**n) != 0

# bit 1 checks if it's loose : n=0
# bit 2 checks if it's tight : n=1
# bit 3 checks if it's tightlepveto: n=2 # only for 2017 and 2018
  
def getCustomId(jetId, jetChHadFrac=0, jetNeuHadFrac=0, jetNeuEMFrac=0, jetEta=0):

  customId = 0 # by default fail
  if getBitDecision(x=jetId, n=0) == True: # if you pass the loose id
    customId = 1 # you're at least loose
  # case where customId = 2 (medium) does not exist anymore, as medium Id is not supported anymore
  if getBitDecision(x=jetId, n=1) == True: # if you pass the tight id
    customId = 3
  if abs(jetEta) < 3.0 and jetChHadFrac > 0.05 and jetNeuHadFrac < 0.8 and jetNeuEMFrac < 0.7: # custom monojet cuts
    customId = 4
  if abs(jetEta) < 3.0 and jetChHadFrac > 0.2 and jetNeuHadFrac < 0.7 and jetNeuEMFrac < 0.7: # tighter custom monojet cuts
    customId = 5

  return customId

if __name__ == '__main__':

  bitmaps_2016 = [0, 1, 3]
  bitmaps_legend_2016 = ['fail', 'loose', 'tight']

  bitmaps_2017 = [0,2,6]
  bitmaps_legend_2017 = ['fail', 'tight', 'tightlepveto']

  print 'About to perform test of jet id utils'

  print '\n\nTest for 2016\n'  
  for i,ibitmap in enumerate(bitmaps_2016):
    print 'original bitmap=({},{})'.format(bitmaps_2016[i],bitmaps_legend_2016[i])
    print 'custom id      ={}'.format(getCustomId(ibitmap))
    print ''
  print '\n\nTest for 2017\n'  
  for i,ibitmap in enumerate(bitmaps_2017):
    print 'original bitmap=({},{})'.format(bitmaps_2017[i],bitmaps_legend_2017[i])
    print 'custom id      ={}'.format(getCustomId(ibitmap))
    print ''
