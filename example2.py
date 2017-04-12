#!/usr/bin/env python
#
# This is an example script showing how to use ch_frb_rfi for properly removing RFI, 
# estimating the variance, hence correctly normalizing the output of the bonsai
# dedisperser, and finally grouping all triggers above a 10-sigma threshold.
#
# It is assumed that you have already studied 'example.py'. This script is intended
# to run on frb1.physics.mcgill.ca.

import numpy as np
import ch_frb_rfi
import rf_pipelines

# Let's choose an acquisition with a real pulsar!
s = ch_frb_rfi.acquisitions.ex_pulsar_search1()

# The following parameters are explained in 'ch_frb_rfi/chains.py'.
(rfi_level, v1_chunk, v2_chunk) = (1, 32, 192)

# Two pipeline runs will be performed in this example.
#
# The first run will create a file in the current directory (./var_example2.h5)
# which contains per-channel variance estimates.  The second run will use these
# estimates to "fill in" the RFI mask with simulated Gaussian noise (via the
# mask_filler transform).  
#
# This fill-in helps the bonsai dedisperser compute running trigger variance estimates.  
# It's an open question whether we'll use it "in production" on the telescope, but our
# working assumption is that we will do so, and will write a fast C++ implementation
# at some point.

p = ch_frb_rfi.transform_parameters(plot_type = 'web_viewer',
                                    make_plots = False,
                                    bonsai_output_plot_stem = 'triggers', 
                                    maskpath = '/data/pathfinder/rfi_masks/rfi_20160705.dat',
                                    rfi_level = rfi_level,
                                    bonsai_use_analytic_normalization = False, 
                                    bonsai_hdf5_output_filename = None,
                                    bonsai_nt_per_hdf5_file = None,
                                    var_est = True,
                                    mask_filler = False,
                                    var_filename = './var_example2.h5',
                                    variance_estimator_v1_chunk = v1_chunk,
                                    variance_estimator_v2_chunk = v2_chunk,
                                    mask_filler_w_cutoff = 0.5,
                                    kfreq = 1,
                                    bonsai_plot_threshold1 = 7,
                                    bonsai_plot_threshold2 = 10,
                                    bonsai_dynamic_plotter = False,
                                    bonsai_event_outfile = 'events_example2.txt',
                                    L1Grouper_thr = 10,
                                    L1Grouper_beam = 0,
                                    L1Grouper_addr = None)

# Using the specified parameters make a chain of transforms for estimating the variance.
t = ch_frb_rfi.transform_chain(p)

# The purpose of the first pipeline run is to create the h5 file containing variance
# estimates (p.var_fileanme = './var_example2.h5').  We do this pipeline run using the
# wrapper function run_in_scratch_dir(), which does not index the run with the web viewer.
ch_frb_rfi.run_in_scratch_dir('example2', s, t)

# Remove the variance_estimator, append the mask_filler and plotter transforms.
p.var_est = False
p.mask_filler = True
p.make_plots = True

t = ch_frb_rfi.transform_chain(p)
t += [ ch_frb_rfi.bonsai.nfreq1K_3tree(p, 1) ]

# Second pipeline run: we use the wrapper function run_for_web_viewer().
# Run the pipeline (again) but now with the mask_filler and bonsai dedisperser.
ch_frb_rfi.run_for_web_viewer('example2', s, t)

print "example2.py: pipeline run successful!"
print "You can view the result at http://frb1.physics.mcgill.ca:5000/"
print "Note that you'll probably need to click the update link (either 'Update directories'"
print "or 'Don't see your directory? Click here to update') before the new pipeline run appears."
