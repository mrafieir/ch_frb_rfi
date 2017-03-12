This directory contains a few "standard" bonsai config files that we use
when testing RFI removal.

The hdf5 files may be made (but not required) in advance.
```
bonsai-mkweight bonsai_nfreq16K_3tree_v1.txt bonsai_nfreq16K_3tree_v1.hdf5
```

On frb1, the directory /data/bonsai_configs contains up-to-date copies of
these files.  The functions in `ch_frb_rfi.bonsai` assume that you're running on frb1.

Current contents:

  - bonsai_nfreq1024_singletree_v1.txt

    Simplest example, intended for RFI studies with 1024-frequency data and
    testing the web viewer.  Searches with a single dedispersion tree to max DM 276.

  - bonsai_nfreq1024_3tree_v1.txt

    Slightly more complicated, also intended for RFI studies with 1024-frequency data `(dt_sample = 0.00131072)`.
    Searches with three dedispersion trees to max DM 552.

  - bonsai_nfreq1024_3tree_v2.txt

    Intended for RFI studies with 1K-frequency data `(dt_sample = 0.00098304)`.
    Searches with three dedispersion trees to max DM 552.

  - bonsai_nfreq16K_3tree_v1.txt

    Intended for RFI studies with 16K-frequency data `(dt_sample = 0.00098304)`.
    Searches with three dedispersion trees to max DM 552.

  - bonsai_nfreq128K_3tree_v1.txt

    Intended for RFI studies with 128K-frequency data `(dt_sample = 0.00098304)`.
    Searches with three dedispersion trees to max DM 552.

More to come!
