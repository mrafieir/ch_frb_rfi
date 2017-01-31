#!/usr/bin/env python
import ch_frb_rfi

n = 20
u16k = False
web = True

plot_type = 'web_viewer' if web else 'big'

p = ch_frb_rfi.transform_parameters(plot_type=plot_type, bonsai_output_plot_stem='triggers')
t = ch_frb_rfi.transform_chain(p)

if u16k:
    s = ch_frb_rfi.acquisitions.baseband_26m_b1937_16_04_22()
    t += [ ch_frb_rfi.bonsai.nfreq16K_3tree(p) ]
    dirname='16K_baseband_26m_b1937_pipeline_outputs'

else:
    s = ch_frb_rfi.acquisitions.baseband_26m_b1937_16_04_22_1K(n)
    t += [ ch_frb_rfi.bonsai.nfreq1024_3tree(p) ]
    dirname='1K_baseband_26m_b1937_pipeline_outputs'

if not web:
    s.run(t, outdir=dirname)
else:
    ch_frb_rfi.run_for_web_viewer(dirname, s, t)
