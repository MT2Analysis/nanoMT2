# nanoMT2
Package to be run on top of nanoAOD-tools to create MT2 analysis trees - BabyTrees

Installation instructions can be found at
https://twiki.cern.ch/twiki/bin/view/SusyMECCA/SusyMT2cernETHLegacy

To run on the grid:
```
voms-proxy-init --voms cms --valid 168:00
```
Please note that for no reason, it seems that it's better to issue the above command right before 
the command to launch the production

## Run-time

### Day-to-day testing

#### Local: 
```
python postproc.py -o output/test_Wlv -N 5001 -w Wlv --doLocal --doMC -y 2017
python postproc.py -o output/test_data -N 5001 -w data --doLocal -y 2017

python postproc.py -o output/test_sig -N 5001 -w sig --dolocal --doMC --doSignal -y 2016 

```
#### Grid: Latest command - testing
```
cd crab

python crab_mt2.py -p TEST15 -l ../data/samples/test_mc_bkg_2017.txt -y 2017 --doMC

python crab_mt2.py -p TEST15 -l ../data/samples/test_data_2017.txt -y 2017
```

### Production

#### Local: Pre-production tests

```
cd utils/testAndValidate/
```
Edit testAndValidate.sh according to the production label, new and old, to test against, then:
```
source testAndValidate.sh
```

#### Grid: launch production
Please remember to clean or move the content of the output directory before launching a production, otherwise all files in it will be copied to the workdir of the job

Are you sure that you looked at the SUSY recommendations ? Have a look !
https://twiki.cern.ch/twiki/bin/viewauth/CMS/SUSRecommendationsRun2Legacy 

```
python crab_mt2.py -p ${PL} -l ../data/samples/mc_bkg_2017.txt -y 2017 --doSkim --doMC 

python crab_mt2.py -p ${PL} -l ../data/samples/data_2017.txt -y 2017 --doSkim
```

#### Versions of productions
We will not version the nanoMT2 code, but please remember to make a commit after launching production and to copy the commit hash below

Convention for the production label: <year>_<label1>_<label2>, label 1 should be changed anytime the code is different, label 2 is only used in case more than one grid production is launched.

Production Label: brief description : git commit hash (can be searched)
```
2017_V00_V04: first production for 2017 data:		 a5b8b241a3cedd5fb408675ffb5581ca26f075f3
2017_V00_V05: first production for 2017 mc: 		 aba436783a88e092663da19189ee9d60fc0683a8
2017_V00_V06: missing data samples for 2017 data:        7e88eabcca49936feb6212931816a95f170757fe
2017_V00_V07: more missing data samples for 2017 data:   895311e5cf2e397cac3d6bd472b2eee4916e7021
2016_V00_V00: first production for 2016 data:            209a1f248cc105c8950d8534cbc66ac38dc28bba
2017_V01_V00: 2017 w/ correct json list                  cbe8fd1791b73b0a9fed4965d7f47fac80dd292a
2017_V01_V01: PUweight, info for btagSF,		 cd6f9a47b4232f97c3572b3ba7c9dbd279a38c3d
2016_V02_V00: isotrack variables, fix for btag info	 9411aeaef2cfc01c6c0744f4e31ca42fe5bc2ad4
2016_V02_V01: same as previous, but for MC               0ea80dd03d0099ac9778fd54c6795a28867db663
```


