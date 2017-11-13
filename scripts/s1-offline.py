#!/usr/bin/env python
"""A faint source at low DM. In this example we use the offline mask_filler."""

import numpy as np
import ch_frb_rfi
import rf_pipelines

s = ch_frb_rfi.acquisitions.incoherent_pathfinder(search_name='frb_incoherent_search_3', sample_index=6)

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
                                    var_filename = './var_s1.h5',
                                    mask_filler_w_cutoff = 0.5,
                                    bonsai_plot_threshold1 = 7,
                                    bonsai_plot_threshold2 = 10,
                                    bonsai_dynamic_plotter = False,
                                    bonsai_plot_all_trees = True,
                                    L1Grouper_thr = 7,
                                    bonsai_event_outfile = 'events_s1_offline')

t = ch_frb_rfi.transform_chain(p)

# Combine stream and transforms into a pipeline.
pipeline = rf_pipelines.pipeline([s]+t)

ch_frb_rfi.run_in_scratch_dir('s1_offline', pipeline)

# In the v16 API, need to "unbind" the pipeline after running, before its constituent
# pipeline_objects can be reused in another pipeline run.
pipeline.unbind()

(p.var_est, p.mask_filler, p.make_plots) = (False, True, True)

t = ch_frb_rfi.transform_chain(p)
t += [ ch_frb_rfi.bonsai.nfreq1K_7tree(p, fpga_counts_per_sample=512, v=3) ]

pipeline = rf_pipelines.pipeline([s]+t)
ch_frb_rfi.run_for_web_viewer('s1_offline', pipeline)

print ":::::::::::: s1_offline done ::::::::::::"
