
import ROOT
import ratioPlot as RP
import array
import os
import re
from ast import literal_eval



qs_common = []
file = open('validation_plots_MT2_common.txt', 'r')
for line in file:
  if line.startswith('#'): continue
  if line == '\n': continue
  data = line.split(':')
  data = map(lambda x: x.strip(),data)
  dic = {}
  dic['name'] = data[1]
  dic['sel'] = data[2]
  dic['hname'] = data[0]
  dic['title'] = data[4]
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

  options = parser.parse_args()

  os.system('mkdir {d}'.format(d=options.outdirname))

  #makeValidationPlots(options.fname1, options.fname2, options.treename1, options.treename2, options.label1, options.label2, options.outdirname)

  qs_to_run = qs_common

  for q in qs_to_run:
    print 'investigating ', q['name']

    ret1,histo1 = RP.makeHistoFromNtuple(infilename=options.fname1, intreename=options.treename1, outhistoname=q['hname'] + '_1', outhistobinning=q['binning'], outhistoquantity=q['name'], outhistoweight='(1)', outhistoselection=q['sel'], outhistosmooth=False )
    ret2,histo2 = RP.makeHistoFromNtuple(infilename=options.fname2, intreename=options.treename2, outhistoname=q['hname'] + '_2', outhistobinning=q['binning'], outhistoquantity=q['name'], outhistoweight='(1)', outhistoselection=q['sel'], outhistosmooth=False )
    if ret1 != -1 and ret2 != -1:
      RP.makeRatioPlot(hNum=histo1, hDen=histo2, nameNum=options.label1, nameDen=options.label2, xtitle=q['title'],ytitle="Entries", ratiotitle="Ratio", norm=options.doNorm, log=options.doLog, outDir=options.outdirname, plotName=q['hname'])
      print 'Entries histo1', histo1.GetEntries(), ' histo2', histo2.GetEntries()
    else:
      print 'Skipping ', q['name']
