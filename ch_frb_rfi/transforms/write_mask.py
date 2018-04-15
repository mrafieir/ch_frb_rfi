import rf_pipelines
import ch_frb_rfi
import numpy as np


class WriteWeights(rf_pipelines.wi_transform):

    def __init__(self, nt_chunk=1024, basename=None):
        name = 'WriteWeights(nt_chunk=%d)' % (nt_chunk)
        rf_pipelines.wi_transform.__init__(self, name)

        self.nt_chunk = nt_chunk
        self.basename = basename

    def _bind_transform(self, json_attrs):
        """
        Any initializations which depend on global pipeline parameters (nfreq, dt_sample, etc.)
        can go here. Before _bind_transform() is called, self.nfreq is automatically initialized.
        The CHIME-specific parameters 'freq_lo_MHz', 'freq_hi_MHz', 'dt_sample' are fields in
        the dictionary 'json_attrs'.
        """
        pass

    def _process_chunk(self, intensity, weights, pos):
        """
        'intensity' and 'weights' are 2D numpy arrays of shape (self.nfreq, self.nt_chunk).
        'pos' is the number of samples processed so far (= nt_chunk * (number of chunks so far)).
        """

        if self.basename is None:
            num = np.count_nonzero(weights)
            den = float(weights.size)

            print 'unmasked_fraction =', (num/den)
        else:
            filename = '%s_%d.npz' % (self.basename, pos/self.nt_chunk)
            np.savez(filename, intensity=intensity, weights=weights)

    def jsonize(self):
        return {'nt_chunk': self.nt_chunk,
                'basename': self.basename}

    @staticmethod
    def from_json(j):
        return WriteWeights(nt_chunk = j['nt_chunk'],
                            basename = j['basename'])
