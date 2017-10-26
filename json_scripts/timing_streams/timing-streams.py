#!/usr/bin/env python

import ch_frb_rfi
import rf_pipelines

# To guard against accidentally overwriting git-managed json files
clobber = False

for (nfreq, nfreq_s) in [ (1024,'1k'), (16384,'16k') ]:
    nt = 100000
    nt_s = '100k'

    p = rf_pipelines.gaussian_noise_stream(nfreq = nfreq, 
                                           nt_tot = nt,
                                           freq_lo_MHz = 400.0,
                                           freq_hi_MHz = 800.0,
                                           dt_sample = 0.00098304, 
                                           sample_rms = 1.0, 
                                           nt_chunk = 1024)

    filename = '../../json_files/timing_streams/gaussian_nfreq%s_nt%s.json' % (nfreq_s, nt_s)

    ch_frb_rfi.utils.write_json(filename, p, clobber=clobber)

