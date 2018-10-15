
PUFILE="PileupData_GoldenJSON_Full2017.root"

echo "Calculating nominal"
pileupCalc.py -i ../json/current_2017.txt --inputLumiJSON=/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/PileUp/pileup_latest.txt --pileupHistName pileup --calcMode true --minBiasXsec 69200 --maxPileupBin 100 --numPileupBins 100 central.root

echo "Calculating up variation" 
pileupCalc.py -i ../json/current_2017.txt --inputLumiJSON=/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/PileUp/pileup_latest.txt --pileupHistName pileup_plus --calcMode true --minBiasXsec 72660 --maxPileupBin 100 --numPileupBins 100 up.root

echo "Calculating down variation"
pileupCalc.py -i ../json/current_2017.txt --inputLumiJSON=/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/PileUp/pileup_latest.txt --pileupHistName pileup_minus --calcMode true --minBiasXsec 65740 --maxPileupBin 100 --numPileupBins 100 down.root

echo "Merging"
hadd $PUFILE central.root up.root down.root

if [ -f $PUFILE ]; then
  echo "Copying"
  cp $PUFILE ../../../../data/pileup/.
  echo "Removing intermediate files"
  rm central.root 
  rm up.root
  rm down.root
else
  echo "something went wrong with creation of file " $PUFILE
  echo "please check"
fi


