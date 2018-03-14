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
from glob import glob
from ch_frb_rfi.transforms import write_mask

# Let's choose an acquisition with a real pulsar!
filename_list = glob("/frb-archiver-1/acq_data/frb_run_9_night 3/beam_0139/chunk*.msg")
filename_list.sort()
s = rf_pipelines.chime_frb_stream_from_filename_list(filename_list[150:600], nt_chunk=1024, noise_source_align= 0)

# The following parameters are explained in 'ch_frb_rfi/chains.py'.
(rfi_level, v1_chunk, v2_chunk) = (0, 32, 192)

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
                                    #bonsai_output_plot_stem = 'triggers', 
                                    #maskpath = None,
                                    #maskpath = '/data/pathfinder/rfi_masks/rfi_20160705.dat', # Bad Channel mask
                                    #detrender_niter = 2, # For current chain of cleaning in L1
                                    #clipper_niter = 6, # For current chain of cleaning in L1
                                    #spline = True, # For current chain of cleaning in L1
                                    #rfi_level = rfi_level, # Uncomment this to do a minimal RFI cleaning.
                                    bonsai_use_analytic_normalization = False, 
                                    bonsai_hdf5_output_filename = None,
                                    bonsai_nt_per_hdf5_file = None,
                                    #bonsai_fill_rfi_mask = True,
                                    var_est = False,
                                    #mask_filler = True,
                                    #variance_estimator_v1_chunk = v1_chunk,
                                    #variance_estimator_v2_chunk = v2_chunk,
                                    #mask_filler_w_cutoff = 0.5,
                                    bonsai_plot_threshold1 = 7,
                                    bonsai_plot_threshold2 = 10,
                                    bonsai_dynamic_plotter = False,
                                    L1b_config = 'L1b_config_site.yaml')

# Using the specified parameters make a chain of transforms for estimating the variance.
t16k = ch_frb_rfi.transform_chain(p)

# Combine stream and transforms into a pipeline.
#pipeline = rf_pipelines.pipeline([s]+t)
#ch_frb_rfi.run_in_scratch_dir('/frb-archiver-1/replay/frb_run_9/no_rfi_cleaning', 'frb_run_9_beam_139', pipeline)
# The purpose of the first pipeline run is to create the h5 file containing variance
# estimates (p.var_filename = './var_example2.h5').  We do this pipeline run using the
# wrapper function run_in_scratch_dir(), which does not index the run with the web viewer.

# In the v16 API, need to "unbind" the pipeline after running, before its constituent
# pipeline_objects can be reused in another pipeline run.
#pipeline.unbind()

# Remove the variance_estimator, append the mask_filler and plotter transforms.
#p.var_est = False
#p.mask_filler = False
#p.make_plots = True

####### Run L1 with default chain of  RFI  Cleaning########

#t1k = ch_frb_rfi.transform_chain(p)
#p1k = rf_pipelines.pipeline(t1k)

#p.detrend_last = False
#_t1k = ch_frb_rfi.transform_chain(p)
#_p1k = rf_pipelines.pipeline(_t1k)
#t16k = [ rf_pipelines.wi_sub_pipeline(_p1k, nfreq_out=1024, nds_out=1) ]
#t16k += ch_frb_rfi.chains.detrender_chain(p, ix=0)

###### Run Bonsai #############
t16k += [ch_frb_rfi.bonsai.make_dedisperser(p, '/home/l1operator/ch_frb_l1/bonsai_configs/bonsai_production_ups_nbeta1_v2_nbits32.hdf5')] # 32 bits
#t16k += [ ch_frb_rfi.bonsai.make_dedisperser(p, '/data/bonsai_configs/bonsai_production_ups_nbeta1_v2.hdf5') ] # 16 bits
#t16k += [write_mask.WriteWeights(basename = 'frb_run_9_beam_139_no_rfi_cleaning')]
pipeline = rf_pipelines.pipeline([s]+t16k)

# Second pipeline run: we use the wrapper function run_for_web_viewer().
# Run the pipeline (again) but now with the mask_filler and bonsai dedisperser.
#ch_frb_rfi.run_for_web_viewer('example2', pipeline)
#ch_frb_rfi.run_in_scratch_dir('example2', None, pipeline)
ch_frb_rfi.run_in_scratch_dir('/frb-archiver-1/replay/frb_run_9/no_rfi_cleaning_2', 'frb_run_9_beam_139', pipeline)

print "example2.py: pipeline run successful!"
print "You can view the result at http://frb1.physics.mcgill.ca:5000/"
