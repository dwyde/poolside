#!/bin/sh

# for debugging info, run:
# ./build.sh -d --line-tracking --source-tracking

# path to the pyjsbuild:
PYJS=~/pyjs/pyjamas/bin/pyjsbuild


options="$*"
#if [ -z $options ] ; then options="-O";fi
$PYJS --print-statements $options -Isrc -o../docs/pyjs/_attachments my_nb
