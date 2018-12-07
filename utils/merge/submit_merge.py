# Script to submit the merging step to batch for a given MT2 production, labelled by a PL
# Split the job submission by groups of samples

from merge import getOptions,getMT2groups

options = getOptions()
mc_or_data = 'mc' if options.doMC else 'data'
MT2groups = getMT2groups() 

# if group is specified from command line, do that, otherwise do all groups 
groups_to_submit_for_merging = [options.group] if options.group != None else MT2groups[options.year][mc_or_data].keys()

# import configurations from command line
PL=options.productionLabel
ML=options.version
year=options.year
doMC=options.doMC

import os
import subprocess
# create logs dir
logsDir = 'logs_{pl}_{ml}'.format(pl=PL,ml=ML)
# create logs dir
command = 'mkdir -p {l}'.format(l=logsDir)
if not os.path.isdir(logsDir):
  subprocess.check_output(command, shell=True)
else: raise RuntimeError('logsDir {l} already present please check'.format(l=logsDir))

# prepare script for submission
for group in groups_to_submit_for_merging:

  template = [
    'source $VO_CMS_SW_DIR/cmsset_default.sh',
    'shopt -s expand_aliases',
    'cmsenv',
    'python merge.py -p {pl} -v {ml} -y {y} {mc} -g {g}'.format(pl=PL, ml=ML, y=year, mc='--doMC' if doMC else '', g=group),
  ]

  template = '\n'.join(template)

  sub_merge_file = 'submit_merge_{y}_{g}.sh'.format(y=year, g=group)
  with open( '{}/{}'.format(logsDir,sub_merge_file), 'w') as f:
    f.write(template)

  command = 'qsub -o {l} -e {l} -N {g}_{y} -q short.q -cwd {l}/{s}'.format(l=logsDir, s=sub_merge_file, y=year, g=group) # short queue should be enough
  # submit
  os.system(command)
