#!/usr/bin/env python
import ch_frb_rfi

# Indicate whether you're using the 16K data.
u16k = True

# If True, then retrieve only the first 'n' files from 'path'.
sample = True
n = 40
path = '/data2/baseband_26m_b1937_16_04_22/*.h5'

# Set True for outputting to the web_viewer. If False, plot 'big'.
web = True
plot_type = 'web_viewer' if web else 'big'

# Define transform parameters. See 'ch_frb_rfi/chain.py' for a list of available parameters.
p = ch_frb_rfi.transform_parameters(plot_type=plot_type, 
                                    bonsai_output_plot_stem='triggers', 
                                    mask=[[445,472]],
                                    clipper_niter=2,
                                    detrender_niter=2)

# Define the chain of transforms.
t = [ ch_frb_rfi.test_16k() ] 
t += ch_frb_rfi.transform_chain(p)

# Read filenames into a list; append bonsai_dedisperser to the list of transforms.

if u16k:
    s = ch_frb_rfi.acquisitions.sample(path, n) if sample else ch_frb_rfi.acquisitions.baseband_26m_b1937_16_04_22()
    t += [ ch_frb_rfi.bonsai.nfreq16K_3tree(p) ]
    dirname = '16K_baseband_26m_b1937_pipeline_outputs__d%d%dc' % (p.detrender_niter, p.clipper_niter)

else:
    s = ch_frb_rfi.acquisitions.sample(path, n) if sample else ch_frb_rfi.acquisitions.baseband_26m_b1937_16_04_22_1K()
    t += [ ch_frb_rfi.bonsai.nfreq1024_3tree(p) ]
    dirname = '1K_baseband_26m_b1937_pipeline_outputs__d%d%dc' % (p.detrender_niter, p.clipper_niter)

# Run rf_pipelines!
if not web:
    s.run(t, outdir=dirname)
else:
    ch_frb_rfi.run_for_web_viewer(dirname, s, t)
