# This module defines CHIME FRB acquisitions on frb1.mcgill.physics.ca
# Most functions here return rf_pipelines.wi_stream objects.

import os
import glob
from types import IntType
import rf_pipelines


def toy():
    """A small arbitrarily-chosen acquisition that we like to use for testing. (1K freq)"""

    filename_list = [ '00000327.h5', '00000344.h5' ]
    filename_list = [ os.path.join('/data/pathfinder/16-09-19-incoherent-without-noise-source',f) for f in filename_list ]

    # Noise source was turned off in this acquisition, so no 'noise_source_align' argument here.
    return rf_pipelines.chime_stream_from_filename_list(filename_list, nt_chunk=1024)


def small():
    """A small arbitrarily-chosen acquisition for testing, a little larger than toy(). (1K freq)"""

    basename_list = [ '00000327.h5', '00000344.h5', '00000360.h5', '00000376.h5', '00000393.h5', '00000409.h5',
                      '00000426.h5', '00000442.h5', '00000458.h5', '00000475.h5', '00000491.h5', '00000508.h5',
                      '00000524.h5', '00000540.h5', '00000557.h5', '00000573.h5', '00000589.h5', '00000606.h5',
                      '00000622.h5', '00000639.h5', '00000655.h5', '00000671.h5', '00000688.h5' ]

    acqdir = '/data/pathfinder/16-09-19-incoherent-without-noise-source'
    filename_list = [ os.path.join(acqdir, basename) for basename in basename_list ]

    # Noise source was turned off in this acquisition, so no 'noise_source_align' argument here.
    return rf_pipelines.chime_stream_from_filename_list(filename_list, nt_chunk=1024)


def incoherent_16_09_19():
    """This is a large acquisition! (~50 GB, 1K freq)"""

    # Noise source was turned off in this acquisition, so no 'noise_source_align' argument here.
    return rf_pipelines.chime_stream_from_acqdir('/data/pathfinder/16-09-19-incoherent-without-noise-source')


def sample(path, start, end):
    """A handy function which allows user to select a range of files from an input path"""

    filename_list = sorted(glob.glob(path))[start:end]
    return rf_pipelines.chime_stream_from_filename_list(filename_list, nt_chunk=1024)


def ex_pulsar_search0():
    """Example: a pulsar in an incoherent-beam acquisition (1K freq)"""

    return rf_pipelines.chime_stream_from_times('/data2/17-02-08-incoherent-data-avalanche/frb_incoherent_search_0', 143897.510543, 144112.258908)


def ex_crab_search0():
    """Example: the Crab pulsar (with two pulses above the 10-sigma threshold at DM=56.6) in an incoherent-beam acquisition (1K freq)."""

    return rf_pipelines.chime_stream_from_times('/data2/17-02-08-incoherent-data-avalanche/frb_incoherent_search_0', 64612.0787149, 64869.7767526)


def crab_16k(n=800):
    """the Crab pulsar in a 16K freq-channel acquisition by the 26m telescope"""
    
    assert type(n) is IntType
    return sample("/data/baseband_26m_processed/17-03-31-crab-20150724T184301Z/*.h5", 0, n)


def incoherent_pathfinder(path='/data2/17-02-08-incoherent-data-avalanche/', search_name=None, sample_index=None):
    """The large catalog of incoherent-beam acquisitions (CHIME Pathfinder)"""
    
    assert (sample_index == None) or ((type(sample_index) == IntType) and sample_index >= 0)
    
    search_path = os.path.join(path, search_name)

    s = { 'frb_incoherent_search_0' : [ '045' , [] ],
          'frb_incoherent_search_1' : [ '021' , [] ],
          'frb_incoherent_search_2' : [ '006' , [] ],
          'frb_incoherent_search_3' : [ '064' , [[165259.558300, 165265.262000],
                                                 [179070.608343, 179628.954092],
                                                 [158841.312379, 159356.708454],
                                                 [222621.576724, 223094.023127],
                                                 [165154.914304, 165412.612342],
                                                 [166185.706455, 166744.052204],
                                                 [197152.420659, 197453.068370]] ],
          
          'frb_incoherent_1c'       : [ '044' , [] ],
          
          'frb_incoherent_2b'       : [ '027' , [[80309.0097766, 80652.6071603],
                                                 [94310.6031616, 94482.4018534],
                                                 [82757.1411354, 82971.8895002],
                                                 [18762.1284250, 19019.8264627],
                                                 [3429.09517824, 3686.79321600]] ],

          'frb_incoherent_2c'       : [ '162' , [] ],
          'frb_incoherent_2d'       : [ '086' , [[16340.5050675, 16555.2534323],
                                                 [30127.3500877, 30256.1991066],
                                                 [36612.7507046, 36784.5493965],
                                                 [37557.6435098, 37686.4925286],
                                                 [135654.696550, 135826.495242]] ],

          'frb_incoherent_3b'       : [ '028' , [[32193.7997824, 32451.4978202]] ],
          'frb_incoherent_3c'       : [ '060' , [] ],

          'frb_incoherent_3d'       : [ '097' , [[9097.78092032, 9269.57961216],
                                                 [134081.329234, 134210.178253],
                                                 [181368.919163, 181497.768182],
                                                 [197346.197504, 197517.996196],
                                                 [196701.952410, 196916.700774]] ],

          'frb_incoherent_4b'       : [ '055' , [[143928.380621, 144143.128986]] ],
          'frb_incoherent_4c'       : [ '142' , [] ],
          'frb_incoherent_4d'       : [ '049' , [] ], }

    if sample_index == None:
        return rf_pipelines.chime_stream_from_acqdir(search_path)
    else:
        return rf_pipelines.chime_stream_from_times(search_path, s[search_name][1][sample_index][0], s[search_name][1][sample_index][1])
