from ROOT import gROOT, TH1F, TH1, kBlack, kRed, kBlue, TCanvas, gStyle, TLegend, TLatex, TFile, TChain, TPad, kWhite




def makeHistoFromNtuple(infilename, intreename, outhistoname, outhistobinning, outhistoquantity, outhistoweight, outhistoselection="(1)", outhistosmooth=True):

  TH1.SetDefaultSumw2()

  # output
  #bins = array('d', outhistobins)
  #bins_n = len(outhistobins)-1
  histo = TH1F(outhistoname, outhistoname, *(outhistobinning))

  # input
  chain = TChain(intreename)
  chain.Add(infilename)

  #print 'Projecting tree to histogram...'

  ret = chain.Project(histo.GetName(), outhistoquantity, '('+outhistoselection + ')*(' + outhistoweight + ')')

  if outhistosmooth:
    histo.Scale(1, 'width')

  return ret,histo




def makeHistSettings(h):
  h.GetYaxis().SetNdivisions(510);
  h.GetYaxis().SetLabelSize(0.06);
  h.GetXaxis().SetLabelSize(0.06);
  h.GetYaxis().SetTitleSize(0.06);
  h.GetXaxis().SetTitleSize(0.08);
  h.GetYaxis().SetTitleOffset(0.96);
  h.GetXaxis().SetTitleOffset(1.0);
  h.GetYaxis().SetLabelOffset(0.01);
  h.GetXaxis().SetLabelOffset(0.01);
  h.GetXaxis().SetTickLength(0.06);
  #h.SetMarkerStyle(1)

def makeRatioSettings(ratioMC):
  #ratioMC.GetYaxis().SetRangeUser(0.75,1.25)
  ratioMC.GetYaxis().SetRangeUser(0.0,2.0)
  ratioMC.GetYaxis().SetNdivisions(504);
  #ratioMC.GetYaxis().SetNdivisions(508);
  ratioMC.GetYaxis().SetLabelSize(0.15);
  ratioMC.GetXaxis().SetLabelSize(0.15);
  ratioMC.GetYaxis().SetTitleSize(0.15);
  ratioMC.GetXaxis().SetTitleSize(0.15);
  ratioMC.GetYaxis().SetTitleOffset(0.35);
  ratioMC.GetXaxis().SetTitleOffset(1.2);
  ratioMC.GetYaxis().SetLabelOffset(0.01);
  ratioMC.GetXaxis().SetLabelOffset(0.03);
  ratioMC.GetXaxis().SetTickLength(0.06);
  #ratioMC.SetFillColor(kBlack)
  ratioMC.SetFillStyle(3004)
 # ratioMC.SetLineColor( kBlack )
  #ratioMC.SetLineWidth(4 )
  #ratioMC.SetMarkerStyle(1)
  #ratioMC.SetMarkerColor(kBlack)
  ratioMC.SetLineWidth(2)

