#!/usr/bin/env python
#
# This script defines acquisition json files for the ~1000 hours of incoherent-beam
# pathfinder data in frb1:/data2/17-02-08-data-avalanche.
#
# We define one json file per ~10 hours of data, so ~100 json files are created.
# When a "long" gap (more than a minute) occurs in the data, we start a new json file.
# Gaps were found by hand, using ch_frb_rfi/scripts/inspect-acquisition-timestamps.py.


import os
import json
import numpy as np
import rf_pipelines


clobber = True
global_run_list = [ ]
global_label_set = set()
global_dirname_set = set()


def process_acquisition(label, dirname, time_ranges):
    """
    Helper function which generates json files for one acquisition.

    'label' should be a short descriptor string such as '0b'.
    'dirname' should be a subdir of /data2/17-02-08-incoherent-data-avalanche, such as 'frb_incoherent_0b'.
    'time_ranges' should be a list of (time_lo, time_hi, nchunks) triples.

    Each triple in 'time_ranges' corresponds to one contiguous stretch of data.  In most acquisitions, 
    there will only be one such contiguous stretch corresponding to the whole acquisition (i.e. 'time_ranges' 
    is a list of length 1).  However, if there are long gaps in the acquisition, then we divide it into 
    multiple contiguous stretches.

    Within each contiguous stretch, the acquisition is divided into 'nchunks' json files.  The caller
    chooses the value of 'nchunks' so that there is ~10 hours of data per json file.
    """

    nparts = 0

    for (time_lo, time_hi, nchunks) in time_ranges:
        assert nchunks >= 1
        assert time_hi > time_lo + nchunks * 900.   # At least 15 minutes per chunk.

        t = np.linspace(time_lo, time_hi, nchunks+1)

        for i in xrange(nchunks):
            # Chunk endpoints.
            # The +/- 150 offsets here are so that consecutive chunks will overlap by 5 minutes.
            t0 = (t[i] - 150.) if (i > 0) else t[i]
            t1 = (t[i+1] + 150.) if (i < nchunks-1) else t[i+1]

            # Note: I don't think we ever need 'noise_source_align' in this acquisition.
            d = os.path.join('/data2/17-02-08-incoherent-data-avalanche', dirname)
            s = rf_pipelines.chime_stream_from_times(d, t0, t1, noise_source_align=False, noisy=False)

            json_filename1 = '17-02-08-incoherent-data-avalanche/run%s_part%d.json' % (label, nparts)
            json_filename2 = '../../json_files/acqs/' + json_filename1
            rf_pipelines.json_write(json_filename2, s, clobber=clobber)

            suffix = 'run%s_part%d' % (label,nparts)
            global_run_list.append([ suffix, json_filename1 ])

            nparts += 1

    assert label not in global_label_set
    assert dirname not in global_dirname_set

    global_label_set.add(label)
    global_dirname_set.add(dirname)


####################################################################################################


# frb_incoherent_0b: 5014 files, acqtime 29.9154068821 hours
# The end time is chosen to exclude the last file 00082165.h5, which is corrupted.
process_acquisition('0b', 'frb_incoherent_0b', [ (220.0, 107910.0, 3) ])

# frb_incoherent_1c: 7431 files, acqtime 44.330717093 hours
process_acquisition('1c', 'frb_incoherent_1c', [ (350.0, 159910.0, 4) ])

# frb_incoherent_1d: 19100 files, acqtime 114.558465547 hours
# There is a 37-minute gap after 83 hours (time range (305780,308070), filenames 00228080.h5 -> 00229824.h5).
# The end time is chosen to exclude the last file 00314644.h5, which is corrupted.
process_acquisition('1d', 'frb_incoherent_1d', [ (6820.0, 305780.0, 8), (308070.0, 419220.0, 3) ])

# frb_incoherent_2b: 4512 files, acqtime 26.9151280242 hours
process_acquisition('2b', 'frb_incoherent_2b', [ (2840.0, 99710.0, 3) ])

