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
    Helper function which adds pipeline_objects to a pipeline.

    The first argument 'p' should be an rf_pipelines.pipeline object.

    Subsequent args should be either pipeline_objects to be appended,
    or lists of pipeline_objects.
    """

    for arg in args:
        if isinstance(arg, rf_pipelines.pipeline_object):
            p.add(arg)
        elif isinstance(arg, list):
            _add_to_pipeline(p, *arg)
        else:
            raise RuntimeError('ch_frb_rfi: arguments to run_for_web_viewer() or run_in_scratch_dir() must be pipeline_objects, or lists of pipeline_objects')


def make_pipeline(*args):
    """
    Helper function which combines pipeline_objects into a pipeline.

    The syntax is flexible: arguments can be either pipeline_objects,
    or lists of pipeline_objects.
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

    Subsequent args must be either pipeline_objects, or lists of pipeline_objects.
    These will be concatenated together to create the pipeline run.
    """

    # run_for_web_viewer() has now been moved to rf_pipelines.utils,
    # and the version in ch_frb_rfi.utils() is just a wrapper.  It's
    # useful to keep this wrapper in place, to avoid breaking old
    # scripts!

    p = make_pipeline(*args)
    rf_pipelines.utils.run_for_web_viewer(run_name, p)


def run_in_scratch_dir(run_name, *args):
    """
    Runs a pipeline in a subdirectory of /data2/scratch_pipelines.
    
    Pipeline runs in this directory will not be indexed by the web viewer, but they
    will stay on disk so that their outputs can be processed by hand if needed.

    Subsequent args must be either pipeline_objects, or lists of pipeline_objects.
    These will be concatenated together to create the pipeline run.
    """

    assert isinstance(run_name, basestring)

    p = make_pipeline(*args)

    (dirname, basename) = make_rundir('scratch_pipelines', run_name)
    outdir = os.path.join(dirname, basename)

    print >>sys.stderr, "creating temporary directory '%s' for running pipeline" % outdir
    os.makedirs(outdir)

    p.run(outdir=outdir, clobber=False)


def sample(path, start, end, nt_chunk=1024):
    """A handy function which allows user to select a range of stream files from an input path"""

    filename_list = sorted(glob.glob(path))[start:end]
    return rf_pipelines.chime_stream_from_filename_list(filename_list, nt_chunk=nt_chunk)


def write_json(filename, p, clobber=False):
    """This helper function is sometimes used to write json files."""

    assert isinstance(filename, basestring)
    assert isinstance(p, rf_pipelines.pipeline_object)
    assert filename.endswith('.json')
    
    d = os.path.dirname(filename)
    if (len(d) > 0) and (not os.path.exists(d)):
        raise RuntimeError("ch_frb_rfi.write_json: directory '%s' does not exist" % d)

    if (not clobber) and os.path.exists(filename):
        raise RuntimeError("ch_frb_rfi.write_json: filename '%s' already exists.  If overwriting is intended, use write_json(clobber=True)" % filename)

    j = p.jsonize()
    f = open(filename, 'w')
    json.dump(j, f, indent=4)
    print >>f, ''  # extra newline
    del f          # close file
    print 'wrote %s' % filename
