import os
import glob
import sys
import time
import json
import rf_pipelines


def make_rundir(topdir, run_name):
    """
    Returns (dirname, basename) pair.

    The 'topdir' argument should be 'web_viewer' or 'scratch_pipelines' 
    (These are subdirectories of /data2 on frb1.physics.mcgill.ca.)

    The 'run_name' argument should be a descriptive string such as 'example2'.
    """

    basename = '%s-%s' % (run_name, time.strftime('%y-%m-%d-%X'))
    dirname = os.path.join('/data2', topdir, os.environ['USER'])
    return (dirname, basename)


def _add_to_pipeline(p, *args):
    """
    Helper function which appends pipeline_objects to a pipeline.

    The first argument 'p' should be an rf_pipelines.pipeline object.

    Subsequent args should be either:
       - pipeline_objects
       - filenames ending in .json
       - lists of either of these
    """

    for arg in args:
        if isinstance(arg, rf_pipelines.pipeline_object):
            p.add(arg)
        elif isinstance(arg, basestring) and arg.endswith('.json'):
            j = json.load(open(arg))
            x = rf_pipelines.pipeline_object.from_json(j)
            p.add(x)
        elif isinstance(arg, list):
            _add_to_pipeline(p, *arg)
        else:
            raise RuntimeError('ch_frb_rfi: arguments to run_for_web_viewer() or run_in_scratch_dir() must be pipeline_objects, filenames ending in .json, or lists of either of these')


def make_pipeline(*args):
    """
    Helper function which combines arguments into a pipeline.

    The syntax is flexible: arguments can be either
       - pipeline_objects
       - filenames ending in .json
       - lists of either of these
    """

    p = rf_pipelines.pipeline()
    _add_to_pipeline(p, *args)

    if p.size == 0:
        raise RuntimeError('ch_frb_rfi: in either run_for_web_viewer() or run_in_scratch_dir(), no pipeline_objects were specified')

    return p


def run_for_web_viewer(run_name, *args):
    """
    Runs a pipeline, with output directory chosen appropriately for the web viewer
    at frb1.physics.mcgill.ca.

    The 'run_name' argument should be a short descriptive string.  The pipeline rundir 
    will look schematically like "(username)/(run_name)_(time)".

    Subsequent arguments can be either
       - pipeline_objects
       - filenames ending in .json
       - lists of either of these

    These will be concatenated together to create the pipeline run.
    """

    # run_for_web_viewer() has now been moved to rf_pipelines.utils,
    # and the version in ch_frb_rfi.utils() is just a wrapper.  It's
    # useful to keep this wrapper in place, to avoid breaking old
    # scripts!

    p = make_pipeline(*args)
    rf_pipelines.utils.run_for_web_viewer(run_name, p, show_stdout=True)

def run_in_scratch_dir(run_name, dirname=None, *args):
    """
    Runs a pipeline in
        - a subdirectory of /data2/scratch_pipelines.
        or
        - dirname (if not None)
    
    Pipeline runs in this directory will not be indexed by the web viewer, but they
    will stay on disk so that their outputs can be processed by hand if needed.

    Subsequent arguments can be either
       - pipeline_objects
       - filenames ending in .json
       - lists of either of the above

    These will be concatenated together to create the pipeline run.
    """

    assert isinstance(run_name, basestring)

    p = make_pipeline(*args)

    if dirname is None:
        (dirname, basename) = make_rundir('scratch_pipelines', run_name)
        outdir = os.path.join(dirname, basename)
    else:
        outdir = os.path.join(dirname, run_name)

    print >>sys.stderr, "creating temporary directory '%s' for running pipeline" % outdir
    os.makedirs(outdir)

    p.run(outdir=outdir, clobber=False)

def run_in_custom_dir(output_directory, output_acq_name, s , p16k):
    """
    Runs rf pipelines in a custom directory : output_directory.
    Name if the json file : output_acq_name
    streams to run the pipeline on : s
    chain of transforms: p16k

    """
                                                                                                                                                       
    p = make_pipeline(s, p16k)                                                                                                                         
                                                                                                                                                       
    outdir = os.path.join(output_directory, output_acq_name)                                                                                           
                                                                                                                                                       
    print >>sys.stderr, "creating temporary directory '%s' for running pipeline" % outdir                                                              
    os.makedirs(outdir)                                                                                                                                
                                                                                                                                                       
    p.run(outdir=outdir, clobber=False)                                                                                                                
                                          

def sample(path, start, end, nt_chunk=1024):
    """A handy function which allows user to select a range of stream files from an input path"""

    filename_list = sorted(glob.glob(path))[start:end]
    return rf_pipelines.chime_stream_from_filename_list(filename_list, nt_chunk=nt_chunk)
