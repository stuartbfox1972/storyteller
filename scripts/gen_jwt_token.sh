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

CLIENTID=$(aws --region ${REGION} cloudformation describe-stack-resource --stack-name ${STACK} --logical-resource-id FrontendUserPoolClient --query "StackResourceDetail.PhysicalResourceId" --output text)

aws --region ${REGION} cognito-idp initiate-auth \
    --client-id ${CLIENTID} \
    --auth-flow USER_PASSWORD_AUTH \
    --auth-parameters USERNAME=${USER},PASSWORD=${PASS} \
    --query 'AuthenticationResult.AccessToken' \
    --output text
