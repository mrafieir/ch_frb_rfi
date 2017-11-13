#!/usr/bin/env python
#
# As explained in MANUAL.md, the same bonsai configs are expected to appear in multiple places:
#  - in git/ch_frb_rfi/bonsai_configs
#  - in git/ch_frb_l1/bonsai_configs
#  - in /data/bonsai_configs (with "derived" hdf5 files created with 'bonsai-mkweight').
#
# This raises the possibility of files becoming out of sync, if they are modified in one place
# and not updated in others, or if the .txt files are updated without regenerating the corresponding
# hdf5 files.  This script will check for inconsistencies, and should be run periodically.


import os
import subprocess


def diff(filename1, filename2):
    p = subprocess.Popen(['diff','-u',filename1,filename2], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    (out, err) = p.communicate()
    exit_status = p.wait()

    if exit_status == 0:
        assert len(out) == 0
        return ''

    if exit_status == 1:
        assert len(out) > 0
        return out

    if len(err) == 0:
        err = "diff -u %s %s failed" % (filename1, filename2)

    raise RuntimeError(err)


####################################################################################################
    

stem1 = set()
stem2 = set()
stem3 = set()
flag = False

for f in os.listdir('../bonsai_configs'):
    if f.endswith('.txt'):
        stem1.add(f[:-4])

for f in os.listdir('/data/bonsai_configs'):
    if f.endswith('.txt'):
        stem2.add(f[:-4])
    if f.endswith('.hdf5'):
        stem3.add(f[:-5])

all_stems = stem1.union(stem2).union(stem3)

for s in all_stems:
    f1 = '../bonsai_configs/%s.txt' % s
    f2 = '/data/bonsai_configs/%s.txt' % s
    f3 = '/data/bonsai_configs/%s.hdf5' % s

    for (ss,f) in [ (stem1,f1), (stem2,f2), (stem3,f3) ]:
        if s not in ss:
            print 'Expected %s, not found' % f
            flag = True

    # Check consistency between git/ch_frb_rfi/bonsai_configs/bonsai_x.txt and /data/bonsai_configs/bonsai_x.txt
    if (s in stem1) and (s in stem2):
        d = diff(f1, f2)
        if len(d) > 0:
            print d
            flag = True

    # Check consistency between /data/bonsai_configs/bonsai_x.txt and /data/bonsai_configs/bonsai_x.hdf5
    if (s in stem2) and (s in stem3):
        f2x = f2 + '.deleteme'
        f3x = f3 + '.deleteme'

        subprocess.check_call(['bonsai-show-config',f2], stdout=open(f2x,'w'))
        subprocess.check_call(['bonsai-show-config',f3], stdout=open(f3x,'w'))

        for line in open(f3x,'r'):
            if (line.find('warning') > 0) or (line.find('old parameter') > 0):
                print line,
                flag = True

        d = diff(f2x, f3x)
        if len(d) > 0:
            print d
            flag = True

        os.remove(f2x)
        os.remove(f3x)


if not flag:
    print 'Looks good!'
