f = {}

f[2016] = {}
f[2017] = {}
f[2018] = {}

# ********
# * 2016 *
# ********
# For Mo19
#f[2016]['data'] = '/store/data/Run2016C/MET/NANOAOD/Nano14Dec2018-v1/10000/75C4E995-2885-8048-BA07-FD4ACCD3572E.root'
f[2016]['data'] = '/store/data/Run2016C/MET/NANOAOD/Nano14Dec2018-v1/10000/AA804D87-467E-6242-9EAA-F3D5A7B27A87.root'
# currently this file cannot be read ?
#f[2016]['data'] = '/store/data/Run2016B_ver2/MET/NANOAOD/Nano14Dec2018_ver2-v1/80000/CD0F76D4-44C6-7742-A060-C75E23889C4A.root'
#f[2016]['Wlv'] = ''
# legacy
#f[2016]['data'] = '/store/data/Run2016B/MET/NANOAOD/22Aug2018_ver2-v1/10000/C83B52FF-34A9-E811-8D07-1CC1DE19286E.root'
#f[2016]['Wlv'] = '/store/mc/RunIISummer16NanoAODv3/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v2/110000/1A7B787F-A7EA-E811-BAF6-549F35AD8BF0.root'
f[2016]['QCD'] = '/store/mc/RunIISummer16NanoAODv3/QCD_HT300to500_BGenFilter_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/100000/782BB8A0-97C7-E811-BA0F-001A648F1C52.root'
f[2016]['sig'] = '/store/mc/RunIISummer16NanoAOD/SMS-T2tt_mStop-500_mLSP-325_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/00000/780DA7C8-2D16-E811-8455-0CC47A13CCFC.root'
# old 2016
#f[2016]['Wlv'] = '/store/mc/RunIISummer16NanoAOD/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v2/90000/5C7D09C9-5E42-E811-8A15-0025905A497A.root'

# ********
# * 2017 *
# ********
# For Mo19
f[2017]['data'] = '/store/data/Run2017D/MET/NANOAOD/Nano14Dec2018-v1/10000/2536594C-ABC3-2A48-87DF-4FF2EDE55069.root'
f[2017]['Wlv'] = '/store/mc/RunIIFall17NanoAODv4/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/10000/45FF054F-C558-A541-AD74-A46F79B96CEB.root'

#f[2017]['data'] = '/store/data/Run2017D/MET/NANOAOD/31Mar2018-v1/10000/2891A264-4C45-E811-A30A-C4346BC80410.root'
#f[2017]['Wlv'] = '/store/mc/RunIIFall17NanoAOD/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/70000/5CD5289E-5856-E811-A5DB-A0369FD0B22A.root'

# old PU
#f[2017]['ttbar'] = '/store/mc/RunIIFall17NanoAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/00000/9035EBEE-7442-E811-AEFB-001E677923F4.root'
# new PU
f[2017]['ttbar'] = '/store/mc/RunIIFall17NanoAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/10000/6C3619FF-BFA9-E811-8824-001E6739CFA9.root'

# ********
# * 2018 *
# ********
# For Mo19

# private production
f[2018]['data'] = '/store/group/phys_susy/mratti/nanoMaking/NanoAODv4RePriv/MET/Run2018C-from_17Sep2018_ver1-NanoAODv4RePriv/181221_221740/0000/myNanoRunData2018ABC_NANO_23.root'

# For Mo19 (600-800 HT sample not yet available)
f[2018]['Wlv'] = '/store/mc/RunIIAutumn18NanoAODv4/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/60000/3EC850FB-2306-B44C-9566-3CBC4D64BFA0.root' 


    #files = ['$XRDGLO//store/group/phys_susy/mratti/nanoMaking/NanoAODv4PrivORIG0/WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4PrivORIG0-from_PUMoriond17_94X_mcRun2_asymptotic_v3_ver2/190307_144426/0000/myNanoRunMc2018_NANO_1.root']
    #files = ['$XRDGLO/store/group/phys_susy/mratti/nanoMaking/NanoAODv4PrivTest3/WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4PrivTest3-from_PUMoriond17_94X_mcRun2_asymptotic_v3_ver2/190307_143303/0000/myNanoRunMc2018_NANO_1.root']
    #files = ['/shome/mratti/nanoaod_workarea/nano_making/CMSSW_9_4_6_patch1/src/PhysicsTools/NanoAOD/test/test94X_Zll_NANO_5K_nodxyIT_diffIso.root']
    #files = ['/shome/mratti/nanoaod_workarea/nano_making/CMSSW_9_4_6_patch1/src/PhysicsTools/NanoAOD/test/test94X_Wlv_NANO_5K_noselIT.root']
    #files = ['/shome/mratti/nanoaod_workarea/nano_making/CMSSW_9_4_6_patch1/src/PhysicsTools/NanoAOD/test/test94X_Wlv_NANO_5K_noCut.root']
    #files = ['/shome/mratti/nanoaod_workarea/nano_making/CMSSW_9_4_6_patch1/src/PhysicsTools/NanoAOD/test/test94X_Wlv_NANO_5K_noCutNoOR.root']
    #files = ['/work/mratti/nanoaod_workarea/nano_making/CMSSW_10_2_9/src/test_for_mini_comparison/SUS-RunIIFall17NanoAODv4-00004.root']
    #files = ['/work/mratti/nanoaod_workarea/nano_making/CMSSW_10_2_9/src/test_for_mini_comparison_2016/SUS-RunIISummer16NanoAODv4-00181.root']


