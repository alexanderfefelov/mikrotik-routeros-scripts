# MikroTik RouterOS Wi-Fi Jammer

Wi-Fi Jammer jams some target access point (identified by SSID) by creating rogue access point with the same SSID/frequency/MAC address.

## Disclaimer

This project is a proof of concept for experimental and educational purposes.

Please don't abuse this project as it may be illegal in your country.

## Installation

Revise the Settings section of `wifi-jammer.rsc`.

Add content of revised `wifi-jammer.rsc` as a script with name `wifi-jammer` under `/system script`.

Schedule execution of the script with command like this:

    /system scheduler add name="wifi-jammer" on-event="/system script run wifi-jammer" interval=10

## Removal

To uninstall Wi-Fi Jammer use this commands:

    /system scheduler remove "wifi-jammer"
    /system script remove "wifi-jammer"
