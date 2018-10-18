# merge.py - A simple script to launch the groupMerger
# Maria Giulia Ratti - ETH Zurich
# the script must be simple enough such that we can enable group splitting in batch

# TODO: implement for signal

def getOptions(MT2groups):
  from argparse import ArgumentParser

  allowed_groups = MT2groups.keys()

  parser = ArgumentParser(description='Merging  options', add_help=True)
  parser.add_argument('-p','--productionLabel', type=str, dest='productionLabel', help='name of the crab production', default='TEST0')
  parser.add_argument('-v','--version', type=str, dest='version', help='suffix for post-processing version', default='v0')
  parser.add_argument('-g', '--group', type=str, dest='group', help='sample group', choices=allowed_groups, default='QCD_LO')
  parser.add_argument('-y','--year', type=int, dest='year', help='year of data taking / MC taking :)', default=2017)

  parser.add_argument('--doMC', dest='doMC', help='is it a monte carlo sample?', action='store_true', default=False)

  return parser.parse_args()


class Group(object):
  def __init__(self,name,exprs=[]):
    self.name = name
    self.exprs = exprs

def getMT2groups():

  Zvv = Group(name='Zvv', exprs=['ZJetsToNuNu_HT'])
  Wlv  = Group(name='Wlv',  exprs=['WJetsToLNu_HT'])
  Zll  = Group(name='Zll',  exprs=['DYJetsToLL_M-50_HT'])
  QCD  = Group(name='QCD',  exprs=['QCD_HT'])
  Top  = Group(name='Top',  exprs=['TT','ST_','tt'])
  Gjets= Group(name='Gjets',exprs=['GJets_HT'])

  # data groups
  MET               = Group(name='MET', exprs=['MET'])
  JetHT             = Group(name='JetHT', exprs=['JetHT'])
  HTMHT             = Group(name='HTMHT', exprs=['HTMHT'])
  SingleElectron    = Group(name='SingleElectron', exprs=['SingleElectron'])
  SingleMuon        = Group(name='SingleMuon', exprs=['SingleMuon'])
  DoubleEG          = Group(name='DoubleEG', exprs=['DoubleEG'])
  DoubleMuon        = Group(name='DoubleMuon', exprs=['DoubleMuon'])
  MuonEG            = Group(name='MuonEG', exprs=['MuonEG'])
  SinglePhoton      = Group(name='SinglePhoton', exprs=['SinglePhoton'])
  DoublePhoton      = Group(name='DoublePhoton', exprs=['DoublePhoton]'])

  MT2groups = {}
  MT2groups['Zvv'] = [Zvv]
  MT2groups['Wlv'] = [Wlv]
  MT2groups['Zll'] = [Zll]
  MT2groups['QCD'] = [QCD]
  MT2groups['Top'] = [Top]
  MT2groups['Gjets'] = [Gjets]
  MT2groups['bkg'] = [Zvv, Wlv, Zll, QCD, Top, Gjets]
  MT2groups['sig'] = []
  MT2groups['data'] = [MET, JetHT, HTMHT, SingleElectron, SingleMuon, DoubleEG, DoubleMuon, MuonEG, SinglePhoton]# DoublePhoton] 

  MT2groups['MET'] = [MET]
  MT2groups['JetHT'] = [JetHT]
  MT2groups['HTMHT'] = [HTMHT]
  MT2groups['SingleElectron'] = [SingleElectron]
  MT2groups['SingleMuon'] = [SingleMuon]
  MT2groups['DoubleEG'] = [DoubleEG]
  MT2groups['DoubleMuon'] = [DoubleMuon]
  MT2groups['MuonEG'] = [MuonEG]
  MT2groups['SinglePhoton'] = [SinglePhoton]
  MT2groups['DoublePhoton'] = [DoublePhoton]


  return MT2groups


if __name__ == "__main__":

  import os

  # options here
  MT2groups = getMT2groups()

  options = getOptions(MT2groups)

  inputPath = '/pnfs/psi.ch/cms/trivcat/store/user/{}/crab/nanoMT2/{}/'.format(os.environ['USER'],  options.productionLabel)
  outputPath = '/scratch/{}/merged_nanoMT2/{}_{}/'.format(os.environ['USER'], options.productionLabel, options.version)
  cfgFile = 'cfg/{df}_{y}_merge_{pl}.txt'.format(df='mc_bkg' if options.doMC else 'data', y=str(options.year), pl=options.productionLabel)

  from groupMerger import GroupMerger

  for MT2Group in MT2groups[options.group]:
    g = GroupMerger(groupName=MT2Group.name, groupExprs=MT2Group.exprs, inputPath=inputPath, outputPath=outputPath, doMC=options.doMC)
    g.configGroupMembers(cfgFile=cfgFile)
    g.configOutput()
    ret = g.process()




  #ret = mergeGroup(group, inputPath, outputPath)
  #if ret: print 'Merging ended successfully'
  #else: print 'Something went wrong'
