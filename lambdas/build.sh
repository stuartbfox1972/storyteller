#!/bin/bash

LambdaBucket=$1
LambdaVersion=$2

cd lambdas
ROOT=$(pwd)

for dir in $(find . -maxdepth 1 -type d | sed -e 's/\.\///g'|grep -v ^\\.)
do
        cd ${ROOT}/"$dir";
        ZIP="$dir"-"$LambdaVersion"
        if [ -f requirements.txt ];
        then
                mkdir -p package
                cd package
                pip install --no-deps --no-compile -t ./ -r ../requirements.txt
                rm -r $(find . -name *dist-info)
                zip -q -r9 ../"$ZIP".zip .
                cd ..
                zip -q -g "$ZIP".zip "$dir".py
        else
                zip -q -r "$ZIP".zip ./
        fi
        aws s3 cp "$ZIP".zip s3://"${LambdaBucket}"/lambdas/"$dir"/"$ZIP".zip
done