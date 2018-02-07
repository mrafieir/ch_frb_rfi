#!/usr/bin/env python
#
# 16K RFI removal for waterfalling short acq
# 1024 time samples are a min requirement.

import ch_frb_rfi
import rf_pipelines


# If 'clobber' is False, then when a json file is created with rf_pipelines.json_write(filename, j),
# we throw an exception if 'filename' already exists, and its contents differ from 'j'.  This is
# to prevent git-managed json files from being modified accidentally.
clobber = True


params = ch_frb_rfi.transform_parameters(plot_type = 'web_viewer',
                                         make_plots = True,
                                         bonsai_output_plot_stem = None,
                                         maskpath = None,
                                         clip_nt = 1024,
                                         detrend_nt = 1024,
                                         detrender_niter=1,
                                         clipper_niter=6,
                                         plot_nypix=1024,
                                         plot_nxpix = 256,
                                         plot_downsample_nt = 1,
                                         plot_nzoom = 2,
                                         spline = True,
                                         bonsai_use_analytic_normalization = False,
                                         bonsai_hdf5_output_filename = None,
                                         bonsai_nt_per_hdf5_file = None,
                                         bonsai_fill_rfi_mask = False,
                                         var_est = False,
                                         mask_filler = False,
                                         bonsai_dynamic_plotter = False,
                                         bonsai_plot_all_trees = False)

t1k = ch_frb_rfi.transform_chain(params)
p1k = rf_pipelines.pipeline(t1k)

params.detrend_last = True
_t1k = ch_frb_rfi.transform_chain(params)
_p1k = rf_pipelines.pipeline(_t1k)

t16k = [ rf_pipelines.wi_sub_pipeline(_p1k, nfreq_out=1024, nds_out=1) ]
t16k += ch_frb_rfi.chains.detrender_chain(params, ix=0)
p16k = rf_pipelines.pipeline(t16k)

filename = '../../json_files/rfi_16k/18-02-07-short-clip-nt-v1.json'
rf_pipelines.utils.json_write(filename, p16k, clobber=clobber)
