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
    unable_to_login_out = config.get('application', 'unable_to_login_out')

    logging.config.fileConfig('logging.conf')

    boxes = []
    with open(boxes_csv, 'rb') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for r in reader:
            boxes.append({fieldnames[i]: r[fieldnames[i]] for i in range(len(fieldnames))})
    logging.info('%d box(es) will be checked', len(boxes))

    WRITE_BUFFER_SIZE = 0
    with open(success_out, 'wb', WRITE_BUFFER_SIZE) as success_out_f, open(unable_to_login_out, 'wb', WRITE_BUFFER_SIZE) as unable_to_login_out_f:
        success_out_writer = csv.writer(success_out_f)
        unable_to_login_out_writer = csv.writer(unable_to_login_out_f)

        processed = 0
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
                        success_out_writer.writerow((host, u, p, identity))
                        logging.info("Success")
                        api.close()
                        break
                    except:
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        logging.error(exc_value)
                        if (str(exc_value) != "cannot log in"):
                            break
                else:
                    continue
                break
            else:
                unable_to_login_out_writer.writerow([host])
            logging.info('%s done', host)
            processed += 1
            if (processed % 50 == 0):
                logging.info('%d boxes processed', processed)
        logging.info('Total %d boxes processed', processed)



if __name__ == '__main__':
    main()
