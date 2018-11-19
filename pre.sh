#!/bin/bash

set -e

CHANGED_FILES=`git diff --name-only master...${TRAVIS_COMMIT}`
YML_FOUND=False
YML=".yml"

for CHANGED_FILE in $CHANGED_FILES; do
  if [[ $CHANGED_FILE =~ $YML ]]; then
    YML_FOUND=True
    break
  fi
done

if [[ $YML_FOUND == False ]]; then
  echo "No YAML file change detected, exiting."
  travis_terminate 0
  exit 1
else
  echo "Yaml File change detected, continuing with build."
fi
