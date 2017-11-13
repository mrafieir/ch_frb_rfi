### CH_FRB_RFI

ch_frb_rfi: A plugin-based framework for processing channelized intensity data in radio astronomy.

This manual isn't 100% complete, but there should be enough examples to get started!

### CONTENTS

  - [Examples: scripting interface](#user-content-examples-scripting-interface)
  - [Examples: JSON file interface](#user-content-examples-json-file-interface)
  - [JSON inventory](#user-content-json-inventory)
     - [Acquisitions](#user-content-json-inventory-acquisitions)
     - [RFI removal](#user-content-json-inventory-rfi-removal)
     - [Dedipsersion](#user-content-json-inventory-dedispersion)
     - [Toy streams](#user-content-json-inventory-toy-streams)

<a name="examples-scripting-interface"></a> 
#### EXAMPLES: SCRIPTING INTERFACE

There are currently two ways to use `ch_frb_rfi`.

First, you can write standalone python scripts which run the pipeline through the python interface in the `ch_frb_rfi` module.
Second, you can write python scripts which output json files, and add them to the "inventory" in `ch_frb_rfi/json_files`.
You can then use command-line tools (`rfp-run`, `rfp-time`, `rfp-analyze`) which form pipelines by chaining together json files.

In this section, we list some examples of the first method (running the pipeline through standalone python scripts).
See comments in the scripts for details.

  - `./example.py`: a few minutes of 1K-channel incoherent-beam data.
  - `./example2.py`: an acquisition with a real pulsar.
  - `./example3.py`: five minutes of 16K-channel Crab pulsar (26m) data.
  - `./s1.py` ... `s13.py`: some examples of interesting subsets of data, collected by Masoud (17-08-11)
  - `./s1-offline.py`: re-analyzing s1.py using offline variance estimation.

<a name="examples-json-file-interface"></a> 
#### EXAMPLES: JSON FILE INTERFACE

The second way of using ch_frb_rfi is to write short scripts which output json file "building blocks",
then use command-line tools (`rfp-run`, `rfp-time`, `rfp-analyze`) to chain these building blocks together.
It is also possible to make "run lists" which allow multiple pipelines in batch mode.
For more information on the command-line tools, see
["Command-line utilities" in rf_pipelines/MANUAL.md](https://github.com/kmsmith137/rf_pipelines/blob/master/MANUAL.md#user-content-command-line-utilities).

The ch_frb_rfi repository already contains some json file "building blocks" in `json_files/`.
The scripts which generate them are in the parallel directory `json_scripts/`.
For a current inventory of json files, see the next section ["JSON inventory"](#user-content-json-inventory).
For now, we just give a few examples of interesting runs which can be done using these building blocks.
In all of these examples, the pipeline runs consist of three json files: an acquisition, an RFI chain, and a dedisperser.

  - Analyze the "17-08-11 Masoud examples".  The following command line uses 6 threads in parallel and takes a few minutes to complete.
    The result will appear in the web viewer under `masoud_examples_s1`, ..., `masoud_examples_s10`.
    ```
    cd ch_frb_rfi/json_files
    rfp-run -w masoud_examples -t 6 acqs/17-08-11-masoud-examples-runlist-first10.json rfi_1k/17-10-24-first-try.json bonsai_1k/bonsai_nfreq1024_7tree_f512_v3.json
    ```

  - Analyze the 16k-upchannelized data.  Note that currently, we only have ~2.5 hours of data in total!  This uses 4 threads and takes ~4 hours to complete.
    The result will appear in the web viewer under `upchannelized_part0`, ..., `upchannelized_part6`.
    ```
    cd ch_frb_rfi/json_files
    rfp-run -w upchannelized -t 4 acqs/17-04-25-utkarsh-26m-16k-runlist.json rfi_16k/17-10-24-first-try.json bonsai_16k/bonsai_production_noups_nbeta1_v2.json
    ```

  - Analyze all of the incoherent-beam pathfinder data.  The following command line should work but I haven't actually tried it yet.  It will take a few days to finish!
    The results will appear in the web viewer under `everything_runX_partY`.
    ```
    cd ch_frb_rfi/json_files
    rfp-run -w everything -t 6 acqs/17-02-08-incoherent-data-avalanche-runlist.json rfi_1k/17-10-24-first-try.json bonsai_1k/bonsai_nfreq1024_7tree_f512_v3.json
    ```

  - Timing the pipeline.  The following command should be run on a 20-core compute node (e.g. frb-compute-0.physics.mcgill.ca),
    and is intended to be representative of the real-time search with 16 beams/node, where each core is responsible for packet decoding,
    RFI removal, and dedipsersion for one beam.  We run 20 timing threads in parallel (one for each core).
    ```
    cd ch_frb_rfi/json_files   # on a 20-core compute node, not frb1!
    rfp-time -t 20 toy_streams/chime_network_nfreq16k_nt100k.json rfi_16k/17-10-24-first-try-noplot.json bonsai_16k/bonsai_production_noups_nbeta1_v2-noplot.json
    ```
    Note that the timing pipeline consists of:
      - `toy_streams/chime_network_nfreq16k_nt100k.json`: dummy network stream, runs the packet decoding kernel but does not receive real packets.
      - `rfi_16k/17-10-24-first-try-noplot.json`: current 16k rfi removal chain, note the "noplot" which removes the plotter_transforms.
      - `bonsai_16k/bonsai_production_noups_nbeta1_v2-noplot.json`: 16k dedispersion, note the "noplot" which disables plotting.

  - "Analyzing" the pipeline.  The `rfp-analyze` utility shows some diagnostic info: buffer latencies and memory footprints.
    It could use more documentation, so the output may be cryptic, but we include an example here for completeness!
    Note that the transform chain here is the same as the timing example above (16k, noplot).
    ```
    rfp-analyze -r toy_streams/chime_network_nfreq16k_nt100k.json rfi_16k/17-10-24-first-try-noplot.json bonsai_16k/bonsai_production_noups_nbeta1_v2-noplot.json
    ```

<a name="json-inventory"></a> 
### JSON INVENTORY

The `json_files/` directory contains json files which correspond to pipeline_objects, and also contains some "run-lists".
The pipeline_object json files are created by scripts in `json_scripts/`.
The run-list json files are simple enough that I usually just write them by hand.

Reminder: to read an rf_pipelines json file, the syntax is
```
j = rf_pipelines.json_read(filename)
p = rf_pipelines.pipeline_object.from_json(j)   # returns an object of type rf_pipelines.pipeline_object
```
To write an rf_pipelines json file, the syntax is
```
j = p.jsonize()    # where p is an object of type rf_pipelines.pipeline_object
rf_pipelines.json_write(filename, j)
```

<a name="json-inventory-acquisitions"></a> 
##### JSON inventory: acquisitions

   - `json_files/acqs/17-04-25-utkarsh-26m-*`
     
     Currently, this is our only 16K-channel dataset!  It is from a 26-m run on 17-04-25, recorded
     in baseband, and upchannelized by Utkarsh's code.  There is ~2.5 hours of data, divided into 7
     parts (i.e. 7 json files).

     We save json files for the 16k-channelized acqs, and 1k-channelized acqs obtained by downsampling
     down to 1024 frequencies.  These latter acqs have (1/16) the data volume and are sometimes useful,
     e.g. for quick plotting or experimenting with tweaks to the "1k" part of the RFI transform chain.

     In hindsight, it would have been better to generate a single json file for all 7 parts combined,
     but I haven't done this yet!  (Due to details of how the upchannelization code works, there will
     be ~1 second gaps at boundaries between the 7 parts, but that's OK.)

   - `json_files/acqs/17-08-11-masoud-examples`

     Some examples of "interesting" incoherent-beam CHIME pathfinder data (also in scripts/s*.py).
     From Masoud (17-08-11).  Note that the runlist `json_files/acqs/17-08-11-masoud-examples-runlist-first10.json`
     only contains the first 10, since #11 is a long acq.

     - s1: A faint source at low DM.
     - s2: An RFI storm which results in a single false positive: (DM, SNR) = (77.62, 10.64).
     - s3: A periodic variation in intensity, combined with RFIs, makes it very hard to suppress all the false positives.
     - s4: This sample contains two major RFI events which result in a large fraction of zero weights along the time axis.
     - s5: This example contains a pulsar. In addition, there seems to be a strange variation in the overall intensity which can be revealed by using (detrender_niter, clipper_niter) = (1, 3).
     - s6: This short sample represents a highly active RF environment!
     - s7: Another highly active RF environment.
     - s8: Another highly active RF environment.
     - s9: This is an interesting example: It contains an RFI storm, a few false positives, and some significant changes in the running variance.
     - s10: B0329 (can be analyzed with rfi_level = 1).
     - s11: 6 hours of data.
     - s12: 5 min of data.
     - s13: 4 min of data.

  - `json_files/acqs/17-02-08-incoherent-data-avalanche`

    Acquisition data files for the ~1000 hours of incoherent-beam pathfinder data in
    frb1:/data2/17-02-08-data-avalanche.

    We define one json file per ~10 hours of data, so ~100 json files are created.
    When a "long" gap (more than a minute) occurs in the data, we start a new json file.

    The runlist `json_files/acqs/17-02-08-incoherent-data-avalanche-runlist.json`
    contains all ~100 json files, and can be used to analyze all of the data with
    one `rfp-run` command (see example earlier in the manual).  This will take a long time of course!

    It would be useful to catalog all "interesting" subsets of the incoherent-beam data
    and put these into another runlist which takes less time to run, but will (hopefully)
    be just as useful as the full dataset for testing RFI transform chains.

<a name="json-inventory-rfi-removal"></a> 
##### JSON inventory: RFI removal

Currently there is only one possibility, but we anticipate adding more RFI transform chains soon.

  - `rfi_1k/17-10-24-first-try.json`: based on 1K-channel RFI transform chain proposed by Masoud in the 17-08-11-examples.

  - `rfi_16k/17-10-24-first-try.json`: simplest 16K-channel chain, obtained by wrapping the 1K-chain in a `wi_sub_pipeline`,
    and adding two 16K-detrenders (one along the time axis, and one along the frequency axis).

Note that `rfi_16k/17-10-24-first-try.json` is the same as the file `rfi_configs/rfi_production_v1.json`
in the [ch_frb_l1 repository](https://github.com/kmsmith137/ch_frb_l1).  The idea is that RFI transform
chains can be developed in the ch_frb_rfi "laboratory" and copied to ch_frb_l1 when we want to use them
in the real-time search.

<a name="json-inventory-dedispersion"></a> 
##### JSON inventory: Dedispersion

The following 1K-channel json files are defined:
  - `json_files/bonsai_1k/bonsai_nfreq1024_7tree_f384_v3-noplot.json`
  - `json_files/bonsai_1k/bonsai_nfreq1024_7tree_f384_v3.json`
  - `json_files/bonsai_1k/bonsai_nfreq1024_7tree_f512_v3-noplot.json`
  - `json_files/bonsai_1k/bonsai_nfreq1024_7tree_f512_v3.json`

The `fXXX` part of the filename is the sampling rate, in FPGA counts per sample.
This is 512 for the incoherent-beam acqs (0.00131072 sec), or 384 for the 16K 26m acqs (0.00098304 sec).

The following 16K-channel json files are defined:
  - `json_files/bonsai_16k/bonsai_production_noups_nbeta1_v2-noplot.json`
  - `json_files/bonsai_16k/bonsai_production_noups_nbeta1_v2.json`
  - `json_files/bonsai_16k/bonsai_production_ups_nbeta1_v2-noplot.json`
  - `json_files/bonsai_16k/bonsai_production_ups_nbeta1_v2.json`

Filenames containing `ups` include an upsampled tree, which makes them more optimal for DM < 820
and pulse width < 1 ms, but they are more computationally expensive.

To use the bonsai json files, you must generate hdf5 files for each bonsai_config (with `bonsai-mkweight`,
see bonsai MANUAL.md for more info) in `/data/bonsai_configs`.  This has already been done on frb1, and
the CHIME compute nodes (frb-compute-X).

For no deep reason, the (variance, reweighting) timescales are currently (100, 100) in
the 1K-channel bonsai configs, and (200, 400) in the 16K-channel configs.  These values
are chosen semi-arbitrarily, and we should do a study to determine optimal settings!

Note that `bonsai_configs/bonsai_production_XX.txt` is the same file as `bonsai_configs/bonsai_production_XX.txt`
in the [ch_frb_l1 repository](https://github.com/kmsmith137/ch_frb_l1).  The idea is that bonsai configs
can be developed in the ch_frb_rfi "laboratory" and copied to ch_frb_l1 when we want to use them
in the real-time search.

From the above discussion, the same bonsai configs are expected to appear in multiple places:
  - in `git/ch_frb_rfi/bonsai_configs`
  - in `git/ch_frb_l1/bonsai_configs`
  - in `/data/bonsai_configs` (with "derived" hdf5 files created with `bonsai-mkweight`).

This raises the possibility of files becoming out of sync, if they are modified in one place
and not updated in others, or if the .txt files are updated without regenerating the corresponding
hdf5 files.  The script `scripts/check-bonsai-config-consistency.py` will check for
inconsistencies, and should be run periodically.

<a name="json-inventory-toy-streams"></a> 
##### JSON inventory: Toy streams

Sometimes we want to run a pipeline with random data, instead of reading an acquisition from disk.

   - `toy_streams/gaussian_nfreqXX_ntXX.json`

     Generates gaussian random intensities.  The `ntXX` part of the filename is the number of time
     samples which will be generated before the stream ends.

   - `toy_streams/chime_network_nfreqXX_ntXX.json`
 
     A "dummy" network stream which runs the packet decoding kernel that is used in the real-time
     search to decode network packets, but does not actually read packets from the network.  This
     is useful for timing (see `rfp-time` example earlier in the manual), since it represents the
     computational cost of the packet decoding kernel in the real-time search.


