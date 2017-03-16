import rf_pipelines
from rf_pipelines import rf_pipelines_c
import ch_frb_rfi

class transform_template(rf_pipelines.py_wi_transform):
    
    def __init__(self, nt_chunk=1024):
        
        name = 'transform_template(nt_chunk=%d)' % (nt_chunk)
        rf_pipelines.py_wi_transform.__init__(self, name)
        
        self.nt_chunk = nt_chunk

    def set_stream(self, stream):

        self.nfreq = stream.nfreq
    
    def process_chunk(self, t0, t1, intensity, weights, pp_intensity, pp_weights):
        pass
