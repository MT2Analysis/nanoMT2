# smsAnalyzer.py - Maria Giulia Ratti, ETH Zurich

# Module to attach metadata to the mt2 trees

import os
import numpy as np
import re
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


class smsAnalyzer(Module):
  def __init__(self,sampleName,isMC):
    self.sampleName = sampleName
    self.isMC = isMC

  def beginJob(self):
    pass
  def endJob(self):
    pass

  def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):

    # create output branches 
    self.out = wrappedOutputTree
    self.out.branch("GenSusyMScan1", "I")
    self.out.branch("GenSusyMScan2", "I")

  def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    pass

  def analyze(self, event):
    verbose = False
    genParticles = Collection(event, "GenPart")

    # get information on the masses of the particles in the current event 
    GenSusyMScan1 = -999;
    GenSusyMScan2 = -999;

    for genP in genParticles:
      if (genP.status == 1 or (genP.statusFlags&2**7)!=0) and abs(genP.pdgId)>1000000:  # condition to find only one copy of the susy particles that we are interested in
        if abs(genP.pdgId) == 1000022:  # neutralino   
          GenSusyMScan2 = int(genP.mass)
          if verbose: print 'Found neutralino with mass=', GenSusyMScan2
        elif genP.pdgId>0: # the other particle, consider only the particle and not the anti-particle
          GenSusyMScan1 = int(genP.mass)
          if verbose: print 'Found another susy particle with mass=', GenSusyMScan1

    # check that the particles were actually found
    if GenSusyMScan1 == -999 or GenSusyMScan2 == -999: raise RuntimeError('Could not set susy particle masses for this event!')

    self.out.fillBranch("GenSusyMScan1", GenSusyMScan1)
    self.out.fillBranch("GenSusyMScan2", GenSusyMScan2)

    # fill event counter accordingly

    return True
