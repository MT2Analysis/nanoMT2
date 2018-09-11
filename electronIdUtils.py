# Utilities to play around with the Electron ID
# useful information:
# http://cmslxr.fnal.gov/source/RecoEgamma/ElectronIdentification/python/Identification/
# In order to get the cuts, check Events->Print("Electron_vidNestedWPBitmap");

def getCuts():

  cut_names = {}
  cut_names['Fall17']={
    0: 'MinPtCut',
    1: 'GsfEleSCEtaMultiRangeCut',
    2: 'GsfEleDEtaInSeedCut',
    3: 'GsfEleDPhiInCut',
    4: 'GsfEleFull5x5SigmaIEtaIEtaCut',
    5: 'GsfEleHadronicOverEMEnergyScaledCut',
    6: 'GsfEleEInverseMinusPInverseCut',
    7: 'GsfEleEffAreaPFIsoCut',
    8: 'GsfEleConversionVetoCut',
    9: 'GsfEleMissingHitsCut',
  }
  cut_names['Spring15']={
  #FIXME
  }
  return cut_names

def getNbitFromBitMap(bitmap, n, base):

  base = int(base)
  n = int(n)
  return (bitmap>>(base*n))%(2**base)

def getIdLevelNoIso(bitmap, tune='Fall17', verbose=False):

  if tune=='Fall17':
    nbits=10 # number of bits to determine wp in tune
    ibit_isocut=7 # position of bit corrsponding to the isocut, counting from 0 to 9
    base=3 # number of bits per cut used
  elif tune== 'Spring15':
    pass # FIXME
  else: raise RunTimeError('Tune not supported')

  results_to_use = []

  for icut,cut_name in getCuts()[tune].items():
    if verbose: print icut, cut_name
    if icut==ibit_isocut: continue # do not count the iso cut, that's the point why we are doing all this
    results_to_use.append(getNbitFromBitMap(bitmap=bitmap, n=icut, base=base))

  # determine id level passed by this electron
  id_level = 0

  if 0 in results_to_use:  return 0
  elif 1 in results_to_use:  return 1
  elif 2 in results_to_use:  return 2
  elif 3 in results_to_use:  return 3
  elif 4 in results_to_use:  return 4

  else: raise RunTimeError('Wrong logic')


if __name__ == '__main__':

  bitmaps = [605047076, 604637220, 613554468, 607275300, 609372452, 611403556, 611469604, 613566692, 613566756, 613566756]
  id_levels = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]

  for i,bitmap in enumerate(bitmaps):
    print 'Bitmap', bitmap
    print 'Original Id level =', id_levels[i]
    print 'Id Level no iso =', getIdLevelNoIso(bitmap=bitmap, tune='Fall17', verbose=False)
    for n in range(0,10):
      if n != 7:
        print 'cut =', n, 'idLevel =', getNbitFromBitMap(bitmap=bitmap,n=n, base=3)
