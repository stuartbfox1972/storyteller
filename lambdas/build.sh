#!/bin/bash 

LambdaBucket=$1
LambdaVersion=$2

cd lambdas

for dir in $(find . -maxdepth 1 -type d | sed -e 's/\.\///g'|grep -v ^\\.)
do
        cd "$dir";
        ZIP="$dir"-"$LambdaVersion".zip
        if [ -f requirements.txt ];
        then
                mkdir -p package
                cd package
                pip install --no-compile -t ./ -r ../requirements.txt
                zip -r9 ../"$dir"-"$LambdaVersion".zip .
                cd ..
                zip -g "$ZIP" "$dir".py
        else
                zip -r "$ZIP".zip ./
        fi
        aws s3 cp "$dir"-"$LambdaVersion".zip s3://"${LambdaBucket}"/lambdas/"$dir"/"$ZIP"
done
