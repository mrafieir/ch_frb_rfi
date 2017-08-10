"""
ch_frb_rfi: currently defines an acqusition database, RFI-removing transform chains, 
    and a transform template.

Functions returning transform chains are imported at top level, e.g.
    ch_frb_rfi.clipper_chain()
    ch_frb_rfi.detrender_chain()
    ch_frb_rfi.transform_chain()

See docstrings for more details.

Functions returning streams are in the 'acqusitions' sub-package, e.g.
    ch_frb_rfi.acquisitions.toy()
    ch_frb_rfi.acquisitions.incoherent_16_09_19()

For a list of all acquisitions available, see dir(ch_frb_rfi.acquisitions).
"""

# These functions are imported to the top level of the ch_frb_rfi package.
from chains import clipper_chain, \
    detrender_chain, \
    transform_chain, \
    transform_parameters

from transform_template import transform_template

from utils import run_for_web_viewer, run_in_scratch_dir, sample

# Example syntax: ch_frb_rfi.acquisitions.toy()
from . import acquisitions

# Example syntax: ch_frb_rfi.bonsai.nfreq1024_singletree()
from . import bonsai
