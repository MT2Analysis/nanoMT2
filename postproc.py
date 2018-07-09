#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor


from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

# you need to have at least one empty module to run
# in principle it's better to use the way modules are passed in nano_postproc.py but it didn't work until now!
class ExampleAnalysis(Module):
  def __init__(self):
    self.writeHistFile=True

  def beginJob(self,histFile=None,histDirName=None):
    #Module.beginJob(self,histFile,histDirName)

    #self.h_vpt=ROOT.TH1F('sumpt',   'sumpt',   100, 0, 1000)
    #self.addObject(self.h_vpt)
    return True

  def analyze(self, event):
    return True

#modules = [ExampleAnalysis()]


from argparse import ArgumentParser
import os
parser = ArgumentParser(description='', add_help=True)
parser.add_argument('-o', '--outdir', type=str, dest='outdirname', help='output dir', default='output/out')
parser.add_argument('-N', '--Nevts',  type=int, dest='nevents', help='max events', default=1001)
options = parser.parse_args()


from PhysicsTools.NanoAODTools.postprocessing.examples.mhtjuProducerCpp import mhtjuProducerCpp
from PhysicsTools.NanoAODTools.postprocessing.modules.common.lepSFProducer import lepSFProducer
from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import btagSFProducer
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import puWeightProducer

#from PhysicsTools.NanoAODTools.postprocessing.modules.jme.mht import mhtProducer
#from PhysicsTools.NanoAODTools.postprocessing.modules.mt2.mht_deltaR import mhtProducer
from PhysicsTools.NanoAODTools.postprocessing.analysis.mt2.mt2VarsProducer import mt2VarsProducer

#modules = [mhtjuProducerCpp(), lepSFProducer('LooseWP_2016', 'GPMVA90_2016')]
#modules = [mhtjuProducerCpp()]
modules = [mt2VarsProducer(isMC=True, year=2017)]
            #lepSFProducer('LooseWP_2016', 'GPMVA90_2016'),
            #btagSFProducer(era='2017', algo = 'csvv2'),
            #puWeightProducer("auto","%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/PileupData_GoldenJSON_Full2016.root" % os.environ['CMSSW_BASE'],"pu_mc","pileup",verbose=False)]
#modules = [ExampleAnalysis()]
#from PhysicsTools.NanoAODTools.postprocessing.framework.exampleModule import exampleProducer
#modules = [exampleProducer(jetSelection=lambda j : j.pt > 30)]

#preselection='Jet_pt[0] > 250'
preselection = ''

#files = ['/scratch/mratti/MT2_test_nanoAODs/WJetsToLNu_HT-400To600__RunIIFall17NanoAOD/74D74976-1EFB-E711-A664-00269E95ACE4.root']
# nanoAOD Run2017 PeriodD MET primary dataset, total of 4.319 (w/o normtag) / 4.224 ifb (w/ normtag)
# full run list: 302030 303434
#files = ['root://cms-xrd-global.cern.ch//store/data/Run2017D/MET/NANOAOD/31Mar2018-v1/10000/2891A264-4C45-E811-A30A-C4346BC80410.root',
#'root://cms-xrd-global.cern.ch//store/data/Run2017D/MET/NANOAOD/31Mar2018-v1/10000/8CE082E9-4745-E811-ABAD-00266CFFCD00.root',
#'root://cms-xrd-global.cern.ch//store/data/Run2017D/MET/NANOAOD/31Mar2018-v1/10000/4061BBAC-5D45-E811-9EB3-00266CFFC7E0.root',
#'root://cms-xrd-global.cern.ch//store/data/Run2017D/MET/NANOAOD/31Mar2018-v1/10000/82944C1A-4945-E811-A345-001E67A400F0.root',
#'root://cms-xrd-global.cern.ch//store/data/Run2017D/MET/NANOAOD/31Mar2018-v1/10000/F69A061A-4745-E811-9E01-A4BF0101202F.root',
#'root://cms-xrd-global.cern.ch//store/data/Run2017D/MET/NANOAOD/31Mar2018-v1/10000/0A4E9DE6-4E45-E811-BDEC-EC0D9A0B30E0.root',
#'root://cms-xrd-global.cern.ch//store/data/Run2017D/MET/NANOAOD/31Mar2018-v1/10000/C87B3AEE-4A45-E811-B81C-90B11C1453E1.root',
#'root://cms-xrd-global.cern.ch//store/data/Run2017D/MET/NANOAOD/31Mar2018-v1/10000/D0B26618-4C45-E811-B98A-001E67DFFB31.root',
#'root://cms-xrd-global.cern.ch//store/data/Run2017D/MET/NANOAOD/31Mar2018-v1/10000/F6434365-4D45-E811-AE2C-001E67A4055F.root',
#'root://cms-xrd-global.cern.ch//store/data/Run2017D/MET/NANOAOD/31Mar2018-v1/10000/303698B0-5D45-E811-B34A-001E675A6928.root',
#'root://cms-xrd-global.cern.ch//store/data/Run2017D/MET/NANOAOD/31Mar2018-v1/210000/D064F6E9-DC46-E811-AF6D-008CFAF28DCE.root']
#files = ['/scratch/mratti/MT2_test_nanoAODs/ZJetsToNuNu_HT-600To800__RunIIFall17NanoAOD/A8548111-275A-E811-A7C4-A0369FC5E71C.root']
#files=[' root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/2CE738F9-C212-E811-BD0E-EC0D9A8222CE.root']
files = ['/shome/mratti/nanoaod_workarea/nano_making/CMSSW_9_4_6_patch1/src/PhysicsTools/NanoAOD/test/test94X_Wlv_NANO_15K.root']
files = ['/shome/mratti/nanoaod_workarea/nano_making/CMSSW_9_4_6_patch1/src/PhysicsTools/NanoAOD/test/test94X_Wlv_NANO_5K_nodxyIT.root']
files = ['/shome/mratti/nanoaod_workarea/nano_making/CMSSW_9_4_6_patch1/src/PhysicsTools/NanoAOD/test/test94X_Wlv_NANO_5K_noselIT.root']

#p=PostProcessor(outputdir,files,cbranchsel='branchSel.txt',modules=modules,noOut=False, maxEvents=1000


#p=PostProcessor(outputdir,files,cbranchsel='branchSel.txt',modules=modules,noOut=False, maxEvents=100000)
p=PostProcessor(options.outdirname,files,cut=preselection,branchsel='branchSel.txt',modules=modules,noOut=False, maxEvents=options.nevents)

p.run()
