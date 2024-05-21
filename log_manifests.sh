#!/bin/bash
cd /zpool0/share/stellaris_backups_steam/automation
. steam_creds.sh
/usr/local/bin/steamctl apps product_info 281990 > steam_manifests/281990.product_info.$(date --iso-8601=seconds).json
