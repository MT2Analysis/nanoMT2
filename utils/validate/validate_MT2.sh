#!/bin/bash



if [[ "$#" -eq 0 ]]; then
echo "ERROR: the script needs at least one argument. Relaunch it with one of the following options:"
echo "source validate_MT2.sh inputFolder"
echo "./validate_MT2.sh fileA.root fileB.root labelA labelB outputFolderName -data/mc"
exit;
fi;


## susy-mT2/validation_mca_MT2.txt --> this contains style
## susy-mT2/validation_MT2.txt --> contains selections
## susy-mT2/validation_plots_MT2.txt --> contains content, plot titles and binning




if [[ "$#" -eq 6 ]]; then
eval `scramv1 runtime -sh`
workingDir="$PWD"

fileA="$1"
fileB="$2"

labelA="$3"
labelB="$4"
outputFolder="$5"
isDataMC="$6"

if [ -d $outputFolder ]; then
    echo "output folder " $outputFolder " already exists. Rewriting.."
else
    mkdir $outputFolder;
    mkdir -p $outputFolder/$labelA/mt2;
    mkdir -p $outputFolder/$labelB/mt2;
    cp $fileA $outputFolder/$labelA/mt2/mt2_tree.root
    cp $fileB $outputFolder/$labelB/mt2/mt2_tree.root


# Here I create a dummy pickle file with the 'All Events' entry, so that the events can be rescaled in the standard way
    pythonTmpScript=$Rand.py
    cat <<EOF > $pythonTmpScript
#!/usr/bin/python
import pickle
file = open("dummyPickle.pck",'wb')
pck = [['All Events', 100], ['Sum Weights', 100.0]]
pickle.dump(pck,file)
file.close()
EOF
    chmod 755 $pythonTmpScript
    ./$pythonTmpScript
    rm $pythonTmpScript


    mkdir -p $outputFolder/$labelA/skimAnalyzerCount
    mkdir -p $outputFolder/$labelB/skimAnalyzerCount
    cp dummyPickle.pck $outputFolder/$labelA/skimAnalyzerCount/SkimReport.pck
    mv dummyPickle.pck $outputFolder/$labelB/skimAnalyzerCount/SkimReport.pck
fi 



### Here one should specify the weights used to rescale the events in one or both samples ### 
cat <<EOF > $outputFolder/inputs.txt
ttHWW   : $labelB : 1. ; FillColor=ROOT.kOrange+10 , Label="$labelB"
ref_ttHWW+ : $labelA : 1. ; FillColor=ROOT.kAzure+2, Label="$labelA"
EOF

# ttHWW   : $labelB : evt_scale1fb*weight_btagsf ; FillColor=ROOT.kOrange+10 , Label="$labelB"
# ref_ttHWW+ : $labelA : evt_scale1fb*weight_btagsf ; FillColor=ROOT.kAzure+2, Label="$labelA"
# EOF


cd plotter/

if [[ "$isDataMC" == "-data" ]]; then
    cat susy-mT2/validation_plots_MT2_common.txt susy-mT2/validation_plots_MT2_data.txt > susy-mT2/validation_plots_MT2
    python mcPlots.py -f --tree mt2  -P $workingDir/$outputFolder  $workingDir/$outputFolder/inputs.txt susy-mT2/validation_MT2.txt susy-mT2/validation_plots_MT2 --pdir $workingDir/$outputFolder/plots -p ref_ttHWW,ttHWW  -u -e --plotmode=norm --showRatio --maxRatioRange 0.65 1.35 --flagDifferences --toleranceForDiff 0.005
elif [[ "$isDataMC" == "-mc" ]]; then
    echo "processing -mc"
    cat susy-mT2/validation_plots_MT2_common.txt susy-mT2/validation_plots_MT2_mc.txt > susy-mT2/validation_plots_MT2   
    python mcPlots.py -f --tree Events  -P $workingDir/$outputFolder  $workingDir/$outputFolder/inputs.txt susy-mT2/validation_MT2.txt susy-mT2/validation_plots_MT2 --pdir $workingDir/$outputFolder/plots -p ref_ttHWW,ttHWW  -e --plotmode=norm --showRatio --maxRatioRange 0.65 1.35 --flagDifferences --toleranceForDiff 0.005
fi;

echo "Cleaning up ..."
rm susy-mT2/validation_plots_MT2

cd $OLDPWD

cp $outputFolder/$labelA/mt2/mt2_tree.root $outputFolder/plots/$labelA.root
cp $outputFolder/$labelB/mt2/mt2_tree.root $outputFolder/plots/$labelB.root

fi;
