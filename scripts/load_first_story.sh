#!/bin/bash

cd scripts

CONFIG=config.txt

if [ -f "$CONFIG" ]; then
    . $CONFIG
else
    STACK=$1
    USER=$2
    PASS=$3
    EMAIL=$4
    REGION=$5
fi

TABLE=$(aws --region ${REGION} cloudformation describe-stack-resource --stack-name ${STACK} --logical-resource-id StoriesTable --query "StackResourceDetail.PhysicalResourceId" --output text)

if [ "$(uname)" == "Darwin" ]; then
    sed -i '' 's/REPLACE_TABLE_NAME/'${TABLE}'/g' first_story.json
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    # Do something under GNU/Linux platform
    sed -i 's/REPLACE_TABLE_NAME/'${TABLE}'/g' first_story.json
fi
aws --region ${REGION} dynamodb batch-write-item --request-items file://first_story.json
