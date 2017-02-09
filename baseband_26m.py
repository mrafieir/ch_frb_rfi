#!/usr/bin/env python
import ch_frb_rfi

sample = 3
start = 5
end = 100
web = False

if sample == 1:
    path = '/data2/baseband_26m_b1937_16_04_22/*.h5'
    bonsai_v = 2
    kfreq = 16
    u16k = True

if sample == 2:
    path = '/data2/baseband_26m_b1937_16_04_22/1k_B1937/*.h5'
    bonsai_v = 2
    kfreq = 1
    u16k = False

if sample == 3:
    path = '/data2/acqhack_b1937_1K/*.h5'
    bonsai_v = 1
    kfreq = 1
    u16k = False

# Define transform parameters. See 'ch_frb_rfi/chain.py' for a list of available parameters.
p = ch_frb_rfi.transform_parameters(plot_type='web_viewer' if web else 'big', 
                                    bonsai_output_plot_stem='triggers', 
                                    mask=[[730,760]],
                                    clipper_niter=2,
                                    detrender_niter=2,
                                    plot_nypix=1024,
                                    kfreq=kfreq)

# Define the chain of transforms.
t = [ ch_frb_rfi.test_16k() ] 
t += ch_frb_rfi.transform_chain(p)

# Read filenames into a list; append bonsai_dedisperser to the list of transforms.

if u16k:
    s = ch_frb_rfi.acquisitions.sample(path, start, end) if sample else ch_frb_rfi.acquisitions.baseband_26m_b1937_16_04_22()
    t += [ ch_frb_rfi.bonsai.nfreq16K_3tree(p) ]
    dirname = '16K_baseband_26m_b1937_pipeline_outputs__d%d%dc' % (p.detrender_niter, p.clipper_niter)

else:
    s = ch_frb_rfi.acquisitions.sample(path, start, end) if sample else ch_frb_rfi.acquisitions.baseband_26m_b1937_16_04_22_1K()
    t += [ ch_frb_rfi.bonsai.nfreq1024_3tree(p, v=bonsai_v) ]
    dirname = '1K_baseband_26m_b1397_pipeline_outputs__d%d%dc' % (p.detrender_niter, p.clipper_niter)

# Run rf_pipelines!
if not web:
    s.run(t, outdir=dirname)
else:
    ch_frb_rfi.run_for_web_viewer(dirname, s, t)
