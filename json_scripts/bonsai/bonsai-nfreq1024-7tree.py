#!/usr/bin/env python

import rf_pipelines
import ch_frb_rfi

# To guard against accidentally overwriting git-managed json files
clobber = False

# I forgot the reason why v2 no longer exists!
for version in [ 3, 4 ]:
    config_filename = '/data/bonsai_configs/bonsai_nfreq1024_7tree_v%s.hdf5' % version
    json_filename = '../../json_files/bonsai_1k/bonsai_nfreq1024_7tree_v%s.json' % version

    t = rf_pipelines.bonsai_dedisperser(config_filename = config_filename,
                                        fill_rfi_mask = True,
                                        img_prefix = 'triggers',
                                        img_ndm = 256,
                                        img_nt = 256,
                                        downsample_nt = 16,
                                        n_zoom = 4,
                                        plot_threshold1 = 7,
                                        plot_threshold2 = 10,
                                        plot_all_trees = True)

    rf_pipelines.utils.json_write(json_filename, t, clobber=clobber)
