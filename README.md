### CH_FRB_RFI

A plugin-based framework for processing channelized intensity data in radio astronomy.

### INSTALLATION

- Please follow all the instructions in [kmsmith137/ch_frb_l1/doc/install.md](https://github.com/kmsmith137/ch_frb_l1/blob/master/doc/install.md)

- Define an environment variable `RFIDATA` pointing to `ch_frb_rfi_data` (e.g. append `export RFIDATA=/frb-archiver-1/ch_frb_rfi_data` to `~/.bashrc`).

- Create a file `Makefile.local` defining a few Makefile variables (see an example in `site/`)

- `make install`

### DOCUMENTATION

See [MANUAL.md](./MANUAL.md).
