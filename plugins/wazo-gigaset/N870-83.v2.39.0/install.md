# Installation

## Role

The `Gigaset N870 IP Pro` needs to be set to the correct role to work with Wazo. By default, the
N870 is set only as a *base*, which means that it does not provide a web interface and needs an
external DECT manager to be able to work properly. It is necessary to set it to the **All-in-one**
role if you want to use it with Wazo. See the [Gigaset
documentation](https://teamwork.gigaset.com/gigawiki/display/GPPPO/FAQ+N870+-+Installation) to know
how to change the role.

## Handset authentication code

In order for the handsets to associate with the DECT base station, it is necessary to enter a PIN in
the register menu on the handset. The authentication code for a device in autoprov mode is `0000`.
For all subsequent handsets, the code is the last four digits of the line extension (e.g. if you
have the `421234` extension, the code will be `1234`). If the line extension is less than four
digits long, leading zeros will be added (e.g. `1` will have the code `0001`).