# hnum nominal, hden var1, hden2 var2
def makeRatioPlot(hNum, hDen, hDen2="", nameNum="num", nameDen="den", nameDen2="", xtitle="pt",ytitle="Entries", ratiotitle="Ratio", norm=False, plotName="ratio", outDir='out'):
  TH1.SetDefaultSumw2()

  # prepare settings of histos
  hNum.SetLineColor(kBlack)
  hNum.SetLineWidth(2)
  hNum.SetMarkerStyle(20)
  #hNum.SetMarkerStyle(1)
  hNum.SetMarkerColor(kBlack)
  hNum.GetYaxis().SetTitle(ytitle)

  hDen.SetLineColor(kRed+1)
  hDen.SetMarkerColor(kRed+1)
  hDen.SetLineWidth(2)
  hDen.SetMarkerStyle(21)
  #hDen.SetMarkerStyle(1)

  if nameDen2 != "":
    hDen2.SetLineColor(kBlue)
    hDen2.SetMarkerColor(kBlue)
    hDen2.SetLineWidth(2)
    hDen2.SetMarkerStyle(22)
    #hDen2.SetMarkerStyle(1)
    makeHistSettings(hDen2)#


  makeHistSettings(hNum)
  makeHistSettings(hDen)




  # prepare canva
  canvas=TCanvas(plotName, plotName, 600, 600)
  canvas.cd()
  yMinP1=0.305;
  bottomMarginP1=0.005;
  pad1 = TPad('pad1','pad1',0,yMinP1,0.99,1)
  pad1.SetLogy()
  pad1.SetBottomMargin(bottomMarginP1)
  pad1.SetFillColor(kWhite)
  pad1.SetTickx()
  pad1.SetTicky()
  pad2 = TPad('pad2','pad2',0.,0.01,.99,0.300)
  pad2.SetTopMargin(0.010)
  pad2.SetBottomMargin(0.40)
  pad2.SetFillColor(kWhite)
  pad2.SetGridy()
  pad1.SetNumber(1)
  pad2.SetNumber(2)
  pad1.Draw()
  pad2.Draw()

  # prepare legend
  leg = TLegend(0.75,0.68,0.82,0.88,'')
  leg.SetBorderSize(0)
  leg.SetTextSize(0.05)


  # Draw
  pad1.cd()
  histo_saver = []

  #hNumNorm = hNum.Clone()
  if norm:
    hNumNorm = hNum.DrawNormalized('LP')
    histo_saver.append(hNumNorm)
  else:
    hNum.Draw('PE')

  hNum.SetMaximum(hNum.GetMaximum()*4)
  #leg.Draw('same')

  #hDenNorm = hDen.Clone()
  if norm:
    hDenNorm = hDen.DrawNormalized('samePE')
    histo_saver.append(hDenNorm)
  else:
    hDen.Draw('samePE')

  #hDenNorm2 = hDen2.Clone()
  if nameDen2 != "":
    if norm:
      hDenNorm2 = hDen2.DrawNormalized('samePE')
      histo_saver.append(hDenNorm2)
    else:
      hDen2.Draw('samePE')
    leg.AddEntry(hDen2, nameDen2, 'PE')

  leg.AddEntry(hDen, nameDen, 'PE')
  leg.AddEntry(hNum, nameNum, 'PE')
  leg.Draw('same')


  #print hNumNorm.Integral(), hDenNorm.Integral(), hDenNorm2.Integral()
  #print hNum.Integral(), hDen.Integral(), hDen2.Integral()

  #######################################################
  ### RATIO PAD
  #######################################################
  pad2.cd()
  hRatio = hNum.Clone()
  if nameDen2 != "": hRatio2 = hNum.Clone()

  if norm:
    hRatio = hNumNorm.Clone()
    hRatio2 = hNumNorm.Clone()
    print 'Ratio integral before division'
    print hRatio.Integral(), hRatio2.Integral()

    hRatio.Divide(hDenNorm)
    if nameDen2 != "": hRatio2.Divide(hDenNorm2)

    print 'Ratio integral after division'
    print hRatio.Integral(), hRatio2.Integral()


  else:
    hRatio.Divide(hDen)
    if nameDen2 != "": hRatio2.Divide(hDen2)



  #hRatio.SetLineColor(kRed+2)
  if nameDen2 != "": hRatio2.SetLineColor(kBlue)

  makeRatioSettings(hRatio)
  if nameDen2 != "": makeRatioSettings(hRatio2)

  hRatio.GetXaxis().SetTitle(xtitle)
  hRatio.GetYaxis().SetTitle(ratiotitle)
  hRatio.SetTitle('')



  hRatio.Draw('PE')
  if nameDen2 != "": hRatio2.Draw('PEsame')
  #hRatio.GetXaxis().SetRangeUser(200.,2000.)

  canvas.cd()
  canvas.Modified()
  canvas.Update()
  #return canvas
  canvas.SaveAs('{d}/{name}.pdf'.format(d=outDir, name = plotName))
  #canvas.SaveAs('ratio_{}_{}.pdf'.format(hNum.GetName(), hDen.GetName()))
  #canvas.SaveAs('plots/ratio_{}_{}.C'.format(hNum.GetName(), hDen.GetName()))
  #canvas.SaveAs('plots/ratio_{}_{}.root'.format(hNum.GetName(), hDen.GetName()))
  #canvas.Close()
