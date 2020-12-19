#!/bin/bash

name=NBA
file=main.yaml

while getopts ":n:t:" opt; do
  case $opt in
    n) name="$OPTARG"
    ;;
    t) file="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

printf "Stack name is %s\n" "$name"
printf "Template file is %s\n" "$file"

echo aws s3 cp $file s3://templates.assets
aws s3 cp $file s3://templates.assets
echo aws cloudformation create-stack --stack-name $name --template-url https://s3.us-west-2.amazonaws.com/templates.assets/$file --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND 
aws cloudformation create-stack --stack-name $name --template-url https://s3.us-west-2.amazonaws.com/templates.assets/$file --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND 
