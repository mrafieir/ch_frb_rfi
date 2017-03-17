#!/usr/bin/env python
import numpy as np
import ch_frb_rfi
import rf_pipelines

test_bonsai = False

# ~20 sec of data; good for catching bugs!
s = ch_frb_rfi.acquisitions.sample('/data2/17-02-08-incoherent-data-avalanche/frb_incoherent_search_0/*.h5', 0, 1)

# ~21 hours of data
#s = ch_frb_rfi.acquisitions.incoherent_search1()

# Define (mostly rfi-related) transform parameters
p = ch_frb_rfi.transform_parameters(plot_type = 'web_viewer', 
                                    bonsai_output_plot_stem = 'triggers', 
                                    maskpath = '/data/pathfinder/rfi_masks/rfi_20160705.dat',
                                    rfi_level = 1,
                                    kfreq = 1)

# Transform chain
t = ch_frb_rfi.transform_chain(p)

# Append variance estimator to the chain
t += [ rf_pipelines.variance_estimator(v1_chunk=128, v2_chunk=80, nt_chunk=1024, fname=None) ]

# Append bonsai dedisperser
if test_bonsai:
    t += [ ch_frb_rfi.bonsai.nfreq1K_3tree(p, 1) ]

# Run the pipeline for web viewer
ch_frb_rfi.run_for_web_viewer('var_est', s, t)
