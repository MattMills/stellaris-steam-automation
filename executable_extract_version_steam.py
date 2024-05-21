import json
import os
import time
import subprocess

processing_dir = '/zpool0/share/stellaris_backups_steam/by_manifest/'
processing_dir = '/zpool0/share/stellaris_backups_gog/'
existing_data = 'existing_executables.json'

target_by_depot_id = {
                        '281992': 'stellaris.exe', #windows
                        '281993': 'stellaris.app/Contents/MacOS/stellaris', #MacOS
                        '281994': 'stellaris',  #linux
}

grep_command = "grep -baPo '\\x00[^\\x00]*v[0-9]+\\.[0-9]+\\.[0-9]+[^\\x00]*\\x00' " #version strings

ed = {}
if(os.path.isfile(existing_data)):
    with open(existing_data) as fh:
        ed = json.load(fh)

dir_list = os.listdir(processing_dir)

for depot_id in dir_list:
    manifest_list = os.listdir('%s/%s' % (processing_dir, depot_id))
    for manifest_id in manifest_list:
        data = {}
        target_name = '%s/%s/%s/%s' % (processing_dir, depot_id, manifest_id, target_by_depot_id[depot_id])
        if not os.path.isfile(target_name):
            print('WARNING: Couldnt find target file %s' % (target_name, ))
            continue
        if os.path.isfile('%s/%s/%s/metadata.json' % (processing_dir, depot_id, manifest_id)):
            print("SKIP %s" % target_name)
            continue
        print("Processing %s" % target_name)

        data['target_file'] = target_name
        data['depot_id'] = depot_id
        data['manifest_id'] = manifest_id

        
        result = subprocess.run("%s%s" % (grep_command, target_name), capture_output=True, shell=True)

        grep_result = result.stdout.split(b'\n')

        best_value = None
        for res in grep_result:
            if len(res) <= 1:
                continue
            res2 = res.split(b':', 1)
            string_offset = res2[0].decode('UTF-8')
            string_value = res2[1][1:-1].decode('UTF-8')

            if string_value.find('WebM Project') == -1 and string_value.find('Stellaris') == -1 and string_value.find(' ') != -1:
                if best_value == None or len(best_value) < len(string_value):
                    best_value = string_value
                    data['string_offset'] = string_offset

        if best_value == None:
            data['string_value'] = 'Unknown version manifest %s' % manifest_id
            data['string_offset'] = 0
        else:
            data['string_value'] = best_value
        print(data)    
        #with open('%s/%s/%s/metadata.json' % (processing_dir, depot_id, manifest_id), 'w') as fh:
        #    json.dump(data, fh)


