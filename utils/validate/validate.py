
import ROOT
import ratioPlot as RP
import array
import os
import re
from ast import literal_eval



qs_common = []
file = open('validation_plots_MT2_common.txt', 'r')
for line in file:
  if '#' in line: continue
  if line == '\n': continue
  data = line.split(':')
  data = map(lambda x: x.strip(),data)
  dic = {}
  dic['name'] = data[0]
  dic['hname'] = data[1]
  dic['title'] = data[3]
  if '[' not in data[2]:
    strings = data[2].split(',')
    tuple = (int(strings[0]), float(strings[1]), float(strings[2]))
    dic['binning'] = tuple
  else:
    histobins = literal_eval(data[2])
    bins_n = len(histobins)-1
    bins = array.array('d', histobins)
    dic['binning'] = (bins_n, bins)
  qs_common.append(dic)
file.close


if __name__ == "__main__":
  #gROOT.ProcessLine('')
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

  options = parser.parse_args()

  os.system('mkdir {d}'.format(d=options.outdirname))

  #makeValidationPlots(options.fname1, options.fname2, options.treename1, options.treename2, options.label1, options.label2, options.outdirname)

  qs_to_run = qs_common

  for q in qs_to_run:
    print 'investigating ', q['name']
    ret1,histo1 = RP.makeHistoFromNtuple(options.fname1, options.treename1, q['name'] + '_1', q['binning'], q['hname'], '(1)', '(1)', False )
    ret2,histo2 = RP.makeHistoFromNtuple(options.fname2, options.treename2, q['name'] + '_2', q['binning'], q['hname'], '(1)', '(1)', False )
    if ret1 != -1 and ret2 != -1:
      RP.makeRatioPlot(hNum=histo1, hDen=histo2, nameNum=options.label1, nameDen=options.label2, xtitle=q['title'],ytitle="Entries", ratiotitle="Ratio", norm=False, outDir=options.outdirname, plotName=q['name'])
    else:
      print 'Skipping ', q['name']
