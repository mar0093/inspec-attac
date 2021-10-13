#!/bin/bash
docker start james-demo
docker exec -it james-demo python3 main.py
