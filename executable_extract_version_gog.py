import json
import os
import time
import subprocess

processing_dir = '/zpool0/share/stellaris_backups_gog/'
existing_data = 'existing_executables.json'

target_by_os_type = {
                        'windows': 'depots/stellaris.exe', #windows
                        'osx': 'depots/stellaris.app/Contents/MacOS/stellaris', #MacOS
}

grep_command = "grep -baPo '\\x00[^\\x00]*v[0-9]+\\.[0-9]+\\.[0-9]+[^\\x00]*\\x00' " #version strings

ed = {}
if(os.path.isfile(existing_data)):
    with open(existing_data) as fh:
        ed = json.load(fh)

dir_list = os.listdir(processing_dir)

for version_id in dir_list:
    os_list = os.listdir('%s/%s' % (processing_dir, version_id))
    for os_type in os_list:
        data = {}
        target_name = '%s/%s/%s/%s' % (processing_dir, version_id, os_type, target_by_os_type[os_type])
        if not os.path.isfile(target_name):
            print('WARNING: Couldnt find target file %s' % (target_name, ))
            continue
        if os.path.isfile('%s/%s/%s/metadata.json' % (processing_dir, version_id, os_type)):
            print("SKIP %s" % target_name)
            continue
        print("Processing %s" % target_name)

        data['target_file'] = target_name

        
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
            data['string_value'] = 'Unknown version - src version/os %s / %s' % (version_id, os_type)
            data['string_offset'] = 0
        else:
            data['string_value'] = best_value
        with open('%s/%s/%s/metadata.json' % (processing_dir, version_id, os_type), 'w') as fh:
            json.dump(data, fh)


