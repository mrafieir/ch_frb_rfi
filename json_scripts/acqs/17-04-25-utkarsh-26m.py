#!/usr/bin/env python

import ch_frb_rfi
import rf_pipelines

# To guard against accidentally overwriting git-managed json files
clobber = False

print 'Note: the 17-04-25 acq is split into 8 parts, but only 4 are currently available'

for part in xrange(4):
    s16k = ch_frb_rfi.acquisitions.upchannelized_17_04_25(part)
    f16k = '../../json_files/acqs/17-04-25-utkarsh-26m-part%d-16k.json' % part
    ch_frb_rfi.utils.write_json(f16k, s16k, clobber=clobber)

    s1k = rf_pipelines.chime_stream_from_acqdir('/data/17-10-01-16k-to-1k/17-04-25-utkarsh-26m-part%d' % part)
    f1k = '../../json_files/acqs/17-04-25-utkarsh-26m-part%d-1k.json' % part
    ch_frb_rfi.utils.write_json(f1k, s1k, clobber=clobber)
