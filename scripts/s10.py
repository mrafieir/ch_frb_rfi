#!/usr/bin/env python
"""
B0329; rfi_level = 1
"""

import numpy as np
import ch_frb_rfi
import rf_pipelines

s = ch_frb_rfi.acquisitions.incoherent_pathfinder(search_name='frb_incoherent_2b', sample_index=2)

p = ch_frb_rfi.transform_parameters(plot_type = 'web_viewer',
                                    make_plots = True,
                                    bonsai_output_plot_stem = 'triggers',
                                    maskpath = '/data/pathfinder/rfi_masks/rfi_20160705.dat',
                                    detrender_niter = 2,
                                    clipper_niter = 3,
                                    spline = True,
                                    bonsai_use_analytic_normalization = False,
                                    bonsai_hdf5_output_filename = None,
                                    bonsai_nt_per_hdf5_file = None,
                                    bonsai_fill_rfi_mask = True,
                                    var_est = False,
                                    mask_filler = False,
                                    mask_filler_w_cutoff = 0.5,
                                    bonsai_plot_threshold1 = 7,
                                    bonsai_plot_threshold2 = 10,
                                    bonsai_dynamic_plotter = False,
                                    bonsai_plot_all_trees = True,
                                    L1Grouper_thr = 10,
                                    bonsai_event_outfile = 'events_s10')

t = ch_frb_rfi.transform_chain(p)
t += [ ch_frb_rfi.bonsai.nfreq1K_7tree(p, v=3) ]

ch_frb_rfi.run_for_web_viewer('s10', s, t)

print ":::::::::::: s10 done ::::::::::::"
