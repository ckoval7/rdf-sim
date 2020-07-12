## RDF Data Simulator
This project is intended to encourage the development of open source radio direction finding (RDF) mapping software. This software generates continuously updating XML files with receiver location and line of bearing (LOB) information. The format is based loosely on the KerberosSDR project.

Please note **the bearing output is inverted** to stay consistent with the current KerberosSDR software. To correct for this in your software, simply do `360 - DOA`.

#### Usage:
You'll need to create a temporary file system so you're not continuously writing the same file to disk.

Option one is to create the tmpfs on the fly. This is best for short term projects.

`sudo mkdir /ram && sudo mount -osize=30m tmpfs /ram -t tmpfs`

Option two is to use the provided `ram.mount` systemd file. This will create the tmpfs anytime you reboot your computer. This option is recommened if you're hosting this on a webserver.

```
sudo cp ./ram.mount /etc/systemd/system/
sudo systemctl enable ram.mount
sudo systemctl start ram.mount
```

If you don't want to use the compass or run a web server, just run `python3 run_df_sim.py`. XML data can be retrieved directly from `/ram/`.

If you would like to use the compass feature or host this on a remote machine, use `./run.sh`. This defaults to port 8080, but can be modified in the script. 

Please refer to the wiki for customizing the script.
