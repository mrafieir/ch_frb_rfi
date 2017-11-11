#!/usr/bin/env python
#
# First try at 16K RFI removal!
# Uses bonsai's online mask filler.
# Based on scripts/derippled.py (by Masoud)

import ch_frb_rfi
import rf_pipelines

# To guard against accidentally overwriting git-managed json files
clobber = True

for make_plots in [ False, True ]:
    params = ch_frb_rfi.transform_parameters(plot_type = 'web_viewer',
                                             make_plots = make_plots,
                                             bonsai_output_plot_stem = 'triggers' if make_plots else None,
                                             maskpath = '/data/pathfinder/rfi_masks/rfi_20160705.dat',
                                             detrender_niter = 2,
                                             clipper_niter = 6,
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
                                             bonsai_plot_all_trees = make_plots)

    t1k = ch_frb_rfi.transform_chain(params)
    p1k = rf_pipelines.pipeline(t1k)

    t16k = [ rf_pipelines.wi_sub_pipeline(p1k, nfreq_out=1024, nds_out=1) ]
    t16k += ch_frb_rfi.chains.detrender_chain(params, ix=0)
    p16k = rf_pipelines.pipeline(t16k)

    for (pobj, suffix) in [ (p1k,'1k'), (p16k,'16k') ]:
        suffix2 = '' if make_plots else '-noplot'
        filename = '../../json_files/rfi_%s/17-10-24-first-try%s.json' % (suffix, suffix2)
        rf_pipelines.utils.json_write(filename, pobj, clobber=clobber)

