





if __name__ == "__main__":


  # options here


  groupName = 'MET'
  inputPath = '/pnfs/psi.ch/cms/trivcat/store/user/mratti/crab/nanoMT2/TEST9/' # please note how the path is indicated
  outputPath = '/scratch/mratti/merged_nanoMT2/TEST9/' # please make sure that this path exists

  from groupMerger import GroupMerger

  g = GroupMerger(groupName=groupName, inputPath=inputPath, outputPath=outputPath)
  g.configGroupMembers(cfgFile='cfg/data_2017_merge.txt')
  g.configOutput()
  ret = g.process()

  #ret = mergeGroup(group, inputPath, outputPath)
  #if ret: print 'Merging ended successfully'
  #else: print 'Something went wrong'
