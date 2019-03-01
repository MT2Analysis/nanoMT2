# mt2VarsProducer.py - Maria Giulia Ratti, ETH Zurich

# This module is meant to produce all mt2Analysis-specific variables and to perform skimming based on them
# It will be a long code, but let's try to keep it simple
# Please note the space convention rather than tab convention wrt other nanoAOD modules

# NOTE: not possible to separate skimming from variables production because the branches are filled in this very same module
# NOTE: this module implicitly shares the naming conventions defined in PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties
#       this is bad, but unfortunately there is no better way to do this, unless I have time to rewrite the jetmet module to suit my needs
# TODO: please put most numerical values in a config file
# TODO: add some truth information

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import os

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import PhysicsTools.NanoAODTools.postprocessing.tools as tools
from PhysicsTools.NanoAODTools.postprocessing.analysis.mt2.mt2Analyzer import getMT2
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.JetReCalibrator import JetReCalibrator

import electronIdUtils as eleUtils
import jetIdUtils as jetUtils

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

class mt2VarsProducer(Module):
  def __init__(self, isMC=True, isSignal=False, year=2017, doSkim=False, doSyst=False, systVar=None, redoJEC2018=False): # 'jesTotalUp', 'jesTotalDown'
    self.year = year
    self.isMC = isMC
    self.isSignal = isSignal
    self.doSkim = doSkim
    self.doSyst = doSyst
    self.systVar = systVar
    self.systSuffix = '_sys_' + self.systVar if self.doSyst else ''
    self.redoJEC2018 = redoJEC2018
    self.writeHistFile=True # needed to make the postprocessor write to output hist file

    # possible year-dependent configurations
    if self.year == 2016:
      self.eleIdTune = 'Spring15'
      self.eleVIDMapName = 'vidNestedWPBitmapSpring15'
      #self.cut_btagWP =  0.8484 # medium WP for 80X csvv2
      self.cut_btagWP = 0.6324 # medium WP for 80X deepcsv
      self.jetIdCustomLevel = 1 # loose
    elif self.year == 2017: 
      self.eleIdTune = 'Fall17V2'
      self.eleVIDMapName = 'vidNestedWPBitmap'
      #self.cut_btagWP =  0.8838 # medium WP for 94X csvv2
      self.cut_btagWP =  0.4941 # medium WP for 94X deepcsv
      self.jetIdCustomLevel = 3 # tight
    elif self.year == 2018:
      self.eleIdTune = 'Fall17V2'
      self.eleVIDMapName = 'vidNestedWPBitmap'
      self.cut_btagWP = 0.4941  # FIXME 
      self.jetIdCustomLevel = 3 # tight

    # configure jet recalibrator
    # JEC recommendation --> https://twiki.cern.ch/twiki/bin/viewauth/CMS/JECDataMC
    if self.redoJEC2018:
      self.jetReCalibrator = JetReCalibrator( 
                                  globalTag="Fall17_17Nov2017_V32_MC", # Fall17_17Nov2017_V32_MC Autumn18_V3_MC 
                                  jetFlavour="AK4PFchs", # poor choice of the term "flavour" in this context!
                                  doResidualJECs=True, # residuals for 2018 data not available yet
                                  jecPath=os.environ['CMSSW_BASE']+"/src/PhysicsTools/NanoAODTools/data/jme/", 
                                  upToLevel=3,
                                  calculateSeparateCorrections = True,  # Needed for T1 MET corrections
                                  calculateType1METCorrection  = False, # True is not supported currently
                                  type1METParams={'jetPtThreshold':15., 'skipEMfractionThreshold':0.9, 'skipMuons':True} # these are the defaults, as 13 TeV MET paper 
                             ) 

  def beginJob(self,histFile,histDirName):
    Module.beginJob(self,histFile,histDirName) # this line is crucial
    self.hEta=ROOT.TH2F('hEta','hEta',50,-5.,5.,50,0.,50.)
    self.hPt= ROOT.TH2F('hPt' ,'hPt' ,50,15.,1265,50,0.,50.)
    self.addObject(self.hEta )
    self.addObject(self.hPt )
  def endJob(self):
    Module.endJob(self)
  def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    self.verbose = False
    self.out = wrappedOutputTree

    self.out.branch("lumi", "I")
    self.out.branch("evt", "L")
    self.out.branch("nJet20{}".format(self.systSuffix), "I")
    self.out.branch("nJet30{}".format(self.systSuffix), "I")
    self.out.branch("nJet30FailId{}".format(self.systSuffix), "I")
    self.out.branch("nJet15HEMFail{}".format(self.systSuffix), "I")
    self.out.branch("nJet30HEMFail{}".format(self.systSuffix), "I")
    self.out.branch("nBJet20{}".format(self.systSuffix), "I")
    self.out.branch("nElectrons10{}".format(self.systSuffix), "I")
    self.out.branch("nMuons10{}".format(self.systSuffix), "I")
    self.out.branch("nPFLep5LowMT{}".format(self.systSuffix), "I")
    self.out.branch("nPFLep5LowMTclean{}".format(self.systSuffix), "I")
    self.out.branch("nPFHad10LowMT{}".format(self.systSuffix), "I")
    self.out.branch("nLepLowMT{}".format(self.systSuffix), "I")
    self.out.branch("nLepHighMT{}".format(self.systSuffix), "I")
    self.out.branch("nRecoLepLowMT{}".format(self.systSuffix), "I")
    self.out.branch("ht{}".format(self.systSuffix), "F")
    self.out.branch("mht_pt{}".format(self.systSuffix), "F")
    self.out.branch("mht_phi{}".format(self.systSuffix), "F")
    self.out.branch("zll_ht{}".format(self.systSuffix), "F")
    self.out.branch("zll_mht_pt{}".format(self.systSuffix), "F")
    self.out.branch("zll_mht_phi{}".format(self.systSuffix), "F")
    self.out.branch("diffMetMht{}".format(self.systSuffix), "F")
    self.out.branch("deltaPhiMin{}".format(self.systSuffix), "F")
    #self.out.branch("deltaPhiMin_had", "F")
    self.out.branch("zll_diffMetMht{}".format(self.systSuffix), "F")
    self.out.branch("zll_deltaPhiMin{}".format(self.systSuffix), "F")
    self.out.branch("jet1_pt{}".format(self.systSuffix), "F")
    self.out.branch("jet2_pt{}".format(self.systSuffix), "F")
    self.out.branch("mt2{}".format(self.systSuffix), "F")
    self.out.branch("met_pt{}".format(self.systSuffix), "F")
    self.out.branch("met_phi{}".format(self.systSuffix), "F")
    self.out.branch("zll_mt2{}".format(self.systSuffix), "F")
    self.out.branch("zll_met_pt{}".format(self.systSuffix), "F")
    self.out.branch("zll_met_phi{}".format(self.systSuffix), "F")

    # vector variables
    self.out.branch("lep_pt{}".format(self.systSuffix), "F", 1, "nLep") # 
    self.out.branch("lep_eta{}".format(self.systSuffix), "F", 1, "nLep") # 
    self.out.branch("lep_phi{}".format(self.systSuffix), "F", 1, "nLep") # 
    self.out.branch("lep_mass{}".format(self.systSuffix), "F", 1, "nLep") # 
    self.out.branch("lep_charge{}".format(self.systSuffix), "F", 1, "nLep") # 
    self.out.branch("lep_pdgId{}".format(self.systSuffix), "F", 1, "nLep") # 
    self.out.branch("lep_dxy{}".format(self.systSuffix), "F", 1, "nLep") #
    self.out.branch("lep_dz{}".format(self.systSuffix), "F", 1, "nLep") # 
    self.out.branch("lep_id{}".format(self.systSuffix), "I", 1, "nLep") # 
    self.out.branch("lep_miniRelIso{}".format(self.systSuffix), "F", 1, "nLep") # 
    self.out.branch("lep_mtw{}".format(self.systSuffix), "F", 1, "nLep") # 

    self.out.branch("isoTrack_pt".format(self.systSuffix), "F", 1, "nIt") #
    self.out.branch("isoTrack_eta".format(self.systSuffix), "F", 1, "nIt") #
    self.out.branch("isoTrack_phi".format(self.systSuffix), "F", 1, "nIt") #
    self.out.branch("isoTrack_mass".format(self.systSuffix), "F", 1, "nIt") #
    self.out.branch("isoTrack_dz".format(self.systSuffix), "F", 1, "nIt") #
    self.out.branch("isoTrack_dxy".format(self.systSuffix), "F", 1, "nIt") #
    self.out.branch("isoTrack_pdgId".format(self.systSuffix), "F", 1, "nIt") #
    self.out.branch("isoTrack_absIso".format(self.systSuffix), "F", 1, "nIt") #
    self.out.branch("isoTrack_miniPFRelIso_chg".format(self.systSuffix), "F", 1, "nIt") #
    self.out.branch("isoTrack_mtw".format(self.systSuffix), "F", 1, "nIt") #
    
    self.out.branch("jet_pt{}".format(self.systSuffix), "F", 1, "nJet") #
    self.out.branch("jet_eta{}".format(self.systSuffix), "F", 1, "nJet") #
    self.out.branch("jet_phi{}".format(self.systSuffix), "F", 1, "nJet")
    self.out.branch("jet_id{}".format(self.systSuffix), "I", 1, "nJet")
    self.out.branch("jet_mcFlavour{}".format(self.systSuffix), "I", 1, "nJet")
    self.out.branch("jet_btagCSV{}".format(self.systSuffix), "F", 1, "nJet")
    self.out.branch("jet_btagDeepCSV{}".format(self.systSuffix), "F", 1, "nJet")

    self.out.branch("zll_pt{}".format(self.systSuffix), "F")
    self.out.branch("zll_eta{}".format(self.systSuffix), "F")
    self.out.branch("zll_phi{}".format(self.systSuffix), "F")
    self.out.branch("zll_mass{}".format(self.systSuffix), "F")
    
  def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    pass
  def analyze(self, event):
    """process event, return True (go to next module) or False (fail, go to next event)"""

    ret = True

    electrons = Collection(event, "Electron")
    muons = Collection(event, "Muon")
    jets = Collection(event, "Jet")
    photons = Collection(event, "Photon")
    if self.year==2017:
      met = Object(event, "METFixEE2017")
    else:
      met = Object(event, "MET")
    if self.verbose: print 'MET is:', met.pt, met.phi
    njets = len(jets)
    isotracks = Collection(event, "IsoTrack")

    # access variated quantities
    # and modify the collections with syst variations if needed
    if self.doSyst:
      var_jet_pts = getattr(event, "Jet_pt_{}".format(self.systVar), None)
      var_met_pt = getattr(event, "MET_pt_{}".format(self.systVar), None)
      var_met_phi = getattr(event, "MET_phi_{}".format(self.systVar), None)

      if var_jet_pts:
        for i,jet in enumerate(jets):
          jet.pt = var_jet_pts[i]
      else: print 'ERROR: jet pts with variation {} not available, using the nominal value'.format(self.systVar)

      if var_met_pt:
        met.pt = var_met_pt
      else: print 'ERROR: MET pt with variation {} not available, using the nominal value'.format(self.systVar)
      if var_met_phi:
        met.phi = var_met_phi
      else: print 'ERROR: MET phi with variation {} not available, using the nominal value'.format(self.systVar)
    # from now on, met.pt, met.phi and jet.pt are variated

    # Perform SELECTIONS
    selected_recoelectrons = []
    selected_recomuons = []
    selected_recoleptons = []
    selected_pfleptons = []
    selected_pfhadrons = []
    selected_jets = []
    baseline_jets = []
    baseline_jets_noId = []

    selected_isoTracks_SnTCompatible = [] 

    for electron in electrons:
      electron.mtw = mtw(electron.pt, electron.phi, met.pt, met.phi)
      if self.year==2017 or self.year==2016: electron.pt /= electron.eCorr # want uncalibrated electron pt to avoid systematics 
      if electron.pt < 10: continue
      if abs(electron.eta)>2.4: continue
      #electron.cutBasedNoIso = eleUtils.getIdLevelNoIso(bitmap=electron.vidNestedWPBitmap, tune=self.eleIdTune)
      if self.verbose: print 'eleVIDmap=', getattr(electron, self.eleVIDMapName)
      electron.cutBasedNoIso = eleUtils.getIdLevelNoIso(bitmap=getattr(electron, self.eleVIDMapName), tune=self.eleIdTune)
      if electron.cutBasedNoIso == 0: continue # iso, d0 and dz cut not included in id, so need to be applied below
      #if electron.cutBased == 0: continue # does not include d0, dz, conv veto
      # d0 and dz cut are not included in the id
      #https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedElectronIdentificationRun2
      if abs(electron.eta + electron.deltaEtaSC) < 1.479:
        if electron.dxy > 0.05: continue 
        if electron.dz > 0.10: continue 
        #if electron.lostHits > 2: continue # included in id 
      else:
        if electron.dxy > 0.10: continue 
        if electron.dz > 0.20: continue 
        #if electron.lostHits > 3: continue # included in id 

      if electron.miniPFRelIso_all > 0.1: continue # is cut
      electron.isToRemove = False
      selected_recoelectrons.append(electron)


    # loop to look for the low pt pf candidates
    for electron in electrons:
      if electron.pt < 5: continue
      if abs(electron.eta)>2.4: continue
      if electron.isPFcand == False: continue # passa la pf id
      #if electron.isFromLostTrack: continue 
      #if electron.fromPV <= 1: continue 
      if electron.pfRelIso03_chg*electron.pt > min(0.2*electron.pt,8): continue
      if abs(electron.dxy) > 0.2: continue
      if abs(electron.dz) > 0.1: continue
      selected_isoTracks_SnTCompatible.append(electron)
      if electron.mtw>100: continue
      if electron.pfRelIso03_chg > 0.2: continue
      electron.isToRemove = False
      selected_pfleptons.append(electron)

    for muon in muons:
      muon.mtw = mtw(muon.pt, muon.phi, met.pt, met.phi)
      if muon.pt < 10: continue
      if abs(muon.eta)>2.4: continue
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
      if abs(muon.eta)>2.4: continue
      if muon.isPFcand == False: continue # passa la pf id
      #if muon.isFromLostTrack: continue
      #if muon.fromPV <= 1: continue 
      if muon.pfRelIso03_chg*muon.pt > min(0.2*muon.pt,8): continue
      if abs(muon.dxy) > 0.2: continue
      if abs(muon.dz) > 0.1: continue
      selected_isoTracks_SnTCompatible.append(muon)
      if muon.mtw>100: continue
      if muon.pfRelIso03_chg > 0.2: continue
      muon.isToRemove = False
      selected_pfleptons.append(muon)

    # maybe some other pf candidates which failed to enter muon collection
    for it in isotracks:
      it.mass = 0.
      it.mtw = mtw(it.pt, it.phi, met.pt, met.phi)
      if abs(it.eta) > 2.4: continue 
      if not it.isPFcand: continue # consider only pfcandidates
      if it.isFromLostTrack: continue 
      if it.fromPV <= 1: continue 
      if abs(it.dxy) > 0.2: continue
      if abs(it.dz) > 0.1: continue
      if abs(it.pdgId) == 11 or abs(it.pdgId) == 13: # muon or electron PFcandidates
        if it.pt<5: continue
        if it.pfRelIso03_chg*it.pt > min(0.2*it.pt,8): continue
        selected_isoTracks_SnTCompatible.append(it)
        if it.mtw>100: continue
        if it.pfRelIso03_chg > 0.2: continue
        it.isToRemove = False
        selected_pfleptons.append(it)
      elif abs(it.pdgId) == 211:
        if it.pt<5: continue # this is actually not effective, since in the nanoAOD only pion tracks with pt>10 GeV are stored
        if it.pfRelIso03_chg*it.pt > min(0.2*it.pt,8): continue
        selected_isoTracks_SnTCompatible.append(it)
        if it.mtw>100: continue
        if it.pfRelIso03_chg > 0.1: continue
        if it.pt<10: continue
        it.isToRemove = False
        selected_pfhadrons.append(it)

    for jet in jets:
      jet.isToRemove = False

      # rewrite over jet pt with re-corrected jet pt based on new JECs 
      if self.redoJEC2018 and self.year==2018 or self.year==2017:
        newJetPt = self.jetReCalibrator.correct(
                    jet=jet,
                    rho=event.fixedGridRhoFastjetAll, # rho from all PF Candidates, used e.g. for JECs
                    delta=0, # DO not put to higher values unless you know what you're doing
                    addCorr=False, # currently only supported option
                    addShifts=False, # syst shift, currently set to 0
                    metShift=[0,0] # currently set to 0
                   ) 
        #print 'DEBUG: jet pt recalibration, old={:.2f} new={:.2f} eta={:.1f} new/old-1={:.2f}'.format(jet.pt,newJetPt,jet.eta,newJetPt/jet.pt-1)
        self.hEta.Fill(jet.eta,(newJetPt/jet.pt-1)*100)
        self.hPt.Fill(jet.pt,(newJetPt/jet.pt-1)*100)
      # define a customId coherently with previous analysis 
      jet.customId = jetUtils.getCustomId(jetId=jet.jetId, jetChHadFrac=jet.chHEF, jetNeuHadFrac=jet.neHEF, jetNeuEMFrac=jet.neEmEF, jetEta=jet.eta)
      if self.verbose:  print 'jet custom id level ', jet.customId
      if jet.pt<20: continue
      if abs(jet.eta)>4.7: continue # large eta cut
      baseline_jets_noId.append(jet)
      if jet.customId < self.jetIdCustomLevel: continue # #
      baseline_jets.append(jet)

    baseline_jets.sort(key=lambda jet: jet.pt, reverse = True)
    baseline_jets_noId.sort(key=lambda jet: jet.pt, reverse = True)
    selected_recoleptons = selected_recomuons + selected_recoelectrons
    selected_recoleptons.sort(key=lambda lep: lep.pt, reverse = True)
    selected_isoTracks_SnTCompatible.sort(key=lambda it: it.pt, reverse = True)

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
    clean_recoleptons_CR = [x for x in clean_recoleptons if (abs(x.pdgId)==13 or (abs(x.pdgId)==11 and x.cutBasedNoIso>1))]
    clean_pfleptons =    [x for x in selected_pfleptons if x.isToRemove == False]
    clean_pfhadrons =    selected_pfhadrons
    clean_leptons =      clean_pfleptons + clean_recoleptons
    
    clean_recoleptons_CR_lowMT = []
    clean_recoleptons_CR_highMT = []
    for i,x in enumerate(clean_recoleptons_CR):
      if x.mtw<100: clean_recoleptons_CR_lowMT.append(x)
      else:  clean_recoleptons_CR_highMT.append(x)

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
    clean_jets30_largeEta_FailId =   [jet for jet in baseline_jets_noId if jet.isToRemove == False and jet.pt > 30 and jet.customId < self.jetIdCustomLevel]
    clean_jets20 =          [jet for jet in baseline_jets if jet.isToRemove == False and abs(jet.eta) < 2.4 ] #
    clean_jets30 =          [jet for jet in baseline_jets if jet.isToRemove == False and jet.pt > 30 and abs(jet.eta) < 2.4]
    #clean_bjets20 =         [jet for jet in clean_jets20 if jet.btagCSVV2 > self.cut_btagWP] # Medium WP 
    clean_bjets20 =         [jet for jet in clean_jets20 if jet.btagDeepB > self.cut_btagWP] # Medium WP deep csv
    jets_HEMfail =          [jet for jet in jets if jet.eta > -3 and jet.eta < -1.4 and jet.phi > -1.57 and jet.phi < -0.87]

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
    nJet15HEMFail = len( [jet for jet in jets_HEMfail if jet.pt > 15] ) # for rejecting events with jets in HEM failure region (2018)
    nJet30HEMFail = len( [jet for jet in jets_HEMfail if jet.pt > 30] )
    nElectrons10 = len(selected_recoelectrons) # for vetoing I do not care about x-cleaning
    nMuons10 = len(selected_recomuons) # for vetoing I do not care about x-cleaning
    nPFLep5LowMT = len(selected_pfleptons) # for vetoing I do not care about x-cleaning
    nPFLep5LowMTclean = len(clean_pfleptons)
    nPFHad10LowMT = len(clean_pfhadrons) # 
    nLepLowMT = len(clean_recoleptons_CR_lowMT) + len(clean_pfleptons)
    nLepHighMT = len(clean_recoleptons_CR_highMT)
    nRecoLepLowMT = len(clean_recoleptons_CR_lowMT)


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


    ####################################################
    # MT2
    ####################################################
    mt2 = getMT2(objects_std, met4vec)
    zll_mt2 = getMT2(zll_objects_std, zll_met4vec) if len(clean_recoleptons)==2 else -99
    #if len(selected_jets)>=2: print getMT2(selected_jets, metTV2 ), met.pt, len(selected_jets)

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
    lep_id = [-99]*len(clean_recoleptons)
    lep_miniRelIso = [-99.]*len(clean_recoleptons)
    lep_mtw = [-99.]*len(clean_recoleptons)
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
      lep_id[i] = int(ilep.mediumId) + int(ilep.tightId) if abs(ilep.pdgId)==13 else ilep.cutBasedNoIso
      # muons: 0 -> default id, 1 -> mediumId, 2 -> tightId
      # electrons: 0 -> fail, 1 -> veto, 2 -> loose, 2 -> medium, 3 -> tight
      lep_miniRelIso[i] = ilep.miniPFRelIso_all
      lep_mtw[i] = ilep.mtw

    ####################################################
    # Pf Leptons isolated + charged PF hadrons isolated + any remaining isolated tracks
    ###################################################
    isoTrack_pt = [-99.]*len(selected_isoTracks_SnTCompatible)
    isoTrack_eta = [-99.]*len(selected_isoTracks_SnTCompatible)
    isoTrack_phi = [-99.]*len(selected_isoTracks_SnTCompatible)
    isoTrack_mass = [-99.]*len(selected_isoTracks_SnTCompatible)
    isoTrack_dz = [-99.]*len(selected_isoTracks_SnTCompatible)
    isoTrack_dxy = [-99.]*len(selected_isoTracks_SnTCompatible)
    isoTrack_pdgId = [-99.]*len(selected_isoTracks_SnTCompatible)
    isoTrack_absIso = [-99.]*len(selected_isoTracks_SnTCompatible)
    isoTrack_miniPFRelIso_chg = [-99.]*len(selected_isoTracks_SnTCompatible)
    isoTrack_mtw = [-99.]*len(selected_isoTracks_SnTCompatible)

    for i,it in enumerate(selected_isoTracks_SnTCompatible):
      isoTrack_pt[i] = it.pt
      isoTrack_eta[i] = it.eta
      isoTrack_phi[i] = it.phi
      isoTrack_mass[i] = it.mass
      isoTrack_dz[i] = it.dz
      isoTrack_dxy[i] = it.dxy                         
      isoTrack_pdgId[i] = it.pdgId
      isoTrack_absIso[i] = it.pfRelIso03_chg*it.pt
      isoTrack_miniPFRelIso_chg[i] = it.miniPFRelIso_chg*it.pt
      isoTrack_mtw[i] = it.mtw

    ####################################################
    # Clean jets
    ###################################################
    jet_pt  = [-99.]*len(clean_jets20_largeEta)
    jet_eta = [-99.]*len(clean_jets20_largeEta)
    jet_phi =  [-99.]*len(clean_jets20_largeEta)
    jet_id = [-99.]*len(clean_jets20_largeEta)
    jet_mcFlavour = [-99]*len(clean_jets20_largeEta)
    jet_btagCSV = [-99.]*len(clean_jets20_largeEta)
    jet_btagDeepCSV = [-99.]*len(clean_jets20_largeEta)

    for i,ijet in enumerate(clean_jets20_largeEta):
      jet_pt[i] = ijet.pt
      jet_phi[i] = ijet.phi
      jet_eta[i] = ijet.eta
      jet_id[i] = ijet.customId 
      jet_btagCSV[i] = ijet.btagCSVV2
      jet_btagDeepCSV[i] = ijet.btagDeepB
      if self.isMC: 
        jet_mcFlavour[i] = ijet.hadronFlavour


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


    ####################################################
    # Skimming
    ###################################################
    doSkim = self.doSkim
    passSkim = False

    signalSkim = (   (  ht > 200 and nJet30 >= 1 and ((nJet30>=2 and mt2>200.) or nJet30==1)  )  and  (  (ht<1000. and met_pt>200.) or (ht>1000 and  met_pt>30)  )   )
    zllSkim =    ( zll_ht > 200. and nJet30 >= 1 and ((nJet30==1 and zll_ht>200.) or (nJet30>1  and zll_mt2>200.)) and ((zll_ht<1000. and zll_met_pt>200.) or (zll_ht>1000 and  zll_met_pt>30)) )
    nlep = nElectrons10 + nMuons10 + nPFLep5LowMT + nPFHad10LowMT
    qcdSkim =    ( (nJet30>1 and nlep==0 and met_pt > 30. and  (diffMetMht < 0.5*met_pt) and mt2>50. ) or  (nJet30==2 and met_pt>200. and ht>200. and nlep==0 and diffMetMht < 0.5*met_pt and deltaPhiMin<0.3) )

    passSkim = signalSkim or zllSkim or qcdSkim # for the moment not running gammaSkim
    ####################################################
    # Fill the tree if needed
    ###################################################
    if(passSkim or not doSkim):
      self.out.fillBranch("lumi", event.luminosityBlock)
      self.out.fillBranch("evt", event.event)
      self.out.fillBranch("nJet20{}".format(self.systSuffix), nJet20)
      self.out.fillBranch("nJet30{}".format(self.systSuffix), nJet30)
      self.out.fillBranch("nJet30FailId{}".format(self.systSuffix), nJet30FailId)
      self.out.fillBranch("nJet15HEMFail{}".format(self.systSuffix), nJet15HEMFail)
      self.out.fillBranch("nJet30HEMFail{}".format(self.systSuffix), nJet30HEMFail)
      self.out.fillBranch("nBJet20{}".format(self.systSuffix), nBJet20)
      self.out.fillBranch("nElectrons10{}".format(self.systSuffix), nElectrons10)
      self.out.fillBranch("nMuons10{}".format(self.systSuffix), nMuons10)
      self.out.fillBranch("nPFLep5LowMT{}".format(self.systSuffix), nPFLep5LowMT)
      self.out.fillBranch("nPFLep5LowMTclean{}".format(self.systSuffix), nPFLep5LowMTclean)
      self.out.fillBranch("nPFHad10LowMT{}".format(self.systSuffix), nPFHad10LowMT)
      self.out.fillBranch("nLepLowMT{}".format(self.systSuffix), nLepLowMT)
      self.out.fillBranch("nLepHighMT{}".format(self.systSuffix), nLepHighMT)
      self.out.fillBranch("nRecoLepLowMT{}".format(self.systSuffix), nRecoLepLowMT)

      self.out.fillBranch("met_pt{}".format(self.systSuffix), met_pt)
      self.out.fillBranch("met_phi{}".format(self.systSuffix), met_phi)
      self.out.fillBranch("zll_met_pt{}".format(self.systSuffix), zll_met_pt)
      self.out.fillBranch("zll_met_phi{}".format(self.systSuffix), zll_met_phi)

      self.out.fillBranch("ht{}".format(self.systSuffix), ht)
      self.out.fillBranch("mht_pt{}".format(self.systSuffix), mht_pt)
      self.out.fillBranch("mht_phi{}".format(self.systSuffix), mht_phi)
      self.out.fillBranch("zll_ht{}".format(self.systSuffix), zll_ht)
      self.out.fillBranch("zll_mht_pt{}".format(self.systSuffix), zll_mht_pt)
      self.out.fillBranch("zll_mht_phi{}".format(self.systSuffix), zll_mht_phi)
      self.out.fillBranch("diffMetMht{}".format(self.systSuffix), diffMetMht)
      self.out.fillBranch("deltaPhiMin{}".format(self.systSuffix), deltaPhiMin)
      #self.out.fillBranch("deltaPhiMin_had", deltaPhiMin_had)
      self.out.fillBranch("zll_diffMetMht{}".format(self.systSuffix), zll_diffMetMht)
      self.out.fillBranch("zll_deltaPhiMin{}".format(self.systSuffix), zll_deltaPhiMin)
      self.out.fillBranch("jet1_pt{}".format(self.systSuffix), jet1_pt)
      self.out.fillBranch("jet2_pt{}".format(self.systSuffix), jet2_pt)

      self.out.fillBranch("mt2{}".format(self.systSuffix), mt2)
      self.out.fillBranch("zll_mt2{}".format(self.systSuffix), zll_mt2)

      self.out.fillBranch("lep_pt{}".format(self.systSuffix), lep_pt)
      self.out.fillBranch("lep_eta{}".format(self.systSuffix), lep_eta)
      self.out.fillBranch("lep_phi{}".format(self.systSuffix), lep_phi)
      self.out.fillBranch("lep_mass{}".format(self.systSuffix), lep_mass)
      self.out.fillBranch("lep_charge{}".format(self.systSuffix), lep_charge)
      self.out.fillBranch("lep_pdgId{}".format(self.systSuffix), lep_pdgId)
      self.out.fillBranch("lep_dxy{}".format(self.systSuffix), lep_dxy)
      self.out.fillBranch("lep_dz{}".format(self.systSuffix), lep_dz)
      self.out.fillBranch("lep_id{}".format(self.systSuffix), lep_id)
      #self.out.fillBranch("lep_tightId", lep_tightId)
      self.out.fillBranch("lep_miniRelIso{}".format(self.systSuffix), lep_miniRelIso)
      self.out.fillBranch("lep_mtw{}".format(self.systSuffix), lep_mtw)
      #self.out.fillBranch("lep_mcMatchId", lep_mcMatchId)
      #self.out.fillBranch("lep_lostHits", lep_lostHits)
      #self.out.fillBranch("lep_convVeto", lep_convVeto)
      #self.out.fillBranch("lep_tightCharge", lep_tightCharge)
      # variables for ele id (?)

      self.out.fillBranch("isoTrack_pt{}".format(self.systSuffix), isoTrack_pt)
      self.out.fillBranch("isoTrack_eta{}".format(self.systSuffix), isoTrack_eta)
      self.out.fillBranch("isoTrack_phi{}".format(self.systSuffix), isoTrack_phi)
      self.out.fillBranch("isoTrack_mass{}".format(self.systSuffix), isoTrack_mass)
      self.out.fillBranch("isoTrack_dz{}".format(self.systSuffix), isoTrack_dz)
      self.out.fillBranch("isoTrack_dxy{}".format(self.systSuffix), isoTrack_dxy)
      self.out.fillBranch("isoTrack_pdgId{}".format(self.systSuffix), isoTrack_pdgId)
      self.out.fillBranch("isoTrack_absIso{}".format(self.systSuffix), isoTrack_absIso)
      self.out.fillBranch("isoTrack_miniPFRelIso_chg{}".format(self.systSuffix), isoTrack_miniPFRelIso_chg)
      self.out.fillBranch("isoTrack_mtw{}".format(self.systSuffix), isoTrack_mtw)

      self.out.fillBranch("jet_pt{}".format(self.systSuffix), jet_pt)
      self.out.fillBranch("jet_eta{}".format(self.systSuffix), jet_eta)
      self.out.fillBranch("jet_phi{}".format(self.systSuffix), jet_phi)
      self.out.fillBranch("jet_id{}".format(self.systSuffix), jet_id)
      self.out.fillBranch("jet_mcFlavour{}".format(self.systSuffix), jet_mcFlavour)
      self.out.fillBranch("jet_btagCSV{}".format(self.systSuffix), jet_btagCSV)
      self.out.fillBranch("jet_btagDeepCSV{}".format(self.systSuffix), jet_btagDeepCSV)

      self.out.fillBranch("zll_pt{}".format(self.systSuffix), zll_pt)
      self.out.fillBranch("zll_eta{}".format(self.systSuffix), zll_eta)
      self.out.fillBranch("zll_phi{}".format(self.systSuffix), zll_phi)
      self.out.fillBranch("zll_mass{}".format(self.systSuffix), zll_mass)

    ####################################################
    # Return
    ###################################################
    if(doSkim and not passSkim): ret = False

    return ret


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

mht = lambda : mt2VarsProducer( isMC=True, year=2017 )
