# Utility to compare the quantities in two mt2 trees

### Wlv state-of-the-art 
python validate.py -f1 ../../output/testmc_94X_nano_std/test94X_Wlv_NANO_5K_noselIT_Skim.root -t1 Events  -f2 /shome/mratti/heppy_workarea/CMSSW_9_4_1/src/CMGTools/TTHAnalysis/cfg/testmc_94X_std_5K_noEleId_v2/WJetsToLNu_HT-600To800/mt2.root -t2 mt2 -o out_std -l1 nano94X -l2 mini94X --doLog

### Zll state-of-the-art
python validate.py -f1 ../../output/testmc_94X_nano_std_Zll/test94X_Zll_NANO_5K_nodxyIT_Skim.root -t1 Events  -f2 /shome/mratti/heppy_workarea/CMSSW_9_4_1/src/CMGTools/TTHAnalysis/cfg/testmc_94X_std_5K_noEleId_v2_Zll/DYJetsToLL_M-50_HT-600to800/mt2.root -t2 mt2 -o out_std_Zll  -l1 nano94X -l2 mini94X --doLog
