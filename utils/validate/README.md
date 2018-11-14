# Utility to compare the quantities in two mt2 trees

### For pre-production
```
NEW_PL='blabla'
OLD_PL='2017_V0'

python validate.py -f1 ../../output/test_preProd_${OLD_PL}_MC/mt2.root -t1 Events -f2 ../../output/test_preProd_${NEW_PL}_MC/mt2.root -t2 Events -o out_${NEW_PL}VS${OLD_PL}_MC -l1 ${OLD_PL} -l2 ${NEW_PL} --doLog

python validate.py -f1 ../../output/test_preProd_${OLD_PL}_data/mt2.root -t1 Events -f2 ../../output/test_preProd_${NEW_PL}_data/mt2.root -t2 Events -o out_${NEW_PL}VS${OLD_PL}_data -l1 ${OLD_PL} -l2 ${NEW_PL} --doLog
```

### Wlv mini vs nano 
```
python validate.py -f1 ../../output/testmc_94X_nano_std/test94X_Wlv_NANO_5K_noselIT_Skim.root -t1 Events  -f2 /shome/mratti/heppy_workarea/CMSSW_9_4_1/src/CMGTools/TTHAnalysis/cfg/testmc_94X_std_5K_noEleId_v2/WJetsToLNu_HT-600To800/mt2.root -t2 mt2 -o out_std -l1 nano94X -l2 mini94X --doLog
```

```
python validate.py -f1 ../../output/test_Wlv_noCut_fixNanoMT2_pt10/mt2.root -t1 Events -f2 /shome/mratti/heppy_workarea/CMSSW_9_4_1/src/CMGTools/TTHAnalysis/cfg/testmc_94X_std_5K_noEleId_v2/WJetsToLNu_HT-600To800/mt2.root  -t2 mt2  -l1 nano94X -l2 mini94X --doLog -o test
```



### Zll mini vs nano
```
python validate.py -f1 ../../output/testmc_94X_nano_std_Zll/test94X_Zll_NANO_5K_nodxyIT_Skim.root -t1 Events  -f2 /shome/mratti/heppy_workarea/CMSSW_9_4_1/src/CMGTools/TTHAnalysis/cfg/testmc_94X_std_5K_noEleId_v2_Zll/DYJetsToLL_M-50_HT-600to800/mt2.root -t2 mt2 -o out_std_Zll  -l1 nano94X -l2 mini94X --doLog
```

### Testing
```
python validate.py -f1 ../../output/test_preProd_2017_V0_mc/test94X_Wlv_NANO_5K_noselIT_Skim.root -t1 Events -f2  ../../output/testmc_94X_nano_std/test94X_Wlv_NANO_5K_noselIT_Skim.root -t2 Events -o out_preprod -l1 new -l2 old --doLog
```
