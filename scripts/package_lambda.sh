#!/bin/bash
cd backend
rm -rf lambda_package.zip
mkdir package
pip install -r requirements.txt -t package
cp lambda_function.py package/
cd package
zip -r ../lambda_package.zip .
cd ..
rm -rf package