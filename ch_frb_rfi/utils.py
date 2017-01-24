import os
import sys
import time
import rf_pipelines


def make_rundir_for_web_viewer(name):
    """Returns (dirname, basename) pair."""

    basename = '%s-%s' % (name, time.strftime('%y-%m-%d-%X'))
    dirname = os.path.join('/data2/web_viewer', os.environ['USER'])
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

    (dirname, basename) = make_rundir_for_web_viewer(run_name)

    # Directory names beginning with underscore are pipeline runs in progress.
    temp_dir = os.path.join(dirname, '_' + basename)
    final_dir = os.path.join(dirname, basename)

    print >>sys.stderr, "creating temporary directory '%s' for running pipeline" % temp_dir
    os.makedirs(temp_dir)

    stream.run(transform_chain, outdir=temp_dir, clobber=False)

    # Pipeline done, remove underscore from directory name.
    print >>sys.stderr, 'renaming %s -> %s' % (temp_dir, final_dir)
    os.rename(temp_dir, final_dir)

