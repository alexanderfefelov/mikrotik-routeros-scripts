#!/usr/bin/env python

from datetime import datetime
from librouteros import connect # https://github.com/luqasz/librouteros
import ConfigParser
import csv
import json
import logging
import logging.config
import os
import os.path
import sys

def main():
    home = os.path.dirname(os.path.abspath(__file__))
    os.chdir(home)

    config = ConfigParser.RawConfigParser()
    config.read('application.conf')
    timeout = float(config.get('application', 'timeout'))
    additional_usernames = filter(None, config.get('application', 'additional_usernames').split(','))
    additional_passwords = config.get('application', 'additional_passwords').split(',')
    boxes_csv = config.get('application', 'boxes_csv')
    success_out = config.get('application', 'success_out')

    logging.config.fileConfig('logging.conf')

    boxes = []
    with open(boxes_csv, 'rb') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for r in reader:
            boxes.append({fieldnames[i]: r[fieldnames[i]] for i in range(len(fieldnames))})
    logging.info('%d box(es) will be checked', len(boxes))

    success = []
    unable_to_login = []
    error = []

    for box in boxes:
        host = box['host']
        username = box['username']
        password = box['password']

        usernames = [username] + additional_usernames
        passwords = [password] + additional_passwords

        logging.info('Processing %s', host)
        for u in usernames:
            for p in passwords:
                try:
                    api = connect(host = host, username = u, password = p, timeout = timeout)
                    identity = api(cmd = '/system/identity/print')[0]['name']
                    success.append((host, u, p, identity))
                    api.close()
                    break
                except:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    logging.error(exc_value)
                    if (str(exc_value) != "cannot log in"):
                        error.append((host, str(exc_value)))
                        break
            else:
                continue
            break
        else:
            unable_to_login.append(host)
        logging.info('%s done', host)

    with open(success_out, 'wb') as f:
        writer = csv.writer(f)
        for r in success:
            writer.writerow(r)


    print(success)

if __name__ == '__main__':
    main()
