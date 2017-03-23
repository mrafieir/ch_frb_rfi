#!/usr/bin/env python
import numpy as np
import ch_frb_rfi
import rf_pipelines

test_script = False

acquisition_index = 1
norm_trig = True

v1_chunk = 128
v2_chunk = 80
outdir = '/data2/var_est'

w_cutoff = 0.5

# -------------------------------------------------------------------

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
elif acquisition_index == 3:
    s = ch_frb_rfi.acquisitions.ex_pulsar_search0()
elif acquisition_index == 4:
    s = ch_frb_rfi.acquisitions.incoherent_1d()
else:
    raise RuntimeError("var_est: invalid acquisition index!")

# Define transform parameters
p = ch_frb_rfi.transform_parameters(plot_type = 'web_viewer', 
                                    bonsai_output_plot_stem = 'triggers', 
                                    maskpath = '/data/pathfinder/rfi_masks/rfi_20160705.dat',
                                    rfi_level = 2,
                                    bonsai_use_analytic_normalization = False, 
                                    bonsai_hdf5_output_filename = None,
                                    bonsai_nt_per_hdf5_file = None,
                                    kfreq = 1)

fname = 'acq%s_r%d' % (acquisition_index, p.rfi_level)

# Transform chain
t = ch_frb_rfi.transform_chain(p)

if not norm_trig:
    # Append a variance estimator to the chain
    t += [ rf_pipelines.variance_estimator(v1_chunk=v1_chunk, v2_chunk=v2_chunk, fname=fname, outdir=outdir) ]
else:
    # Append the mask filler and bonsai dedisperser
    t += [ rf_pipelines.mask_filler(var_file='%s/%s_v1_%d_v2_%d.h5' % (outdir, fname, v1_chunk, v2_chunk), w_cutoff=w_cutoff) ]
    t += [ ch_frb_rfi.bonsai.nfreq1K_3tree(p, 1) ]

# Run the pipeline for web viewer
ch_frb_rfi.run_for_web_viewer('var_est', s, t)
