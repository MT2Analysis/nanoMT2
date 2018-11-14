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

  allowedYears = [2016, 2017, 2018]

  from argparse import ArgumentParser
  parser = ArgumentParser(description='', add_help=True)
  parser.add_argument('-o', '--outdir', type=str, dest='outdirname', help='name of the output dir', default='output/out')
  parser.add_argument('-N', '--Nevts',  type=int, dest='nevents', help='max events to run on', default=-1)
  parser.add_argument('-w', '--what', type=str, dest='what', help='what sample to run on: Wlv, Zll when doLocal is activated', default='Wlv')
  parser.add_argument('-y','--year', type=int, dest='year', help='year of data taking / MC taking :)', default=2017, choices=allowedYears)

  parser.add_argument('--doLocal', dest='doLocal', help='do local test, no crab involved', action='store_true', default=False)
  parser.add_argument('--doMC', dest='doMC', help='is it a monte carlo sample?', action='store_true', default=False)
  parser.add_argument('--doSignal', dest='doSignal', help='is it a signal sample?', action='store_true', default=False)
  parser.add_argument('--doSyst', dest='doSyst', help='do you want to run syst variations?', action='store_true', default=False)
  parser.add_argument('--doSkim', dest='doSkim', help='perform skimming?', action='store_true', default=False)
  parser.add_argument('--doSkipJSON', dest='doSkipJSON', help='do you want to avoid running the json selection ?', action='store_true', default=False)

  return parser.parse_args()

if __name__ == '__main__':

  ## Options
  options = getOptions()
  print options

  ## Job and modules settings
  preselection = None
  sampleName = 'dummy'
  dofwkJobReport = False
  haddFileName = '{}/{}'.format(options.outdirname, 'mt2.root')
  jsonInput = None
  puFilePrefix = '%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/' % os.environ['CMSSW_BASE']
  # NOTE: current choices reflect what is already implemented in nanoAOD-tools
  if options.year==2016:    
    puFileData = puFilePrefix + 'PileupData_GoldenJSON_Full2016.root' 
    puFileMC =   puFilePrefix + 'pileup_profile_Summer16.root'
  elif options.year==2017:  
    puFileData = puFilePrefix + 'pileup_Cert_294927-306462_13TeV_PromptReco_Collisions17_withVar.root' 
    puFileMC = 'auto'
  elif options.year==2018:  
    puFileData = None
    puFileMC = None

  if options.doLocal:
    print 'Running in local'
    from unitTestFiles import f
    sampleName = 'test'
    #files = ['root://cms-xrd-global.cern.ch/' + f[options.year][options.what] ]
    #files = ['/shome/mratti/nanoaod_workarea/nano_making/CMSSW_9_4_6_patch1/src/PhysicsTools/NanoAOD/test/test94X_Zll_NANO_5K_nodxyIT_diffIso.root']
    #files = ['/shome/mratti/nanoaod_workarea/nano_making/CMSSW_9_4_6_patch1/src/PhysicsTools/NanoAOD/test/test94X_Wlv_NANO_5K_noselIT.root']
    files = ['/shome/mratti/nanoaod_workarea/nano_making/CMSSW_9_4_6_patch1/src/PhysicsTools/NanoAOD/test/test94X_Wlv_NANO_5K_noCut.root']
    #files = ['/shome/mratti/nanoaod_workarea/nano_making/CMSSW_9_4_6_patch1/src/PhysicsTools/NanoAOD/test/test94X_Wlv_NANO_5K_noCutNoOR.root']
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
  from PhysicsTools.NanoAODTools.postprocessing.analysis.mt2.smsAnalyzer import smsAnalyzer

  modules = [ 
   mt2VarsProducer(isMC=options.doMC, isSignal=options.doSignal, year=options.year, doSkim=options.doSkim, doSyst=False, systVar=None),
   metaDataProducer(xSecFile='data/xSec/xSecs_{}.txt'.format(str(options.year)), sampleName=sampleName, isMC=options.doMC, year=options.year),
   #lepSFProducer('LooseWP_2016', 'GPMVA90_2016'),
   #btagSFProducer(era=str(options.year), algo='csvv2'),
  ]
  ### jet met uncertainties module module needs to be run before mt2VarsProducer
  if options.doSyst:
    modules.insert(0,jetmetUncertaintiesProducer(str(options.year), 'Fall17_17Nov2017_V6_MC', [ 'Total' ], redoJEC=True, attachToEvt=True, attachToTree=False))
    modules.insert(1,mt2VarsProducer(isMC=options.doMC, year=options.year, doSkim=options.doSkim, doSyst=options.doSyst, systVar='jesTotalUp'))
    modules.insert(2,mt2VarsProducer(isMC=options.doMC, year=options.year, doSkim=options.doSkim, doSyst=options.doSyst, systVar='jesTotalDown'))

  ### modules to be loaded only for MC
  if options.doMC and options.doSyst==False:
    modules.insert(0, puWeightProducer(myfile=puFileMC, targetfile=puFileData, myhist='pu_mc', targethist='pileup', name='puWeight', norm=True, verbose=False, nvtx_var='Pileup_nTrueInt', doSysVar=True))

  ### last module is for the signal analysis
  if options.doSignal:
    modules.insert(len(modules), smsAnalyzer(sampleName=sampleName,isMC=options.doMC))

  ## Define the post-processor
  p=PostProcessor(outputDir=options.outdirname,inputFiles=files,cut=preselection,branchsel='data/branchSel/branchSel.txt', outputbranchsel='data/branchSel/branchSel.txt',
                  modules=modules,noOut=False, maxEvents=options.nevents, fwkJobReport=dofwkJobReport, haddFileName=haddFileName, provenance=True, jsonInput=jsonInput)

  ## Actually run the whole thing
  p.run()
