#!/bin/bash 

LambdaBucket=$1
LambdaVersion=$2

cd lambdas

for dir in $(find . -maxdepth 1 -type d | sed -e 's/\.\///g'|grep -v ^\\.)
do
        cd "$dir";
        if [ -f requirements.txt ];
        then
                mkdir -p package
                cd package
                pip install --no-compile -t ./ -r ../requirements.txt
                zip -r9 ../"$dir"-"$LambdaVersion".zip .
                cd ..
                zip -g "$dir"-"$LambdaVersion".zip "$dir".py
        else
                zip -r "$dir"-"$LambdaVersion".zip ./
        fi
        aws s3 cp "$dir"-"$LambdaVersion".zip s3://"${LambdaBucket}"/lambdas/"$dir"/"$dir"-"$LambdaVersion".zip
done
