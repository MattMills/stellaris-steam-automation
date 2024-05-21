import os
import json
import time
import sys
import subprocess


steam_dir_path = '/zpool0/share/stellaris_backups_steam/'
steam_app_id = '281990'
steam_sub_ids = ['281992', '281993', '281994']

discovered_manifests = {}
if not os.path.isfile('discovered_manifests.json'):
    print('ERROR: Missing discovered_manifests.json')
    exit()

if os.getenv('STEAMCTL_USER', None) == None:
    print('ERROR: Missing STEAMCTL_USER env variable')
    exit()

if os.getenv('STEAMCTL_PASSWORD', None) == None:
    print('ERROR: Missing STEAMCTL_PASSWORD env variable')
    exit()

with open('discovered_manifests.json') as fh:
    discovered_manifests = json.load(fh)

#Download files from a manifest to a directory called 'temp':
for depot_id in steam_sub_ids:
    known_manifests = []

    historical_manifests = {}
    if not os.path.isfile('steamdb_manifests_%s.json' % (depot_id,)):
        print('ERROR: Missing steamDB historical data')
        exit()

    with open('steamdb_manifests_%s.json' % (depot_id,)) as fh:
        historical_manifests = json.load(fh)

    for manifest in historical_manifests:   
        parsed_manifest_id = manifest['ManifestID'].split('\\n')
        if parsed_manifest_id[0] not in known_manifests:
            known_manifests.append(parsed_manifest_id[0])

    for manifest_id in discovered_manifests[depot_id].keys():
        if manifest_id not in known_manifests:
            known_manifests.append(manifest_id)

    for manifest_id in known_manifests:
        output_dir = '%sby_manifest/%s/%s' % (steam_dir_path, depot_id, manifest_id)
        if os.path.isfile('%s/.complete_flag' % (output_dir, )):
            continue

        os.makedirs(output_dir, exist_ok=True)

        ret = subprocess.call("/usr/local/bin/steamctl depot download --app %s --depot %s --manifest %s -o %s" % (steam_app_id, depot_id, manifest_id, output_dir), shell=True) 
        if ret != 0:
            print('FATAL: SteamCTL non zero return code...')
            exit()

        with open('%s/.complete_flag' % (output_dir, ), 'w') as fh:
            fh.write('yup')

