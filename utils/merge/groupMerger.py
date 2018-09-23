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
    return None

  list = out.split('\n')
  list = filter(lambda x: x != '', list)
  protocol = 'root://t3dcachedb.psi.ch:1094/'
  list_new = map(lambda x: protocol + x, list)


  #issue the command haddnano.py out.root joined_string
  try:
    tmpdir = tempfile.mkdtemp(prefix=os.environ['USER']+'_') 
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

  def __init__(self, groupName, groupExprs, inputPath, outputPath, doMC, doForceMerging=False):
    self.groupName = groupName
    self.groupExprs = groupExprs
    self.inputPath = inputPath
    self.outputPath = outputPath
    self.groupMembers = [] # una lista di stringhe indicanti i sample del gruppo
    self.groupMembersMerged = [] #
    self.doMC = doMC
    self.doForceMerging = doForceMerging

    print 'Initialized groupmerger with groupName={}, inputPath={}, outputPath={}'.format(self.groupName,self.inputPath,self.outputPath )

  def configGroupMembers(self,cfgFile='cfg/data_2017_merge.txt'):
    if not os.path.isfile(cfgFile): raise RuntimeError('cfg file not a valid one')

    f=open(cfgFile)

    for line in f:
      if '#' in line: continue
      if line == '\n': continue
      matches = map(lambda x: x in line, self.groupExprs)
      #if self.groupExpr in line:
      if True in matches:
        #els = dataset.split('/')
        sample = '%s/%s' %(line.split('/')[1], line.split('/')[2]) # don't care about last bit , the datatier
        #print sample
        self.groupMembers.append(sample)

    if len(self.groupMembers)==0:
      raise RuntimeError('ERROR: this group has no members!')

    print 'Configured group members for group=%s:' % self.groupName
    print '\n  '.join(self.groupMembers)

    # check if for each group member there is a corresponding valid dir, otherwise exit before it's too late!
    for sample in self.groupMembers:
      fullSamplePath = '%s/%s/' %(self.inputPath, sample)
      if not os.path.isdir(fullSamplePath): 
        raise RuntimeError('ERROR: sample %s has no associated valid path' % sample)

  def configOutput(self):
    # check output path exists , if not create one
    if not os.path.isdir(self.outputPath):
      print 'Creating outputpath'
      ret = os.mkdir(self.outputPath) # None if everything goes smoothly
      return ret

  def clean(self):
    ret = 0
    for el in self.groupMembersMerged:
      if os.path.isfile(el):
        ret += subprocess.call('rm {}'.format(el), shell=True)

    if ret==0: print 'Cleaned current mergedMembers for group ', self.groupName
    else: print 'Group', self.groupName, 'not fully cleaned, please check', self.groupMembersMerged

  def process(self):
  # idea is to do the merging for each sample separately, in a tmp
  # then copy the merged samples for the group in the outputpath

    print 'Started merging for group=', self.groupName

    for i,sample in enumerate(self.groupMembers):
      print 'Start merging for sample', sample
      fullSamplePath = '%s/%s/' %(self.inputPath, sample)
      mergedFileName=mergeMember(fullSamplePath=fullSamplePath)
      print 'DEBUG', mergedFileName
      if 'mt2' in mergedFileName: # further protection against problems in mergeMember, should not be needed, but here we are
        print 'Sample successfully merged, tmp path is ', mergedFileName
        self.groupMembersMerged.append(mergedFileName)
      else:
        if not self.doForceMerging:
          print ('Could not merge sample %s,  exiting' % sample) # cleaning
          self.clean()
          return 1

      # now copy the merged file
      if self.doMC: # if it's MC, use only the PD name - not the campaign please
        outp = self.outputPath + '/' + self.groupMembers[i].split('/')[0] + '.root'
      else: # if it's data, also call based on the period
        outp = self.outputPath + '/' + self.groupMembers[i].split('/')[0] + '_' + self.groupMembers[i].split('/')[1] + '.root'
      cp_command = 'cp {inp} {outp}'.format(inp=mergedFileName, outp=outp)
      print 'Going to copy sample ', sample, 'to output ', outp
      ret = subprocess.call(cp_command, shell=True)
      if ret!=0:
        print 'ERROR in copying to outputpath, exit code=', ret
        print 'Copying for sample %s did not work, cleaning and exiting' % self.groupMembersMerged # prefer to exit instead of risking of forgetting a file
        self.clean()
        return ret

      else: 
        print 'Successfully merged and copied sample=%s in group=%s, copied in outputPath=%s' % (sample, self.groupName, self.outputPath)
        self.clean()
 
    print 'Merging and copying for group=%s is finished \n' %self.groupName
    return 0


