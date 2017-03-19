#!/usr/bin/env python
import numpy as np
import ch_frb_rfi
import rf_pipelines

test_script = True

acquisition_index = 0
norm_trig = False

# Select an acquisition
if test_script is True:
    print "var_est: test in progress"
    acquisition_index = 'test'
    s = ch_frb_rfi.acquisitions.sample('/data2/17-02-08-incoherent-data-avalanche/frb_incoherent_search_0/*.h5', 0, 1)
elif acquisition_index == 0:
    s = ch_frb_rfi.acquisitions.incoherent_search0()
elif acquisition_index == 1:
    s = ch_frb_rfi.acquisitions.incoherent_search1()
elif acquisition_index == 2:
    s = ch_frb_rfi.acquisitions.incoherent_1c()
else:
    raise RuntimeError("var_est: invalid acquisition index!")

# Define transform parameters
p = ch_frb_rfi.transform_parameters(plot_type = 'web_viewer', 
                                    bonsai_output_plot_stem = 'triggers', 
                                    maskpath = '/data/pathfinder/rfi_masks/rfi_20160705.dat',
                                    rfi_level = 1,
                                    kfreq = 1)

# Transform chain
t = ch_frb_rfi.transform_chain(p)

if not norm_trig:
    # Append a variance estimator to the chain
    t += [ rf_pipelines.variance_estimator(v1_chunk=128, v2_chunk=80, nt_chunk=1024, fname='acq%s' % acquisition_index, outdir='/data2/var_est') ]
else:
    # Append the mask filler and bonsai dedisperser
    t += [ rf_pipelines.mask_filler() ]
    t += [ ch_frb_rfi.bonsai.nfreq1K_3tree(p, 1) ]

# Run the pipeline for web viewer
ch_frb_rfi.run_for_web_viewer('var_est', s, t)
