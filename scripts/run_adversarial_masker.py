#!/usr/bin/env python
#
# This script is intended to be run on frb1.physics.mcgill.ca.
#
# The 'adversarial_masker' is a half-finished transform, intended to stress-test the
# online variance estimation logic by masking a bunch of rectangle-shaped regions of 
# the input array.  If the online variance estimation logic is working well, then the 
# trigger plots shouldn't show any false positives!
#
# This script runs the adversarial_masker and creates an 'adversarial_masker'
# web viewer entry.


import numpy.random 
import rf_pipelines
import ch_frb_rfi

bonsai_config_filename = '/data/bonsai_configs/bonsai_nfreq1024_7tree_f512_v3.hdf5'
nt_tot = 8192 * 1024
n_zoom = 8

s = rf_pipelines.gaussian_noise_stream(nfreq=1024, 
                                       nt_tot = nt_tot,
                                       freq_lo_MHz = 400.0, 
                                       freq_hi_MHz = 800.0, 
                                       dt_sample = 1.31072e-3)

t_masker = rf_pipelines.adversarial_masker()

t_plotter = rf_pipelines.plotter_transform(img_prefix='waterfall1', 
                                           img_nfreq = 256,
                                           img_nt = 256,
                                           downsample_nt = 16,
                                           n_zoom = n_zoom)

t_dedisp = rf_pipelines.bonsai_dedisperser(config_filename = bonsai_config_filename,
                                           fill_rfi_mask = True,
                                           img_prefix = 'toy_pipeline',
                                           img_ndm = 256,
                                           img_nt = 256,
                                           downsample_nt = 16,
                                           n_zoom = n_zoom,
                                           plot_all_trees = True)

ch_frb_rfi.run_for_web_viewer('adversarial_masker', s, [t_masker, t_plotter, t_dedisp])
