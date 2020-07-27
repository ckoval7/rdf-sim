#!/bin/bash
rm -rf /ram/*
cp -r ./web/* /ram/
php -S 0.0.0.0:8080 -t /ram/ > /dev/null 2>&1 &
python3 ./run_df_sim.py
