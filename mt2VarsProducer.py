# This module is meant to produce all mt2Analysis-specific variables
# It will be a long code, but let's try to keep it simple and at least you won't have to search for objets defined in other packages!
# Please note the space convention rather than tab convention wrt other nanoAOD modules

# TODO: please put most numerical values in a config file

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import PhysicsTools.NanoAODTools.postprocessing.tools as tools
from PhysicsTools.NanoAODTools.postprocessing.analysis.mt2.mt2Analyzer import getMT2

def stampP(obj):
  print 'pt={:>8} eta={:>8} phi={:>8}'.format(obj.pt, obj.eta, obj.phi)

# my implementation of closest
# returns index of DeltaR-closest element in collecion wrt obj
def closest(obj,collection):
  ret = None; drMin = 999
  #print 'info in closest'
  #print obj, collection
  for i,x in enumerate(collection):
    #print stampP(obj)
    #print stampP(x)
    dr = tools.deltaR(obj,x)
    #print 'dr=',dr
    if dr < drMin:
      ret = i; drMin = dr
  return (ret,drMin)

def mtw(x1_pt, x1_phi, x2_pt, x2_phi):
  import math
  return math.sqrt(2*x1_pt*x2_pt*(1-math.cos(x1_phi-x2_phi)))

def getBitDecision(x, n): # x is an integer
  return x & 2**n != 0

def getDeltaPhiMin(objects, met4vec):
    if len(objects) == 0: return -99
    deltaPhiMin = 999
    for n,obj in enumerate(objects):
      if n>3: break
      thisDeltaPhi = abs(tools.deltaPhi(obj.phi, met4vec.Phi()))
      if thisDeltaPhi < deltaPhiMin: deltaPhiMin=thisDeltaPhi
    return deltaPhiMin

def getHt(objects):
  return sum([x.pt for x in objects]) if len(objects)>0 else -99

def getMht4vec(objects):
  if len(objects)>0:
    return ROOT.TLorentzVector( -1.*(sum([x.p4().Px() for x in objects])) , -1.*(sum([x.p4().Py() for x in objects])), 0, 0 )
  else:
    return ROOT.TLorentzVector(0, 0, 0, 0)


