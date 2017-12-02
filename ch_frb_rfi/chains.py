# This file contains RFI transform chains for CHIME!
# Most functions here return lists of rf_pipelines.wi_transform objects.

import os
import sys
import glob
import numpy as np
import rf_pipelines

class transform_parameters:
    """
    transform_parameters: an aggregator class to hold parameters for initializing transforms.

    Constructor syntax:

        p = transform_parameters(rfi_level=0, detrender_niter=None, clipper_niter=None, detrend_nt=1024, clip_nt=1024, detrend_last=True, two_pass=True, spline=False,
                                 make_plots=True, plot_type=None, plot_downsample_nt=None, plot_nxpix=None, plot_nypix=None, bonsai_plot_nypix=256, plot_nzoom=None,
                                 bonsai_output_plot_stem=None, bonsai_use_analytic_normalization=False, bonsai_hdf5_output_filename=None, bonsai_nt_per_hdf5_file=0, 
                                 bonsai_plot_threshold1=6, bonsai_plot_threshold2=10, bonsai_dynamic_plotter=False, maskpath=None, bonsai_event_outfile=None, 
                                 bonsai_plot_all_trees=False, bonsai_fill_rfi_mask=False, mask=None, variance_estimator_v1_chunk=32, variance_estimator_v2_chunk=192, 
                                 var_filename=None, var_est=False, mask_filler=False, mask_filler_w_cutoff=0.5, L1Grouper_thr=7, L1Grouper_beam=0, L1Grouper_addr=None)
    
    with arguments as follows:

       - rfi_level: specifies the severity of the RF environment. Possible modes are           
           0: is the base mode which is recommended for a relatively quiet environment. (detrender_niter=1, clipper_niter=3)
           1: can handle some storms. (detrender_niter=2, clipper_niter=3)
           2: is recommended for obtaining very low false-positive rates. (detrender_niter=2, clipper_niter=6)
            
           Note: If detrender_niter and clipper_niter are specified explicitly, then these are used. 

       - detrender_niter/clipper_niter: 
           number of iterations of outer detrender loop and inner clipper loop.

       - detrend_nt/clip_nt: 
           chunk sizes (in time samples) for detrender transforms and clipper transforms respectively.

       - detrend_last: if True, then the RFI transform chain ends with a chain of detrenders.
           This is required for removing intensity residuals due to preceding transforms.

       - two_pass: if True, then the first round of clipper transforms will use a
            more numerically stable, but slightly slower, clipping algorithm.

       - spline: if True, then spline_detrender will be used instead of the polynomial_detrender.  (Experimental.)
            Currently only for AXIS_FREQ!  If the results of this experiment look good, then I'll implement
            AXIS_TIME and AXIS_NONE.

       - bonsai_output_plot_stem: if None, then no bonsai plots will be written. If a string is 
            specified (e.g. 'triggers'), then a sequence of bonsai plots will be written with 
            filenames beginning with the string (e.g. triggers_0_tree2.png).
    
       - bonsai_use_analytic_normalization: if True, then the dedisperser will use the exact trigger
           normalization, assuming a toy model in which each input (frequency, time) sample is an
           uncorrelated Gaussian.  Not suitable for real data!

       - bonsai_hdf5_output_filename: if specified, HDF5 file(s) containing coarse-grained triggers will be written.

       - bonsai_nt_per_hdf5_file: only meaningful if bonsai_hdf5_output_filename=True.  Zero means "one big file".

       - bonsai_plot_nypix: is a bonsai plot argument. It specifies the number of pixels along the DM axis.

       - (bonsai_plot_threshold1, bonsai_plot_threshold2) are bonsai plot arguments. They specify the following color scheme:
            
            (X < threshold1) : (blue to red)
            (threshold1 < X < threshold2) : (yellow)
            (threshold2 < X) : (light green)

       - bonsai_dynamic_plotter: if True, then the old color scheme (with a higher dynamic range from blue to red) is used.

       - bonsai_event_outfile: specifies a file path to the grouper output. The grouper is disabled by default. 

       - bonsai_plot_all_trees: if False, only tree 0 will be plotted; if True, all trees will be plotted.

       - bonsai_fill_rfi_mask: if True, then bonsai's online_mask_filler will be enabled.

       - maskpath: is a full path to the mask file which contains a list of previously-identified 
            RFI-contaminated frequency channels. If None, then the argument 'mask' is used instead.
        
       - mask: is a list of to-be-masked frequency channels in this format: e.g. mask=[[401,413.7],[654,736.012]]
            
       Note: If both 'mask' and 'maskpath' are None, then the badchannel_mask transform is disabled. Otherwise,
            the badchannel_mask transfrom can be appended to the transform chain via append_badchannel_mask().
       
       - (variance_estimator_v1_chunk, variance_estimator_v2_chunk, var_filename) = (128, 80, None)
            define parameters for the variance_estimator transform (see its docstrings!).

       - var_est: if True, then it appends a variance_estimator transform to the chain after all clippers and 
            detrenders. Hence, transform_chain = [ .. , the last detrenders, variance_estimator ].
       
       - mask_filler: if True, then a mask_filler transform is appended to the chain after all clippers but 
            before the last detrenders (and the bonsai dedisperser). Hence, 
            transform_chain = [ .. , mask_filler , the last detrenders (, bonsai_dedisperser) ].

       Note: the variance_estimator and mask_filler transforms are not allowed to be in the same chain!

       - mask_filler_w_cutoff: is the cutoff value for weights in the mask_filler transform. Only meaningful if
            mask_filler is not None. E.g., a w_cutoff value of 0.5 corresponds to a 25% w_cutoff in the 
            incoherent-beam data.

       - (L1Grouper_thr, L1Grouper_beam, L1Grouper_addr) specify parameters for the L1Grouper which may be called
            in the bonsai dedisperser transform. (see their docstrings!)
            Note: 'bonsai_event_outfile' determines whether to en(/dis)able the L1Grouper.

    The way the plotting parameters are determined deserves special explanation!

       - If the four "fine-grained" plotting parameters (plot_downsample_nt, plot_nxpix, plot_nypix, plot_nzoom)
         are specified explicitly, then these are used.

       - As a shortcut, one can specify the string-valued argument 'plot_type':

           plot_type='web_viewer'  shortcut for (plot_downsample_nt, plot_nxpix, plot_nypix, plot_nzoom) = (16, 256, 256, 4)
           plot_type='big'         shortcut for (plot_downsample_nt, plot_nxpix, plot_nypix, plot_nzoom) = (16, 1200, 512, 1)

       - Specifying fine-grained plotting parameters will override the plot_type defaults, e.g.
           p = ch_frb_rfi.transform_parameters(plot_type='web_viewer', plot_nzoom=6)
         gives (plot_downsample_nt, plot_nxpix, plot_nypix, plot_nzoom) = (16, 256, 256, 6).

       - If make_plots is False, then the plotter transform is disabled.

    By default (if no plotting-related constructor arguments are specified), plotting is disabled.
    """

    def __init__(self, rfi_level=0, detrender_niter=None, clipper_niter=None, detrend_nt=1024, clip_nt=1024, detrend_last=True, two_pass=True, spline=False,
                 make_plots=True, plot_type=None, plot_downsample_nt=None, plot_nxpix=None, plot_nypix=None, bonsai_plot_nypix=256, plot_nzoom=None, 
                 bonsai_output_plot_stem=None, bonsai_use_analytic_normalization=False, bonsai_hdf5_output_filename=None, bonsai_nt_per_hdf5_file=0,
                 bonsai_plot_threshold1=6, bonsai_plot_threshold2=10, bonsai_dynamic_plotter=False, bonsai_event_outfile=None, bonsai_plot_all_trees=False,
                 bonsai_fill_rfi_mask=False, maskpath=None, mask=None, variance_estimator_v1_chunk=32, variance_estimator_v2_chunk=192, var_filename=None, 
                 var_est=False, mask_filler=False, mask_filler_w_cutoff=0.5, L1Grouper_thr=7, L1Grouper_beam=0, L1Grouper_addr=None):

        nv = 0
        if var_est: nv += 1
        if mask_filler: nv += 1
        if bonsai_fill_rfi_mask: nv += 1

        if nv > 1:
            raise RuntimeError("transform_parameters: at most one of { var_est, mask_filler, bonsai_fill_rfi_mask } may be specified")

        self.rfi_level = rfi_level
        self.detrend_nt = detrend_nt
        self.clip_nt = clip_nt
        self.detrend_last = detrend_last

        self.two_pass = two_pass
        self.spline = spline

        self.bonsai_output_plot_stem = bonsai_output_plot_stem
        self.bonsai_plot_nypix = bonsai_plot_nypix
        self.bonsai_use_analytic_normalization = bonsai_use_analytic_normalization
        self.bonsai_hdf5_output_filename = bonsai_hdf5_output_filename
        self.bonsai_nt_per_hdf5_file = bonsai_nt_per_hdf5_file
        self.bonsai_plot_threshold1 = bonsai_plot_threshold1
        self.bonsai_plot_threshold2 = bonsai_plot_threshold2
        self.bonsai_dynamic_plotter = bonsai_dynamic_plotter
        self.bonsai_event_outfile = bonsai_event_outfile
        self.bonsai_plot_all_trees = bonsai_plot_all_trees
        self.bonsai_fill_rfi_mask = bonsai_fill_rfi_mask

        self.L1Grouper_thr = L1Grouper_thr
        self.L1Grouper_beam = L1Grouper_beam
        self.L1Grouper_addr = L1Grouper_addr

        self.maskpath = maskpath
        self.mask = mask

        self.variance_estimator_v1_chunk = variance_estimator_v1_chunk
        self.variance_estimator_v2_chunk = variance_estimator_v2_chunk
        self.var_filename = var_filename
        self.var_est = var_est

        self.mask_filler = mask_filler
        self.mask_filler_w_cutoff = mask_filler_w_cutoff

        # This block of code selects a pair of (detrender_niter, clipper_nitr) 
        # values based on input parameters. See docstring above!

        if (detrender_niter is not None) and (clipper_niter is not None):
           print "transform_parameters: the preset rfi_level is disabled."
           self.detrender_niter = detrender_niter
           self.clipper_niter = clipper_niter
        elif self.rfi_level == 0:
           (self.detrender_niter, self.clipper_niter) = (1, 3)
        elif self.rfi_level == 1:
           (self.detrender_niter, self.clipper_niter) = (2, 3)
        elif self.rfi_level == 2:
           (self.detrender_niter, self.clipper_niter) = (2, 6)
        else:
           raise RuntimeError("transform_parameters: either a valid rfi_level (0, 1, or 2) or a (detrender_niter, clipper_nitr)" 
                              + " pair must be specified.")
 
        # The rest of the constructor initializes plotting parameters.
        # See docstring above for a description of the initialization logic!
        
        self.make_plots = make_plots

        if plot_type is 'big':
            self.plot_downsample_nt = 16
            self.plot_nxpix = 1200
            self.plot_nypix = 512
            self.plot_nzoom = 1
        elif plot_type is 'web_viewer':
            self.plot_downsample_nt = 16
            self.plot_nxpix = 256
            self.plot_nypix = 256
            self.plot_nzoom = 4
        elif plot_type is not None:
            raise RuntimeError("ch_frb_rfi.transform_parameters constructor: plot_type='%s' is unrecognized" % plot_type)
        elif (plot_downsample_nt is None) and (plot_nxpix is None) and (plot_nypix is None) and (plot_nzoom is not None):
            # OK: no plots will be written
            self.make_plots = False
        elif (plot_downsample_nt is None) or (plot_nxpix is None) or (plot_nypix is None) or (plot_nzoom is None):
            raise RuntimeError("transform_parameters: if plot_type is unspecified, then either all or none of"
                               + " (plot_downsample_nt, plot_nxpix, plot_nypix, plot_nzoom) must be specified")

        if plot_downsample_nt is not None:
            self.plot_downsample_nt = plot_downsample_nt
        if plot_nxpix is not None:
            self.plot_nxpix = plot_nxpix
        if plot_nypix is not None:
            self.plot_nypix = plot_nypix
        if plot_nzoom is not None:
            self.plot_nzoom = plot_nzoom

    def append_plotter_transform(self, transform_chain, img_prefix):
        if self.make_plots:
            t = rf_pipelines.plotter_transform(img_prefix, self.plot_nypix, self.plot_nxpix, self.plot_downsample_nt, self.plot_nzoom)
            transform_chain.append(t)

    def append_badchannel_mask(self, transform_chain):
        if (self.maskpath != None) or (self.mask != None):
            t = rf_pipelines.badchannel_mask(mask_path=self.maskpath, mask_ranges=self.mask)
            transform_chain.append(t)
    
    def append_variance_estimator(self, transform_chain, ix):
        if (self.var_est) and (ix == self.detrender_niter - 1):
            if self.var_filename is None:
                raise RuntimeError('ch_frb_rfi.parameters.append_variance_estimator() was called, but var_filename is None')
            t = rf_pipelines.variance_estimator(v1_chunk=self.variance_estimator_v1_chunk, v2_chunk=self.variance_estimator_v2_chunk, var_filename=self.var_filename, nt_chunk=self.clip_nt) 
            transform_chain.append(t)

    def append_mask_filler(self, transform_chain, ix):
        if (self.mask_filler) and (ix == self.detrender_niter - 1):
            if self.var_filename is None:
                raise RuntimeError('ch_frb_rfi.parameters.append_mask_filler() was called, but var_filename is None')
            t = rf_pipelines.mask_filler(var_file=self.var_filename, w_cutoff=self.mask_filler_w_cutoff, nt_chunk=self.clip_nt)            
            transform_chain.append(t)

