# MikroTik RouterOS Wi-Fi Jammer

## Installation

Revise the Settings section of `wifi-jammer.rsc`.

Add content of revised `wifi-jammer.rsc` as a script with name `wifi-jammer` under `/system script`.

Schedule execution of the script with command like this:

    /system scheduler add name="wifi-jammer" on-event="/system script run wifi-jammer" interval=10

## Removal

To uninstall Wi-Fi Jammer use this commands:

    /system scheduler remove "wifi-jammer"
    /system script remove "wifi-jammer"
