import os
import glob
import sys
import time
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


def run_for_web_viewer(run_name, stream, transform_chain):
    """
    Runs a pipeline, with output directory chosen appropriately for the web viewer
    at frb1.physics.mcgill.ca.

    The 'run_name' argument should be a short descriptive string.  The pipeline rundir 
    will look schematically like "(username)/(run_name)_(time)".
    """

    assert isinstance(run_name, basestring)
    assert isinstance(stream, rf_pipelines.wi_stream)
    assert all(isinstance(t,rf_pipelines.wi_transform) for t in transform_chain)

    (dirname, basename) = make_rundir('web_viewer', run_name)

    # Directory names beginning with underscore are pipeline runs in progress.
    temp_dir = os.path.join(dirname, '_' + basename)
    final_dir = os.path.join(dirname, basename)

    print >>sys.stderr, "creating temporary directory '%s' for running pipeline" % temp_dir
    os.makedirs(temp_dir)

    stream.run(transform_chain, outdir=temp_dir, clobber=False)

    # Pipeline done, remove underscore from directory name.
    print >>sys.stderr, 'renaming %s -> %s' % (temp_dir, final_dir)
    os.rename(temp_dir, final_dir)


def run_in_scratch_dir(run_name, stream, transform_chain):
    """
    Runs a pipeline in a subdirectory of /data2/scratch_pipelines.
    
    Pipeline runs in this directory will not be indexed by the web viewer, but they
    will stay on disk so that their outputs can be processed by hand if needed.
    """

    for t in transform_chain:
        print t.name, isinstance(t,rf_pipelines.wi_transform)

    assert isinstance(run_name, basestring)
    assert isinstance(stream, rf_pipelines.wi_stream)
    assert all(isinstance(t,rf_pipelines.wi_transform) for t in transform_chain)

    (dirname, basename) = make_rundir('scratch_pipelines', run_name)
    outdir = os.path.join(dirname, basename)

    print >>sys.stderr, "creating temporary directory '%s' for running pipeline" % outdir
    os.makedirs(outdir)

    stream.run(transform_chain, outdir=outdir, clobber=False)


def sample(path, start, end, nt_chunk=1024):
    """A handy function which allows user to select a range of stream files from an input path"""

    filename_list = sorted(glob.glob(path))[start:end]
    return rf_pipelines.chime_stream_from_filename_list(filename_list, nt_chunk=nt_chunk)
