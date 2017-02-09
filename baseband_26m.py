#!/usr/bin/env python
import ch_frb_rfi

sample = 4
start = 0
end = 30
web = False

if sample == 1:
    path = '/data2/baseband_26m_b1937_16_04_22/*.h5'
    bonsai_v = 2
    kfreq = 16
    nypix = 16384

if sample == 2:
    path = '/data2/baseband_26m_b1937_16_04_22/1k_B1937/*.h5'
    bonsai_v = 2
    kfreq = 1
    nypix = 1024

if sample == 3:
    path = '/data2/acqhack_b1937_1K/*.h5'
    bonsai_v = 1
    kfreq = 1
    nypix = 1024

if sample == 4:
    path = '/data2/baseband_26m_b1937_16_04_22/128k/*.h5'
    bonsai_v = 1
    kfreq = 128
    nypix = 131072

# Define transform parameters. See 'ch_frb_rfi/chain.py' for a list of available parameters.
p = ch_frb_rfi.transform_parameters(plot_type='web_viewer' if web else 'big', 
                                    bonsai_output_plot_stem='triggers', 
                                    mask=[[730,760]],
                                    clipper_niter=2,
                                    detrender_niter=2,
                                    plot_nypix=nypix,
                                    plot_nxpix=1200,
                                    kfreq=kfreq)

# Define the chain of transforms.
t = [ ch_frb_rfi.test_16k() ] 
t += ch_frb_rfi.transform_chain(p)

# Read filenames into a list; append bonsai_dedisperser to the list of transforms.
s = ch_frb_rfi.acquisitions.sample(path, start, end)

if kfreq == 128:
    t += [ ch_frb_rfi.bonsai.nfreq128K_3tree(p) ]
if kfreq == 16:
    t += [ ch_frb_rfi.bonsai.nfreq16K_3tree(p) ]
if kfreq == 1:
    t += [ ch_frb_rfi.bonsai.nfreq1024_3tree(p, bonsai_v) ]

dirname = '%sK_baseband_26m_b1397_d%d%dc' % (kfreq, p.detrender_niter, p.clipper_niter)
if not web:
    s.run(t, outdir=dirname)
else:
    ch_frb_rfi.run_for_web_viewer(dirname, s, t)
