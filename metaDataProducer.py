# metaDataProducer.py - Maria Giulia Ratti, ETH Zurich

# Module to run attach metadata to the mt2 trees

import os
import numpy as np
import re
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

def idData(name):
  if   'JetHT' in name: return 1
  elif 'HTMHT' in name: return 2
  elif 'MET' in name: return 3
  elif 'DoubleEG' in name: return 4
  elif 'DoubleMuon' in name: return 5
  elif 'MuonEG' in name: return 6
  elif 'SinglePhoton' in name: return 7
  elif 'SingleMuon' in name: return 8
  elif 'SingleElectron' in name: return 9
  else:
    print 'ERROR, no id found for this dataset'
    return -1

class metaDataProducer(Module):
  def __init__(self,xSecFile,sampleName,isMC,year):
    self.xSecFile = xSecFile
    self.sampleName = sampleName
    self.isMC = isMC
    self.year = year
  def beginJob(self):
    pass
  def endJob(self):
    pass

  def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    (id,xSec,filterEff,kFac) = (1,1,1,1)

    if self.isMC:
      if not os.path.isfile(self.xSecFile):
       raise RuntimeError('cross-sections file is not available', self.xSecFile )
      else:
       f=open(self.xSecFile)
       for line in f:
         if '#' in line or line == '\n': continue # skip commented lines and empty lines
         data = re.split(' |\t|\n', line) # split based on any space or tab - this should take all cases into account
         data = filter(lambda x: x != '', data) # remove all empty elements from the list
         sName = data[1]
         if sName in self.sampleName: # if match, make assignment
           (id,xSec,filterEff,kFac) = (int(data[0]),float(data[2]),float(data[3]),float(data[4]))
           break # if you matched don't keep on looping

    else: # data
      id = idData(self.sampleName) # the others kept to 1

    # initialize quantities to be filled in analyze
    self.id = id
    self.xSec = xSec
    self.filterEff = filterEff
    self.kFac = kFac

    print 'Metadata for this sample: id={}, year={}, xSec={}, filterEff={}, kFac={}'.format(self.id,self.year,self.xSec,self.filterEff,self.kFac)

    # create output branches with proper name, following previous convention
    self.out = wrappedOutputTree
    self.out.branch("evt_id", "I")
    self.out.branch("evt_xsec", "F")
    self.out.branch("evt_filter", "F")
    self.out.branch("evt_kfactor", "F")
    self.out.branch("evt_year", "I")
    self.out.branch("isData", "I")

  def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    pass

  def analyze(self, event):

    self.out.fillBranch("evt_id", self.id)
    self.out.fillBranch("evt_xsec", self.xSec)
    self.out.fillBranch("evt_filter", self.filterEff)
    self.out.fillBranch("evt_kfactor", self.kFac)
    self.out.fillBranch("evt_year", self.year)

    isData = not self.isMC
    isData_int = int(isData)
    self.out.fillBranch("isData", isData_int )

    return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
exampleSample = '/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'
metaData = lambda : metaDataProducer(xSecFile='file.txt',sampleName=exampleSample,isMC=True)
