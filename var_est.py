#!/usr/bin/env python
import numpy as np
import ch_frb_rfi
import rf_pipelines

s = ch_frb_rfi.acquisitions.sample('/data2/17-02-08-incoherent-data-avalanche/frb_incoherent_search_0/*.h5', 0, 2)

p = ch_frb_rfi.transform_parameters(plot_type = 'web_viewer', 
                                    bonsai_output_plot_stem = 'triggers', 
                                    maskpath = '/data/pathfinder/rfi_masks/rfi_20160705.dat',
                                    rfi_level = 1,
                                    kfreq = 1)

t = ch_frb_rfi.transform_chain(p)
t += [ ch_frb_rfi.bonsai.nfreq1K_3tree(p, 1) ]

ch_frb_rfi.run_for_web_viewer('var_est', s, t)
