#!/usr/bin/env python
#
# This little script determines whether there are any timestamp gaps in a run.
# Written for CHIME pathfinder (or 26-m) data, and may need tweaking after we get full CHIME going.

import os
import sys
import h5py


if len(sys.argv) != 2:
    print >>sys.stderr, 'Usage: inspect-acquisition-timestamps.py <dirname>'
    sys.exit(2)

dirname = sys.argv[1]
basenames = sorted(os.listdir(dirname))
nfiles = 0
tstart = 0.0
tprev = 0.0

print 'Inspecting', dirname

for b in basenames:
    if not b.endswith('.h5'):
        continue

    try:
        f = h5py.File(os.path.join(dirname,b), 'r')
        timestamp_array = f['index_map']['time'][:]
    except KeyboardInterrupt:
        raise
    except:
        print "%s: couldn't read file and/or timestamp array (%d files so far)" % (b, nfiles)

    (t0, t1) = (timestamp_array[0], timestamp_array[-1])
    assert t0 < t1

    if nfiles == 0:
        tstart = tprev = t0

    expected_gap = 21.4735257599  # hardcoded
    actual_gap = t1 - tprev

    if actual_gap > expected_gap + 1.0:
        print '%s: %s second gap (%d files so far, acqtime %s seconds)' % (b, actual_gap - expected_gap, nfiles, tprev-tstart)
    
    tprev = t1
    nfiles += 1

print '%s: %d files, %s hours, t0=%s, t1=%s' % (dirname, nfiles, (tprev-tstart)/3600., tstart, tprev)
