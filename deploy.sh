#!/bin/sh

# a wrapper for deploying using fabric
# deploy current branch to $deploy_target

# ensure environment vars are set
if [ -z "${deploy_target+xxx}" ]; then
    echo "ERROR: please set deploy_target environment variable to TEST | STAGE | PROD"
    exit
fi;
# there's a better way to do this...
if [ ! $deploy_target = "TEST" ]; then
    if [ ! $deploy_target = "STAGE" ]; then
	if [ ! $deploy_target = "PROD" ]; then
	    echo "ERROR: valid deploy_targets are TEST | STAGE | PROD"
	    exit
	fi
    fi
fi;

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
fab -H ubuntu@$TARGET deploy
