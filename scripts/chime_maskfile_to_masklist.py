#!/usr/bin/env python
import datetime
import rf_pipelines


today = str(datetime.date.today())
mask_filename = './badchannel_mask_%s.dat' % today

class masklist_capturing_transform(rf_pipelines.wi_transform):
    def __init__(self):
        rf_pipelines.wi_transform.__init__(self, 'masklist_capturing_transform')
        
    def _process_chunk(self, intensity, weights, pos):
        if hasattr(self, 'masklist'):
            return
        
        self.masklist = [ ]
        for ifreq in xrange(self.nfreq):
            if weights[ifreq,0] == 0.0:
                self.masklist.append(ifreq)

s = rf_pipelines.gaussian_noise_stream(
    nfreq = 1024,
    nt_tot = 1024,
    freq_lo_MHz = 400.0,
    freq_hi_MHz = 800.0,
    dt_sample = 1.0e-3
)
    
t1 = rf_pipelines.badchannel_mask(mask_filename)

t2 = masklist_capturing_transform()

p = rf_pipelines.pipeline([s,t1,t2])
p.run(outdir=None, verbosity=1)

print 'The following channels were masked:', t2.masklist
