#!/usr/bin/env python
#
# 16K RFI removal with a 4-sec latency!

import ch_frb_rfi
import rf_pipelines

# If 'clobber' is False, then when a json file is created with rf_pipelines.json_write(filename, j),
# we throw an exception if 'filename' already exists, and its contents differ from 'j'.  This is
# to prevent git-managed json files from being modified accidentally.
clobber = False

for make_plots in [ False, True ]:
    params = ch_frb_rfi.transform_parameters(plot_type = 'web_viewer',
                                             plot_nypix = 1024,
                                             plot_nxpix = 256,
                                             plot_downsample_nt = 16,
                                             plot_nzoom = 4,
                                             max_nt_buffer = 4,
                                             make_plots = make_plots,
                                             bonsai_plot_nypix = 1024,
                                             bonsai_output_plot_stem = 'triggers' if make_plots else None,
                                             maskpath = None,
                                             rfi_level = -1,
                                             aux_clip_first = True,
                                             aux_clip_last = True,
                                             aux_detrend_first = True,
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
                                             bonsai_plot_all_trees = False,
                                             detrend_last = False)

    t1k = ch_frb_rfi.transform_chain(params)
    p1k = rf_pipelines.pipeline(t1k)

    t16k = [ rf_pipelines.wi_sub_pipeline(p1k, nfreq_out=1024, nds_out=1) ]

    params.detrend_last = True
    t16k += ch_frb_rfi.chains.detrender_chain(params, ix=1, jx=0)

    p16k = rf_pipelines.pipeline(t16k)
    
    suffix = '' if make_plots else '-noplot'
    filename = '../../json_files/rfi_16k/18-10-25-low-latency-v1%s.json' % suffix

    rf_pipelines.utils.json_write(filename, p16k, clobber=clobber)
