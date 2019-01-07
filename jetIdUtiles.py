# Utility to re-create the jet id definition of the previous analysis 

def getBitDecision(x, n): # x is an integer
  return (x & 2**n) != 0

# if getBitDecision(jet.jetId, 2) == False: continue  #  bit1 is loose (always false in 2017 since it does not exist), bit2 is tight, bit3 is tightLepVeto"

def getCustomId(jetId, jetChHadFrac, jetNeuHadFrac, jetNeuEMFrac, jetEta):

  customId = 0 # by default fail
  if getBitDecision(jetId, 1) == True: # if you pass the loose id
    customId = 1 # you're at least loose
  # case where customId = 2 (medium) does not exist anymore, as medium Id is not supported anymore
  if getBitDecision(jetId, 2) == True: # if you pass the tight
    customId = 3
  if abs(jetEta) < 3.0 and jetChHadFrac > 0.05 and jetNeuHadFrac < 0.8 and jetNeuEMFrac < 0.7: # custom monojet cuts
    customId = 4
  if abs(jetEta) < 3.0 and jetChHadFrac > 0.2 and jetNeuHadFrac < 0.7 and jetNeuEMFrac < 0.7: # tighter custom monojet cuts
    customId = 5

  return customId

if __name__ == '__main__':

  
