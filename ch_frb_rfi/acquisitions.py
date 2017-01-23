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


def incoherent_16_09_19():
    # Noise source was turned off in this acqusition, so no 'noise_source_align' argument here.
    return rf_pipelines.chime_stream_from_acqdir('/data/pathfinder/16-09-19-incoherent-without-noise-source')
