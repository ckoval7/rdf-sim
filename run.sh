#!/bin/bash
cp index.html /ram/index.html
cp -r compass /ram/compass
php -S 0.0.0.0:8080 -t /ram/ > /dev/null 2>&1 &
python ./run_df_sim.py
