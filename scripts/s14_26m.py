#!/usr/bin/env python

import numpy as np
import ch_frb_rfi
import rf_pipelines

s = ch_frb_rfi.sample('/data/ugiri/20170425T231531Z_chime_beamformed_1/*.h5', 0, 1000)

p = ch_frb_rfi.transform_parameters(plot_type = 'web_viewer',
                                    maskpath = '/data/pathfinder/rfi_masks/rfi_20160705.dat',
                                    make_plots = True,
                                    bonsai_output_plot_stem = 'triggers', 
                                    rfi_level = 2,
                                    spline = True,
                                    bonsai_use_analytic_normalization = False,
                                    bonsai_fill_rfi_mask = True,
                                    var_est = False,
                                    mask_filler = False,
                                    kfreq = 16,
                                    bonsai_dynamic_plotter = False,
                                    bonsai_plot_all_trees = True,
                                    L1Grouper_thr = 10,
                                    #plot_nypix = 16384
                                   )

t = ch_frb_rfi.transform_chain(p)
t += [ ch_frb_rfi.bonsai.nfreq16K_7tree(p, 1) ]

ch_frb_rfi.run_for_web_viewer('s14_26m', s, t)

print ":::::::::::: s14_26m done ::::::::::::"
