#!/usr/bin/env python

import rf_pipelines
import ch_frb_rfi

# To guard against accidentally overwriting git-managed json files
clobber = False

# Filenames are constructed from 'stems' as bonsai_production_$(stem).hdf5
stem_list = [ 'noups_nbeta1_v2', 'ups_nbeta1_v2' ]

for stem in stem_list:
    config_filename = '/data/bonsai_configs/bonsai_production_%s.hdf5' % stem
    json_filename1 = '../../json_files/bonsai/bonsai_production_%s.json' % stem
    json_filename2 = '../../json_files/bonsai/bonsai_production_%s-noplot.json' % stem

    # FIXME: currently, there are two versions of the bonsai_dedisperser, written in C++ and python.
    # In the pipeline json output, they are represented as 'bonsai_dedisperser_python' and 'bonsai_dedisperser_cpp'.
    # The two versions of the bonsai_dedisperser will be combined eventually!
    #
    # We use the C++ version in the "-noplot" case, and the python version in the "with-plot" case.
    # This is because the C++ version is needed for 'rfp-time', and the python version implements plotting.

    # Note: using large 'ndm' (1024)
    t1 = rf_pipelines.bonsai_dedisperser(config_filename = config_filename,
                                         fill_rfi_mask = True,
                                         img_prefix = 'triggers',
                                         img_ndm = 1024,
                                         img_nt = 256,
                                         downsample_nt = 16,
                                         n_zoom = 4,
                                         plot_threshold1 = 7,
                                         plot_threshold2 = 10,
                                         plot_all_trees = True)

    t2 = rf_pipelines.bonsai_dedisperser_cpp(config_filename = config_filename,
                                             fill_rfi_mask = True)
    
    rf_pipelines.utils.json_write(json_filename1, t1, clobber=clobber)
    rf_pipelines.utils.json_write(json_filename2, t2, clobber=clobber)

    
