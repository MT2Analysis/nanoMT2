# Script to configure crab and crab submission

# python crab_mt2.py -p TEST1 -l ../samples/mc_bkg_2017.txt -y 2017 --doMC

## Options
from argparse import ArgumentParser
import os
parser = ArgumentParser(description='Crab submission options', add_help=True)
parser.add_argument('-p','--productionLabel', type=str, dest='productionLabel', help='name of the production, please make sure it was not used before', default='TEST0')
parser.add_argument('-l', '--list', type=str, dest='inputList', help='a txt file containing datasets, one per line', metavar='list', default='../data/samples/mc_bkg_2017.txt')
parser.add_argument('-y','--year', type=int, dest='year', help='year of data taking / MC taking :)', default=2017)
parser.add_argument('--doMC', dest='doMC', help='is it a monte carlo sample?', action='store_true', default=False)
parser.add_argument('--doSignal', dest='doSignal', help='is it a signal sample?', action='store_true', default=False)
parser.add_argument('--doSyst', dest='doSyst', help='do you want to run syst variations?', action='store_true', default=False)
parser.add_argument('--doSkim', dest='doSkim', help='perform skimming?', action='store_true', default=False)
parser.add_argument('--doSkipJSON', dest='doSkipJSON', help='do you want to avoid running the json selection ?', action='store_true', default=False)
parser.add_argument('--doUnblindedJSON', dest='doUnblindedJSON', help='do you want to use the partially unblinded 2017/2018 jsons ?', action='store_true', default=False)

options = parser.parse_args()

## Json configuration
if not options.doMC and not options.doSkipJSON and not options.doUnblindedJSON: 
  jsonFile = '../data/json/current_%s.txt' % (str(options.year))
elif not options.doMC and not options.doSkipJSON and options.doUnblindedJSON:
  jsonFile = '../data/json/goodruns_%s_unblinded.json' % (str(options.year))

## Checks here
if not os.path.isfile(options.inputList): raise RuntimeError('Sample list not available')
if not options.doMC and not options.doSkipJSON and not os.path.isfile(jsonFile): raise RuntimeError('Json file not available')

## Read samples
f=open(options.inputList) # first argument is the filename containing the samples to be run
datasets = f.readlines()
datasets = [x.strip() for x in datasets]
datasets = filter(lambda x: '#' not in x, datasets) # remove commented lines
datasets = filter(lambda x: x!='\n', datasets) # remove empty lines
datasets = filter(lambda x: x!='', datasets) # remove empty lines

## CRAB Configurations
# Change only if you know what you're doing
import sys
import os
from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

exampleSample = '/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'
config.General.requestName = options.productionLabel + '_' + exampleSample.split('/')[1]  # only for crab log information
config.General.workArea = '/shome/%s/crab_workarea/nanoMT2/%s/' % (getUsernameFromSiteDB(), options.productionLabel) #
config.General.transferOutputs = True
config.General.transferLogs = False
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_%s_%s.sh' % ('MC' if options.doMC else 'data', options.year) # crab_script_MC_2017.sh
config.JobType.scriptArgs = [] # arguments for postproc.py: TODO: understand how to use them https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3ConfigurationFile#CRAB_configuration_parameters, for the moment just setup different scripts
config.JobType.inputFiles = ['../data','../postproc.py','../../../../../scripts/haddnano.py'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.sendPythonFolder	 = True # unfortunately this is crucial, but can become at times problematic
config.Data.inputDataset = exampleSample
config.Data.inputDBS = 'global' # should be changed only in case you are running over privately produced samples
config.Data.splitting = 'FileBased' if options.doMC else 'EventAwareLumiBased'#'EventAwareLumiBased' 'LumiBased'
config.Data.unitsPerJob = 5 if options.doMC else 1000000 # 1000000 1000 # 1M events per job, 115 M in period B of MET pd
# The path where the output is stored will be:  /store/user/$USER/crab/nanoMT2/productionLabel/PD/campaign/timestamp/counter/mt2_bla.root
config.Data.outLFNDirBase = '/store/user/%s/crab/nanoMT2/%s/' % (getUsernameFromSiteDB(), options.productionLabel) # may want to change nanoMT2 in a more descriptive version of the code
config.Data.outputDatasetTag = exampleSample.split('/')[2]  #  campaign
config.Data.publication = True
config.Data.allowNonValidInputDataset = True
config.Site.storageSite = 'T3_CH_PSI' # T3_CH_PSI # T2_CH_CSCS
config.Site.whitelist = ['T3_CH_PSI', 'T2_CH_CERN', 'T2_CH_CSCS_HPC'] # T2_CH_CERN
config.Data.ignoreLocality = True # if true will use AAA, otherwise job will go where dataset is
#config.Site.blacklist = ['T2_CH_CSCS']

if not options.doMC and not options.doSkipJSON:
  config.Data.lumiMask = jsonFile


## Actually send crab commands
from CRABAPI.RawCommand import crabCommand

for dataset in datasets :
  if dataset.startswith('/') == False: raise RuntimeError('invalid dataset, please check your list and resubmit with a different productionLabel')

  print 'Working on dataset ', dataset

  if options.doMC: 
    dataset_nickName = dataset.split('/')[1]
    if 'ext' in dataset: dataset_nickName = dataset.split('/')[1] + '_ext' + dataset.split('/')[2].split('ext')[1]
  else: dataset_nickName = dataset.split('/')[1] + '_' + dataset.split('/')[2]
  config.General.requestName = options.productionLabel + '_' + dataset_nickName

  config.Data.outputDatasetTag = dataset.split('/')[2] # campaign

  config.Data.inputDataset = dataset

  if 'USER' in dataset:
    import re
    config.Data.inputDBS = 'phys03'
    config.General.requestName = re.sub(r'(.*)-[^.]*', '\\1', config.General.requestName)
    config.Data.outputDatasetTag = re.sub(r'(.*)-[^.]*', '\\1', config.Data.outputDatasetTag)

  if dataset=='/MuonEG/Run2018D-14Sep2018_ver2-v1/NANOAOD':
    print 'have you switched off the GRL for this sample? if not, do it otherwise the job will fail'
    config.Data.splitting = 'FileBased'
    config.Data.unitsPerJob = 1
    config.Data.runRange = ''
    config.Data.lumiMask  = ''

  print 'Going to submit job with following parameters: '
  print '   outputdatasettag = ', config.Data.outputDatasetTag
  print '   requestname =      ', config.General.requestName
  print '   inputdataset =     ', config.Data.inputDataset 

  crabCommand('submit', config = config)
