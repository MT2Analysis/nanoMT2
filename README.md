# nanoMT2
Package to be run on top of nanoAOD-tools to create MT2 analysis trees - BabyTrees

Installation instructions can be found at
https://twiki.cern.ch/twiki/bin/view/SusyMECCA/SusyMT2cernETHLegacy

To run on the grid:
```
voms-proxy-init --voms cms --valid 96:00
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
Please remember to save the pre-production tests with the same label as the one used for production

```
python postproc.py --year 2017 --doMC -o output/test_preProd_<PL>_MC  -w Wlv --doLocal -N 5001 

python postproc.py --year 2017        -o output/test_preProd_<PL>_data -w data --doLocal -N 5001
``` 

#### Grid: launch production
```
python crab_mt2.py -p TEST15 -l ../data/samples/mc_bkg_2017.txt -y 2017 --doMC --doSyst

python crab_mt2.py -p TEST15 -l ../data/samples/data_2017.txt -y 2017
```

#### Versions of productions
We will not version the nanoMT2 code, but please remember to make a commit with the pre-production label in to make sure that you can go back in time and read what your code was doing when you launced it.

Production Label: brief description

2017_V0: first production for 2017 bkg MC and data 



