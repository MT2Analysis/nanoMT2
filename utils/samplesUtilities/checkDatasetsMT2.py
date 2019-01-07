# Check existing samples for MT2 analysis (and make a list of them)
#
# setup:  
# source ~/.bash_profile
# voms-proxy-init --voms cms

import os
import os.path

class Group(object):
  def __init__(self,name,expr):
    self.name = name
    self.expr = expr

def checkMT2Datasets(inputFile, campaign, dataFormat, status, groups, info, doGroupQuery):
  
  if not os.path.isfile(inputFile): raise RuntimeError('Provided input list does not exist')

  for group in groups:
    print '#****\n# Summary for:  group =', group.expr,  ' campaign =' , campaign, ' datatier =', dataFormat, ' status =', status, '\n#****\n'
    f = open(inputFile, "r")
    
    for line in f:
      # skip commented and empty lines
      if '#' in line: continue
      if line == '\n': continue
  
      exprs = group.expr.split('|')
      match = filter(lambda x : x in line, exprs)
      if len(match) > 1 : raise RuntimeError('wrong logic')
      if match:
        dataset = '/' + line.split('\n')[0] + '/' + campaign + '/' + dataFormat
        command = 'dasgoclient --query="dataset dataset= {d} status={s}"'.format(d=dataset, s=status)
        if info: print 'Going to run command:     ' , command
        print '# Gen sample: ', line.split('\n')[0]
        os.system(command)
        print ''

    f.close()
    if doGroupQuery:
      dataset = '/' + group.expr + '*/' + campaign + '/' + dataFormat
      command = 'dasgoclient --query="dataset dataset = {d} status={s}"'.format(d=dataset, s=status)
      print '# Query for group: ', group.name, '  expr: ', group.expr
      os.system(command)
      print ''

if __name__ == "__main__":

  import time
  print '# This list was generated on ', time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())

  # define all MT2 groups you might be interested in
  # Be sure that this group exists in the sample list input file
  # TODO: implement signals and data
  Zinv_LO = Group(name='Zinv_LO', expr='ZJetsToNuNu_HT')
  Wlv_LO  = Group(name='Wlv_LO',  expr='WJetsToLNu_HT')
  Zll_LO  = Group(name='Zll_LO',  expr='DYJetsToLL_M-50_HT')
  QCD_LO  = Group(name='QCD_LO',  expr='QCD_HT')
  Top     = Group(name='Top',     expr='TT|ST_|tt')
  Gjets_LO= Group(name='Gjets_LO',expr='GJets_HT')

  T1qqqq  = Group(name='T1qqqq',  expr='T1qqqq')
  T1bbbb  = Group(name='T1bbbb',  expr='T1bbbb')
  T1tttt  = Group(name='T1tttt',  expr='T1tttt')
  T2qq  = Group(name='T2qq',  expr='T2qq')
  T2bb  = Group(name='T2bb',  expr='T2bb')
  T2tt  = Group(name='T2tt',  expr='T2tt')
  #data2017= Group(name='', expr='MET|JetHT|HTMHT|DoubleEG|MuonEG|DoubleMuon|SingleElectron|SingleMuon|SinglePhoton')

  MT2groups = {}
  MT2groups['Zinv_LO'] = [Zinv_LO]
  MT2groups['Wlv_LO'] = [Wlv_LO]
  MT2groups['Zll_LO'] = [Zll_LO]
  MT2groups['QCD_LO'] = [QCD_LO]
  MT2groups['Top'] = [Top]
  MT2groups['Gjets'] = [Gjets_LO]
  MT2groups['bkg'] = [Zinv_LO, Wlv_LO, Zll_LO, QCD_LO, Top, Gjets_LO]
  MT2groups['sig'] = [T1qqqq, T1bbbb, T1tttt, T2qq, T2bb, T2tt]
  #MT2groups['data'] = [data2017]
  MT2groups['all'] = MT2groups['bkg'] + MT2groups['sig'] #+ MT2groups['data']

  # define options
  from argparse import ArgumentParser
  import os
  parser = ArgumentParser(description='', add_help=True)

  allowed_groups = MT2groups.keys()
  allowed_formats = ['MINIAOD*', 'NANOAOD*']
  allowed_status = ['*', 'VALID', 'PRODUCTION', 'INVALID']
  allowed_campaigns = ['RunIIFall17*12Apr2018*', 'RunIISummer16NanoAOD*05Feb2018*', 'RunIISummer16NanoAODv3*', 'RunIIAutumn18NanoAOD*', '*', 'RunIIFall17NanoAODv4*']

  # description of the campaigns
  # RunIIAutumn18NanoAOD*                       2018 baseline nano 
  # RunIIFall17*12Apr2018*    			2017 baseline nano (and mini) production
  # RunIISummer16NanoAODv3*                     2016 baseline nano (in principle!)
  # RunIISummer16NanoAOD*05Feb2018*             2016 first nano production
  # RunIIFall17NanoAODv4*                       2017 Moriond19 samples

  parser.add_argument('-c', '--campaign', type=str, dest='campaign', help='production campaign expression, allows for *', choices=allowed_campaigns, default='RunIIFall17*12Apr2018*')
  parser.add_argument('-f', '--format', type=str, dest='dataFormat', help='datatier', choices=allowed_formats, default='MINIAOD*')
  parser.add_argument('-s', '--status', type=str, dest='status', help='das status', choices=allowed_status, default='VALID')
  parser.add_argument('-g', '--group', type=str, dest='group', help='sample group', choices=allowed_groups, default='QCD_LO')
  parser.add_argument('-l', '--inputlist', type=str, dest='inputFile', help='a txt file containing file paths, one per line', metavar='list', default='./PDsamples/mc_bkgs_mt2_initial.txt')
  parser.add_argument('--info', dest='info', help='show das commands', action='store_true', default=False)
  parser.add_argument('--dogroupquery', dest='doGroupQuery', help='also perform the group query', action='store_true', default=False)
  
  options = parser.parse_args()

  groupsToCheck = MT2groups[options.group]
  checkMT2Datasets(options.inputFile, options.campaign, options.dataFormat, options.status, groupsToCheck, options.info, options.doGroupQuery)
