#!/usr/bin/env python
#
# This is an example script showing how to use ch_frb_rfi for properly removing RFI, 
# estimating the variance, and hence correctly normalizing the output of the bonsai
# dedisperser for a single-dish (i.e., the 26m telescope in this example) acquisition
# with 16K frequency channels. 
#
# It is assumed that you have already studied 'example.py' and 'example2.py'.
#
# This script is intended to run on frb1.physics.mcgill.ca.

import numpy as np
import ch_frb_rfi
import rf_pipelines

s = ch_frb_rfi.acquisitions.ex_crab_16k()

p = ch_frb_rfi.transform_parameters(plot_type = 'web_viewer',
                                    make_plots = False,
                                    bonsai_output_plot_stem = 'triggers', 
                                    rfi_level = 2,
                                    bonsai_use_analytic_normalization = False, 
                                    var_est = True,
                                    var_filename = './var_example3.h5',
                                    variance_estimator_v1_chunk = 32,
                                    variance_estimator_v2_chunk = 192,
                                    mask_filler_w_cutoff = 0.5,
                                    kfreq = 16,
                                    bonsai_plot_threshold1 = 7,
                                    bonsai_plot_threshold2 = 10,
                                    bonsai_dynamic_plotter = False,
                                    bonsai_event_outfile = './events_example3')

t = ch_frb_rfi.transform_chain(p)

ch_frb_rfi.run_in_scratch_dir('example3', s, t)

p.var_est = False
p.mask_filler = True
p.make_plots = True

t = ch_frb_rfi.transform_chain(p)
t += [ ch_frb_rfi.bonsai.nfreq16K_3tree(p, 1) ]

ch_frb_rfi.run_for_web_viewer('example3', s, t)

print "example3.py: pipeline run successful!"
print "You can view the result at http://frb1.physics.mcgill.ca:5000/"
print "Note that you'll probably need to click the update link (either 'Update directories'"
print "or 'Don't see your directory? Click here to update') before the new pipeline run appears."
