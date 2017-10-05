# MikroTik RouterOS Ringtones

## Installation

Add content of .rsc files as scripts under `/system script`.

## Usage

Run any ringtone with command like this:

    /system script run RINGTONE_NAME

or schedule execution with command like this:

    /system scheduler add name="RINGTONE_NAME" on-event="/system script run RINGTONE_NAME" interval=10
