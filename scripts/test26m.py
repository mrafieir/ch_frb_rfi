#!/usr/bin/env python

import numpy as np
import ch_frb_rfi
import rf_pipelines

s = ch_frb_rfi.sample('/data/ugiri/20170425T231531Z_chime_beamformed_1/*.h5', 0, 1000)

p = ch_frb_rfi.transform_parameters(plot_type = 'web_viewer',
                                    maskpath = '/data/pathfinder/rfi_masks/rfi_20160705.dat',
                                    make_plots = False,
                                    bonsai_output_plot_stem = 'triggers', 
                                    rfi_level = 2,
                                    bonsai_use_analytic_normalization = False, 
                                    var_est = True,
                                    var_filename = './var_test26m.h5',
                                    mask_filler_w_cutoff = 0.25,
                                    kfreq = 16,
                                    bonsai_dynamic_plotter = False,
                                    #plot_nypix = 16384
                                   )

t = ch_frb_rfi.transform_chain(p)

ch_frb_rfi.run_in_scratch_dir('test26m', s, t)

p.var_est = False; p.mask_filler = True; p.make_plots = True

t = ch_frb_rfi.transform_chain(p)
t += [ ch_frb_rfi.bonsai.nfreq16K_3tree(p, 1) ]

ch_frb_rfi.run_for_web_viewer('test26m', s, t)

print ":::::::::::: test26m done ::::::::::::"
