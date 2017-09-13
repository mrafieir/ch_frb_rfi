"""
Each function in this module returns a bonsai_dedisperser transform,
which can be appended to an rf_pipelines transform chain.

See ch_frb_io/bonsai_configs/README.md for descriptions of the bonsai
transforms defined here.
"""

import os
import h5py
import rf_pipelines
import rf_pipelines.rf_pipelines_c

from . import chains


def make_dedisperser(parameters, config_filename):
    assert isinstance(parameters, chains.transform_parameters)

    if (parameters.bonsai_output_plot_stem is not None) and (not parameters.make_plots):
        raise RuntimeError("ch_frb_rfi.transform_parameters: it is now an error to specify 'bonsai_output_plot_stem' without specifying 'plot_type'")

    return rf_pipelines.bonsai_dedisperser(config_filename = config_filename, 
                                           fill_rfi_mask = parameters.bonsai_fill_rfi_mask,
                                           hdf5_output_filename = parameters.bonsai_hdf5_output_filename, 
                                           nt_per_hdf5_file = parameters.bonsai_nt_per_hdf5_file,
                                           use_analytic_normalization = parameters.bonsai_use_analytic_normalization,
                                           img_prefix = parameters.bonsai_output_plot_stem, 
                                           img_ndm = parameters.bonsai_plot_nypix, 
                                           img_nt = parameters.plot_nxpix, 
                                           downsample_nt = parameters.plot_downsample_nt, 
                                           n_zoom = parameters.plot_nzoom,
                                           plot_threshold1 = parameters.bonsai_plot_threshold1,
                                           plot_threshold2 = parameters.bonsai_plot_threshold2,
                                           dynamic_plotter = parameters.bonsai_dynamic_plotter, 
                                           plot_all_trees = parameters.bonsai_plot_all_trees,
                                           event_outfile = parameters.bonsai_event_outfile,
                                           L1Grouper_thr = parameters.L1Grouper_thr,
                                           L1Grouper_beam = parameters.L1Grouper_beam,
                                           L1Grouper_addr = parameters.L1Grouper_addr)

# -------------------------------------------------------------------------------------------------------

def _config(basename):
    return os.path.join('/data/bonsai_configs', basename)
        

def nfreq1024_singletree(parameters):
    return make_dedisperser(parameters, _config('bonsai_nfreq1024_singletree_v1.hdf5'))

def nfreq1K_3tree(parameters, v):
    return make_dedisperser(parameters, _config('bonsai_nfreq1024_3tree_v%s.hdf5' % v))

def nfreq1K_7tree(parameters, v=1):
    return make_dedisperser(parameters, _config('bonsai_nfreq1024_7tree_v%s.hdf5' % v))

def nfreq16K_3tree(parameters, v):
    return make_dedisperser(parameters, _config('bonsai_nfreq16K_3tree_v%s.hdf5' % v))

def nfreq128K_3tree(parameters, v):
    return make_dedisperser(parameters, _config('bonsai_nfreq128K_3tree_v%s.hdf5' % v))

def nfreq16K_7tree(parameters, v=1):
    return make_dedisperser(parameters, _config('bonsai_nfreq16K_7tree_v%s.hdf5' % v))
