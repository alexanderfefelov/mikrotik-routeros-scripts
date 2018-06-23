# run-script-api

This program runs RouterOS script on a bunch of routers via API.

## How to use

Install dependencies:

    pip install librouteros

Fill up the [`boxes.csv`](boxes.csv) file.

Create a script to execute. See [`example.api`](example.api).

Run your script:

    run-script-api.py /path/to/script

Check out the `results.out` file.
