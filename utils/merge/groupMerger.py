# groupMerger.py - Maria Giulia Ratti, ETH Zurich

# Class to handle merging of crab nanoAODs for a group of samples

import os
import subprocess
import tempfile

def mergeMember(fullSamplePath, fileName='mt2.root'):
# returns the path of the merged file

  #path = '/pnfs/psi.ch/cms/trivcat/store/user/mratti/crab/nanoMT2/TEST9/MET/MET_Run2017C-31Mar2018-v1/*/*/*root'
  path = '{}/*/*/*root'.format(fullSamplePath, fileName)

  try:
    out = subprocess.check_output('ls {}'.format(path), shell=True)
  except subprocess.CalledProcessError as e:
    print 'ERROR in reading the input files', e
    return False,None

  list = out.split('\n')
  list = filter(lambda x: x != '', list)
  protocol = 'root://t3dcachedb.psi.ch:1094/'
  list_new = map(lambda x: protocol + x, list)


  #issue the command haddnano.py out.root joined_string
  try:
    tmpdir = tempfile.mkdtemp() # it's hard for this to fail, I hope
    hadd_command = '{hadd} {outp} {inp}'.format(hadd='../../../../../../scripts/haddnano.py',
                                              outp='{}/{}'.format(tmpdir, fileName),
                                              inp=' '.join(list_new) )
    # FIXME: to run on batch you'll have to copy the script where the job is processed, relative path won't work
    subprocess.call(hadd_command, shell=True)
  except subprocess.CalledProcessError as e:
    print 'ERROR in merging the files'
    return None

  outFileName = '{}/{}'.format(tmpdir, fileName)
  return outFileName


class GroupMerger(object):

  def __init__(self, groupName, groupExpr, inputPath, outputPath, doForceMerging=False):
    self.groupName = groupName
    self.groupExpr = groupExpr
    self.inputPath = inputPath
    self.outputPath = outputPath
    self.groupMembers = [] # una lista di stringhe indicanti i sample del gruppo
    self.groupMembersMerged = [] #
    self.doForceMerging = doForceMerging

    print 'Initialized groupmerger with groupName={}, inputPath={}, outputPath={}'.format(self.groupName,self.inputPath,self.outputPath )

  def configGroupMembers(self,cfgFile='cfg/data_2017_merge.txt'):
    if not os.path.isfile(cfgFile): raise RuntimeError('cfg file not a valid one')

    f=open(cfgFile)

    for line in f:
      if '#' in line: continue
      if line == '\n': continue
      if self.groupExpr in line:
        #els = dataset.split('/')
        sample = '%s/%s' %(line.split('/')[1], line.split('/')[2]) # don't care about last bit , the datatier
        #print sample
        self.groupMembers.append(sample)

    if len(self.groupMembers)==0:
      raise RuntimeError('ERROR: this group has no members!')


  def configOutput(self):
    # check output path exists , if not create one
    if not os.path.isdir(self.outputPath):
      print 'Creating outputpath'
      ret = os.mkdir(self.outputPath) # None if everything goes smoothly
      return ret

  def clean(self):
    ret = 0
    for el in self.groupMembersMerged:
      ret += subprocess.call('rm {}'.format(el), shell=True)

    if ret==0: print 'Cleaned mergedMembers for group ', self.groupName
    else: print 'Group', self.groupName, 'not fully cleaned, please check', self.groupMembersMerged

  def process(self):
  # idea is to do the merging for each sample separately, in a tmp
  # then make the merge for the group - directly in the outputpath

    print 'Started merging for group=', self.groupName

    for i,sample in enumerate(self.groupMembers):
      print 'Start merging for ', sample
      fullSamplePath = '%s/%s/' %(self.inputPath, sample)
      mergedFileName=mergeMember(fullSamplePath=fullSamplePath)
      print mergedFileName
      if mergedFileName:
        print 'Sample successfully merged, tmp path is ', mergedFileName
        self.groupMembersMerged.append(mergedFileName)
      else:
        if not self.doForceMerging:
          print ('Could not merge sample %s,  exiting' % sample) # cleaning
          self.clean()
          return False

    # now merge the merged files
    if len(self.groupMembersMerged)==0:
      print 'No members in group %s, exiting' % self.groupName
      return 1
    else:
      hadd_command = '{hadd} {outp} {inp}'.format(hadd='../../../../../../scripts/haddnano.py',
                                              outp='{}/{}.root'.format(self.outputPath, self.groupName),# full output will have the name of the group
                                              inp=' '.join(self.groupMembersMerged))

      try:
        subprocess.call(hadd_command, shell=True)
      except subprocess.CalledProcessError as e:
        print 'ERROR in merging the members together', e
        print 'Group merging for group %s did not work, cleaning and exiting' % self.groupName
        self.clean()
        return 1

      self.clean() # when you have finished clean the intermediate steps
      print 'Successfully merged samples for group=%s, outputPath=%s' %(self.groupName, '{}/{}.root'.format(self.outputPath, self.groupName))

      return 0
