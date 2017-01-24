# This module defines CHIME FRB acquisitions on frb1.mcgill.physics.ca
# Most functions here return rf_pipelines.wi_stream objects.

import os
import rf_pipelines

def toy():
    """A small arbitrarily-chosen acquisition that we like to use for testing."""

    filename_list = [ '00000327.h5', '00000344.h5' ]
    filename_list = [ os.path.join('/data/pathfinder/16-09-19-incoherent-without-noise-source',f) for f in filename_list ]

    # Noise source was turned off in this acqusition, so no 'noise_source_align' argument here.
    return rf_pipelines.chime_stream_from_filename_list(filename_list, nt_chunk=1024)


def small():
    """A small arbitrarily-chosen acquisition for testing, a little larger than toy()."""

    basename_list = [ '00000327.h5', '00000344.h5', '00000360.h5', '00000376.h5', '00000393.h5', '00000409.h5',
                      '00000426.h5', '00000442.h5', '00000458.h5', '00000475.h5', '00000491.h5', '00000508.h5',
                      '00000524.h5', '00000540.h5', '00000557.h5', '00000573.h5', '00000589.h5', '00000606.h5',
                      '00000622.h5', '00000639.h5', '00000655.h5', '00000671.h5', '00000688.h5' ]

    acqdir = '/data/pathfinder/16-09-19-incoherent-without-noise-source'
    filename_list = [ os.path.join(acqdir, basename) for basename in basename_list ]

    # Noise source was turned off in this acqusition, so no 'noise_source_align' argument here.
    return rf_pipelines.chime_stream_from_filename_list(filename_list, nt_chunk=1024)


def incoherent_16_09_19():
    """This is a large acquisition! (~50 GB)"""

    # Noise source was turned off in this acqusition, so no 'noise_source_align' argument here.
    return rf_pipelines.chime_stream_from_acqdir('/data/pathfinder/16-09-19-incoherent-without-noise-source')
