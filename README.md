## RDF Data Simulator
This project is intended to encourage the development of open source radio direction finding (RDF) mapping software. This software generates continuously updating XML files with receiver location and line of bearing (LOB) information. The format is based loosely on the KerberosSDR project.

Please note **the bearing output is inverted** to stay consistent with the current KerberosSDR software. To correct for this in your software, simply do `360 - DOA`.

#### Usage:

New Instructions coming soon.

Install dependencies: `pip3 install -r requirements.txt`

Then run `run_df_sim_example.py`.
