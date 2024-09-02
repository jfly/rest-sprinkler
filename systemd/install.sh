#!/usr/bin/env bash

set -euo pipefail

if [ $# -ne 1 ]; then
	echo "Usage: $0 [HA_API_TOKEN]" >/dev/stderr
	echo "" >/dev/stderr
	echo 'Where [HA_API_TOKEN] is a "Long-lived access token" created in your Home Assistant profile.' >/dev/stderr
	exit 1
fi

ha_api_token=$1

cd "$(dirname "$0")"

project_root=$(realpath ../)

sed \
	-e "s,__WORKING_DIRECTORY__,$project_root,g" \
	-e "s,__HA_API_TOKEN__,$ha_api_token,g" \
	rest-sprinkler.service | sudo tee /etc/systemd/system/rest-sprinkler.service

systemctl daemon-reload
systemctl enable --now rest-sprinkler
