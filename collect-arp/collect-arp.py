#!/usr/bin/env python

import sys
import os
import ConfigParser
import json
import logging
import logging.config
from datetime import datetime
import gzip
import routeros_api # https://github.com/socialwifi/RouterOS-api


def setup_encoding(): # https://stackoverflow.com/a/40346898
    reload(sys)
    sys.setdefaultencoding('latin-1')


def main():
    home = os.path.dirname(os.path.abspath(__file__))
    os.chdir(home)

    config = ConfigParser.RawConfigParser()
    config.read('application.conf')
    data_dir = config.get('application', 'data_dir')
    boxes = json.loads(config.get('application', 'boxes_json'))

    logging.config.fileConfig('logging.conf')

    setup_encoding()

    for box in boxes:
        host = box['host']
        login = box['login']
        password = box['password']

        try:
            logging.info("Processing %s", host)
            connection = routeros_api.RouterOsApiPool(host, username = login, password = password)
            api = connection.get_api()
            resource = api.get_resource('/ip/arp')
            entries = resource.get() # List of {u'complete': u'true', u'published': u'false', u'dynamic': u'true', u'invalid': u'false', u'mac-address': u'00:12:34:56:78:9A', u'disabled': u'false', u'address': u'10.9.8.7', u'interface': u'v1234', u'DHCP': u'false', u'id': u'*BDF'}
            data = set([(entry['mac-address'], entry['interface']) for entry in entries if 'mac-address' in entry])
            file_name = datetime.now().strftime('%Y%m%d%H%M%S') + '-' + host + '.gz'
            file_path = os.path.join(data_dir, file_name)
            with gzip.open(file_path, 'wb') as file:
                for obj in data:
                    file.write(' '.join(obj) + '\n')
            logging.info("%s done", host)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.error(exc_value)
            pass
        finally:
            connection.disconnect()


if __name__ == '__main__':
    main()
