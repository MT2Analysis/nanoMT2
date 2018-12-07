# merge.py - A simple script to launch the groupMerger
# Maria Giulia Ratti - ETH Zurich

# TODO: implement for signal

class Group(object):
  def __init__(self,name,exprs=[]):
    self.name = name
    self.exprs = exprs # needed to match with the sample names in the cfg/list.txt

def getMT2groups():

  Zvv = Group(name='Zvv', exprs=['ZJetsToNuNu_HT'])
  Wlv  = Group(name='Wlv',  exprs=['WJetsToLNu_HT'])
  Zll  = Group(name='Zll',  exprs=['DYJetsToLL_M-50_HT'])
  QCD  = Group(name='QCD',  exprs=['QCD_HT'])
  Top  = Group(name='Top',  exprs=['TT','ST_','tt'])
  Gjets= Group(name='Gjets',exprs=['GJets_HT'])

  MET               = Group(name='MET', exprs=['MET'])
  JetHT             = Group(name='JetHT', exprs=['JetHT'])
  HTMHT             = Group(name='HTMHT', exprs=['HTMHT'])
  SingleElectron    = Group(name='SingleElectron', exprs=['SingleElectron'])
  SingleMuon        = Group(name='SingleMuon', exprs=['SingleMuon'])
  DoubleEG          = Group(name='DoubleEG', exprs=['DoubleEG'])
  DoubleMuon        = Group(name='DoubleMuon', exprs=['DoubleMuon'])
  MuonEG            = Group(name='MuonEG', exprs=['MuonEG'])
  SinglePhoton      = Group(name='SinglePhoton', exprs=['SinglePhoton'])
  DoublePhoton      = Group(name='DoublePhoton', exprs=['DoublePhoton'])
  EGamma      	    = Group(name='Egamma', exprs=['EGamma'])
  

  MT2groups = {}
  MT2groups[2016] = {}
  MT2groups[2017] = {}
  MT2groups[2018] = {}

  for year in MT2groups.keys():
    MT2groups[year]={}
    MT2groups[year]['data']={}
    MT2groups[year]['mc']={}

    MT2groups[year]['mc']['Zvv'] = [Zvv]
    MT2groups[year]['mc']['Wlv'] = [Wlv]
    MT2groups[year]['mc']['Zll'] = [Zll]
    MT2groups[year]['mc']['QCD'] = [QCD]
    MT2groups[year]['mc']['Top'] = [Top]
    MT2groups[year]['mc']['Gjets'] = [Gjets]
    MT2groups[year]['mc']['sig'] = []

    if year == 2016 or year == 2017:
      MT2groups[year]['data']['MET'] = [MET]
      MT2groups[year]['data']['JetHT'] = [JetHT]
      MT2groups[year]['data']['HTMHT'] = [HTMHT]
      MT2groups[year]['data']['SingleElectron'] = [SingleElectron]
      MT2groups[year]['data']['SingleMuon'] = [SingleMuon]
      MT2groups[year]['data']['DoubleEG'] = [DoubleEG]
      MT2groups[year]['data']['DoubleMuon'] = [DoubleMuon]
      MT2groups[year]['data']['MuonEG'] = [MuonEG]
      MT2groups[year]['data']['SinglePhoton'] = [SinglePhoton]
      MT2groups[year]['data']['DoublePhoton'] = [DoublePhoton]
    elif year == 2018:
      MT2groups[year]['data']['MET'] = [MET]
      MT2groups[year]['data']['JetHT'] = [JetHT]
      MT2groups[year]['data']['SingleMuon'] = [SingleMuon]
      MT2groups[year]['data']['DoubleMuon'] = [DoubleMuon]
      MT2groups[year]['data']['MuonEG'] = [MuonEG]
      MT2groups[year]['data']['EGamma'] = [EGamma]
       
  return MT2groups


def getOptions():
  from argparse import ArgumentParser

  parser = ArgumentParser(description='Merging  options', add_help=True)
  parser.add_argument('-p','--productionLabel', type=str, dest='productionLabel', help='name of the crab production', default='TEST0')
  parser.add_argument('-v','--version', type=str, dest='version', help='suffix for post-processing version', default='v0')
  parser.add_argument('-g', '--group', type=str, dest='group', help='sample group', default=None)
  parser.add_argument('-y','--year', type=int, dest='year', help='year of data taking / MC taking :)', default=2017)

  parser.add_argument('--doMC', dest='doMC', help='is it a monte carlo sample?', action='store_true', default=False)

  return parser.parse_args()

if __name__ == "__main__":

  import os

  # options here
  options = getOptions()

  mc_or_data = 'mc' if options.doMC else 'data'

  MT2groups = getMT2groups()

  inputPath = '/pnfs/psi.ch/cms/trivcat/store/user/{}/crab/nanoMT2/{}/'.format(os.environ['USER'],  options.productionLabel)
#  outputPath = '/scratch/{}/merged_nanoMT2/{}_{}/'.format(os.environ['USER'], options.productionLabel, options.version)
  outputPath = '/pnfs/psi.ch/cms/trivcat/store/user/{}/merged_nanoMT2/{}_{}/'.format(os.environ['USER'], options.productionLabel, options.version)
  cfgFile = 'cfg/{df}_{y}_merge_{pl}.txt'.format(df='mc_bkg' if options.doMC else 'data', y=str(options.year), pl=options.productionLabel)

  from groupMerger import GroupMerger

  for MT2Group in MT2groups[options.year][mc_or_data][options.group]:
    g = GroupMerger(groupName=MT2Group.name, groupExprs=MT2Group.exprs, inputPath=inputPath, outputPath=outputPath, doMC=options.doMC)
    g.configGroupMembers(cfgFile=cfgFile)
    g.configOutput()
    ret = g.process()

