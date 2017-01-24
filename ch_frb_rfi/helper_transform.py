import numpy as np
from types import DictType, ListType
import pprint

import rf_pipelines
from rf_pipelines import rf_pipelines_c


class helper_transform(rf_pipelines.py_wi_transform):
    """
    This transform utilizes HELPER FUNCTIONS to perform 
    an iterated chian of transforms, which may include 
    detrending and clipping algorithms. The iteraion is 
    controlled (hence optimized) by user-defined parameters.

    Constructor syntax:

      t = helper_transform(nt_chunk=1024, fdict=None, rms_cut=0., mask_cut=0.05, max_niter=1, test=False):
      
      'nt_chunk=1024' is the buffer size (in number of samples).

      'fdict=None' must be passed as a dictionary which contains the following lists of transforms:
       
       fdict = {'py':[], 'imitate_cpp':[], 'cpp':[]}
       
       where the key:value pairs are:
        
        'py': [python-based helper functions]
        'imitate_cpp': [python-based cpp-imitated helper functions]
        'cpp': [cpp-based helper functions]
       
       e.g., fdict = {'py' : [ 'clip_fx(...)', 'filter_stdv(...)' ], 
                      'imitate_cpp' : [ 'filter_stdv(..., imitate_cpp=True)' ], 
                      'cpp' : [ 'rf_pipelines_c.apply_intensity_clipper(...)' ]
                     }
      
      'rms_cut=0.' is the rms threshold for the entire chunk.
       If the chunk rms is above this threshold, then all weights 
       are set to zero and further iterations are broken.

      'mask_cut=0.05' is the masking thershold for the entire chunk.
       Iterations proceed only if two consecutive iterations result
       in a fraction-of-unmasked difference greater than this value.
    
      'max_niter=1' is the maximum number of iterations for each chunk.

      'test=False' triggers the test flag.
    """

    def __init__(self, nt_chunk=1024, fdict=None, rms_cut=0., mask_cut=0.05, max_niter=1, test=False):
        
        assert nt_chunk > 0
        assert (type(fdict) is DictType) and ({key for key in fdict.keys()} == {'py', 'imitate_cpp', 'cpp'}),\
            "helper_transform: 'fdict' must be a dictionary with the following format:\n fdict = {'py':[], 'imitate_cpp':[], 'cpp':[]}"
        
        counter = 0
        for value in fdict.values():
            assert type(value) is ListType
            if not value:
                counter += 1
        if ((counter < 2) or (counter == 3)) and (test is False):
            raise RuntimeError("helper_transform(test=False): Supply a non-empty list for only one of the following keys and leave the rest as empty lists: 'py', 'imitate_cpp', 'cpp'")
        
        assert rms_cut >= 0., "helper_transform: rms threshold must be >= 0."
        assert 0.0 <= mask_cut < 0.1
        assert max_niter >= 1
        assert type(test) == bool
        
        self.nt_chunk = nt_chunk
        self.fdict = fdict
        self.rms_cut = rms_cut
        self.mask_cut = mask_cut
        self.max_niter = max_niter
        self.test = test
        self.name = 'helper_transform(nt_chunk=%d, *(fdict)=%d, rms_cut=%f, mask_cut=%f, max_niter=%d)'\
            % (nt_chunk, sum(map(len, fdict.values())), rms_cut, mask_cut, max_niter)

    def set_stream(self, stream):
        
        self.nfreq = stream.nfreq
        
    def process_chunk(self, t0, t1, intensity, weights, pp_intensity, pp_weights):
        
        if self.test:
            raw_weights = weights.copy()
            self.max_niter = 1
            test_results = {}
            rms = 0

        for ix in xrange(self.max_niter):

            if not self.test:
                (mean, rms) = rf_pipelines_c.weighted_mean_and_rms(intensity, weights)

                unmasked_before = self.unmasked(weights)
                unmasked_after = unmasked_before

                if rms > self.rms_cut:
                    weights[:] = 0.
                    break

                if (ix > 0) and (abs(unmasked_before - unmasked_after) < self.mask_cut):
                    break

            for (key, value) in self.fdict.items():
                
                if self.test:
                    weights = raw_weights.copy()

                if not value:
                    if self.test:
                        test_results[key] = []
                    pass

                else:
                    for fx in self.fdict[key]:
                        exec(fx)

                    if self.test:
                        test_results[key] = [self.unmasked(weights), np.mean(weights), np.std(weights)]

            if self.test:
                p = pprint.PrettyPrinter()
                p.pprint(test_results)
                print '\n-----------------------\n'
            else:
                unmasked_after = self.unmasked(weights)

    def unmasked(self, weights):
 
        return np.count_nonzero(weights) / float(weights.size)

