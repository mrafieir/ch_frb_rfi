#!/usr/bin/env python
import ch_frb_rfi
import rf_pipelines

# Indicate whether to use the web_viewer as output.
web = True

# From the list below, select a sample index to process.
sample = 4

# The first file index (starts at 0).
start = 0
# The last file index (has no limit; must be greater than 'start').
end = 60

# Enable time-selected samples
ts_mode = True
ts_n = 5

assert end > start >= 0, "baseband_26m: Invalid (start, end) file indeces"
assert type(web) is bool

# This is a constantly changing list of samples. We will hopefully incorporate 
# this in 'acquisitions.py' and 'bonsai.py'. 'kfreq' is the upchannelization 
# (from 1K=1024) factor. 'nypix' may be adjusted so that each pixel (on waterfall 
# plots) corresponds to a unique frequency channel.

# B0329 is in this acquisition! 1K-channel data
if sample == 1:
    kfreq = 1
    path = '/data2/acqhack_confirmed_b0329_1K/*.h5'
    bonsai_v = 1

# same as 1, but in 16K
if sample == 2:
    kfreq = 16
    path = '/data2/baseband_26m_processed/16k_B0329/*.h5'
    bonsai_v = 1

# B1937 (pulsar not found; intended for RFI studies in 16K-channel data)
if sample == 3:
    kfreq = 16
    path = '/data2/baseband_26m_processed/16k_B1937/*.h5'
    bonsai_v = 1

# incoherent-beam data from the pathfinder; processed 0-7600
# weights are between 0.0 and 2; ts_n = -1 contains a pulsar;
if sample == 4:
    kfreq = 1
    path = '/data2/17-02-08-incoherent-data-avalanche/frb_incoherent_search_0/*.h5'
    bonsai_v = 1
    tsample = [[14189.1626598, 14275.0620058],
               [2335.05292288, 2463.90194176],
               [5169.73133824, 5341.53003008],
               [14275.0620058, 14446.8606976],
               [70882.7309670, 71054.5296589],
               [84154.1799117, 84368.9282765],
               [90811.7147648, 90983.5134566],
               [96266.3232307, 96481.0715955],
               [97984.3101491, 98156.1088410],
               [98499.7062246, 98671.5049165],
               [119716.844667, 119974.542705],
               [143897.510543, 144112.258908]]

if sample == 5:
    kfreq = 1
    path = '/data2/17-02-08-incoherent-data-avalanche/frb_incoherent_search_1/*.h5'
    bonsai_v = 1
    tsample = [[1207.79177984, 1379.59047168],
               [2238.58393088, 2453.33229568],
               [74694.6822144, 74866.4809062],
               [47206.8915200, 47335.7405389],
               [75811.3737114, 75983.1724032]]

# ts_n = 0 is an RFI storm; processed 4000-5000
if sample == 6:
    kfreq = 1
    path = '/data2/17-02-08-incoherent-data-avalanche/frb_incoherent_0b/*.h5'
    bonsai_v = 1
    tsample = [[87586.4627610, 88359.5568742],
               [103563.741102, 103778.489467]]

# Define transform parameters. See 'ch_frb_rfi/chain.py' for a list of available parameters.
p = ch_frb_rfi.transform_parameters(plot_type = 'web_viewer' if web else 'big', 
                                    bonsai_output_plot_stem = 'triggers', 
                                    maskpath = '/data/pathfinder/rfi_masks/rfi_20160705.dat',
                                    clipper_niter = 3,
                                    detrender_niter = 2,
                                    kfreq = kfreq)

# Define the chain of transforms. test_16k() is currently empty; it's a working template
# for future developments.
t = [ ch_frb_rfi.test_16k() ]
t += ch_frb_rfi.transform_chain(p)

# Read filenames into a list
if ts_mode:
    path = path[:-4]
    print "processing tsample(%s, %s)" % (tsample[ts_n][0], tsample[ts_n][1])
    s = rf_pipelines.chime_stream_from_times(path, tsample[ts_n][0], tsample[ts_n][1])
else:
    s = ch_frb_rfi.acquisitions.sample(path, start, end)

# Append a bonsai_dedisperser to the list of transforms.
t += [ eval('ch_frb_rfi.bonsai.nfreq%sK_3tree(p, bonsai_v)' % kfreq) ]

# Create a name for the output directory.
dirname = '%sK-%dD-%dC' % (kfreq, p.detrender_niter, p.clipper_niter)

# Run the pipeline (not) for web_viewer.
if not web:
    s.run(t, outdir=dirname)
else:
    ch_frb_rfi.run_for_web_viewer(dirname, s, t)
