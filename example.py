#!/usr/bin/env python
#
# This is an example script showing how to use ch_frb_rfi, a python library
# containing our current RFI removal code, and some functions to make scripting
# pipeline runs easier.
#
# This script is intended to run on frb1.physics.mcgill.ca.


import ch_frb_rfi


# First, make the 'transform_parameters' object.
# This is an aggregator for parameters which determine the transform chain.
# All parameters have defaults which can be overridden as constructor arguments.
# Here, we just override a few parameters which are related to plotting (by default,
# no plots will be produced).
#
# See the ch_frb_rfi.transform_parameters docstring for more details, and a list
# of all parameters available.

p = ch_frb_rfi.transform_parameters(plot_type = 'big',                    # write size-(1200,512) waterfall plots
                                    bonsai_output_plot_stem='triggers')   # write bonsai plots to filenames beginning with 'triggers_...'


# Second, make a stream (object of type rf_pipelines.wi_stream).  
# The submodule ch_frb_rfi.acquisitions defines some "standard" acquisitions on frb1.
# (See 'dir(ch_frb_rfi.acquisitions) for a complete list'.)

s = ch_frb_rfi.acquisitions.small()   # A small example acq containing a few minutes of data


# Third, make a transform chain (list of rf_pipelines.wi_transform objects)
# There are lots of functions returning transform_chains, which aren't documented systematically
# since our RFI removal code is still under development.  
#
# The function ch_frb_io.transform_chain() returns "the" CHIME RFI-removing chain.  
# Note that this is still under development and will change in future versions!
#
# The submodule ch_frb_rfi.bonsai defines a few "standard" dedispersers that we sometimes use.
# See bonsai_configs/README.md for a list!

t = ch_frb_rfi.transform_chain(p)               # ch_frb_rfi.transform_chain() returns a list of transforms
t += [ ch_frb_rfi.bonsai.nfreq1024_3tree(p) ]    # ch_frb_rfi.bonsai.nfreq1024_3tree() returns a single transform


# Fourth, run the pipeline!  (this is the usual rf_pipelines syntax, not anything defined in ch_frb_rfi)

s.run(t, outdir='example_pipeline_outputs')
