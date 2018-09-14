import os

if __name__ == "__main__":

  dataFormat = 'NANOAOD' # or 'NANOAOD'
  campaign = 'Run2017*' # 22Aug2018 Run2017*31Mar2018*
  # https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD#Centrally_produced_samples
  # https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMiniAOD
  PDs = ['SinglePhoton', 'DoublePhoton', 'JetHT', 'HTMHT', 'MET', 'SingleElectron', 'SingleMuon', 'DoubleEG', 'DoubleMuon', 'MuonEG']
  #PDs = ['MET']
  for PD in PDs:
    command = 'dasgoclient --query="dataset=/{pd}/{c}/{df}"'.format(pd=PD,c=campaign, df=dataFormat)
    print '# ****\n# Summary for:  PD =', PD,  ' campaign =' , campaign, ' datatier =', dataFormat, '\n# ****\n'
    os.system(command)
