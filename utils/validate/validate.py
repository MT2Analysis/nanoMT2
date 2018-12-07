
import ROOT
import ratioPlot as RP
import array
import os
import os.path
import re
from ast import literal_eval



qs_common = []
file = open('validation_plots_MT2_common.txt', 'r')
#file = open('validation_single.txt', 'r')
for line in file:
  if line.startswith('#'): continue
  if line == '\n': continue
  data = line.split(':')
  data = map(lambda x: x.strip(),data)
  dic = {}
  dic['name'] = data[1]; dic['sel'] = data[2]; dic['hname'] = data[0]; dic['title'] = data[4]
  if '[' not in data[3]:
    strings = data[3].split(',')
    tuple = (int(strings[0]), float(strings[1]), float(strings[2]))
    dic['binning'] = tuple
  else:
    histobins = literal_eval(data[3])
    bins_n = len(histobins)-1
    bins = array.array('d', histobins)
    dic['binning'] = (bins_n, bins)
  #print dic
  qs_common.append(dic)
file.close


def getRelDiff(n1, n2):
  if n2!= 0:
    res = float(n1)/float(n2) - 1
  elif n2==0 and n1==0 :
    res = 0
  else:
    print 'Cannot compute rel diff wrt 0, skipping'
    res = None
  return res

def getBinDiff(h1, h2):
  ROOT.TH1.SetDefaultSumw2()
  #if ROOT.TH1.CheckConsistency(h1, h2): # if they're consistent check difference between the two
  # currently a protected member, cannot be used
  for iBin in range(1,h1.GetNbinsX()):
    diff = getRelDiff(h1.GetBinContent(iBin), h2.GetBinContent(iBin))
    if diff!=None: print 'Bin={}, evts1={}, evts2={}, rel diff={:.4f}%'.format(iBin, h1.GetBinContent(iBin), h2.GetBinContent(iBin), diff*100)

  totdiff = getRelDiff(h1.GetEntries(), h2.GetEntries())
  print 'Tot diff, evts1={}, evts2={}, rel diff={:.2f}%'.format(h1.GetEntries(), h2.GetEntries(), totdiff)

if __name__ == "__main__":
  # add style please
  ROOT.gROOT.ProcessLine('.L ~/CMS_style/tdrstyle.C')
  ROOT.gROOT.ProcessLine('setTDRStyle()')
  ROOT.gROOT.SetBatch(True)

  from argparse import ArgumentParser
  import os
  parser = ArgumentParser(description='', add_help=True)

  parser.add_argument('-f1', '--file1', type=str, dest='fname1', help='')
  parser.add_argument('-f2', '--file2', type=str, dest='fname2', help='')
  parser.add_argument('-t1', '--tree1', type=str, dest='treename1', help='', default = 'Events')
  parser.add_argument('-t2', '--tree2', type=str, dest='treename2', help='', default = 'mt2')
  parser.add_argument('-l1', '--label1', type=str, dest='label1', help='', default = 'A')
  parser.add_argument('-l2', '--label2', type=str, dest='label2', help='', default = 'B')
  parser.add_argument('-o', '--outdir', type=str, dest='outdirname', help='output dir')
  parser.add_argument('--doNorm', dest='doNorm', help='do shape comparison', action='store_true', default=False)
  parser.add_argument('--doLog', dest='doLog', help='use Log scale on y axis', action='store_true', default=False)
  parser.add_argument('--doFriend', dest='doFriend', help='do friend trees checks', action='store_true', default=False)
  parser.add_argument('-s', '--selection', type=str, dest='sel', help='selection; in case of friend tree, an example is abs(ht/new.ht-1)>0.05', default='(1)')

  options = parser.parse_args()

  os.system('mkdir {d}'.format(d=options.outdirname))

  #makeValidationPlots(options.fname1, options.fname2, options.treename1, options.treename2, options.label1, options.label2, options.outdirname)

  if os.path.isfile(options.fname1)==False or os.path.isfile(options.fname2)==False: raise RuntimeError('One of the two files is not available, \n{} \n{}'.format(options.fname1, options.fname2))

  qs_to_run = qs_common

  for q in qs_to_run:
    print 'investigating ', q['name']


    if options.doFriend == False:
      ret1,histo1 = RP.makeHistoFromNtuple(infilename=options.fname1, intreename=options.treename1, outhistoname=q['hname'] + '_1', outhistobinning=q['binning'], outhistoquantity=q['name'], outhistoweight='(1)', outhistoselection=q['sel'] + '&&({})'.format(options.sel), outhistosmooth=False )
      ret2,histo2 = RP.makeHistoFromNtuple(infilename=options.fname2, intreename=options.treename2, outhistoname=q['hname'] + '_2', outhistobinning=q['binning'], outhistoquantity=q['name'], outhistoweight='(1)', outhistoselection=q['sel'] + '&&({})'.format(options.sel), outhistosmooth=False )

    else:
      ret1,ret2,histo1,histo2 = RP.makeHistosFromFriends(infilename1=options.fname1, infilename2=options.fname2, intreename1=options.treename1, intreename2=options.treename2, \
                                                         outhistoname=q['hname'], outhistobinning=q['binning'], outhistoquantity=q['name'], outhistoweight='(1)', \
                                                         outhistoselection=q['sel'] + '*({})'.format(options.sel), outhistosmooth=False, index='evt', friendname='new')
    # now you should have the histograms
    if ret1 != -1 and ret2 != -1:
      # do the ratio plot
      RP.makeRatioPlot(hNum=histo1, hDen=histo2, nameNum=options.label1, nameDen=options.label2, xtitle=q['title'],ytitle="Entries", ratiotitle="Ratio", norm=options.doNorm, log=options.doLog, outDir=options.outdirname, plotName=q['hname'])
      print 'Entries histo1', histo1.GetEntries(), ' histo2', histo2.GetEntries()

      # catch bin-by-bin differences
      print 'Analyzing bin differences'
      getBinDiff(h1=histo1, h2=histo2)
      print '\n'
    else:
      print 'Skipping ', q['name']



      # do the friend tree buisness
