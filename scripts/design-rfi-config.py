#!/usr/bin/env python
#
# This script comes in handy for fine-tuning the RFI transform chain.

import glob
import numpy as np
import ch_frb_rfi
import rf_pipelines

stream_files='/data/frb-archiver/acq_data/frb_B0329+54_2018-10-26-01-50/beam_0141'
s = ch_frb_rfi.utils.sample(stream_files+'/chunk*.msg', 10, 100, msg=True)

# s.append(ch_frb_rfi.WriteWeights(nt_chunk=1024*2))

detrend_16k = True
write_json = True
output_path = './design-rfi-config_chain.json'

params = ch_frb_rfi.transform_parameters(plot_type = 'web_viewer',
                                         plot_nypix = 1024,
                                         plot_nxpix = 256,
                                         plot_downsample_nt = 16,
                                         plot_nzoom = 4,
                                         max_nt_buffer = 10,
                                         make_plots = True,
                                         bonsai_output_plot_stem = 'triggers',
                                         bonsai_plot_nypix = 1024,
                                         #maskpath = None,
                                         maskpath = '/data/pathfinder/rfi_masks/rfi_20160705.dat',
                                         #detrender_niter = 3,
                                         #clipper_niter = 5,
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
                                         bonsai_plot_all_trees = True,
                                         detrend_last = not detrend_16k)

t1k = ch_frb_rfi.transform_chain(params)
p1k = rf_pipelines.pipeline(t1k)

t16k = [ rf_pipelines.wi_sub_pipeline(p1k, nfreq_out=1024, nds_out=1) ]

if detrend_16k:
    params.detrend_last = True
    t16k += ch_frb_rfi.chains.detrender_chain(params, ix=1, jx=0)
    params.append_plotter_transform(t16k, 'dc_out_last')

if write_json:
    assert isinstance(output_path, str) and output_path.endswith('.json')
    p16k = rf_pipelines.pipeline(t16k)
    rf_pipelines.utils.json_write(output_path, p16k, clobber=True)
    #rf_pipelines.utils.json_write('design-rfi-config_acq.json', s, clobber=True)

w = ch_frb_rfi.WriteWeights(nt_chunk=1024*2) 
t16k += [ w, ch_frb_rfi.bonsai.nfreq16K_production(params, 2, False) ]

p16k = rf_pipelines.pipeline([s]+t16k)
ch_frb_rfi.run_for_web_viewer('design-rfi-config', p16k)

print 'design-rfi-config done!'
