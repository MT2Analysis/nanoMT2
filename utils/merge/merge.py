# Script to merge output of crab into one file per group of samples
# This script is thought to work on the PSI tier3
#

import subprocess

def mergeSample(dirSample, fileName='mt2.root'):

  #path = '/pnfs/psi.ch/cms/trivcat/store/user/mratti/crab/nanoMT2/TEST9/MET/MET_Run2017C-31Mar2018-v1/*/*/*root'
  path = '{}/*/*/{}*root'.format(dirSample, fileName)

  try:
    out = subprocess.check_output('ls {}'.format(path), shell=True)
  except subprocess.CalledProcessError as e:
    print 'ERROR', e
    print 'Continuing'


  list = out.split('\n')
  list = filter(lambda x: x != '')
  protocol = 'root://t3dcachedb.psi.ch:1094/'
  list_new = map(lambda x: protocol + x, list)
  input_hadd = ' '.join(list_new)

  #issue the command haddnano.py out.root joined_string



def mergeGroup():
  pass

if __name__ == "__main__":


  # options here



  outputPath = '/scratch/mratti/merged_nanoMT2/' # please make sure that this path exists
  inputPath = ''


  #
