import rf_pipelines
import ch_frb_rfi

class transform_template(rf_pipelines.wi_transform):
    
    def __init__(self, nt_chunk=1024):
        name = 'transform_template(nt_chunk=%d)' % (nt_chunk)
        rf_pipelines.wi_transform.__init__(self, name)
        
        self.nt_chunk = nt_chunk

        
    def _bind_transform(self, json_attrs):
        """
        Any initializations which depend on global pipeline parameters (nfreq, dt_sample, etc.) can go here.
        Before _bind_transform() is called, self.nfreq is automatically initialized.
        The CHIME-specific parameters 'freq_lo_MHz', 'freq_hi_MHz', 'dt_sample' are fields in
        the dictionary 'json_attrs'.
        """
        pass

    
    def _process_chunk(self, intensity, weights, pos):
        """
        'intensity' and 'weights' are 2D numpy arrays of shape (self.nfreq, self.nt_chunk).
        'pos' is the number of samples processed so far (= nt_chunk * (number of chunks so far)).
        """
        pass
