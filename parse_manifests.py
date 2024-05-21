import json
import os
import sys
import time
from datetime import datetime



process_dir = 'steam_manifests/'
complete_dir = 'completed_steam_manifests/'
fail_dir = 'failed_steam_manifests/'

app_ids = ['281992', '281993', '281994']


if not os.path.isdir(process_dir) or not os.path.isdir(complete_dir):
    print('FATAL: process dir or complete dir does not exist')
    exit()



discovered_manifests = {}

if os.path.isfile('discovered_manifests.json'):
    with open('discovered_manifests.json') as fh:
        discovered_manifests = json.load(fh)
else:
    for app_id in app_ids:
        discovered_manifests[app_id] = {}


for filename in os.listdir(process_dir):
    #281990.product_info.2023-08-08T09:18:01-06:00.json
    if not os.path.isfile('%s/%s' % (process_dir, filename)) or filename[-4:] != 'json':
        continue

    parts = filename.split('.')
    timestamp = datetime.strptime(parts[2], '%Y-%m-%dT%H:%M:%S%z')
    unix_timestamp = timestamp.timestamp()

    try:
        with open('%s/%s' % (process_dir, filename)) as fh:
            manifest = json.load(fh)

            for app_id in app_ids:
                manifest_id = manifest['depots'][app_id]['manifests']['public']

                if 'gid' in manifest_id:
                    manifest_id = manifest_id['gid']
                
                if manifest_id not in discovered_manifests[app_id].keys():
                    discovered_manifests[app_id][manifest_id] = {'first': unix_timestamp, 'last': unix_timestamp}
                else:
                    if unix_timestamp < discovered_manifests[app_id][manifest_id]['first']:
                        discovered_manifests[app_id][manifest_id]['first'] = unix_timestamp
                    if unix_timestamp > discovered_manifests[app_id][manifest_id]['last']:
                        discovered_manifests[app_id][manifest_id]['last'] = unix_timestamp

        os.rename('%s/%s' % (process_dir, filename), '%s/%s' % (complete_dir, filename))

    except json.decoder.JSONDecodeError:
        print('PARSE FAIL: %s' % (filename,))
        os.rename('%s/%s' % (process_dir, filename), '%s/%s' % (fail_dir, filename))

 
with open('discovered_manifests.json', 'w') as fh:
    json.dump(discovered_manifests, fh)  
