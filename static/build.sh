#!/bin/bash

StackName=$1
StaticAssetsBucket=$2

cd static

poolId=$(aws cloudformation describe-stack-resource --stack-name ${StackName} --logical-resource-id UserPool --query "StackResourceDetail.PhysicalResourceId" --output text)
clientId=$(aws cloudformation describe-stack-resource --stack-name ${StackName} --logical-resource-id FrontendUserPoolClient --query "StackResourceDetail.PhysicalResourceId" --output text)
cat <<<EOF
{
    "poolId": "${poolId}",
    "clientId": "${clientId}"
}>js/cognito-config.json
aws s3 cp --recursive --exclude buildspec.yml ./ s3://"${StaticAssetsBucket}"/