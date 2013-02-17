#!/bin/bash

# Script for rsyncing the public domain data set. 
# Make sure the data fabric is mounted.
rsync --copy-links --delete --ignore-errors --recursive --times --verbose  datasets.hathitrust.org::non_google/ /Volumes/home/bo.marchman/non_google