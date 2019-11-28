#!/bin/bash

echo  'starting project'
cd /usr/src/Finance
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple
cd /usr/src/Finance
gunicorn -w 1 -b 0.0.0.0:8000 manage:application
