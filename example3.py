#!/usr/bin/env python
#
# This is an example script showing an (offline) L1 analysis of 
# ~ 5 minutes of the Crab pulsar data (26m) in 16K frequency channels.
#
# It is assumed that you have already studied 'example.py' and 'example2.py'.
#
# This script is intended to run on frb1.physics.mcgill.ca.

import numpy as np
import ch_frb_rfi
import rf_pipelines

s = ch_frb_rfi.acquisitions.crab_16k(n=300)

p = ch_frb_rfi.transform_parameters(plot_type = 'web_viewer',
                                    make_plots = False,
                                    bonsai_output_plot_stem = 'triggers', 
                                    rfi_level = 1,
                                    bonsai_use_analytic_normalization = False, 
                                    var_est = True,
                                    var_filename = './var_example3.h5',
                                    variance_estimator_v1_chunk = 64,
                                    variance_estimator_v2_chunk = 100,
                                    mask_filler_w_cutoff = 0.25,
                                    kfreq = 16,
                                    bonsai_plot_threshold1 = 7,
                                    bonsai_plot_threshold2 = 10,
                                    bonsai_dynamic_plotter = False,
                                    bonsai_event_outfile = './events_example3.dat')

t = ch_frb_rfi.transform_chain(p)

# Combine stream and transforms into a pipeline.
pipeline = rf_pipelines.pipeline([s]+t)

ch_frb_rfi.run_in_scratch_dir('example3', pipeline)

# In the v16 API, need to "unbind" the pipeline after running, before its constituent
# pipeline_objects can be reused in another pipeline run.
pipeline.unbind()

# Remove the variance_estimator, append the mask_filler and plotter transforms.
p.var_est = False
p.mask_filler = True
p.make_plots = True

t = ch_frb_rfi.transform_chain(p)
t += [ ch_frb_rfi.bonsai.nfreq16K_3tree(p, fpga_counts_per_sample=384, v=1) ]

pipeline = rf_pipelines.pipeline([s]+t)
ch_frb_rfi.run_for_web_viewer('example3', pipeline)

print "example3.py: pipeline run successful!"
print "You can view the result at http://frb1.physics.mcgill.ca:5000/"
