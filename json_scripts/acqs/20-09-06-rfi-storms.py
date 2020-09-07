#!/usr/bin/env python

import os
import re
import json
import rf_pipelines as rfp

input_topdir = '/frb-archiver-1/acq_data'
min_nfiles = 100

output_topdir = '../../json_files/acqs'
output_relpath = '20-09-06-rfi-storms'

# If 'clobber' is False, then when a json file is created with rf_pipelines.json_write(filename, j),
# we throw an exception if 'filename' already exists, and its contents differ from 'j'.  This is
# to prevent git-managed json files from being modified accidentally.
clobber = False


####################################################################################################


runlist = [ ]
nfiles_tot = 0

for acq_relpath in sorted(os.listdir(input_topdir)):
    if not acq_relpath.startswith('rfi_storm'):
        continue

    acq_abspath = os.path.join(input_topdir, acq_relpath)

    for beam_relpath in sorted(os.listdir(acq_abspath)):
        assert re.match(r'beam_(\d+)', beam_relpath)
        beam_abspath = os.path.join(acq_abspath, beam_relpath)

        data_relpath_list = sorted(os.listdir(beam_abspath))
        data_abspath_list = [ os.path.join(beam_abspath,f) for f in data_relpath_list ]
        nfiles = len(data_relpath_list)

        stream_name = '%s_%s' % (acq_relpath, beam_relpath)
        stream_relpath = os.path.join(output_relpath, '%s.json' % stream_name)
        stream_abspath = os.path.join(output_topdir, stream_relpath)

        for filename in data_relpath_list:
            assert re.match(r'chunk_(\d+).msg', filename)
        
        if nfiles < min_nfiles:
            print('    %s: %d data files found (min_nfiles=%d), skipping' % (beam_abspath, nfiles, min_nfiles))
            continue

        print('%s: %d data files found' % (beam_abspath, nfiles))

        stream = rfp.chime_frb_stream_from_filename_list(data_abspath_list)
        rfp.json_write(stream_abspath, stream, clobber=clobber)

        runlist.append((stream_name, stream_relpath))
        nfiles_tot += nfiles

print 'wrote %d streams (%s total data files)' % (len(runlist), nfiles_tot)

runlist_abspath = os.path.join(output_topdir, '%s-runlist.json' % output_relpath)
f = open(runlist_abspath, 'w')
json.dump(runlist, f, indent=4)
print >>f, ''  # extra newline
f.close()

print 'wrote', runlist_abspath
