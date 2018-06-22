#!/usr/bin/env python

from __future__ import print_function
from datetime import datetime
from librouteros import connect # https://github.com/luqasz/librouteros
import ConfigParser
import csv
import gzip
import json
import logging
import logging.config
import os
import os.path
import sys


def setup_encoding(): # https://stackoverflow.com/a/40346898
    reload(sys)
    sys.setdefaultencoding('latin-1')


def main():
    if (len(sys.argv)) != 2:
        print('Usage: {0} /path/to/script'.format(sys.argv[0]))
        sys.exit(1)

    script_path = sys.argv[1]
    if (not os.path.isfile(script_path)):
        print('File {0} does not exist'.format(sys.argv[1]))
        sys.exit(1)

    home = os.path.dirname(os.path.abspath(__file__))
    os.chdir(home)

    config = ConfigParser.RawConfigParser()
    config.read('application.conf')
    timeout = float(config.get('application', 'timeout'))
    boxes_csv = config.get('application', 'boxes_csv')
    results_out = config.get('application', 'results_out')

    logging.config.fileConfig('logging.conf')

    setup_encoding()

    boxes = []
    with open(boxes_csv, 'rb') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for r in reader:
            boxes.append({fieldnames[i]: r[fieldnames[i]] for i in range(len(fieldnames))})
    logging.info('%d box(es) will be processed', len(boxes))

    script = ''
    with open(script_path) as f:
        script = f.read().splitlines()

    WRITE_BUFFER_SIZE = 0
    with open(results_out, 'wb', WRITE_BUFFER_SIZE) as results_out_f:
        processed = 0
        for box in boxes:
            host = box['host']
            username = box['username']
            password = box['password']

            print('# -----[ {0} ]-----'.format(host), file = results_out_f)
            try:
                logging.info('Processing %s', host)
                api = connect(host = host, username = username, password = password, timeout = timeout)
                for line in script:
                    cmd = line.strip()
                    if (len(cmd) > 0 and not line.startswith('#')):
                        print('# {0}'.format(cmd), file = results_out_f)
                        splitted = cmd.split(' ', 1)
                        command = splitted[0]
                        arguments = dict()
                        if (len(splitted) == 2):
                            arguments = json.loads(splitted[1])
                        result = api(cmd = command, **arguments)
                        print(json.dumps(result), file = results_out_f)
                api.close()
                logging.info('%s done', host)
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                logging.error(exc_value)
            processed += 1
            if (processed % 50 == 0):
                logging.info('%d boxes processed', processed)
        logging.info('%d boxes processed', processed)


if __name__ == '__main__':
    main()
