import os
from argparse import ArgumentParser


def getOptions():

  allowed_formats = ['MINIAOD', 'NANOAOD']
  allowed_status = ['*', 'VALID', 'PRODUCTION', 'INVALID']
  allowed_campaigns = ['Run2017*31Mar2018*', 'Run2016*22Aug2018*', 'Run2018*14Sep2018*', 'Run2018*17Sep2018*' ]

  #   Brief explanations of the campaigns here please !
  #  'Run2017*31Mar2018*' 		     # 2017 94X re-reco 
  #  'Run2016*22Aug2018*' 		     # 2016 94X legacy
  #  'Run2018*14Sep2018*'	             # 2018 101X(?) prompt-reco -> this will not be used for legacy results -> recipe for combination ->
  #  'Run2018*17Sep2018*' # ONLY FOR MINI    # 2018 102X    re-reco     -> for legacy -> pilot requests for re-reco are running 17Sep2018

  # https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD#Centrally_produced_samples
  # https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMiniAOD
  parser = ArgumentParser(description='', add_help=True)

  parser.add_argument('-c', '--campaign', type=str, dest='campaign', help='production campaign expression, allows for *', choices=allowed_campaigns, default='*Run2017*31Mar2018*')
  parser.add_argument('-f', '--format', type=str, dest='dataFormat', help='datatier', choices=allowed_formats, default='NANOAOD')
  parser.add_argument('-s', '--status', type=str, dest='status', help='das status', choices=allowed_status, default='*')
  
  return parser.parse_args()


if __name__ == "__main__":
  import time
  print '# This list was generated on ', time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())

  options = getOptions()

  PDs = ['SinglePhoton', 'DoublePhoton', 'JetHT', 'HTMHT', 'MET', 'SingleElectron', 'SingleMuon', 'DoubleEG', 'DoubleMuon', 'MuonEG']
  if '2018' in options.campaign: 
    PDs = ['EGamma', 'JetHT', 'MET', 'SingleMuon', 'DoubleMuon', 'MuonEG']
  #PDs = ['MET']

  for PD in PDs:
    command = 'dasgoclient --query="dataset=/{pd}/{c}/{df} dataset status={s}"'.format(pd=PD,c=options.campaign, df=options.dataFormat, s=options.status)
    print '\n\n###  ', command
    print '# ****\n# Summary for:  PD =', PD,  ' campaign =' , options.campaign, ' datatier =', options.dataFormat, ' status =', options.status, '\n# ****\n'
    os.system(command)
