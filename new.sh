#!/bin/bash
docker build -t inspec-attac .
docker run --name james-demo -v $PWD/static:/usr/src/app/static -it inspec-attac
