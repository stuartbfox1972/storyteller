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
                pip install --system --no-compile -t ./ -r ../requirements.txt
                cd ..
        fi
        zip -r "$dir"-"$LambdaVersion".zip ./
        aws s3 cp "$dir"-"$LambdaVersion".zip s3://"${LambdaBucket}"/lambdas/"$dir"/"$dir"-"$LambdaVersion".zip
done
