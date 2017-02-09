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
    ibeam = 0

    # If waterfall plots are being made, keep bonsai plots in sync.
    if parameters.make_plots:
        nt_per_file = parameters.plot_nxpix * parameters.plot_downsample_nt

    # This block of code has been written in an awkward way, which happens to work
    # in both rf_pipelines v11 (the current master branch) and v12_devel (in which case
    # it returns the "old" C++ bonsai_dedisperser, not the "new" python version).
    #
    # When rf_pipelines v12 is finished and merged to master, we can replace this
    # block of code by a call to rf_pipelines.bonsai_dedispeser(), which will return
    # the "new" python transform.

    import rf_pipelines.rf_pipelines_c
    config_filename = os.path.join('/data/bonsai_configs', bonsai_config_hdf5_basename)
    trigger_filename = parameters.bonsai_output_hdf5_filename if parameters.bonsai_output_hdf5_filename else ''
    trigger_plot_stem = parameters.bonsai_output_plot_stem if parameters.bonsai_output_plot_stem else ''
    return rf_pipelines.rf_pipelines_c.make_bonsai_dedisperser(config_filename, trigger_filename, trigger_plot_stem, nt_per_file, ibeam)


def nfreq1024_singletree(parameters):
    return _make_dedisperser(parameters, 'bonsai_nfreq1024_singletree_v1.hdf5')

def nfreq1024_3tree(parameters, v):
    return _make_dedisperser(parameters, 'bonsai_nfreq1024_3tree_v%s.hdf5' %v)

def nfreq16K_3tree(parameters, v):
    return _make_dedisperser(parameters, 'bonsai_nfreq16K_3tree_v%s.hdf5' %v)

def nfreq128K_3tree(parameters, v):
    return _make_dedisperser(parameters, 'bonsai_nfreq128K_3tree_v%s.hdf5' %v)
