import json
import os
import time
import subprocess

processing_dir = '/zpool0/share/stellaris_backups_steam/'
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

dir_list = os.listdir('%s/by_manifest' % (processing_dir,))

for depot_id in dir_list:
    manifest_list = os.listdir('%s/by_manifest/%s' % (processing_dir, depot_id))
    for manifest_id in manifest_list:
        data = {}
        target_name = '%s/by_manifest/%s/%s/%s' % (processing_dir, depot_id, manifest_id, target_by_depot_id[depot_id])
        metadata_file = '%s/by_manifest/%s/%s/metadata.json' % (processing_dir, depot_id, manifest_id)
        if not os.path.isfile(target_name):
            print('WARNING: Couldnt find target file %s' % (target_name, ))
            continue
        if not os.path.isfile(metadata_file):
            print("WARNING: No metadata file %s" % metadata_file)
            continue

        print("Processing %s" % metadata_file)
    
        with open(metadata_file) as fh:
            data = json.load(fh)

        try:
            os.mkdir('%s/by_version/%s/' % (processing_dir, depot_id))
        except:
            pass
        
        
        if data['string_value'].find('  ') == -1:
            version_parts = data['string_value'].split(' ')
        else:
            split1 = data['string_value'].split('  ')
            version_parts = split1[0].split(' ')

        version = None

        for part in version_parts:
            if part[0:1] == 'v':
                version = part
                codename = data['string_value'][0:data['string_value'].find(version)]
                other_part = data['string_value'][data['string_value'].find(version)+len(version):]
                
        if version == None:
            filename = 'zzABNORMAL - %s' % data['string_value']
        else:
            filename = '%s %s %s' % (version, codename, other_part)


        filename = filename.replace(':', '-')
        src = '%s/by_manifest/%s/%s' % (processing_dir, depot_id, manifest_id)
        tgt = '%s/by_version/%s/%s' % (processing_dir, depot_id, filename)
        if(os.path.islink(tgt)):
            continue
        os.symlink(src, tgt, target_is_directory=True)


