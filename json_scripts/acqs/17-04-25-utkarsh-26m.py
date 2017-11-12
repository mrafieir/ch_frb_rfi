#!/usr/bin/env python
#
# This script generates json files for the 16k-upchannelized '17-04-25-utkarsh-26m' acqs.
#
# This is our only 16k-upchannelized data, for now!  It is from a 26-m run on 17-04-25, recorded
# in baseband, and upchannelized by Utkarsh's code.  There is ~2.5 hours of data, divided into 7
# parts (i.e. 7 json files).
#
# We save json files for the 16k-channelized acqs, and 1k-channelized acqs obtained by downsampling
# down to 1024 frequencies.  These latter acqs have (1/16) the data volume and are sometimes useful,
# e.g. for quick plotting or experimenting with tweaks to the "1k" part of the RFI transform chain.
#
# In hindsight, it would have been better to generate a single json file for all 7 parts combined,
# but I haven't done this yet!  (Due to details of how the upchannelization code works, there will
# be ~1 second gaps at boundaries between the 7 parts, but that's OK.)
#
# If running from scratch, this script will need to be run twice.  The first time, it will generate
# json files for the 16k-channel acqs, and print instructions to the screen for genererating the
# 1k-channelized data (i.e. the data itself, not json files) by running '../../scripts/downsample-16k-acq.py'.
# The second time, it will generate the 1k-channelized json files.

import os
import ch_frb_rfi
import rf_pipelines


# If 'clobber' is False, then when a json file is created with rf_pipelines.json_write(filename, j),
# we throw an exception if 'filename' already exists, and its contents differ from 'j'.  This is
# to prevent git-managed json files from being modified accidentally.
clobber = False


# The 16K data needs to be "derippled" (see note 'pfb_ripples.pdf' sent to the chimefrb_twg list on 2017-10-04).
# This is done using a 'chime_16k_derippler' transform which takes a single parameter, the 'deripple_fudge_factor'.
# A value of 0.0 means "no deripple correction", a value of 1.0 means "full deripple correction".
#
# In the 17-04-25-utkarsh-26m acq, the ripple effect is seen in the data at 80% of the analytically predicted value,
# for reasons that are unknown.  Since Utkarsh's code applies the deripple correction, it overcorrects for the
# ripple effect.  We compensate for this by using a _negative_ correction, i.e. deripple_fudge_factor = -0.2.

deripple_fudge_factor = -0.2
nparts = 7

missing_1k_flag = False

for part in xrange(nparts):
    # Make 16k stream.
    acqdir = '/data/17-10-01-16k-data/17-04-25-utkarsh-26m-part%d' % part
    stream_16k = rf_pipelines.chime_stream_from_acqdir(acqdir)
    
    # Append derippler.
    derippler = rf_pipelines.chime_16k_derippler(fudge_factor=deripple_fudge_factor)
    stream_16k = rf_pipelines.pipeline([stream_16k, derippler])

    # Write json file for the 16k acq
    json_filename_16k = '../../json_files/acqs/17-04-25-utkarsh-26m-16k/part%d.json' % part
    rf_pipelines.utils.json_write(json_filename_16k, stream_16k, clobber=clobber)

    # Does the 1k acq exist?  If not, print instructions for generating it.
    acqdir_1k = '/data/17-10-01-16k-to-1k/17-04-25-utkarsh-26m-part%d' % part
    acqfile_1k = os.path.join(acqdir_1k, '00000000.h5')

    if not os.path.exists(acqfile_1k):
        print "Note: 1K-channelized acq '%s' does not exist, you need to run this command:" % acqfile_1k
        print "   ../../scripts/downsample-16k-acq.py %s /data/17-10-01-16k-to-1k/17-04-25-utkarsh-26m-part4" % json_filename_16k
        missing_1k_flag = True
        continue

    # If so, write json file for the 1k acq.
    stream_1k = rf_pipelines.chime_stream_from_acqdir('/data/17-10-01-16k-to-1k/17-04-25-utkarsh-26m-part%d' % part)
    json_filename_1k = '../../json_files/acqs/17-04-25-utkarsh-26m-1k/part%d.json' % part

    rf_pipelines.utils.json_write(json_filename_1k, stream_1k, clobber=clobber)

if missing_1k_flag:
    print "Note: you should rerun this script (./17-04-25-utkarsh-26m.py) after generating all 1K-channelized acqs, as noted above"
