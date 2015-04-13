#!/bin/sh

# a wrapper for deploying fab
# deploy $git_branch to $deploy_target

# ensure environment vars are set
if [ -z "${git_branch+xxx}" ]; then
    echo ERROR: please set git_branch environment variable
    exit
fi;
if [ -z "${deploy_target+xxx}" ]; then
    echo ERROR: please set deploy_target environment variable to 
    exit
fi;
# there's a better way to do this...
if [ ! $deploy_target = "TEST" ]; then
    if [ ! $deploy_target = "STAGE" ]; then
	if [ ! $deploy_target = "PROD" ]; then
	    echo ERROR: valid deploy_targets are TEST, STAGE, PRO
	    exit
	fi
    fi
fi;

# check out correct branch
git checkout $git_branch

# deploy to target
TARGET=""
if [ $deploy_target = "TEST" ]; then
    TARGET="ul04.seedscientific.com"
fi;
if [ $deploy_target = "STAGE" ]; then
    TARGET="poliostage.seedscientific.com"
fi;
if [ $deploy_target = "PROD" ]; then
    TARGET="polio.seedscientific.com"
fi;
echo TODO: fab -h ubuntu@$TARGET deploy
