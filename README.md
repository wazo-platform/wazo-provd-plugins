# wazo-provd-plugins

`wazo-provd-plugins` is the complete collection of phone provisioning plugins available for Wazo.

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

A key that is not present in a `plugin-info` file means that this information is unknown. This
situation is possible when a new key is added and only some plugins support it, or when it was not
possible to test it.
