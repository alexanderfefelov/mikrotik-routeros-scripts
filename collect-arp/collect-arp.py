#!/usr/bin/env python

from datetime import datetime
from librouteros import connect # https://github.com/luqasz/librouteros
import ConfigParser
import gzip
import json
import logging
import logging.config
import os
import sys


def setup_encoding(): # https://stackoverflow.com/a/40346898
    reload(sys)
    sys.setdefaultencoding('latin-1')


def main():
    home = os.path.dirname(os.path.abspath(__file__))
    os.chdir(home)

    config = ConfigParser.RawConfigParser()
    config.read('application.conf')
    out_dir = config.get('application', 'out_dir')
    timeout = float(config.get('application', 'timeout'))
    boxes = json.loads(config.get('application', 'boxes_json'))

    logging.config.fileConfig('logging.conf')

    setup_encoding()

    for box in boxes:
        host = box['host']
        username = box['username']
        password = box['password']

        try:
            logging.info('Processing %s', host)
            api = connect(host = host, username = username, password = password, timeout = timeout)
            entries = api(cmd = '/ip/arp/print')
            api.close()
            data = set([(entry['mac-address'], entry['interface']) for entry in entries if 'mac-address' in entry])
            file_name = datetime.now().strftime('%Y%m%d%H%M%S') + '-' + host + '.gz'
            file_path = os.path.join(out_dir, file_name)
            with gzip.open(file_path, 'wb') as file:
                for obj in data:
                    file.write(' '.join(obj) + '\n')
            logging.info('%s done', host)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.error(exc_value)


if __name__ == '__main__':
    main()
