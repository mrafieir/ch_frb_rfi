#!/usr/bin/env python
import ch_frb_rfi

s = ch_frb_rfi.acquisitions.baseband_26m_b1937_16_04_22()

p = ch_frb_rfi.transform_parameters(plot_type = 'big',
                                    bonsai_output_plot_stem='triggers')


t = ch_frb_rfi.transform_chain(p)
t += [ ch_frb_rfi.bonsai.nfreq16K_3tree(p) ]

s.run(t, outdir='baseband_26m_b1937_pipeline_outputs')
