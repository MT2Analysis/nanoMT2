import glob
import os
import subprocess


def getOptions():
  from argparse import ArgumentParser

  parser = ArgumentParser(description='Options for further data merging and duplicates removal', add_help=True)
  parser.add_argument('-p','--productionLabel', type=str, dest='productionLabel', help='name of the crab production', default='TEST0')
  parser.add_argument('-v','--version', type=str, dest='version', help='suffix for post-processing version', default='v0')
  parser.add_argument('-y','--year', type=int, dest='year', help='year of data taking / MC taking :)', default=2017)
  parser.add_argument('--doForce', dest='doForce', help='Force, even if not all samples available', action='store_true', default=False)

  return parser.parse_args()


if __name__ == "__main__":

  options = getOptions()


  inputPath = '/scratch/{U}/merged_nanoMT2/{PL}_{ML}/'.format(U=os.environ['USER'], PL=options.productionLabel, ML=options.version)
  if not os.path.isdir(inputPath):
    raise RuntimeError('Input path {} is not valid'.format(inputPath))
  outputPath = inputPath + '/merged/'

  if options.year==2017:
    periods = ['B', 'C', 'D', 'E', 'F']
    #periods = ['B']
  elif options.year==2016:
    periods = ['B', 'C', 'D', 'E', 'F', 'G', 'E', 'H']
  elif options.year==2018:
    pass

  pds = ['HTMHT', 'JetHT', 'MET', 'DoubleEG', 'DoubleMuon', 'MuonEG', 'SingleElectron', 'SingleMuon', 'SinglePhoton'] #'DoublePhoton' ]



  print 'Running merging and duplicates removal'
  print options
  print 'inputPath={}'.format(inputPath)
  print 'periods={}'.format(periods)
  print 'PDs={}'.format(pds)

  # first create dir where to store output and intermediate output
  ret = os.mkdir(outputPath) # None if everything goes smoothly

  if ret!=None: raise RuntimeError('Problem in creating output directory, exit code=', ret)

  # second check that all files you want to work on exist
  warnings = 0
  print '\n -> Checking availability of samples'
  for period in periods:
    for pd in pds:
      allFiles = glob.glob(inputPath + '/*root')
      samplePathExpr = '{pd}_Run{year}{period}'.format(pd=pd,year=options.year,period=period)
      matches = filter(lambda x: samplePathExpr in x, allFiles)
      if len(matches)==0:
        print 'WARNING: sample %s not available in inputPath' % samplePathExpr
        warnings += 1
      elif len(matches)>1:
        print 'WARNING: more than one rootfile for %s' % samplePathExpr
        warnings += 1

  if options.doForce or warnings==0:
    for period in periods:
      print '\n -> Going to merge samples for period={}'.format(period)
      #  merge all available pds of a period in one dataset
      samples_to_merge = glob.glob('{inputPath}/*_Run{year}{period}*root'.format(inputPath=inputPath, year=options.year,period=period) )
      #print samples_to_merge
      sample_merged = '{outputPath}/merged_Run{year}{period}.root'.format(outputPath=outputPath, year=options.year, period=period)

      command = '{haddnano} {outP} {inP}'.format(
         haddnano='../../../../../../scripts/haddnano.py',
         outP=sample_merged,
         inP=' '.join(samples_to_merge)
      )
      try:
        ret = subprocess.call(command, shell=True)
        pass

      except subprocess.CalledProcessError as e:
        print 'ERROR! samples were not merged successfully, going to next '
        continue

      # if merging went smoothly, remove duplicates
      print '\n -> Going to remove duplicates from merged file'
      command = 'echo \"gROOT->LoadMacro(\\"removeDuplicates.C\\"); removeDuplicates(\\"{i}\\",1,\\"{o}\\", \\"Events\\"); gSystem->Exit(0);\" | root.exe -b -l;'.format(i=sample_merged, o=sample_merged.replace('.root', '_noDupl.root'))
      #print command
      try:
        ret = subprocess.call(command, shell=True)
      except subprocess.CalledProcessError as e:
        print 'ERROR in duplicate removal'

      print '\n\n\n'
  # then remove duplicates from it
