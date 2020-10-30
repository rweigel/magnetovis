#!/bin/bash
#
# Executes a script in Paraview. Automatically locates Paraview.
#
# Usage:
#   ./magnetovis.sh --script=file.py
#
# TODO: Write in Python. Do directory listing of /Applications and find most recent
# Paraview. Give instructions for setting PYTHONPATH, perhaps allow
# 	--pythonpath=/opt/anaconda3/envs/python2.7/lib/python2.7/site-packages

PARAVIEW=paraview
if ! [ -x "$(command -v paraview)" ]; then
   PARAVIEW=/Applications/ParaView-5.8.0.app/Contents/MacOS/paraview
fi
if ! [ -x "$(command -v $PARAVIEW)" ]; then
   echo "Paraview not found"
   exit 1
fi
eval "PYTHONPATH=/opt/anaconda3/envs/python2.7/lib/python2.7/site-packages:. $PARAVIEW $@"
