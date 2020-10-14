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

POOLID=$(aws --region ${REGION} cloudformation describe-stack-resource --stack-name ${STACK} --logical-resource-id UserPool --query "StackResourceDetail.PhysicalResourceId" --output text)
CLIENTID=$(aws --region ${REGION} cloudformation describe-stack-resource --stack-name ${STACK} --logical-resource-id UserPoolClient --query "StackResourceDetail.PhysicalResourceId" --output text)

aws --region ${REGION} cognito-idp sign-up \
  --client-id ${CLIENTID} \
  --username ${USER} \
  --password ${PASS} \
  --user-attributes Name="email",Value="${EMAIL}"

aws --region ${REGION} cognito-idp admin-confirm-sign-up \
  --user-pool-id ${POOLID} \
  --username ${USER}
