import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import PhysicsTools.NanoAODTools.postprocessing.tools as tools

from PhysicsTools.NanoAODTools.postprocessing.analysis.mt2.mt2Analyzer import getMT2


# my implementation of closest
def closest(obj,collection):
    ret = None; drMin = 999
    for i,x in enumerate(collection):
        dr = tools.deltaR(obj,x)
        if dr < drMin:
            ret = i; drMin = dr
    return (ret,drMin)


class mt2VarProducer(Module):
    def __init__(self, jetSelection, muonSelection, electronSelection):
        self.jetSel = jetSelection
        self.muSel = muonSelection
        self.elSel = electronSelection
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.verbose = False
        self.out = wrappedOutputTree
        #self.out.branch("MHT_pt",  "F");
        #self.out.branch("MHT_phi", "F");
        #self.out.branch("Jet_mhtCleaning", "b", lenVar="nJet")

        self.out.branch("gamma_MET_pt", "F")
        self.out.branch("gamma_MET_phi", "F")
        self.out.branch("ht", "F")
        self.out.branch("mht_pt", "F")
        self.out.branch("mht_phi", "F")
        self.out.branch("zll_ht", "F")
        self.out.branch("zll_mht_pt", "F")
        self.out.branch("zll_mht_phi", "F")
        self.out.branch("mt2", "F")

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
        #isotracks = Collection(event, "IsoTrack")
        #mht = ROOT.TLorentzVector()

        # make gamma met , not including overlap removal with jets
        gamma_met = ROOT.TVector2()
        lead_gamma = ROOT.TVector2()
        # remove leading photon with given cuts
        # collections are sorted in pt - take leading photon
        gamma_met.SetMagPhi(met.pt, met.phi)
        if len(photons)>0:
          lead_gamma.SetMagPhi(photons[0].pt, photons[0].phi)
          gamma_met += lead_gamma

        self.out.fillBranch("gamma_MET_pt", gamma_met.Mod())
        self.out.fillBranch("gamma_MET_phi", gamma_met.Phi())

        cleanedP4 = [] # p4 needed for ht, mht, mt2 computation in SR and 1lepton region
        cleanedP4_zll = [] # p4 needed for ht, mht, mt2 computation in zll region
        selected_electrons = []
        selected_muons = []
        selected_jets = []

        # FIXME: no need to create p4 for objects

        for electron in electrons:
          if electron.pt < 10: continue
          if abs(electron.eta)>2.4: continue
          if electron.cutBased == 0: continue
          # isolation cut ?
          electron.isToRemove = False
          selected_electrons.append(electron)
          electronP4 = ROOT.TLorentzVector()
          electronP4.SetPtEtaPhiM(electron.pt, electron.eta, electron.phi, electron.mass)
          cleanedP4.append(electronP4)

        for muon in muons:
          if muon.pt < 10: continue
          if abs(muon.eta)>2.4: continue
          # id cut isolation ?
          muon.isToRemove = False
          selected_muons.append(muon)
          muonP4 = ROOT.TLorentzVector()
          muonP4.SetPtEtaPhiM(muon.pt, muon.eta, muon.phi, muon.mass)
          cleanedP4.append(muonP4)

        selected_leptons = selected_muons + selected_electrons
        # remove PF leptons within Delta R of a reco lepton
        #selected_isotracks = []
        #for it in isotracks:
        #  if not it.isPFcand: continue # consider only ofcandidates
        #  if abs(it.pdgId) != 11 or (abs(pdgId) == 11 or abs(pdgId) != 13): continue # consider only pfelectron / pfmuons
        #  # TODO: add the pt requirements, some are already done at nanoAOD level
        #  for lep in selected_leptons:
        #    if tools.deltaR(it.eta,it.phi,lep.eta,lep.phi) < 0.1:
        #      lep.isToRemove = True # mark the lepton as to be removed
        #      selected_isotracks.append(it)
        #      #break # go to next isotrack as soon as you find a matching lepton
        ## FIXME: what to do with PF charged hadrons ?

        for jet in jets:
          if jet.pt<30: continue
          if abs(jet.eta)<2.4: continue
          jet.isToRemove = False
          selected_jets.append(jet)
          jetP4 = ROOT.TLorentzVector()
          jetP4.SetPtEtaPhiM(jet.pt,jet.eta,jet.phi,jet.mass)
          cleanedP4.append(jetP4)
          cleanedP4_zll.append(jetP4)

        # now remove closest jet to lepton within DeltaR
        for lep in selected_leptons:
          if lep.isToRemove: continue
          (ijet,dRmin) = closest(lep,selected_jets)
          if self.verbose: print ijet,dRmin
          if ijet and dRmin<0.4: # mark that jet to be removed
            selected_jets[ijet].isToRemove = True

        # compute ht, mht
        #FIXME: find a better way to initialize four-vectors!
        mht = ROOT.TLorentzVector(0, 0, 0, 0)
        zll_mht = ROOT.TLorentzVector(0, 0, 0, 0)
        ht = 0
        zll_ht = 0

        for ip4 in cleanedP4:
          ht += ip4.Pt()
          mht += ip4 # they are both TLorentzVector
        for ip4 in cleanedP4_zll:
          zll_ht += ip4.Pt()
          zll_mht += ip4

        self.out.fillBranch("ht", ht)
        self.out.fillBranch("zll_ht", zll_ht)
        self.out.fillBranch("mht_pt", mht.Pt())
        self.out.fillBranch("zll_mht_pt", zll_mht.Pt())
        self.out.fillBranch("mht_phi", mht.Phi())
        self.out.fillBranch("zll_mht_phi", zll_mht.Phi())

        # TODO: this is provisional I'm passing selected_jets without condition for OR
        metTV2 = ROOT.TVector2()
        metTV2.SetMagPhi(met.pt, met.phi)
        mt2 = getMT2(selected_jets, metTV2 )
        #if len(selected_jets)>=2: print getMT2(selected_jets, metTV2 ), met.pt, len(selected_jets)
        self.out.fillBranch("mt2", mt2)

        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

mht = lambda : mt2VarProducer( lambda j : j.pt > 40,
                            lambda mu : mu.pt > 20 and mu.miniPFIso_all/mu.pt < 0.2,
                            lambda el : el.pt > 20 and el.miniPFIso_all/el.pt < 0.2 )
