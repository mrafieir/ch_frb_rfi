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

    trigger_filename = parameters.bonsai_output_hdf5_filename if parameters.bonsai_output_hdf5_filename else ''

    if not parameters.new_bonsai_transform:
        # Logic for old bonsai transform (preserved but will be phased out soon)
        #
        # This block of code has been written in an awkward way, which happens to work
        # in both rf_pipelines v11 (the current master branch) and v12_devel (in which case
        # it returns the "old" C++ bonsai_dedisperser, not the "new" python version).

        trigger_plot_stem = parameters.bonsai_output_plot_stem if parameters.bonsai_output_plot_stem else ''
        nt_per_file = (parameters.plot_nxpix * parameters.plot_downsample_nt) if parameters.make_plots else 16384
        ibeam = 0
        
        return rf_pipelines.rf_pipelines_c.make_bonsai_dedisperser(config_filename, trigger_filename, trigger_plot_stem, nt_per_file, ibeam)
       
    # New bonsai transform logic follows...

    if (parameters.bonsai_output_plot_stem is not None) and (not parameters.make_plots):
        raise RuntimeError("ch_frb_rfi.transform_parameters: it is now an error to specify 'bonsai_output_plot_stem' without specifying 'plot_type'")

    return rf_pipelines.bonsai_dedisperser(config_hdf5_filename = config_filename, 
                                           img_prefix = parameters.bonsai_output_plot_stem, 
                                           img_ndm = parameters.bonsai_plot_nypix, 
                                           img_nt = parameters.plot_nxpix, 
                                           downsample_nt = parameters.plot_downsample_nt, 
                                           n_zoom = parameters.plot_nzoom, 
                                           trigger_hdf5_filename = trigger_filename)


####################################################################################################


def _config(basename):
    return os.path.join('/data/bonsai_configs', basename)
        

def nfreq1024_singletree(parameters):
    return make_dedisperser(parameters, _config('bonsai_nfreq1024_singletree_v1.hdf5'))

def nfreq1K_3tree(parameters, v):
    return make_dedisperser(parameters, _config('bonsai_nfreq1024_3tree_v%s.hdf5' % v))

def nfreq16K_3tree(parameters, v):
    return make_dedisperser(parameters, _config('bonsai_nfreq16K_3tree_v%s.hdf5' % v))

def nfreq128K_3tree(parameters, v):
    return make_dedisperser(parameters, _config('bonsai_nfreq128K_3tree_v%s.hdf5' % v))
