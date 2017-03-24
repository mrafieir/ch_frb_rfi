#!/usr/bin/env python
import numpy as np
import ch_frb_rfi
import rf_pipelines

test_script = False
norm_trig = True
acquisition_index = 5
v1_chunk = 128
v2_chunk = 80
outdir = '/data2/var_est'
rfi_level = 2

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
elif acquisition_index == 5:
    s = ch_frb_rfi.acquisitions.ex_storm_1d()
else:
    raise RuntimeError("var_est: invalid acquisition index!")

fname = 'acq%s_r%d' % (acquisition_index, rfi_level)

p = ch_frb_rfi.transform_parameters(plot_type = 'web_viewer', 
                                    bonsai_output_plot_stem = 'triggers', 
                                    maskpath = '/data/pathfinder/rfi_masks/rfi_20160705.dat',
                                    rfi_level = rfi_level,
                                    bonsai_use_analytic_normalization = False, 
                                    bonsai_hdf5_output_filename = None,
                                    bonsai_nt_per_hdf5_file = None,
                                    mask_filler = '%s/%s_v1_%d_v2_%d.h5' % (outdir, fname, v1_chunk, v2_chunk) if norm_trig else None,
                                    mask_filler_w_cutoff = 0.5,
                                    kfreq = 1)

t = ch_frb_rfi.transform_chain(p)

if not norm_trig:
    t += [ rf_pipelines.variance_estimator(v1_chunk=v1_chunk, v2_chunk=v2_chunk, fname=fname, outdir=outdir) ]
else:
    t += [ ch_frb_rfi.bonsai.nfreq1K_3tree(p, 1) ]

ch_frb_rfi.run_for_web_viewer('var_est', s, t)
