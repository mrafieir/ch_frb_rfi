#!/usr/bin/env python
import numpy as np
import ch_frb_rfi
import rf_pipelines

norm_trig = False

v1_chunk = 32
v2_chunk = 192
rfi_level = 2

acquisition_index = 'ex_pulsar0'
s = ch_frb_rfi.acquisitions.ex_pulsar_search0()

p = ch_frb_rfi.transform_parameters(plot_type = 'web_viewer', 
                                    bonsai_output_plot_stem = 'triggers', 
                                    maskpath = '/data/pathfinder/rfi_masks/rfi_20160705.dat',
                                    rfi_level = rfi_level,
                                    bonsai_use_analytic_normalization = False, 
                                    bonsai_hdf5_output_filename = None,
                                    bonsai_nt_per_hdf5_file = None,
                                    var_est = not norm_trig,
                                    var_path = '/data2/var_est/example2/acq%s_r%d' % (acquisition_index, rfi_level),
                                    variance_estimator_v1_chunk = v1_chunk,
                                    variance_estimator_v2_chunk = v2_chunk,
                                    mask_filler = '/data2/var_est/example2/acq%s_r%d_v1_%d_v2_%d.h5' %\
                                                  (acquisition_index, rfi_level, v1_chunk, v2_chunk) if norm_trig else None,
                                    mask_filler_w_cutoff = 0.5,
                                    kfreq = 1)

t = ch_frb_rfi.transform_chain(p)
if norm_trig:
    t += [ ch_frb_rfi.bonsai.nfreq1K_3tree(p, 1) ]

ch_frb_rfi.run_for_web_viewer('example2', s, t)
