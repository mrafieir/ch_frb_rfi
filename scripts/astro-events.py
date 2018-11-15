#!/usr/bin/env python
#
# This script comes in handy for post-processing astro events.

import glob
import numpy as np
import ch_frb_rfi
import rf_pipelines

stream_files = '/frb-archiver-1/2018/4/2/astro_519866/intensity/raw/0118/'
s = ch_frb_rfi.utils.sample(stream_files+'/*.msgpack', 0, 12, msg=True)

write_json = True
detrend_16k = True

params = ch_frb_rfi.transform_parameters(plot_type = 'web_viewer',
                                         plot_nypix = 1024,
                                         plot_nxpix = 256,
                                         plot_downsample_nt = 16,
                                         plot_nzoom = 4,
                                         make_plots = False,
                                         bonsai_plot_nypix = 1024,
                                         maskpath = None,
                                         detrender_niter = 3,
                                         clipper_niter = 5,
                                         spline = True,
                                         bonsai_use_analytic_normalization = False,
                                         bonsai_hdf5_output_filename = None,
                                         bonsai_nt_per_hdf5_file = None,
                                         bonsai_fill_rfi_mask = False,
                                         var_est = True,
                                         var_filename = './astro-events_var.h5',
                                         variance_estimator_v1_chunk = 16,
                                         variance_estimator_v2_chunk = 64,
                                         mask_filler = False,
                                         mask_filler_w_cutoff = 0.5,
                                         bonsai_plot_threshold1 = 7,
                                         bonsai_plot_threshold2 = 10,
                                         bonsai_dynamic_plotter = False,
                                         bonsai_plot_all_trees = False,
                                         detrend_last = not detrend_16k)

t1k = ch_frb_rfi.transform_chain(params)
p1k = rf_pipelines.pipeline(t1k)

t16k = [ rf_pipelines.wi_sub_pipeline(p1k, nfreq_out=1024, nds_out=1) ]

if detrend_16k:
    params.detrend_last = True
    t16k += ch_frb_rfi.chains.detrender_chain(params, ix=1, jx=0)
    params.append_plotter_transform(t16k, 'dc_out_last')

if write_json:
    p16k = rf_pipelines.pipeline(t16k)
    rf_pipelines.utils.json_write('./astro-events_chain.json', p16k, clobber=True)

t16k += [ ch_frb_rfi.bonsai.nfreq16K_production(params, 2, False) ]
p16k = rf_pipelines.pipeline([s]+t16k)

ch_frb_rfi.run_in_scratch_dir('astro-events', None, p16k)
p16k.unbind()

params.var_est = False
params.mask_filler = True
params.make_plots = True
params.bonsai_plot_all_trees = True
params.bonsai_output_plot_stem = 'triggers'

t1k = ch_frb_rfi.transform_chain(params)
p1k = rf_pipelines.pipeline(t1k)

t16k = [ rf_pipelines.wi_sub_pipeline(p1k, nfreq_out=1024, nds_out=1) ]

if detrend_16k:
    params.detrend_last = True
    t16k += ch_frb_rfi.chains.detrender_chain(params, ix=1, jx=0)
    params.append_plotter_transform(t16k, 'dc_out_last')

t16k += [ ch_frb_rfi.bonsai.nfreq16K_production(params, 2, False) ]
p16k = rf_pipelines.pipeline([s]+t16k)

ch_frb_rfi.run_for_web_viewer('astro-events', p16k)

print 'astro-events done!'
