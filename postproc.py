#!/usr/bin/env python
#Script to launch the post-processing of nanoAODs


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
    return elements[3]
  else:
    return elements[3] + '_' + elements[2]

# TODO: please add the allowed options !
from argparse import ArgumentParser
parser = ArgumentParser(description='', add_help=True)
parser.add_argument('-o', '--outdir', type=str, dest='outdirname', help='name of the output dir', default='output/out')
parser.add_argument('-N', '--Nevts',  type=int, dest='nevents', help='max events to run on', default=-1)
parser.add_argument('-w', '--what', type=str, dest='what', help='what sample to run on: Wlv, Zll when doLocal is activated', default='Wlv')
parser.add_argument('-y','--year', type=int, dest='year', help='year of data taking / MC taking :)', default=2017)

parser.add_argument('--doLocal', dest='doLocal', help='do local test, no crab involved', action='store_true', default=False)
parser.add_argument('--doMC', dest='doMC', help='is it a monte carlo sample?', action='store_true', default=False)
parser.add_argument('--doSkim', dest='doSkim', help='perform skimming?', action='store_true', default=False)

options = parser.parse_args()
print options


import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module


## Preselection
# FIXME: define a reasonable preselection based on quantites already present in the nanoAOD or defined after (?)
preselection = ''
sampleName = 'ABRACADABRA'

## Define input files here
if options.doLocal:
  print 'Running in local'
  dofwkJobReport = False
  haddFileName = None
  if options.what == 'Wlv':
    #files = ['/shome/mratti/nanoaod_workarea/nano_making/CMSSW_9_4_6_patch1/src/PhysicsTools/NanoAOD/test/test94X_Wlv_NANO_15K.root']
    #files = ['/shome/mratti/nanoaod_workarea/nano_making/CMSSW_9_4_6_patch1/src/PhysicsTools/NanoAOD/test/test94X_Wlv_NANO_5K_V2.root']
    files = ['/shome/mratti/nanoaod_workarea/nano_making/CMSSW_9_4_6_patch1/src/PhysicsTools/NanoAOD/test/test94X_Wlv_NANO_5K_noselIT.root']
    sampleName = 'WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8'
  elif options.what == 'Zll':
    #files = ['/shome/mratti/nanoaod_workarea/nano_making/CMSSW_9_4_6_patch1/src/PhysicsTools/NanoAOD/test/test94X_Zll_NANO_5K_V2.root']
    files = ['/shome/mratti/nanoaod_workarea/nano_making/CMSSW_9_4_6_patch1/src/PhysicsTools/NanoAOD/test/test94X_Zll_NANO_5K_nodxyIT.root']
    sampleName = 'DYJetsToLL_M-50_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8'
  elif options.what == 'data':
    files = ['root://cms-xrd-global.cern.ch//store/data/Run2017D/MET/NANOAOD/31Mar2018-v1/10000/2891A264-4C45-E811-A30A-C4346BC80410.root']
    sampleName = 'MET_Run2017D' # -31Mar2018-v1
else:
  print 'Running on the grid'
  dofwkJobReport = True
  haddFileName = 'mt2.root'
  #this takes care of converting the input files from CRAB
  import PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper as CH # inputFiles,runsAndLumis
  files = CH.inputFiles() # it is aweful that the input files are obtained in a such a confused way, but crab doesn't seem to support anything better than that!
  #sampleName = CH.inputSampleName() # FIXME: must define the sampleName in this case
  sampleName = getSampleName(files=files, isMC=options.doMC) # This is really poor, but CMS hasn't thought of any sample handler, which is a bit of a shame
  #print sampleName

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.examples.mhtjuProducerCpp import mhtjuProducerCpp
from PhysicsTools.NanoAODTools.postprocessing.modules.common.lepSFProducer import lepSFProducer
from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import btagSFProducer
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import puWeightProducer
from PhysicsTools.NanoAODTools.postprocessing.analysis.mt2.mt2VarsProducer import mt2VarsProducer
from PhysicsTools.NanoAODTools.postprocessing.analysis.mt2.metaDataProducer import metaDataProducer

#modules = [mhtjuProducerCpp(), lepSFProducer('LooseWP_2016', 'GPMVA90_2016')]
#modules = [mhtjuProducerCpp()]
modules = [ mt2VarsProducer(isMC=options.doMC, year=options.year, doSkim=options.doSkim),
            metaDataProducer(xSecFile='data/xSec/xSecs_2016.txt', sampleName=sampleName, isMC=options.doMC, year=options.year) ]
            #lepSFProducer('LooseWP_2016', 'GPMVA90_2016'),
            #btagSFProducer(era='2017', algo = 'csvv2'),
            #puWeightProducer("auto","%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/PileupData_GoldenJSON_Full2016.root" % os.environ['CMSSW_BASE'],"pu_mc","pileup",verbose=False)]


p=PostProcessor(outputDir=options.outdirname,inputFiles=files,cut=preselection,branchsel='data/branchSel/branchSel.txt', outputbranchsel='data/branchSel/branchSel.txt',
                modules=modules,noOut=False, maxEvents=options.nevents, fwkJobReport=dofwkJobReport, haddFileName=haddFileName, provenance=True)

p.run()
