# This module is meant to produce all mt2Analysis-specific variables
# It will be a long code, but let's try to keep it simple and at least you won't have to search for objets defined in other packages!
# Please note the space convention rather than tab convention wrt other nanoAOD modules

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import PhysicsTools.NanoAODTools.postprocessing.tools as tools
from PhysicsTools.NanoAODTools.postprocessing.analysis.mt2.mt2Analyzer import getMT2


# my implementation of closest
# returns index of DeltaR-closest element in collecion wrt obj
def closest(obj,collection):
  ret = None; drMin = 999
  for i,x in enumerate(collection):
    dr = tools.deltaR(obj,x)
    if dr < drMin:
      ret = i; drMin = dr
  return (ret,drMin)

def mtw(x1_pt, x1_phi, x2_pt, x2_phi):
  import math
  return math.sqrt(2*x1_pt*x2_pt*(1-math.cos(x1_phi-x2_phi)))

def getBitDecision(x, n): # x is an integer
  return x & 2**n != 0


class mt2VarsProducer(Module):
  def __init__(self, isMC=True, year=2017):
    self.year = year
    self.isMC = isMC
    pass
  def beginJob(self):
    pass
  def endJob(self):
    pass
  def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    self.verbose = False
    self.out = wrappedOutputTree


    self.out.branch("nJet20", "I")
    self.out.branch("nJet30", "I")
    self.out.branch("nBJet20", "I")
    self.out.branch("nElectrons10", "I")
    self.out.branch("nMuons10", "I")
    self.out.branch("nPFLep5LowMT", "I")
    self.out.branch("nPFHad10LowMT", "I")
    self.out.branch("nLepLowMT", "I")
    self.out.branch("ht", "F")
    self.out.branch("mht_pt", "F")
    self.out.branch("mht_phi", "F")
    self.out.branch("diffMetMht", "F")
    self.out.branch("deltaPhiMin", "F")
    self.out.branch("jet1_pt", "F")
    self.out.branch("jet2_pt", "F")
    self.out.branch("mt2", "F")
    self.out.branch("met_pt", "F")
    self.out.branch("met_phi", "F")



    # TODO: create the other branches


  def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    pass
  def analyze(self, event):
    """process event, return True (go to next module) or False (fail, go to next event)"""
    electrons = Collection(event, "Electron")
    muons = Collection(event, "Muon")
    jets = Collection(event, "Jet")
    photons = Collection(event, "Photon")
    met = Object(event, "MET")
    njets = len(jets)
    isotracks = Collection(event, "IsoTrack")

    # Perform SELECTIONS
    selected_recoelectrons = []
    selected_recomuons = []
    selected_recoleptons = []
    selected_pfleptons = []
    selected_pfhadrons = []
    selected_jets = []
    baseline_jets = []

    # Want to loop explicitly on the objects to add the isToRemove flag -
    # - which I need to check for overlaps between objects efficiently
    # otherwise I could do it with filter(lambda x: blabla)
    for electron in electrons:
      if electron.pt < 10: continue
      if abs(electron.eta)>2.4: continue
      if electron.cutBased == 0: continue
      # could it be instead Electron_convVeto the flag to check ?
      if electron.miniPFRelIso_all/electron.pt > 0.1: continue
      # TODO: check miniPFRelIso_all does not include /pt
      electron.isToRemove = False
      selected_recoelectrons.append(electron)

    for muon in muons:
      if muon.pt < 10: continue
      if abs(muon.eta)>2.4: continue
      # id cut if isLooseMuon coincides with loose working point
      if abs(muon.dz)>0.5: continue
      if abs(muon.dxy)>0.2: continue
      if muon.miniPFRelIso_all/muon.pt > 0.2: continue
      muon.isToRemove = False
      selected_recomuons.append(muon)

    for it in isotracks:
      it.mass = 0.
      if not it.isPFcand: continue # consider only pfcandidates
      if abs(it.dz)>0.1: continue
      if abs(it.pdgId) == 11 or abs(it.pdgId) == 13: # muon or electron PFcandidates
        if it.pt<5: continue
        if it.pfRelIso03_chg/it.pt > 0.2: continue
        MT_it_met = mtw(it.pt, it.phi, met.pt, met.phi)
        if MT_it_met > 100: continue
        it.isToRemove = False
        selected_pfleptons.append(it)
      else:
        if it.pt<10: continue
        if it.pfRelIso03_chg/it.pt > 0.1: continue
        it.isToRemove = False
        selected_pfhadrons.append(it)

    for jet in jets:
      jet.isToRemove = False
      if self.verbose:  print 'jet id tight ', getBitDecision(jet.jetId, 2)
      if getBitDecision(jet.jetId, 2) == False: continue  #  bit1 is loose (always false in 2017 since it does not exist), bit2 is tight, bit3 is tightLepVeto"
      if jet.pt<20: continue # TODO: is it the right cut?
      if abs(jet.eta)>4.7: continue
      baseline_jets.append(jet)
      #if abs(jet.eta)<2.4: continue
      #selected_jets.append(jet)

    baseline_jets.sort(key=lambda jet: jet.pt, reverse = True)
    selected_recoleptons = selected_recomuons + selected_recoelectrons

    # ##################################################
    # NOW PERFORM THE CROSS-CLEANING
    # ##################################################
    for it in selected_pfleptons:
      (irl,dRmin) = closest(it,selected_recoleptons)
      if irl and dRmin<0.1:
        it.isToRemove = True # mark the pflepton for removal because it overlaps with a selected reco lepton
      #else: clean_pfleptons.append(it)
        # mark the pfleptons as to be removed to be removed

    # now remove closest jet to lepton within DeltaR
    for lep in selected_recoleptons:
      (ijet,dRmin) = closest(lep,baseline_jets)
      if self.verbose: print ijet,dRmin
      if ijet and dRmin<0.4: # mark that jet to be removed
        baseline_jets[ijet].isToRemove = True

    # ##################################################
    # cleaned collections of objects
    # ##################################################    #selected_jets = [jet for jet in baseline_jets if abs(jet.eta) < 2.4]
    clean_jets20 =        [jet for jet in baseline_jets if jet.isToRemove == False and abs(jet.eta) < 2.4 and jet.pt > 20]
    clean_jets30 =        [jet for jet in clean_jets20 if jet.pt > 30]
    clean_bjets20 =       [jet for jet in clean_jets20 if jet.btagCSVV2 > 0.8838]
    clean_recoleptons =   selected_recoleptons
    clean_recoelectrons = selected_recoelectrons
    clean_recomuons =     selected_recomuons
    clean_pfleptons =    [it for it in selected_pfleptons if it.isToRemove == False]
    clean_pfelectrons =  [lep for lep in clean_pfleptons if abs(it.pdgId) == 11]
    clean_pfmuons =      [lep for lep in clean_pfleptons if abs(it.pdgId) == 13]
    clean_pfhadrons =    selected_pfhadrons # TODO: check
    clean_leptons =      clean_pfleptons + clean_recoleptons
    objects_std =        clean_jets30 + clean_leptons

    ####
    # Additional sorting should happen here
    objects_std.sort(key=lambda obj: obj.pt, reverse = True)

    # ##################################################
    # Now you're ready to count objects
    # ##################################################
    nJet20 = len(clean_jets20)
    nJet30 = len(clean_jets30)
    nBJet20 = len(clean_bjets20)
    nElectrons10 = len(clean_recoelectrons)
    nMuons10 = len(clean_recomuons)
    nPFLep5LowMT = len(clean_pfleptons)
    nPFHad10LowMT = len(clean_pfhadrons)
    nLepLowMT = len(clean_leptons) # TODO: add MT cut on selected recoleptons for this variable

    self.out.fillBranch("nJet20", nJet20)
    self.out.fillBranch("nJet30", nJet30)
    self.out.fillBranch("nBJet20", nBJet20)
    self.out.fillBranch("nElectrons10", nElectrons10)
    self.out.fillBranch("nMuons10", nMuons10)
    self.out.fillBranch("nPFLep5LowMT", nPFLep5LowMT)
    self.out.fillBranch("nPFHad10LowMT", nPFHad10LowMT)
    self.out.fillBranch("nLepLowMT", nLepLowMT)

    ####################################################
    # HT and MHT computations, hadronic variables
    ####################################################
    mht4vec = ROOT.TLorentzVector( -1.*(sum([x.p4().Px() for x in objects_std])) , -1.*(sum([x.p4().Py() for x in objects_std])), 0, 0 )
    met4vec = ROOT.TLorentzVector()
    met4vec.SetPtEtaPhiM(met.pt, 0., met.phi, 0.)
    diffMetMht4vec = ROOT.TLorentzVector(mht4vec-met4vec)

    ht = sum([x.pt for x in objects_std]) if len(objects_std)>0 else -99
    mht_pt =  mht4vec.Pt() if len(objects_std)>0 else -99
    mht_phi = mht4vec.Phi() if len(objects_std)>0 else -99
    diffMetMht = ROOT.TMath.Sqrt( diffMetMht4vec.Px()*diffMetMht4vec.Px() + diffMetMht4vec.Py()*diffMetMht4vec.Py() ) if len(objects_std)>0 else -99
    deltaPhiMin = 999
    for n,obj in enumerate(objects_std):
      if n>3: break
      thisDeltaPhi = abs(tools.deltaPhi(obj.phi, met4vec.Phi()))
      if thisDeltaPhi < deltaPhiMin: deltaPhiMin=thisDeltaPhi
    jet1_pt = clean_jets30[0].pt if len(clean_jets30)>0 else -99
    jet2_pt = clean_jets30[1].pt if len(clean_jets30)>1 else -99

    self.out.fillBranch("ht", ht)
    self.out.fillBranch("mht_pt", mht_pt)
    self.out.fillBranch("mht_phi", mht_phi)
    self.out.fillBranch("diffMetMht", diffMetMht)
    self.out.fillBranch("deltaPhiMin", deltaPhiMin)
    self.out.fillBranch("jet1_pt", jet1_pt)
    self.out.fillBranch("jet2_pt", jet2_pt)

    ####################################################
    # MT2
    ####################################################
    mt2 = getMT2(objects_std, met4vec)
    #if len(selected_jets)>=2: print getMT2(selected_jets, metTV2 ), met.pt, len(selected_jets)
    self.out.fillBranch("mt2", mt2)

    ###################################################
    # MET computations
    ###################################################
    met_pt = met.pt
    met_phi = met.phi

    self.out.fillBranch("met_pt", met_pt)
    self.out.fillBranch("met_phi", met_phi)

    ''''# make gamma met , not including overlap removal with jets
    gamma_met = ROOT.TVector2()
    lead_gamma = ROOT.TVector2()
    # remove leading photon with given cuts
    # collections are sorted in pt - take leading photon
    gamma_met.SetMagPhi(met.pt, met.phi)
    if len(photons)>0:
      lead_gamma.SetMagPhi(photons[0].pt, photons[0].phi)
      gamma_met += lead_gamma

    self.out.fillBranch("gamma_MET_pt", gamma_met.Mod())
    self.out.fillBranch("gamma_MET_phi", gamma_met.Phi())'''

    return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

mht = lambda : mt2VarsProducer( isMC=True, year=2017 )
