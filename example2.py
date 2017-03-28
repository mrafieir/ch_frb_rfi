#!/usr/bin/env python
#
# This is an example script showing how to use ch_frb_rfi for properly removing RFI, 
# estimating the varinace, and hence correctly normalizing the output of the bonsai
# dedisperser. It is assumed that you have already studied 'example.py'.
#
# This script is intended to run on frb1.physics.mcgill.ca.

import numpy as np
import ch_frb_rfi
import rf_pipelines

# Let's choose an acquisition with a real pulsar!
acquisition_index = 'pulsar1'
s = ch_frb_rfi.acquisitions.ex_pulsar_search1()

# The following paramaters are explained in 'ch_frb_rfi/chains.py'.
(rfi_level, v1_chunk, v2_chunk) = (1, 32, 192)

p = ch_frb_rfi.transform_parameters(plot_nzoom = 0, # disable plotter transforms
                                    bonsai_plot_nypix = None,
                                    bonsai_output_plot_stem = 'triggers', 
                                    maskpath = '/data/pathfinder/rfi_masks/rfi_20160705.dat',
                                    rfi_level = rfi_level,
                                    bonsai_use_analytic_normalization = False, 
                                    bonsai_hdf5_output_filename = None,
                                    bonsai_nt_per_hdf5_file = None,
                                    var_est = True,
                                    var_path = '/data2/var_est/example2/acq%s_r%d' % (acquisition_index, rfi_level),
                                    variance_estimator_v1_chunk = v1_chunk,
                                    variance_estimator_v2_chunk = v2_chunk,
                                    mask_filler_w_cutoff = 0.5,
                                    kfreq = 1,
                                    bonsai_plot_threshold1 = 7,
                                    bonsai_plot_threshold2 = 10,
                                    bonsai_dynamic_plotter = False)

# Using the specified parameters make a chain of transforms for estimating the variance.
t = ch_frb_rfi.transform_chain(p)

# The variance estimates are saved in 'p.var_path'.
ch_frb_rfi.run_for_web_viewer('example2', s, t)

# Remove the variance_estimator, append the mask_filler and plotter transforms.
p.var_est = False
p.mask_filler = '/data2/var_est/example2/acq%s_r%d_v1_%d_v2_%d.h5' % (acquisition_index, rfi_level, v1_chunk, v2_chunk)
p.plot_type = 'web_viewer'

t = ch_frb_rfi.transform_chain(p)
t += [ ch_frb_rfi.bonsai.nfreq1K_3tree(p, 1) ]

# Run the pipeline (again) but now with the mask_filler and bonsai dedisperser.
ch_frb_rfi.run_for_web_viewer('example2', s, t)
