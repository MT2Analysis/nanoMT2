# This module is an adaptation and simplification of MT2Analyzer.py in heppy
import ROOT
from ROOT.heppy import Hemisphere
from ROOT.heppy import Davismt2
davismt2 = Davismt2()


def computeMT2(visApx, visApy, visBpx, visBpy, invispx, invispy):
# creates auxiliary arrays of transverse momenta
# calls DavisMt2 method

  import array
  import numpy

  invisVector= array.array('d',[0.,invispx,invispy])
  visAVector = array.array('d',[0.,visApx, visApy])
  visBVector = array.array('d',[0.,visBpx, visBpy])

  davismt2.set_momenta(visAVector,visBVector,invisVector);
  davismt2.set_mn(0);

  return davismt2.get_mt2()


def getMT2(objects, met):
# objects - list of Objects
# met - ROOT.TLorentzVector()
# creates auxiliary arrays for objects and met
# calls Hemisphere method

  if len(objects)>=2:
    pxvec  = ROOT.std.vector(float)()
    pyvec  = ROOT.std.vector(float)()
    pzvec  = ROOT.std.vector(float)()
    Evec  = ROOT.std.vector(float)()
    grouping  = ROOT.std.vector(int)()

    for jet in objects:
      pxvec.push_back(jet.p4().Px())
      pyvec.push_back(jet.p4().Py())
      pzvec.push_back(jet.p4().Pz())
      Evec.push_back(jet.p4().Energy())

    # this magical object groups together the 4 vectors into two hemispheres
    hemisphere = Hemisphere(pxvec, pyvec, pzvec, Evec, 2, 3)
    grouping=hemisphere.getGrouping()

    pseudoJet1px = 0
    pseudoJet1py = 0
    pseudoJet1pz = 0
    pseudoJet1energy = 0
    multPSJ1 = 0

    pseudoJet2px = 0
    pseudoJet2py = 0
    pseudoJet2pz = 0
    pseudoJet2energy = 0
    multPSJ2 = 0

    # we build two "pseudo-jets", i.e. two four-vectors that are the sum of the 4-vectors of each hemisphere
    for index in range(0, len(pxvec)):
      if(grouping[index]==1):
        pseudoJet1px += pxvec[index]
        pseudoJet1py += pyvec[index]
        pseudoJet1pz += pzvec[index]
        pseudoJet1energy += Evec[index]
        multPSJ1 += 1
      if(grouping[index]==2):
        pseudoJet2px += pxvec[index]
        pseudoJet2py += pyvec[index]
        pseudoJet2pz += pzvec[index]
        pseudoJet2energy += Evec[index]
        multPSJ2 += 1

    pseudoJet1pt2 = pseudoJet1px*pseudoJet1px + pseudoJet1py*pseudoJet1py
    pseudoJet2pt2 = pseudoJet2px*pseudoJet2px + pseudoJet2py*pseudoJet2py

    # pt^2 ordering
    if pseudoJet1pt2 >= pseudoJet2pt2:
      pseudoJet1p4 = ROOT.TLorentzVector( pseudoJet1px, pseudoJet1py, pseudoJet1pz, pseudoJet1energy )
      pseudoJet2p4 = ROOT.TLorentzVector( pseudoJet2px, pseudoJet2py, pseudoJet2pz, pseudoJet2energy )
    else:
      pseudoJet1p4 = ROOT.TLorentzVector( pseudoJet2px, pseudoJet2py, pseudoJet2pz, pseudoJet2energy )
      pseudoJet2p4 = ROOT.TLorentzVector( pseudoJet1px, pseudoJet1py, pseudoJet1pz, pseudoJet1energy )

    # TODO: here I could choose to save the information on these pseudojets
    # for the moment only use the information to compute the mt2 variable

    mt2 = computeMT2(visApx=pseudoJet1p4.Px(), visApy=pseudoJet1p4.Py(), visBpx=pseudoJet2p4.Px(), visBpy=pseudoJet2p4.Py(), invispx=met.Px(), invispy=met.Py())
    return mt2


  #else: raise RuntimeError("Something's wrong with MT2 calculation, expect at least two objects")
  else:
    #print 'cannot compute mt2 variable for this event'
    return -999
