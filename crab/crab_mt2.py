'''Script to configure crab and crab submission'''

# This should be the only thing to change every production
productionLabel = 'TEST0'
# The path where the output is stored will be:  /store/user/$USER/crab/nanoMT2/productionLabel/datasetname/timestamp/counter/mt2_bla.root


# From here on you should change only if you know what you're doing
import sys
import os
from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

exampleSample = '/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'
config.General.requestName = productionLabel + '_' + exampleSample.split('/')[1]  # only for crab log information
#config.General.workArea = '/afs/cern.ch/work/s/scoopers/private/crabspace/crab_projects/2016/V4/' # what is this for ?
config.General.transferOutputs = True
config.General.transferLogs = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
#config.JobType.scriptArgs = ['doMC','year 2017'] # arguments for postproc.py, the order is not random !
config.JobType.scriptArgs = [] # arguments for postproc.py, the order is not random ! FIXME
config.JobType.inputFiles = ['../branchSel.txt','../postproc.py','../../../../../scripts/haddnano.py'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.sendPythonFolder	 = True # unfortunately this is crucial
config.Data.inputDataset = exampleSample
config.Data.inputDBS = 'global' # should be changed only in case you have private production
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 30 # for the moment split in less jobs, was 4, FIXME: choose something reasonable based on an average size of the sample
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.outLFNDirBase = '/store/user/%s/crab/nanoMT2/%s/' % (getUsernameFromSiteDB(), productionLabel) # may want to change nanoMT2 in a more descriptive version of the code
config.Data.outputDatasetTag = 'generic' #exampleSample.split('/')[1] # only gen sample name
config.Data.publication = True
config.Data.allowNonValidInputDataset = True
config.Site.storageSite = 'T3_CH_PSI' # T3_CH_PSI # T2_CH_CSCS


if __name__ == '__main__':

    f=open(sys.argv[1]) # first argument is the filename containing the samples to be run

    datasets = f.readlines()

    datasets = [x.strip() for x in datasets]

    from CRABAPI.RawCommand import crabCommand

    for dataset in datasets :

        if dataset.startswith('/') == False: raise RuntimeError('invalid dataset, please check your list')

        print 'Working on dataset ', dataset

        #config.General.requestName = productionLabel + '_' + dataset.split('/')[1]
        config.General.requestName = productionLabel + '_' + dataset.split('/')[1]

        config.Data.inputDataset = dataset

        #config.Data.outputDatasetTag = dataset.split('/')[1]

        crabCommand('submit', config = config)
