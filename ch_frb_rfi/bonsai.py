"""
Each function in this module returns a bonsai_dedisperser transform,
which can be appended to an rf_pipelines transform chain.

See ch_frb_io/bonsai_configs/README.md for descriptions of the bonsai
transforms defined here.
"""

import os
import h5py
import rf_pipelines

from . import chains


def _make_dedisperser(parameters, bonsai_config_hdf5_basename):
    assert isinstance(parameters, chains.transform_parameters)

    # Default
    nt_per_file = 16384

    # If waterfall plots are being made, keep bonsai plots in sync.
    if parameters.make_plots:
        nt_per_file = parameters.plot_nxpix * parameters.plot_downsample_nt

    return rf_pipelines.bonsai_dedisperser(config_hdf5_filename = os.path.join('/data/bonsai_configs', bonsai_config_hdf5_basename),
                                           trigger_hdf5_filename = parameters.bonsai_output_hdf5_filename,
                                           trigger_plot_stem = parameters.bonsai_output_plot_stem,
                                           nt_per_file = nt_per_file)


def nfreq1024_singletree(parameters):
    return _make_dedisperser(parameters, 'bonsai_nfreq1024_singletree_v1.hdf5')

def nfreq1024_3tree(parameters):
    return _make_dedisperser(parameters, 'bonsai_nfreq1024_3tree_v1.hdf5')

def nfreq16K_3tree(parameters):
    return _make_dedisperser(parameters, 'bonsai_nfreq16K_3tree_v1.hdf5')
