# Merge
Utility to merge the MT2 babytrees from crab into a single root file per sample, using ```haddnano.py```.

The main class is ```GroupMerger```: it handles the merging and copy to a specified output directory. The merging and copying is done on a group of samples basis.

A group of samples can be e.g. all the QCD samples and so on.
The supported groups are specified in the launching script ```merge.py```.

The handling of samples via groups makes the parallelisation easier, as well as improving the book-keeping of possibly missing samples to merge.

The version of the output file will be characterised by two labels, the production label (PL) and the merging label (ML):
- production label, version of nanoMT2, indicated with capital letters, e.g. V01_V03
- merging label, version of merge, indicated with lower case, e.g. v2

The merging is done sample-per-sample in a /tmp directory and then the merged file is copied to a to the tier3 storage element area
```/pnfs/psi.ch/cms/trivcat/store/user/$USER/merged_nanoMT2/${PL}_${ML}/<SAMPLE-NAME>```

### Configuration
Add the list of samples that you want to do the merging for in ```cfg/```, one list for data, one list for MC.

Everytime there is a new nanoMT2 production with production label PL, create (and commit!) a new sample list with the following naming convention:

```
data_<YEAR>_merge_<PL>.txt
mc_bkg_<YEAR>_merge_<PL>.txt
```

Please also remember to set your proxy:
```
voms-proxy-init --voms cms
```

### Run-time
#### Full production (run on batch
```
python submit_merge.py -p ${PL} -v ${ML} -y 2016 --doMC  # or omit --doMC 
```
#### Testing (run interactively)
```
python merge.py -p TEST14 -v ${ML} -g Wlv -y 2017 --doMC
python merge.py -p TEST14 -v ${ML} -g data -y 2017
```
##### Some examples (run interactively)
Data:
```
python merge.py -p ${PL} -v ${ML} -g data -y 2017
```
or, separately:
```
python merge.py -p ${PL} -v ${ML} -y 2017 -g MET
python merge.py -p ${PL} -v ${ML} -y 2017 -g JetHT
python merge.py -p ${PL} -v ${ML} -y 2017 -g HTMHT
python merge.py -p ${PL} -v ${ML} -y 2017 -g SingleElectron
python merge.py -p ${PL} -v ${ML} -y 2017 -g SingleMuon
python merge.py -p ${PL} -v ${ML} -y 2017 -g DoubleEG
python merge.py -p ${PL} -v ${ML} -y 2017 -g DoubleMuon
python merge.py -p ${PL} -v ${ML} -y 2017 -g MuonEG
python merge.py -p ${PL} -v ${ML} -y 2017 -g SinglePhoton
#python merge.py -p ${PL} -v ${ML} -y 2017 -g DoublePhoton
```

MC:

```
python merge.py -p ${PL} -v ${ML} -g all -y 2017 --doMC
```
or, separately,

```
python merge.py -p ${PL} -v ${ML} -y 2017 --doMC -g Zvv
python merge.py -p ${PL} -v ${ML} -y 2017 --doMC -g Wlv
python merge.py -p ${PL} -v ${ML} -y 2017 --doMC -g Zll
python merge.py -p ${PL} -v ${ML} -y 2017 --doMC -g Top
python merge.py -p ${PL} -v ${ML} -y 2017 --doMC -g QCD
python merge.py -p ${PL} -v ${ML} -y 2017 --doMC -g Gjets
```


## Further treatment for data
Since for data we are running on different primary datasets, it is important to remove the duplicated events across them.

First, all PDs of the same period will be merged, then the duplicates will be removed

The outputs will be stored in a /merged/ dir inside the original directory

By activating --doForce, the merging and duplicate removal will happen even if not all samples are available

```
python data_merge_and_remove_duplicates.py -y 2017 -p ${PL} -v ${ML} --doForce
```
