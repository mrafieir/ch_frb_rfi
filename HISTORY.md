- Version 11:

   - New RFI configs with an overall 4-sec latency and a uniform
     nt_chunk size in clipping transforms

- Version 10:

   - From Dustin: mask_counter functionality

   - From Alex: L1b usage.

   - New script for post-processing astro events

- Version 9:

   - New transform chain (v1.6, aux-enabled)

- Version 8:

   - From Chitrang: New transform for writing weights to disk

   - New RFI config for processing short events

- Version 7:

   - New RFI configs based on transform chain v1.5

- Version 6:

   - From Alex: L1b functionality

   - From Maya and Kendrick: Updates following API changes in rf_pipelines_v16

   - New scripts for the verification of bonsai and rf_pipelines

   - Json files/scripts, MANUAL.md

- Version 5:

   - Minor updates following API changes in bonsai v9.

   - Integration of variance_estimator, mask_filler.

- Version 4:

   - New transform chain (v1.5)

   - New transform parameter `rfi_level` which allows user to select an appropriate
   chain of transforms based on the severity of the RF environment

- Version 3:

   - Minor updates reflecting API changes in bonsai_v8, rf_pipelines_v13
 
- Version 2:

   - New transform chain (v1.4) and bonsai configurations for analyzing
     16K-frequency data

   - From Kendrick: New library (ch_frb_rfi) for running rf_pipelines
