#!/usr/bin/env python

import ch_frb_rfi
import rf_pipelines

# To guard against accidentally overwriting git-managed json files
clobber = False

for (nfreq, nt_per_packet, nfreq_s) in [ (1024,256,'1k'), (16384,16,'16k') ]:
    nt_tot = 100000
    nt_str = '100k'

    assert nfreq % 1024 == 0
    nupfreq = nfreq // 1024

    p = rf_pipelines.gaussian_noise_stream(nfreq = nfreq, 
                                           nt_tot = nt_tot,
                                           freq_lo_MHz = 400.0,
                                           freq_hi_MHz = 800.0,
                                           dt_sample = 0.00098304, 
                                           sample_rms = 1.0, 
                                           nt_chunk = 1024)

    filename = '../../json_files/toy_streams/gaussian_nfreq%s_nt%s.json' % (nfreq_s, nt_str)
    rf_pipelines.utils.json_write(filename, p, clobber=clobber)

    p = rf_pipelines.chime_dummy_network_stream(nt_tot, nupfreq=nupfreq, nt_per_packet=nt_per_packet)

    filename = '../../json_files/toy_streams/chime_network_nfreq%s_nt%s.json' % (nfreq_s, nt_str)
    rf_pipelines.utils.json_write(filename, p, clobber=clobber)
