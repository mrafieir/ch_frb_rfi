#!/usr/bin/env python
import ch_frb_rfi

# From the list below, select a sample index to process.
sample = 1
# The first file index (starts at 0).
start = 0
# The last file index (has no limit; must be greater than 'start').
end = 60
# Indicate whether to use the web_viewer as output.
web = True

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

# Define transform parameters. See 'ch_frb_rfi/chain.py' for a list of available parameters.
p = ch_frb_rfi.transform_parameters(plot_type = 'web_viewer' if web else 'big', 
                                    bonsai_output_plot_stem = 'triggers', 
                                    maskpath = '/data/pathfinder/rfi_masks/rfi_20160705.dat',
                                    clipper_niter = 4,
                                    detrender_niter = 2,
                                    kfreq = kfreq)

# Define the chain of transforms. test_16k() is currently empty; it's a working template
# for future developments.
t = [ ch_frb_rfi.test_16k() ]
t += ch_frb_rfi.transform_chain(p)

# Read filenames into a list
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
