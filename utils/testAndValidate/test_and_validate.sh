PL="2016_V02_V02"
OLD_PL="2016_V00_V00"
MC=false # or false if data
YEAR=2016


echo "Going to run local test for PL=" $PL "  year=" $YEAR "  MC=" $MC
cd ../../.
if [ "$MC" = true ] ; then
  python postproc.py --year $YEAR --doMC -o ~/MT2_UNIT_TESTS/output/test_preProd_${PL}_MC  -w Wlv --doLocal -N 50001 --doSkim
else
  python postproc.py --year $YEAR     -o ~/MT2_UNIT_TESTS/output/test_preProd_${PL}_data -w data --doLocal -N 50001 --doSkim
fi

echo ""
echo "Test should be over at this point"
echo "Going to run validation with old production= " $OLD_PL

cd utils/validate/

if [ "$MC" = true ] ; then

  python validate.py -f1 ~/MT2_UNIT_TESTS/output/test_preProd_${OLD_PL}_MC/mt2.root -t1 Events -f2 ~/MT2_UNIT_TESTS/output/test_preProd_${PL}_MC/mt2.root -t2 Events -o ~/MT2_UNIT_TESTS/validate/out_${PL}VS${OLD_PL}_MC -l1 ${OLD_PL} -l2 ${PL} --doLog

else

  python validate.py -f1 ~/MT2_UNIT_TESTS/output/test_preProd_${OLD_PL}_data/mt2.root -t1 Events -f2 ~/MT2_UNIT_TESTS/output/test_preProd_${PL}_data/mt2.root -t2 Events -o ~/MT2_UNIT_TESTS/validate/out_${PL}VS${OLD_PL}_data -l1 ${OLD_PL} -l2 ${PL} --doLog

fi

cd -

echo ""
echo "Validation plots created"
echo "Going to publish them on website"

if [ "$MC" = true ] ; then

  scp -r ~/MT2_UNIT_TESTS/validate/out_${PL}VS${OLD_PL}_MC mratti@lxplus.cern.ch:/eos/user/m/mratti/www/MT2/validation/.
  #scp -i /shome/mratti/.ssh/id_lxplus HTACCESS mratti@lxplus.cern.ch:/eos/user/m/mratti/www/MT2/validation/out_${PL}VS${OLD_PL}_MC/.htaccess

else
  scp -r ~/MT2_UNIT_TESTS/validate/out_${PL}VS${OLD_PL}_data mratti@lxplus.cern.ch:/eos/user/m/mratti/www/MT2/validation/.
  #scp HTACCESS mratti@lxplus.cern.ch:/eos/user/m/mratti/www/MT2/validation/out_${PL}VS${OLD_PL}_data/.htaccess

fi

