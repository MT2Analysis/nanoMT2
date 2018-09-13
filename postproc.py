# postproc.py - Maria Giulia Ratti, ETH Zurich

# Script to setup and launch the post-processing of nanoAODs for the MT2 analysis

# FIXME:  2016 is not really supported currently, due to missing isotracks
# NOTE: Please check the xsection file to make sure that the naming is correct !

import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module


def getSampleName(files, isMC):
# this is ugly (and not very safe (?)) but it's not my fault
# this sample name will be used to search for the cross-sections
  first = files[0]
  import re
  new = re.sub(r'.*/store', '/store', first)
  #redirector = 'root://cms-xrd-global.cern.ch/'
  #if first.startswith(redirector): first.replace(redirector, '')
  elements = new.split('/')
  elements = filter(lambda x: x != '', elements) # for safety reasons, remove empty strings
  if isMC:
    sampleName = elements[3]
  else:
    sampleName = elements[3] + '_' + elements[2]
  print 'Determined sampleName ', sampleName
  return sampleName

def getOptions():
# TODO: please add the allowed choices !

  from argparse import ArgumentParser
  parser = ArgumentParser(description='', add_help=True)
  parser.add_argument('-o', '--outdir', type=str, dest='outdirname', help='name of the output dir', default='output/out')
  parser.add_argument('-N', '--Nevts',  type=int, dest='nevents', help='max events to run on', default=-1)
  parser.add_argument('-w', '--what', type=str, dest='what', help='what sample to run on: Wlv, Zll when doLocal is activated', default='Wlv')
  parser.add_argument('-y','--year', type=int, dest='year', help='year of data taking / MC taking :)', default=2017)

  parser.add_argument('--doLocal', dest='doLocal', help='do local test, no crab involved', action='store_true', default=False)
  parser.add_argument('--doMC', dest='doMC', help='is it a monte carlo sample?', action='store_true', default=False)
  parser.add_argument('--doSyst', dest='doSyst', help='do you want to run syst variations?', action='store_true', default=False)
  parser.add_argument('--doSkim', dest='doSkim', help='perform skimming?', action='store_true', default=False)
  parser.add_argument('--doSkipJSON', dest='doSkipJSON', help='do you want to avoid running the json selection ?', action='store_true', default=False)

  return parser.parse_args()

if __name__ == '__main__':

  ## Options
  options = getOptions()
  print options

  ## Job settings
  preselection = None
  sampleName = 'dummy'
  dofwkJobReport = False
  haddFileName = '{}/{}'.format(options.outdirname, 'mt2.root')
  jsonInput = None

  if options.doLocal:
    print 'Running in local'
    if options.what == 'Wlv':
      #files = ['/shome/mratti/nanoaod_workarea/nano_making/CMSSW_9_4_6_patch1/src/PhysicsTools/NanoAOD/test/test94X_Wlv_NANO_15K.root']
      #files = ['/shome/mratti/nanoaod_workarea/nano_making/CMSSW_9_4_6_patch1/src/PhysicsTools/NanoAOD/test/test94X_Wlv_NANO_5K_V2.root']
      if options.year == 2017:
        # used only for nano vs mini files = ['/shome/mratti/nanoaod_workarea/nano_making/CMSSW_9_4_6_patch1/src/PhysicsTools/NanoAOD/test/test94X_Wlv_NANO_5K_noselIT.root']
        files = ['root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAOD/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/70000/5CD5289E-5856-E811-A5DB-A0369FD0B22A.root']
      elif options.year == 2016:
        files = ['root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v2/90000/5C7D09C9-5E42-E811-8A15-0025905A497A.root']
      sampleName = 'WJetsToLNu_HT-600To800'
    elif options.what == 'Zll':
      #files = ['/shome/mratti/nanoaod_workarea/nano_making/CMSSW_9_4_6_patch1/src/PhysicsTools/NanoAOD/test/test94X_Zll_NANO_5K_V2.root']
      files = ['/shome/mratti/nanoaod_workarea/nano_making/CMSSW_9_4_6_patch1/src/PhysicsTools/NanoAOD/test/test94X_Zll_NANO_5K_nodxyIT.root']
      sampleName = 'DYJetsToLL_M-50_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8'
    elif options.what == 'data':
      files = ['root://cms-xrd-global.cern.ch//store/data/Run2017D/MET/NANOAOD/31Mar2018-v1/10000/2891A264-4C45-E811-A30A-C4346BC80410.root']
      sampleName = 'MET_Run2017D-31Mar2018-v1' #
  else:
    print 'Running on the grid'
    dofwkJobReport = True
    haddFileName = 'mt2.root'
    import PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper as CH # inputFiles,runsAndLumis
    if not options.doMC and not options.doSkipJSON:
      jsonInput = CH.runsAndLumis()
    #this takes care of converting the input files from CRAB
    files = CH.inputFiles() # it is aweful that the input files are obtained in a such a confused way, but crab doesn't seem to support anything better than that!
    sampleName = getSampleName(files=files, isMC=options.doMC) # This is really poor, but CMS hasn't thought of any sample handler, which is a bit of a shame
    print 'Sample name figured from files', sampleName

  ## Modules to be run
  from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
  #from PhysicsTools.NanoAODTools.postprocessing.examples.mhtjuProducerCpp import mhtjuProducerCpp
  from PhysicsTools.NanoAODTools.postprocessing.modules.common.lepSFProducer import lepSFProducer
  from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import btagSFProducer
  from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import puWeightProducer
  from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
  from PhysicsTools.NanoAODTools.postprocessing.analysis.mt2.mt2VarsProducer import mt2VarsProducer
  from PhysicsTools.NanoAODTools.postprocessing.analysis.mt2.metaDataProducer import metaDataProducer

  modules = [ mt2VarsProducer(isMC=options.doMC, year=options.year, doSkim=options.doSkim, doSyst=False, systVar=None),
              metaDataProducer(xSecFile='data/xSec/xSecs_{}.txt'.format(str(options.year)), sampleName=sampleName, isMC=options.doMC, year=options.year) ]
              #lepSFProducer('LooseWP_2016', 'GPMVA90_2016'),
              #btagSFProducer(era=str(options.year), algo='csvv2')]
              #puWeightProducer("auto","%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/PileupData_GoldenJSON_Full2016.root" % os.environ['CMSSW_BASE'],"pu_mc","pileup",verbose=False)]
  if options.doSyst:
    modules.insert(0,jetmetUncertaintiesProducer(str(options.year), "Fall17_17Nov2017_V6_MC", [ "Total" ], redoJEC=True, attachToEvt=True, attachToTree=False))
    modules.insert(1,mt2VarsProducer(isMC=options.doMC, year=options.year, doSkim=options.doSkim, doSyst=options.doSyst, systVar='jesTotalUp'))
    modules.insert(2,mt2VarsProducer(isMC=options.doMC, year=options.year, doSkim=options.doSkim, doSyst=options.doSyst, systVar='jesTotalDown'))


  ## Define the post-processor
  p=PostProcessor(outputDir=options.outdirname,inputFiles=files,cut=preselection,branchsel='data/branchSel/branchSel.txt', outputbranchsel='data/branchSel/branchSel.txt',
                  modules=modules,noOut=False, maxEvents=options.nevents, fwkJobReport=dofwkJobReport, haddFileName=haddFileName, provenance=True, jsonInput=jsonInput)

  ## Actually run the whole thing
  p.run()
