# wazo-provd-plugins

`wazo-provd-plugins` is the complete collection of phone provisioning plugins available for Wazo.

## Repositories and branches

The plugins in the `master` branch for the latest release are Python 3 only and are published to the new repository URL.
The old versions of the plugins compatible with Python 2 are location in the branch `python2`.

## Plugin information files

The plugin information files (`plugin-info`) contain metadata about plugins in JSON format.
They include the supported phone models, firmware versions and features.

Valid keys are described as follows:

* `lines` (integer): the number of lines
* `high_availability` (boolean): high availability support
* `function_keys` (integer): maximum number of function keys
* `expansion_modules` (integer): maximum number of expansion modules
* `switchboard` (boolean): switchboard support
* `protocol` (string): the protocol used by the phones, usually `sip` or `sccp`
* `type` (string): the device type. Can be either `deskphone`, `dect`, `wifidect`, `conference`, `pager`,
  `ata`, `softphone`, `doorphone`, `generic` or `gateway`
* `multicell` (boolean): DECT multicell support. Only defined when `type` is `dect`.

A key that is not present in a `plugin-info` file means that this information is unknown. This
situation is possible when a new key is added and only some plugins support it, or when it was not
possible to test it.

### Install files

A file named `install.md` can be present at the root of a plugin. If present, it is important to
read prior to installation, as it can provide some information on what to do to get it running.

### Limitations file

A file named `limitations.md` can be present at the root of a plugin. If present, it can be useful
to read if you want to know what is not supported or what is not completely supported by the plugin
or the phone.

## Firmware management

If you wish to host firmwares for specific phones, go to the `plugins/_firmwares` directory.
Find the subdirectory specific to the brand (i.e `yealink`) then put the firmware files into it.
You can then execute `make upload-firmwares` to upload them to the web server.

## Add a new firmware brand

Create a new subdirectory named after the brand in `plugins/_firmwares` and put an empty file
named `.brand` in it. Commit it to the git repository. Then, add the firmware files and execute
`make upload-firmwares`.

## Download all firmware

If you wish to download all firmwares present on the web server, you can execute
`make download-firmwares`

## To build Test plugins

wazo-test-plugins is mainly used by wazo-provd integration tests. To build it,
we can execute
`make build-tests`

