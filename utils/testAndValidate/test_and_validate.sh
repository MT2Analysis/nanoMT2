PL="2016_V08_V00"
OLD_PL="2018_V04_V00"
MC=false # or false if data
YEAR=2018

echo "Going to run local test for PL=" $PL "  year=" $YEAR "  MC=" $MC
cd ../../.
if [ "$MC" = true ] ; then
  echo 'MC'
  python postproc.py --year $YEAR --doMC -o /work/$USER/MT2_UNIT_TESTS/output/test_preProd_${PL}_MC  -w Wlv --doLocal -N 50001 --doSkim
  echo "finished running"
else
  echo 'Data'
  python postproc.py --year $YEAR     -o /work/$USER/MT2_UNIT_TESTS/output/test_preProd_${PL}_data -w data --doLocal -N 50001 --doSkim
  echo "finished running"
fi

echo ""
echo "Test should be over at this point"
echo "Going to run validation with old production= " $OLD_PL

cd utils/validate/

if [ "$MC" = true ] ; then

  python validate.py -f1 /work/$USER/MT2_UNIT_TESTS/output/test_preProd_${OLD_PL}_MC/mt2.root -t1 Events -f2 /work/$USER/MT2_UNIT_TESTS/output/test_preProd_${PL}_MC/mt2.root -t2 Events -o /work/$USER/MT2_UNIT_TESTS/validate/out_${PL}VS${OLD_PL}_MC -l1 ${OLD_PL} -l2 ${PL} --doLog
echo "ciao"

else

  python validate.py -f1 /work/$USER/MT2_UNIT_TESTS/output/test_preProd_${OLD_PL}_data/mt2.root -t1 Events -f2 /work/$USER/MT2_UNIT_TESTS/output/test_preProd_${PL}_data/mt2.root -t2 Events -o /work/$USER/MT2_UNIT_TESTS/validate/out_${PL}VS${OLD_PL}_data -l1 ${OLD_PL} -l2 ${PL} --doLog --doNorm
echo "ciao"

fi

cd ../testAndValidate

echo ""
echo "Validation plots created"
echo "Going to publish them on website"

if [ "$MC" = true ] ; then

  scp -r /work/$USER/MT2_UNIT_TESTS/validate/out_${PL}VS${OLD_PL}_MC mratti@lxplus.cern.ch:/eos/user/m/mratti/www/MT2/validation/.
  scp HTACCESS mratti@lxplus.cern.ch:/eos/user/m/mratti/www/MT2/validation/out_${PL}VS${OLD_PL}_MC/.htaccess

else
  scp -r /work/$USER/MT2_UNIT_TESTS/validate/out_${PL}VS${OLD_PL}_data mratti@lxplus.cern.ch:/eos/user/m/mratti/www/MT2/validation/.
  scp HTACCESS mratti@lxplus.cern.ch:/eos/user/m/mratti/www/MT2/validation/out_${PL}VS${OLD_PL}_data/.htaccess

fi

