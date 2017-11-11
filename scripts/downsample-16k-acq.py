#!/usr/bin/env python
#
# downsample-16k-acq.py <src_acq.json> <dst_acqdir>
#
# Downsamples a 16K-channel acq down to 1K-channels.
# The input acq must be jsonized already.
# The output acq is written to a single HDF5 file dst_acqdir/00000000.h5.
#
# Example (on frb1):
#
#  ./downsample-16k-acq.py ../json_files/acqs/17-04-25-utkarsh-26m-16k/part0.json /data/17-10-01-16k-to-1k/17-04-25-utkarsh-26m-part0


import os
import sys


if len(sys.argv) != 3:
    print >>sys.stderr, 'usage: downsample-16k-acq.py <src_acq.json> <dst_acqdir>'
    sys.exit(2)

(srcfile, dstdir) = (sys.argv[1], sys.argv[2])

if not srcfile.endswith('.json'):
    print >>sys.stderr, "Fatal: source file '%s' must end in .json" % srcfile

if not os.path.exists(srcfile):
    print >>sys.stderr, "Fatal: source file '%s' does not exist" % srcfile
    sys.exit(1)

if os.path.exists(dstdir):
    print >>sys.stderr, "Fatal: destination directory '%s' already exists, this is treated as an error to avoid accidentally overwriting data" % dstdir
    sys.exit(1)


####################################################################################################


import rf_pipelines

j = rf_pipelines.json_read(srcfile)
stream = rf_pipelines.pipeline_object.from_json(j)

dstfile = os.path.join(dstdir, '00000000.h5')
writer = rf_pipelines.chime_file_writer(dstfile)
writer = rf_pipelines.wi_sub_pipeline(writer, Df=16, Dt=1)

pipeline = rf_pipelines.pipeline([stream, writer])

print 'Creating directory', dstdir
os.makedirs(dstdir)

print 'Running pipeline'
pipeline.run(outdir=None)
