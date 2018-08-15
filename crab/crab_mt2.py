# Script to configure crab and crab submission

# python crab_mt2.py -p TEST1 -l ../samples/mc_bkg_2017.txt -y 2017 --doMC

from argparse import ArgumentParser
import os
parser = ArgumentParser(description='Crab submission options', add_help=True)
parser.add_argument('-p','--productionLabel', type=str, dest='productionLabel', help='name of the production, please make sure it was not used before', default='TEST0')
parser.add_argument('-l', '--list', type=str, dest='inputFile', help='a txt file containing datasets, one per line', metavar='list', default='../samples/mc_bkg_2017.txt')
parser.add_argument('-y','--year', type=str, dest='year', help='year of data taking / MC taking :)', default='2017')
parser.add_argument('--doMC', dest='doMC', help='is it a monte carlo sample?', action='store_true', default=False)

options = parser.parse_args()

# Change only if you know what you're doing
# CRAB Configurations
import sys
import os
from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

exampleSample = '/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'
config.General.requestName = options.productionLabel + '_' + exampleSample.split('/')[1]  # only for crab log information
config.General.workArea = '/shome/%s/crab_workarea/nanoMT2/%s/' % (getUsernameFromSiteDB(), options.productionLabel) #
config.General.transferOutputs = True
config.General.transferLogs = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_%s_%s.sh' % ('MC' if options.doMC else 'data', options.year) # crab_script_MC_2017.sh
config.JobType.scriptArgs = [] # arguments for postproc.py: TODO: understand how to use them https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3ConfigurationFile#CRAB_configuration_parameters, for the moment just setup different scripts
config.JobType.inputFiles = ['../data','../postproc.py','../../../../../scripts/haddnano.py'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.sendPythonFolder	 = True # unfortunately this is crucial, but can become at times problematic
config.Data.inputDataset = exampleSample
config.Data.inputDBS = 'global' # should be changed only in case you are running over privately produced samples
config.Data.splitting = 'FileBased' if options.doMC else 'EventAwareLumiBased'
config.Data.unitsPerJob = 10 # FIXME: 10 is too much, something around 4-5 is better
#config.Data.splitting = 'EventAwareLumiBased'
# The path where the output is stored will be:  /store/user/$USER/crab/nanoMT2/productionLabel/datasetname_decided_by_crab_crazily/datasetNickName/timestamp/counter/mt2_bla.root
config.Data.outLFNDirBase = '/store/user/%s/crab/nanoMT2/%s/' % (getUsernameFromSiteDB(), options.productionLabel) # may want to change nanoMT2 in a more descriptive version of the code
config.Data.outputDatasetTag = 'WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8' #exampleSample.split('/')[1] # only gen sample name
config.Data.publication = True
config.Data.allowNonValidInputDataset = True
config.Site.storageSite = 'T3_CH_PSI' # T3_CH_PSI # T2_CH_CSCS


# Actually send crab commands

f=open(options.inputFile) # first argument is the filename containing the samples to be run
datasets = f.readlines()
datasets = [x.strip() for x in datasets]
datasets = filter(lambda x: '#' not in x, datasets) # remove commented lines
datasets = filter(lambda x: x!='\n', datasets) # remove empty lines
datasets = filter(lambda x: x!='', datasets) # remove empty lines

from CRABAPI.RawCommand import crabCommand

for dataset in datasets :
  if dataset.startswith('/') == False: raise RuntimeError('invalid dataset, please check your list and resubmit with a different productionLabel')

  print 'Working on dataset ', dataset

  if options.doMC: dataset_nickName = dataset.split('/')[1]
  else: dataset_nickName = dataset.split('/')[1] + '_' + dataset.split('/')[2]

  config.General.requestName = options.productionLabel + '_' + dataset_nickName
  config.Data.outputDatasetTag = dataset_nickName
  config.Data.inputDataset = dataset

  crabCommand('submit', config = config)
