# nanoMT2
Package to be run on top of nanoAOD-tools

Installation instructions can be found at
https://twiki.cern.ch/twiki/bin/view/SusyMECCA/SusyMT2cernETHLegacy


# Run-time

## Local: Command for nano vs mini validation
python postproc.py -o output/testmc_94X_nano_std -N 5001 -w Wlv --doLocal --doMC

python postproc.py -o output/testmc_94X_nano_std_Zll -N 5001 -w Zll --doLocal --doMC

## Local: Latest command
python postproc.py --year 2017 --doMC -o output/test -w Wlv --doLocal --doSkim

## Grid: Latest command - testing
cd crab
python crab_mt2.py -p TEST10 -l ../samples/mc_bkg_2017.txt -y 2017 --doMC --doSkim
python crab_mt2.py -p TEST10 -l ../samples/data_2017.txt -y 2017 --doSkim

## Grid: note
Please check the xsection file to make sure that the naming is correct !

## Grid: launch production
work in progress
