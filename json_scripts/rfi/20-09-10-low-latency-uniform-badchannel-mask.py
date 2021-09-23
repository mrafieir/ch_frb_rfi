#!/usr/bin/env python
#
# This is a 16K RFI-removal config with an overall 4-sec latency and a uniform
# nt_chunk size in clipping transforms.  It uses a static badchannel mask (see
# below) for suppressing false positives during RFI storms (based on analysis
# of acquisitions obtained in August and September 2020).

import ch_frb_rfi
import rf_pipelines

# If 'clobber' is False, then when a json file is created with rf_pipelines.json_write(filename, j),
# we throw an exception if 'filename' already exists, and its contents differ from 'j'.  This is
# to prevent git-managed json files from being modified accidentally.
clobber = False

# The following freq ranges were identified as the source of false positives during RFI storms
# in August and September 2020.  See 'json_files/acqs/20-09-07-masoud-rfi-storms-runlist.json'
# for a list of runs which contain such storms.
mask = [[ 440.2099609375, 440.4052734375 ],
        [ 417.1630859375, 417.6269531250 ],
        [ 418.3105468750, 419.2138671875 ],
        [ 781.8115234375, 786.6943359375 ]]

for make_plots in [ False, True ]:
    params = ch_frb_rfi.transform_parameters(plot_type = 'web_viewer',
                                             plot_nypix = 1024,
                                             plot_nxpix = 256,
                                             plot_downsample_nt = 4,        # Smaller ratio compared to the usual 16.
                                             plot_nzoom = 4,
                                             max_nt_buffer = 4,
                                             make_plots = make_plots,
                                             bonsai_plot_nypix = 1024,
                                             bonsai_output_plot_stem = 'triggers' if make_plots else None,
                                             maskpath = None,
                                             mask = mask,
                                             detrender_niter = 2,
                                             clipper_niter = 6,
                                             two_pass = False,
                                             rfi_level = -1,
                                             aux_clip_first = False,
                                             aux_clip_last = False,
                                             aux_detrend_first = False,
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
                                             bonsai_plot_all_trees = make_plots,
                                             detrend_last = False,
                                             mask_counter = True)

    t1k = ch_frb_rfi.transform_chain(params)
    p1k = rf_pipelines.pipeline(t1k)

    t16k = [ rf_pipelines.wi_sub_pipeline(p1k, nfreq_out=1024, nds_out=1) ]

    params.detrend_last = True
    params.mask_counter = False

    t16k += ch_frb_rfi.chains.detrender_chain(params, ix=1, jx=0)

    if make_plots:
        params.plot_nypix = 1024 * 16       # The last waterfall is plotted in 16K.
        params.append_plotter_transform(t16k, 'dc_out_last')

    p16k = rf_pipelines.pipeline(t16k)
    
    suffix = '' if make_plots else '-noplot'
    filename = '../../json_files/rfi_16k/20-09-10-low-latency-uniform-badchannel-mask%s.json' % suffix

    rf_pipelines.utils.json_write(filename, p16k, clobber=clobber)
