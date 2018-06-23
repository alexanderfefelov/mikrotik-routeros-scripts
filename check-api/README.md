# check-api

This script checks RouterOS [API](https://wiki.mikrotik.com/wiki/Manual:API) connectivity and credentials.

## How to use

Install dependencies:

    pip install librouteros

Fill up the [`boxes.csv`](boxes.csv) file.

Revise the [`application.conf`](application.conf) file.

Run:

    check-api.py

Check out the `success.out` and `unable_to_login.out` files.
