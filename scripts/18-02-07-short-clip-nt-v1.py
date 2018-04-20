#!/usr/bin/env python
#
# 16K RFI removal for waterfalling short acq
# 1024 time samples are a min requirement.

import os
from glob import glob
import numpy as np
import ch_frb_rfi
import rf_pipelines


def run_rf_pipelines(filename_list, output_dir, output_acq_path):
    params = ch_frb_rfi.transform_parameters(plot_type = 'web_viewer',
                                             make_plots = False,
                                             bonsai_output_plot_stem = None,
                                             maskpath = None,
                                             two_pass = True,
                                             clip_nt = 1024,
                                             eq_clip_nt = True,
                                             detrend_nt = 1024,
                                             rfi_level = -1,
                                             aux_clip_first = True,
                                             aux_clip_last = True,
                                             aux_detrend_first = False,
                                             detrender_niter = 1,
                                             clipper_niter = 6,
                                             plot_nypix = 1024,
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

    t16k = [ rf_pipelines.wi_sub_pipeline(p1k, nfreq_out=1024, nds_out=1) ]

    params.detrend_last = True
    t16k += ch_frb_rfi.chains.detrender_chain(params, ix=1, jx=0)

    t16k += [ ch_frb_rfi.WriteWeights(basename=output_acq_path+'/data') ]
    p16k = rf_pipelines.pipeline(t16k)
    
    s = rf_pipelines.chime_frb_stream_from_filename_list(filename_list, nt_chunk=1024, noise_source_align=0)
    ch_frb_rfi.utils.run_in_scratch_dir(output_acq_path, output_dir, s, p16k)


def main(toplevel_dir='/frb-archiver-1', acq_name='test-18-02-07-short-clip-nt-v1'):

    assert isinstance(toplevel_dir, str)
    assert isinstance(acq_name, str)

    filename_list = ["/frb-archiver-1/2018/4/19/astro_6570662/intensity/raw/0138/astro_6570662_20180419220657569002_beam0138_00019667_01.msgpack",
                     "/frb-archiver-1/2018/4/19/astro_6570662/intensity/raw/0138/astro_6570662_20180419220657569002_beam0138_00019668_01.msgpack"]

    output_dir = os.path.join(toplevel_dir, os.environ['USER'])
    output_acq_path = os.path.join(output_dir, acq_name)

    run_rf_pipelines(filename_list, output_dir, output_acq_path)
    files = sorted(glob(output_acq_path+'/data*.npz'))

    fs = [np.load(f) for f in files]
    intensity = np.concatenate([f['intensity'] for f in fs], axis=1)
    weights = np.concatenate([f['weights'] for f in fs], axis=1)

    np.savez(output_acq_path+'/data_all.npz', intensity=intensity, weights=weights)

if __name__ == "__main__":
    main()
