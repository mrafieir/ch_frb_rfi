#!/usr/bin/env python
"""
This is an interesting example: It contains an RFI storm, a few false positives,
and some significant changes in the running variance.
"""

import numpy as np
import ch_frb_rfi
import rf_pipelines

s = ch_frb_rfi.acquisitions.incoherent_pathfinder(search_name='frb_incoherent_2d', sample_index=0)

p = ch_frb_rfi.transform_parameters(plot_type = 'web_viewer',
                                    make_plots = False,
                                    bonsai_output_plot_stem = 'triggers',
                                    maskpath = '/data/pathfinder/rfi_masks/rfi_20160705.dat',
                                    detrender_niter = 2,
                                    clipper_niter = 6,
                                    bonsai_use_analytic_normalization = False,
                                    bonsai_hdf5_output_filename = None,
                                    bonsai_nt_per_hdf5_file = None,
                                    var_est = True,
                                    mask_filler = False,
                                    var_filename = './var_s9.h5',
                                    mask_filler_w_cutoff = 0.5,
                                    bonsai_plot_threshold1 = 7,
                                    bonsai_plot_threshold2 = 10,
                                    bonsai_dynamic_plotter = False,
                                    bonsai_plot_all_trees = True,
                                    L1Grouper_thr = 10,
                                    bonsai_event_outfile = 'events_s9')

t = ch_frb_rfi.transform_chain(p)

ch_frb_rfi.run_in_scratch_dir('s9', s, t)

(p.var_est, p.mask_filler, p.make_plots) = (False, True, True)

t = ch_frb_rfi.transform_chain(p)
t += [ ch_frb_rfi.bonsai.nfreq1K_7tree(p, 1) ]

ch_frb_rfi.run_for_web_viewer('s9', s, t)

print ":::::::::::: s9 done ::::::::::::"