##############################  T R A N S F O R M   C H A I N S  ##############################


def detrender_chain(parameters, ix):
    assert isinstance(parameters, transform_parameters)

    if (not parameters.detrend_last) and (parameters.detrender_niter == (ix + 1)): return []

    # AXIS_TIME (nt_chunk must be nonzero here)
    ret = [ rf_pipelines.polynomial_detrender(polydeg=4, axis='time', nt_chunk=parameters.detrend_nt) ]

    # AXIS_FREQ (nt_chunk=0 is OK here)
    if parameters.spline:
        ret += [ rf_pipelines.spline_detrender(nbins=6, axis='freq', nt_chunk=0) ]
    else:
        ret += [ rf_pipelines.polynomial_detrender(polydeg=12, axis='freq', nt_chunk=0) ]

    return ret


def clipper_chain(parameters, ix):
    two_pass = parameters.two_pass and (ix == 0)
    
    return [ rf_pipelines.std_dev_clipper(sigma=3, axis=1, nt_chunk=parameters.clip_nt, Df=1, Dt=1, two_pass=two_pass),
             rf_pipelines.std_dev_clipper(sigma=3, axis=1, nt_chunk=2*parameters.clip_nt, Df=1, Dt=1, two_pass=two_pass),
             rf_pipelines.std_dev_clipper(sigma=3, axis=1, nt_chunk=6*parameters.clip_nt, Df=1, Dt=1, two_pass=two_pass),

             rf_pipelines.std_dev_clipper(sigma=3, axis=0, nt_chunk=6*parameters.clip_nt, Df=1, Dt=1, two_pass=two_pass),
             rf_pipelines.std_dev_clipper(sigma=3, axis=0, nt_chunk=6*parameters.clip_nt, Df=1, Dt=1, two_pass=two_pass),
             
             rf_pipelines.intensity_clipper(sigma=5, niter=9, iter_sigma=5, axis=0, nt_chunk=parameters.clip_nt, Df=1, Dt=1, two_pass=two_pass),
             rf_pipelines.intensity_clipper(sigma=5, niter=9, iter_sigma=5, axis=1, nt_chunk=parameters.clip_nt, Df=1, Dt=1, two_pass=two_pass),

             rf_pipelines.intensity_clipper(sigma=5, niter=9, iter_sigma=3, axis=None, nt_chunk=parameters.clip_nt, Df=2, Dt=16, two_pass=two_pass),
             rf_pipelines.intensity_clipper(sigma=5, niter=9, iter_sigma=3, axis=0, nt_chunk=parameters.clip_nt, Df=2, Dt=16, two_pass=two_pass) ]

       
def transform_chain(parameters):
    transform_chain = [ ]
    parameters.append_plotter_transform(transform_chain, 'raw')
    parameters.append_badchannel_mask(transform_chain)

    for ix in xrange(parameters.detrender_niter):
        
        for jx in xrange(parameters.clipper_niter):
            transform_chain += clipper_chain(parameters, ix)
        
        parameters.append_plotter_transform(transform_chain, 'dc_out_a%d' % ix)
        
        parameters.append_mask_filler(transform_chain, ix)
        transform_chain += detrender_chain(parameters, ix)
        parameters.append_variance_estimator(transform_chain, ix)

        parameters.append_plotter_transform(transform_chain, 'dc_out_b%d' % ix)

    return transform_chain