def passEleId(electron):
  passId = True
  if abs(electron.eta + electron.deltaEtaSC) < 1.479:
    if electron.sieie > 0.01114: passId = False
    # delta eta ieta cut
    # delta phi ieta cut
    if electron.hoe > 0.181: passId = False
    if abs(electron.eInvMinusPInv) > 0.207: passId = False
    if abs(electron.dxy) > 0.0564: passId = False
    if abs(electron.dz) > 0.472: passId = False
    if electron.lostHits > 2: passId = False
    if electron.convVeto == False: passId = False
  else:
    if electron.sieie > 0.0352: passId = False
    # delta eta ieta cut
    # delta phi ieta cut
    if electron.hoe > 0.116: passId = False
    if abs(electron.eInvMinusPInv) > 0.174: passId = False
    if abs(electron.dxy) > 0.222: rpassId = False
    if abs(electron.dz) > 0.921: passId = False
    if electron.lostHits > 3: passId = False
    if electron.convVeto == False: passId = False
  return passId

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

    #self.out.branch("evt", "L")


    self.out.branch("nJet20", "I")
    self.out.branch("nJet30", "I")
    self.out.branch("nJet30FailId", "I")
    self.out.branch("nBJet20", "I")
    self.out.branch("nElectrons10", "I")
    self.out.branch("nMuons10", "I")
    self.out.branch("nPFLep5LowMT", "I")
    self.out.branch("nPFLep5LowMTclean", "I")
    self.out.branch("nPFHad10LowMT", "I")
    self.out.branch("nLepLowMT", "I")
    self.out.branch("nRecoLepLowMT", "I")
    self.out.branch("ht", "F")
    self.out.branch("mht_pt", "F")
    self.out.branch("mht_phi", "F")
    self.out.branch("zll_ht", "F")
    self.out.branch("zll_mht_pt", "F")
    self.out.branch("zll_mht_phi", "F")
    self.out.branch("diffMetMht", "F")
    self.out.branch("deltaPhiMin", "F")
    #self.out.branch("deltaPhiMin_had", "F")
    self.out.branch("zll_diffMetMht", "F")
    self.out.branch("zll_deltaPhiMin", "F")
    self.out.branch("jet1_pt", "F")
    self.out.branch("jet2_pt", "F")
    self.out.branch("mt2", "F")
    self.out.branch("met_pt", "F")
    self.out.branch("met_phi", "F")
    self.out.branch("zll_mt2", "F")
    self.out.branch("zll_met_pt", "F")
    self.out.branch("zll_met_phi", "F")

    self.out.branch("lep_pt", "F", 1, "nLep") # TODO: understand what is the size at the end what is 1 and what is nLep ?
    self.out.branch("lep_eta", "F", 1, "nLep") # what is 1 and what is nLep ?
    self.out.branch("lep_phi", "F", 1, "nLep") # what is 1 and what is nLep ?
    self.out.branch("lep_mass", "F", 1, "nLep") # what is 1 and what is nLep ?
    self.out.branch("lep_charge", "F", 1, "nLep") # what is 1 and what is nLep ?
    self.out.branch("lep_pdgId", "F", 1, "nLep") # what is 1 and what is nLep ?
    self.out.branch("lep_dxy", "F", 1, "nLep") # what is 1 and what is nLep ?
    self.out.branch("lep_dz", "F", 1, "nLep") # what is 1 and what is nLep ?
    self.out.branch("lep_miniRelIso", "F", 1, "nLep") # what is 1 and what is nLep ?

    self.out.branch("jet_pt", "F", 1, "nJet") #
    self.out.branch("jet_eta", "F", 1, "nJet") #
    self.out.branch("jet_phi", "F", 1, "nJet")
    self.out.branch("jet_id", "I", 1, "nJet")

    self.out.branch("zll_pt", "F")
    self.out.branch("zll_eta", "F")
    self.out.branch("zll_phi", "F")
    self.out.branch("zll_mass", "F")

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
    #evt = Object(event, "event")

    #self.out.fillBranch("evt", evt)

    # Perform SELECTIONS
    selected_recoelectrons = []
    selected_recomuons = []
    selected_recoleptons = []
    selected_pfleptons = []
    selected_pfhadrons = []
    selected_jets = []
    baseline_jets = []
    baseline_jets_noId = []

    for electron in electrons:
      electron.pt /= electron.eCorr # FIXME: for the moment uncalibrated pt to match with heppy, but prefer to have it calibrated
      if electron.pt < 10: continue
      if abs(electron.eta)>2.4: continue
      #if electron.cutBased == 0: continue # does not include d0, dz, conv veto FIXME: for the moment removed electron ID
      # d0 and dz cut are not included in the id
      #https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedElectronIdentificationRun2
      if abs(electron.eta + electron.deltaEtaSC) < 1.479:
      #  if electron.dxy > 0.05: continue
      #  if electron.dz > 0.10: continue
         if electron.lostHits > 2: continue
      #else:
      #  if electron.dxy > 0.10: continue
      #  if electron.dz > 0.20: continue
         if electron.lostHits > 3: continue
      # try to use the cuts exactly how stated in the int note
      #if not passEleId(electron): continue
      if electron.miniPFRelIso_all > 0.1: continue
      electron.isToRemove = False
      selected_recoelectrons.append(electron)


    # loop to look for the low pt pf candidates
    for electron in electrons:
      if electron.pt < 5: continue
      if electron.isPFcand == False: continue # passa la pf id
      if electron.pfRelIso03_chg > 0.2: continue
      if abs(electron.dz)>0.1: continue
      if mtw(electron.pt, electron.phi, met.pt, met.phi)>100: continue
      electron.isToRemove = False
      selected_pfleptons.append(electron)

    for muon in muons:
      if muon.pt < 10: continue
      if abs(muon.eta)>2.4: continue
      #if muon.isPFcand: continue
      #print 'medium id for muon ', muon.mediumId
      #print 'tight id for muon ', muon.tightId
      #if muon.tightId == False: continue # medium working point instead of loose
      # isLooseMuon coincides with loose working point so no cut is needed in principle
      if abs(muon.dz)>0.5: continue
      if abs(muon.dxy)>0.2: continue
      if muon.miniPFRelIso_all > 0.2: continue
      muon.isToRemove = False
      selected_recomuons.append(muon)

    # loop again to recover low pt PFcandidates
    for muon in muons:
      if muon.pt < 5: continue
      if muon.isPFcand == False: continue # passa la pf id
      if muon.pfRelIso03_chg > 0.2: continue
      if abs(muon.dz)>0.1: continue
      if mtw(muon.pt, muon.phi, met.pt, met.phi)>100: continue
      muon.isToRemove = False
      selected_pfleptons.append(muon)

    # maybe some other pf candidates which failed to enter muon collection
    for it in isotracks:
      it.mass = 0.
      if not it.isPFcand: continue # consider only pfcandidates
      if mtw(it.pt, it.phi, met.pt, met.phi)>100: continue
      if abs(it.dz)>0.1: continue
      if abs(it.pdgId) == 11 or abs(it.pdgId) == 13: # muon or electron PFcandidates
        if it.pt<5: continue
        if it.pfRelIso03_chg > 0.2: continue
        it.isToRemove = False
        selected_pfleptons.append(it)
      elif abs(it.pdgId == 211):
        if it.pt<10: continue
        if it.pfRelIso03_chg > 0.1: continue
        it.isToRemove = False
        selected_pfhadrons.append(it)

    for jet in jets:
      jet.isToRemove = False
      if self.verbose:  print 'jet id tight ', getBitDecision(jet.jetId, 2)
      if jet.pt<20: continue
      if abs(jet.eta)>4.7: continue # large eta cut
      baseline_jets_noId.append(jet)
      if getBitDecision(jet.jetId, 2) == False: continue  #  bit1 is loose (always false in 2017 since it does not exist), bit2 is tight, bit3 is tightLepVeto"
      baseline_jets.append(jet)

    baseline_jets.sort(key=lambda jet: jet.pt, reverse = True)
    baseline_jets_noId.sort(key=lambda jet: jet.pt, reverse = True)
    selected_recoleptons = selected_recomuons + selected_recoelectrons


    # ##################################################
    # NOW PERFORM THE CROSS-CLEANING: stage 1
    # ##################################################
    for it in selected_pfleptons:
      (irl,dRmin) = closest(it,selected_recoleptons)
      #print 'info in cleaning ', irl, dRmin
      if irl!=None and dRmin<0.01:
        it.isToRemove = True # mark the pflepton for removal because it overlaps with a the closest selected reco lepton
        #print 'info in cleaning ', stampP(it),
        #print 'info in cleaning ', it.isToRemove

    clean_recoleptons =   selected_recoleptons
    clean_recoelectrons = selected_recoelectrons
    clean_recomuons =     selected_recomuons
    clean_recoelectrons_CR = [el for el in clean_recoelectrons] # FIXME: for the moment removed loose id requirement if el.cutBased>1] # require electrons also to be loose
    clean_recomuons_CR = clean_recomuons
    clean_recoleptons_CR = clean_recoelectrons_CR + clean_recomuons_CR
    clean_recoleptons_CR_lowMT = [x for x in clean_recoleptons_CR if mtw(x.pt, x.phi, met.pt, met.phi)<100]
    clean_pfleptons =    [x for x in selected_pfleptons if x.isToRemove == False]
    #clean_pfelectrons =  [x for x in clean_pfleptons if abs(x.pdgId) == 11]
    #clean_pfmuons =      [x for x in clean_pfleptons if abs(x.pdgId) == 13]
    clean_pfhadrons =    selected_pfhadrons
    clean_leptons =      clean_pfleptons + clean_recoleptons

    #print '************************'
    #print 'NEW EVENT'
    #print 'Size of clean leptons aka selectedIsoCleanTrack: ', len(clean_pfleptons)
    #for x in clean_pfleptons: stampP(x)

    # ##################################################
    # NOW PERFORM THE CROSS-CLEANING: stage 2, remove closest jet to lepton within given DeltaR
    # ##################################################
    for lep in clean_leptons:
      #print 'info in cleaning stage 2'
      (ijet,dRmin) = closest(lep,baseline_jets)
      #print ijet, dRmin
      if self.verbose: print ijet,dRmin
      if ijet!=None and dRmin<0.4: # mark that closest jet to a clean lepton to be removed because it overlaps with it
        baseline_jets[ijet].isToRemove = True
        #print ijet, 'is to remove', baseline_jets[ijet].isToRemove


    # repeat x-cleaning for all jets including those that pass the id # TODO: personally I think we should remove this x-cleaning
    for lep in clean_leptons:
      (ijet,dRmin) = closest(lep,baseline_jets_noId)
      if self.verbose: print ijet,dRmin
      if ijet!=None and dRmin<0.4: # mark that closest jet to a clean lepton to be removed because it overlaps with it
        baseline_jets_noId[ijet].isToRemove = True

    clean_jets20_largeEta = [jet for jet in baseline_jets if jet.isToRemove == False]
    clean_jets30_largeEta = [jet for jet in baseline_jets if jet.isToRemove == False and jet.pt > 30]
    clean_jets40_largeEta = [jet for jet in baseline_jets if jet.isToRemove == False and jet.pt > 40]
    clean_jets30_largeEta_FailId =   [jet for jet in baseline_jets_noId if jet.isToRemove == False and jet.pt > 30 and getBitDecision(jet.jetId, 2) == False]
    clean_jets20 =          [jet for jet in baseline_jets if jet.isToRemove == False and abs(jet.eta) < 2.4 ] # TODO: check 2.5 heppy
    clean_jets30 =          [jet for jet in baseline_jets if jet.isToRemove == False and jet.pt > 30 and abs(jet.eta) < 2.4] # TODO: check 2.5 heppy
    clean_bjets20 =         [jet for jet in clean_jets20 if jet.btagCSVV2 > 0.8838]

    objects_std =            clean_jets30 + clean_leptons
    objects_std_deltaPhi =   clean_jets30_largeEta + clean_leptons
    zll_objects_std =        clean_jets30
    zll_objects_deltaPhi =   clean_jets30_largeEta

    ####
    # Additional sorting should happen here
    #objects_std.sort(key=lambda obj: obj.pt, reverse = True)
    objects_std_deltaPhi.sort(key=lambda obj: obj.pt, reverse = True)
    clean_jets40_largeEta.sort(key=lambda obj: obj.pt, reverse = True)
    clean_jets30.sort(key=lambda obj: obj.pt, reverse = True)
    #zll_objects_std.sort(key=lambda obj: obj.pt, reverse = True)

    # ##################################################
    # Now you're ready to count objects
    # ##################################################
    nJet20 = len(clean_jets20)
    nJet30 = len(clean_jets30)
    nBJet20 = len(clean_bjets20)
    nJet30FailId = len(clean_jets30_largeEta_FailId)
    nElectrons10 = len(selected_recoelectrons) # for vetoing I do not care about x-cleaning
    nMuons10 = len(selected_recomuons) # for vetoing I do not care about x-cleaning
    nPFLep5LowMT = len(selected_pfleptons) # for vetoing I do not care about x-cleaning
    nPFLep5LowMTclean = len(clean_pfleptons)
    nPFHad10LowMT = len(selected_pfhadrons) # for vetoing I do not care about x-cleaning
    nLepLowMT = len(clean_recoleptons_CR_lowMT) + len(clean_pfleptons)
    nRecoLepLowMT = len(clean_recoleptons_CR_lowMT)

    self.out.fillBranch("nJet20", nJet20)
    self.out.fillBranch("nJet30", nJet30)
    self.out.fillBranch("nJet30FailId", nJet30FailId)
    self.out.fillBranch("nBJet20", nBJet20)
    self.out.fillBranch("nElectrons10", nElectrons10)
    self.out.fillBranch("nMuons10", nMuons10)
    self.out.fillBranch("nPFLep5LowMT", nPFLep5LowMT)
    self.out.fillBranch("nPFLep5LowMTclean", nPFLep5LowMTclean)
    self.out.fillBranch("nPFHad10LowMT", nPFHad10LowMT)
    self.out.fillBranch("nLepLowMT", nLepLowMT)
    self.out.fillBranch("nRecoLepLowMT", nRecoLepLowMT)

    ###################################################
    # MET computations
    ###################################################
    # NB: convention for all zll-removed variables of the outputtree
    # (i.e. variables involving with prefix zll AND involving met in the computation):
    #if len(clean_recoleptons)!=2 they must be set to -99

    met4vec = ROOT.TLorentzVector()
    met4vec.SetPtEtaPhiM(met.pt, 0., met.phi, 0.)
    met_pt = met.pt
    met_phi = met.phi

    # zll met # I want it to be always defined
    zll_met4vec = ROOT.TLorentzVector(met4vec)
    zll_met_pt = -99
    zll_met_phi = -99
    if len(clean_recoleptons)==2:
      px = met4vec.Px() + clean_recoleptons[0].p4().Px() + clean_recoleptons[1].p4().Px()
      py = met4vec.Py() + clean_recoleptons[0].p4().Py() + clean_recoleptons[1].p4().Py()
      zll_met4vec = ROOT.TLorentzVector(px, py, 0, 0)
      zll_met_pt = zll_met4vec.Pt()
      zll_met_phi = zll_met4vec.Phi()

    self.out.fillBranch("met_pt", met_pt)
    self.out.fillBranch("met_phi", met_phi)
    self.out.fillBranch("zll_met_pt", zll_met_pt)
    self.out.fillBranch("zll_met_phi", zll_met_phi)

    ####################################################
    # HT and MHT computations, hadronic variables
    ####################################################
    # Ht
    ht =      getHt(objects_std)
    zll_ht =  getHt(zll_objects_std) if len(clean_recoleptons)==2 else -99 # I don't like this initialization, but that's life

    # Mht
    mht4vec = getMht4vec(objects_std)
    mht_pt =  mht4vec.Pt() if len(objects_std)>0 else -99
    mht_phi = mht4vec.Phi() if len(objects_std)>0 else -99
    zll_mht4vec = getMht4vec(zll_objects_std)
    #zll_mht_pt = mht_pt if len(clean_recoleptons)==2 else -99
    #zll_mht_phi = mht_phi if len(clean_recoleptons)==2 else -99
    zll_mht_pt = zll_mht4vec.Pt() if len(clean_recoleptons)==2 else -99
    zll_mht_phi = zll_mht4vec.Phi() if len(clean_recoleptons)==2 else -99

    # Diff MET MHT
    diffMetMht4vec = ROOT.TLorentzVector(mht4vec-met4vec)
    zll_diffMetMht4vec = ROOT.TLorentzVector(zll_mht4vec-zll_met4vec)

    diffMetMht =     ROOT.TMath.Sqrt( diffMetMht4vec.Px()*diffMetMht4vec.Px()         + diffMetMht4vec.Py()*diffMetMht4vec.Py() )         if len(objects_std)>0 else -99
    zll_diffMetMht = ROOT.TMath.Sqrt( zll_diffMetMht4vec.Px()*zll_diffMetMht4vec.Px() + zll_diffMetMht4vec.Py()*zll_diffMetMht4vec.Py() ) if len(zll_objects_std)>0 and len(clean_recoleptons)==2 else -99

    # DeltaPhi
    deltaPhiMin = getDeltaPhiMin(objects_std_deltaPhi, met4vec)
    #deltaPhiMin_had = getDeltaPhiMin(clean_jets40_largeEta, met4vec)
    zll_deltaPhiMin = getDeltaPhiMin(zll_objects_deltaPhi, zll_met4vec) if len(clean_recoleptons)==2 else -99

    jet1_pt = clean_jets20[0].pt if len(clean_jets20)>0 else -99 # for a reson that only the MINDS of the previous MT2 analysis can understand, these jets start from pt > 20 GeV : FUCK YOU!
    jet2_pt = clean_jets20[1].pt if len(clean_jets20)>1 else -99 # same goes for the second leading jet pt

    self.out.fillBranch("ht", ht)
    self.out.fillBranch("mht_pt", mht_pt)
    self.out.fillBranch("mht_phi", mht_phi)
    self.out.fillBranch("zll_ht", zll_ht)
    self.out.fillBranch("zll_mht_pt", zll_mht_pt)
    self.out.fillBranch("zll_mht_phi", zll_mht_phi)
    self.out.fillBranch("diffMetMht", diffMetMht)
    self.out.fillBranch("deltaPhiMin", deltaPhiMin)
    #self.out.fillBranch("deltaPhiMin_had", deltaPhiMin_had)
    self.out.fillBranch("zll_diffMetMht", zll_diffMetMht)
    self.out.fillBranch("zll_deltaPhiMin", zll_deltaPhiMin)
    self.out.fillBranch("jet1_pt", jet1_pt)
    self.out.fillBranch("jet2_pt", jet2_pt)


    ####################################################
    # MT2
    ####################################################
    mt2 = getMT2(objects_std, met4vec)
    zll_mt2 = getMT2(zll_objects_std, zll_met4vec) if len(clean_recoleptons)==2 else -99
    #if len(selected_jets)>=2: print getMT2(selected_jets, metTV2 ), met.pt, len(selected_jets)
    self.out.fillBranch("mt2", mt2)
    self.out.fillBranch("zll_mt2", zll_mt2)


    ####################################################
    # Lepton quantities
    ####################################################
    # save quantities of the various cleaned electrons and muons
    # with the naming as in https://twiki.cern.ch/twiki/bin/view/SusyMECCA/BabyTrees
    # all these quantities are arrays of floats (sic!), not std::vectors<float>

    lep_pt  = [-99.]*len(clean_recoleptons)
    lep_eta = [-99.]*len(clean_recoleptons)
    lep_phi =  [-99.]*len(clean_recoleptons)
    lep_mass = [-99.]*len(clean_recoleptons)
    lep_charge = [-99.]*len(clean_recoleptons)
    lep_pdgId = [-99.]*len(clean_recoleptons)
    lep_dxy = [-99.]*len(clean_recoleptons)
    lep_dz = [-99.]*len(clean_recoleptons)
    lep_miniRelIso = [-99.]*len(clean_recoleptons)
    # and this goes for the other variables

    for i,ilep in enumerate(clean_recoleptons):
      lep_pt[i] = ilep.pt
      lep_eta[i] = ilep.eta
      lep_phi[i] = ilep.phi
      lep_mass[i] = ilep.mass
      lep_charge[i] = ilep.charge
      lep_pdgId[i] = ilep.pdgId
      lep_dxy[i] = ilep.dxy
      lep_dz[i] = ilep.dz
      lep_miniRelIso[i] = ilep.miniPFRelIso_all
      #[i] = ilep.


    self.out.fillBranch("lep_pt", lep_pt)
    self.out.fillBranch("lep_eta", lep_eta)
    self.out.fillBranch("lep_phi", lep_phi)
    self.out.fillBranch("lep_mass", lep_mass)
    self.out.fillBranch("lep_charge", lep_charge)
    self.out.fillBranch("lep_pdgId", lep_pdgId)
    self.out.fillBranch("lep_dxy", lep_dxy)
    self.out.fillBranch("lep_dz", lep_dz)
    #self.out.fillBranch("lep_tightId", lep_tightId)
    self.out.fillBranch("lep_miniRelIso", lep_miniRelIso)
    #self.out.fillBranch("lep_mcMatchId", lep_mcMatchId)
    #self.out.fillBranch("lep_lostHits", lep_lostHits)
    #self.out.fillBranch("lep_convVeto", lep_convVeto)
    #self.out.fillBranch("lep_tightCharge", lep_tightCharge)
    # variables for ele id (?)


    ####################################################
    # Clean jets
    ###################################################
    jet_pt  = [-99.]*len(clean_jets20_largeEta)
    jet_eta = [-99.]*len(clean_jets20_largeEta)
    jet_phi =  [-99.]*len(clean_jets20_largeEta)
    jet_id = [-99.]*len(clean_jets20_largeEta)

    for i,ijet in enumerate(clean_jets20_largeEta):
      jet_pt[i] = ijet.pt
      jet_phi[i] = ijet.phi
      jet_eta[i] = ijet.eta
      jet_id[i] = int(getBitDecision(ijet.jetId, 2)) #getJetID(ijet)

    self.out.fillBranch("jet_pt", jet_pt)
    self.out.fillBranch("jet_eta", jet_eta)
    self.out.fillBranch("jet_phi", jet_phi)
    self.out.fillBranch("jet_id", jet_id)

    #####
    # Zll
    ######
    zll4vec = ROOT.TLorentzVector(0, 0, 0, 0)
    for ilep in clean_recoleptons:
      zll4vec += ilep.p4()
    zll_pt = zll4vec.Pt() if len(clean_recoleptons)==2 else -99
    zll_eta = zll4vec.Eta() if len(clean_recoleptons)==2 else -99
    zll_phi = zll4vec.Phi() if len(clean_recoleptons)==2 else -99
    zll_mass = zll4vec.M() if len(clean_recoleptons)==2 else -99

    self.out.fillBranch("zll_pt", zll_pt)
    self.out.fillBranch("zll_eta", zll_eta)
    self.out.fillBranch("zll_phi", zll_phi)
    self.out.fillBranch("zll_mass", zll_mass)


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
