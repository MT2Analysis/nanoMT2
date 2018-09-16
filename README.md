# nanoMT2
Package to be run on top of nanoAOD-tools to create MT2 analysis trees - BabyTrees

Installation instructions can be found at
https://twiki.cern.ch/twiki/bin/view/SusyMECCA/SusyMT2cernETHLegacy

To run on the grid:
```
voms-proxy-init --voms cms --valid 168:00
```

## Run-time

### Day-to-day testing

#### Local: Command for nano vs mini validation
```
python postproc.py -o output/testmc_94X_nano_std -N 5001 -w Wlv --doLocal --doMC

python postproc.py -o output/testmc_94X_nano_std_Zll -N 5001 -w Zll --doLocal --doMC
```
#### Grid: Latest command - testing
```
cd crab

python crab_mt2.py -p TEST15 -l ../data/samples/mc_bkg_2017.txt -y 2017 --doMC --doSyst

python crab_mt2.py -p TEST15 -l ../data/samples/data_2017.txt -y 2017
```

### Production

#### Local: Pre-production tests
Please remember to save the pre-production tests with the same production label PL as the one used for production

```
python postproc.py --year 2017 --doMC -o output/test_preProd_${PL}_MC  -w Wlv --doLocal -N 50001 --doSkim --doSyst

python postproc.py --year 2017        -o output/test_preProd_${PL}_data -w data --doLocal -N 50001 --doSkim
``` 
--> NEXT: perform validation, use utils/validate and follow instructions there


#### Grid: launch production
```
python crab_mt2.py -p ${PL} -l ../data/samples/mc_bkg_2017.txt -y 2017 --doSkim --doMC --doSyst

python crab_mt2.py -p ${PL} -l ../data/samples/data_2017.txt -y 2017 --doSkim
```

#### Versions of productions
We will not version the nanoMT2 code, but please remember to make a commit after launching production and to copy the commit hash below

Production Label: brief description : git commit hash (can be searched)
```
2017_v00_v04: first production for 2017 data:		 a5b8b241a3cedd5fb408675ffb5581ca26f075f3
2017_v00_v05: first production for 2017 mc: 		 aba436783a88e092663da19189ee9d60fc0683a8
```


