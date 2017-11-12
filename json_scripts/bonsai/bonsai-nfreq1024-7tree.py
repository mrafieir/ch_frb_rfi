#!/usr/bin/env python

import rf_pipelines
import ch_frb_rfi

# To guard against accidentally overwriting git-managed json files
clobber = False

for version in [ 3, 4 ]:
    config_filename = '/data/bonsai_configs/bonsai_nfreq1024_7tree_v%s.hdf5' % version
    json_filename1 = '../../json_files/bonsai_1k/bonsai_nfreq1024_7tree_v%s.json' % version
    json_filename2 = '../../json_files/bonsai_1k/bonsai_nfreq1024_7tree_v%s-noplot.json' % version

    # FIXME: currently, there are two versions of the bonsai_dedisperser, written in C++ and python.
    # In the pipeline json output, they are represented as 'bonsai_dedisperser_python' and 'bonsai_dedisperser_cpp'.
    # The two versions of the bonsai_dedisperser will be combined eventually!
    #
    # We use the C++ version in the "-noplot" case, and the python version in the "with-plot" case.
    # This is because the C++ version is needed for 'rfp-time', and the python version implements plotting.

    t1 = rf_pipelines.bonsai_dedisperser(config_filename = config_filename,
                                         fill_rfi_mask = True,
                                         img_prefix = 'triggers',
                                         img_ndm = 256,
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
