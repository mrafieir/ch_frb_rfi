#!/usr/bin/env python
import ch_frb_rfi

# From the list below, select a sample index to process.
sample = 3
# The first file index (starts at 0).
start = 0 
# The last file index (has no limit; must be greater than 'start').
end = 400
# Indicate whether to use the web_viewer as output.
web = True

assert end > start >=0, "baseband_26m: Invalid (start, end) file indeces"
assert type(web) is bool

# This is a constantly changing list of samples. We will hopefully incorporate 
# this (perhaps as a unified dictionary) in 'acquisitions.py' and 'bonsai.py'.
# 'kfreq' is the upchannelization (from 1K=1024) factor. 'nypix' may be adjusted
# so that each pixel (on waterfall plots) corresponds to a unique frequency channel.
if sample == 1:
    kfreq = 1
    path = '/data2/acqhack_b1937_1K/*.h5'
    bonsai_v = 1
    nypix = 1024

if sample == 2:
    kfreq = 1
    path = '/data2/baseband_26m_b1937_16_04_22/1k_B1937/*.h5'
    bonsai_v = 2
    nypix = 1024

if sample == 3:
    kfreq = 16
    path = '/data2/baseband_26m_b1937_16_04_22/*.h5'
    bonsai_v = 1
    nypix = 16384

if sample == 4:
    kfreq = 128
    path = '/data2/baseband_26m_b1937_16_04_22/128k/*.h5'
    bonsai_v = 1
    nypix = 131072

# Define transform parameters. See 'ch_frb_rfi/chain.py' for a list of available parameters.
p = ch_frb_rfi.transform_parameters(plot_type='web_viewer' if web else 'big', 
                                    bonsai_output_plot_stem='triggers', 
                                    mask=[[730,760]],
                                    clipper_niter=2,
                                    detrender_niter=2,
                                    plot_nypix=nypix,
                                    plot_nxpix=1200,
                                    kfreq=kfreq)

# Define the chain of transforms. test_16k() is currently empty; it's a working template
# for future developments.
t = [ ch_frb_rfi.test_16k() ]
t += ch_frb_rfi.transform_chain(p)

# Read filenames into a list
s = ch_frb_rfi.acquisitions.sample(path, start, end)

# Append a bonsai_dedisperser to the list of transforms.
t += [ eval('ch_frb_rfi.bonsai.nfreq%sK_3tree(p, bonsai_v)' % kfreq) ]

# Create a name for the output directory.
dirname = '%sK_baseband_26m_d%d%dc' % (kfreq, p.detrender_niter, p.clipper_niter)

# Run the pipeline (not) for web_viewer.
if not web:
    s.run(t, outdir=dirname)
else:
    ch_frb_rfi.run_for_web_viewer(dirname, s, t)