# frb_incoherent_2c: 26975 files, acqtime 161.762421055 hours.
# There is a 51-minute gap after 96 hours (time range (348980,352070), filenames 00262873.h5 -> 00265215.h5).
process_acquisition('2c', 'frb_incoherent_2c', [ (4450.0, 348980.0, 10), (352070.0, 586770.0, 6) ])

# frb_incoherent_2d: 14381 files, acqtime 85.786239158 hours
process_acquisition('2d', 'frb_incoherent_2d', [ (3160.0, 311964.0, 9) ])

# frb_incoherent_3b: 4742 files, acqtime 28.287131466 hours
process_acquisition('3b', 'frb_incoherent_3b', [ (1190.0, 103000.0, 3) ])

# frb_incoherent_3c: 9930 files, acqtime 60.2862689394 hours
# There is a 63-minute gap after 16 hours (time range (62230,66060), filenames 00044372.h5 -> 00047288.h5)
process_acquisition('3c', 'frb_incoherent_3c', [ (4080.0, 62230.0, 2), (66060.0, 221090.0, 4) ])

# frb_incoherent_3d: 16237 files, acqtime 96.86129887 hours
process_acquisition('3d', 'frb_incoherent_3d', [ (4900.0, 353580.0, 10) ])

# frb_incoherent_4b: 9169 files, acqtime 54.8559967573 hours
# There is a ~10-hour stretch of "suspicious" data with lots of small gaps, covering time range (92830, 127850).
# This starts about an hour into part 2, and stops a few minutes into part 3.
# Does this stretch of suspicious data behave differently in the pipeline?
process_acquisition('4b', 'frb_incoherent_4b', [ (9030.0, 206490.0, 5) ])

# frb_incoherent_4c: 23827 files, acqtime 142.137272639 hours
process_acquisition('4c', 'frb_incoherent_4c', [ (8460.0, 520124.0, 14) ])

# frb_incoherent_4d: 8296 files, acqtime 49.4901770468 hours
process_acquisition('4d', 'frb_incoherent_4d', [ (4270.0, 182420.0, 5) ])

# frb_incoherent_5b: 2405 files, acqtime 14.3480145692 hours
process_acquisition('5b', 'frb_incoherent_5b', [ (500.0, 52140.0, 2) ])

# frb_incoherent_5c: 17251 files, acqtime 103.958154445 hours
process_acquisition('5c', 'frb_incoherent_5c', [ (560.0, 374790.0, 10) ])

# frb_incoherent_search_0: 7678 files, acqtime 45.801193472 hours
process_acquisition('0', 'frb_incoherent_search_0', [ (450.0, 165320.0, 4) ])

# frb_incoherent_search_1: 3612 files, acqtime 21.5464189042 hours
process_acquisition('1', 'frb_incoherent_search_1', [ (570.0, 78120.0, 2) ])

# frb_incoherent_search_2: 1074 files, acqtime 6.40684559929 hours
process_acquisition('2', 'frb_incoherent_search_2', [ (610.0, 23660.0, 1) ])

# frb_incoherent_search_3: 10754 files, acqtime 64.1505744213 hours
process_acquisition('3', 'frb_incoherent_search_3', [ (1950.0, 232880.0, 6) ])

# frb_incoherent_search_4: 8601 files, acqtime 52.5057418126 hours
# There is a 72-minute gap after 51 hours, followed by 39 minutes of data, then the acquisition ends.
# In this case, I just decided to exclude the data after the gap.
process_acquisition('4', 'frb_incoherent_search_4', [ (430.0, 181400.0, 5) ])


####################################################################################################


run_list_filename = '../../json_files/acqs/17-02-08-incoherent-data-avalanche-runlist.json'

f = open(run_list_filename, 'w')
json.dump(global_run_list, f, indent=4)
print >>f, ''  # extra newline
f.close()

print 'wrote', run_list_filename
