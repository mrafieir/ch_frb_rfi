#!/usr/bin/env python
#
# Some examples of "interesting" incoherent-beam CHIME pathfinder data (also in scripts/s*.py)
# From Masoud (17-08-11)

import rf_pipelines
import ch_frb_rfi

# To guard against accidentally modifying git-managed json files
clobber = False

# Masoud says: "A faint source at low DM"
rf_pipelines.json_write('../../json_files/acqs/17-08-11-masoud-examples/s1.json', 
                        ch_frb_rfi.acquisitions.incoherent_pathfinder(search_name='frb_incoherent_search_3', sample_index=6),
                        clobber = clobber)

# Masoud says: "An RFI storm which results in a single false positive: (DM, SNR) = (77.62, 10.64)"
rf_pipelines.json_write('../../json_files/acqs/17-08-11-masoud-examples/s2.json',
                        ch_frb_rfi.acquisitions.incoherent_pathfinder(search_name='frb_incoherent_4b', sample_index=0),
                        clobber = clobber)

# Masoud says: "A periodic variation in intensity, combined with RFIs, makes it very hard to suppress all the false positives."
rf_pipelines.json_write('../../json_files/acqs/17-08-11-masoud-examples/s3.json',
                        ch_frb_rfi.acquisitions.incoherent_pathfinder(search_name='frb_incoherent_search_3', sample_index=5),
                        clobber = clobber)

# Masoud says: "This sample contains two major RFI events which result in a large fraction of zero weights along the time axis."
rf_pipelines.json_write('../../json_files/acqs/17-08-11-masoud-examples/s4.json',
                        ch_frb_rfi.acquisitions.incoherent_pathfinder(search_name='frb_incoherent_3b', sample_index=0),
                        clobber = clobber)

# Masoud says: "This example contains a pulsar. In addition, there seems to be a strange variation
# in the overall intensity which can be revealed by using (detrender_niter, clipper_niter) = (1, 3)."
rf_pipelines.json_write('../../json_files/acqs/17-08-11-masoud-examples/s5.json',
                        ch_frb_rfi.acquisitions.incoherent_pathfinder(search_name='frb_incoherent_2d', sample_index=4),
                        clobber = clobber)

# Masoud says: "This short sample represents a highly active RF environment!"
rf_pipelines.json_write('../../json_files/acqs/17-08-11-masoud-examples/s6.json',
                        ch_frb_rfi.acquisitions.incoherent_pathfinder(search_name='frb_incoherent_2d', sample_index=3),
                        clobber = clobber)

# Masoud says: "Another highly active RF environment."
rf_pipelines.json_write('../../json_files/acqs/17-08-11-masoud-examples/s7.json',
                        ch_frb_rfi.acquisitions.incoherent_pathfinder(search_name='frb_incoherent_2d', sample_index=2),
                        clobber = clobber)

# Masoud says: "Another highly active RF environment."
rf_pipelines.json_write('../../json_files/acqs/17-08-11-masoud-examples/s8.json',
                        ch_frb_rfi.acquisitions.incoherent_pathfinder(search_name='frb_incoherent_2d', sample_index=1),
                        clobber = clobber)

# Masoud says: "This is an interesting example: It contains an RFI storm, a few false positives,
# and some significant changes in the running variance."
rf_pipelines.json_write('../../json_files/acqs/17-08-11-masoud-examples/s9.json',
                        ch_frb_rfi.acquisitions.incoherent_pathfinder(search_name='frb_incoherent_2d', sample_index=0),
                        clobber = clobber)

# Masoud says: "B0329 (can be analyzed with rfi_level = 1)"
rf_pipelines.json_write('../../json_files/acqs/17-08-11-masoud-examples/s10.json',
                        ch_frb_rfi.acquisitions.incoherent_pathfinder(search_name='frb_incoherent_2b', sample_index=2),
                        clobber = clobber)

# Masoud says: "6 hours of data"
rf_pipelines.json_write('../../json_files/acqs/17-08-11-masoud-examples/s11.json',
                        ch_frb_rfi.acquisitions.incoherent_pathfinder(search_name='frb_incoherent_search_2'),
                        clobber = clobber)

# Masoud says: "5 min of data"
rf_pipelines.json_write('../../json_files/acqs/17-08-11-masoud-examples/s12.json',
                        ch_frb_rfi.acquisitions.incoherent_pathfinder(search_name='frb_incoherent_search_3', sample_index=6),
                        clobber = clobber)

# Masoud says: "4 min of data"
rf_pipelines.json_write('../../json_files/acqs/17-08-11-masoud-examples/s13.json',
                        ch_frb_rfi.acquisitions.incoherent_pathfinder(search_name='frb_incoherent_3d', sample_index=4),
                        clobber = clobber)
