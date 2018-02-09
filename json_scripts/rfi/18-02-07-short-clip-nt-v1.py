#!/usr/bin/env python
#
# 16K RFI removal for waterfalling short acq
# 1024 time samples are a min requirement.

import ch_frb_rfi
import rf_pipelines
from ch_frb_rfi import write_mask
import numpy as np
from glob import glob

def run_rf_pipelines(filename_list, output_directory, output_acq_name, output_filename):

    # If 'clobber' is False, then when a json file is created with rf_pipelines.json_write(filename, j),
    # we throw an exception if 'filename' already exists, and its contents differ from 'j'.  This is
    # to prevent git-managed json files from being modified accidentally.
    clobber = True
    
    params = ch_frb_rfi.transform_parameters(plot_type = 'web_viewer',
                                             make_plots = False,
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
    t16k += [write_mask.WriteWeights(basename = output_filename)]
    p16k = rf_pipelines.pipeline(t16k)
    
    s = rf_pipelines.chime_frb_stream_from_filename_list(filename_list, nt_chunk=1024, noise_source_align= 0)
    ch_frb_rfi.utils.run_in_custom_dir(output_directory,output_acq_name, s , p16k)

def main():
    filename_list = [
                
            "/home/patelchi/astro_98134_2018129302653857_beam0000_00258920_01.msgpack",
            "/home/patelchi/astro_98134_2018129302653857_beam0000_00258921_01.msgpack",
            "/home/patelchi/astro_98134_2018129302653857_beam0000_00258922_01.msgpack",
    #        "/home/patelchi/astro_98252_20181293330523560_beam0000_00259127_01.msgpack",
    #        "/home/patelchi/astro_98252_20181293330523560_beam0000_00259128_01.msgpack",
    #        "/home/patelchi/astro_98252_20181293330523560_beam0000_00259129_01.msgpack"
        ]
    output_filename = "test"
    output_acq_name = "chitrang_test_run_98134"
    output_directory = "./"
    run_rf_pipelines(filename_list, output_directory, output_acq_name, output_filename) 
    files = glob(output_directory+'/%s*.npz'%output_filename)
    files.sort()
    fs = [np.load(f) for f in files]
    intensity = [f['intensity'] for f in fs]
    weights = [f['weights'] for f in fs]
    intensity_combined = np.hstack(intensity)[::-1]
    weights_combined = np.hstack(weights)[::-1]
    np.savez('test_run_98134.npz', intensity=intensity_combined, weights=weights_combined)

if __name__ == "__main__":
    main()
