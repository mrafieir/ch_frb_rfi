#!/usr/bin/env python
#
# This script is intended to be run on frb1.physics.mcgill.ca.
#
# The 'adversarial_masker' is a transform intended to stress-test the online variance
# estimation logic by masking regions of the input array. If the online variance 
# estimation logic is working well, then the  trigger plots shouldn't show any false positives!
#
# This script runs the adversarial_masker and creates an 'adversarial_masker'
# web viewer entry.


import numpy.random 
import rf_pipelines
import ch_frb_rfi

# Total size of timestream, currently set by hand.
# If the adversarial_masker code is extended to include more rectangles,
# nt_tot will probably need to be increased!
nt_tot = 700 * 1024 * 6
    

s = rf_pipelines.gaussian_noise_stream(nfreq=1024, 
                                       nt_tot = nt_tot,
                                       freq_lo_MHz = 400.0, 
                                       freq_hi_MHz = 800.0, 
                                       dt_sample = 1.0e-3)

t_masker = rf_pipelines.adversarial_masker()

t_plotter = rf_pipelines.plotter_transform(img_prefix='waterfall1', 
                                           img_nfreq = 256,
                                           img_nt = 256,
                                           downsample_nt = 16,
                                           n_zoom = 6)

t_dedisp = rf_pipelines.bonsai_dedisperser(config_filename = '/data/bonsai_configs/bonsai_nfreq1024_7tree_v1.txt',
                                           img_prefix = 'toy_pipeline',
                                           img_ndm = 256,
                                           img_nt = 256,
                                           downsample_nt = 16,
                                           n_zoom = 6,
                                           plot_all_trees = True)

ch_frb_rfi.run_for_web_viewer('adversarial_masker', s, [t_masker,t_plotter,t_dedisp])
