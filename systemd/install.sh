#!/usr/bin/env bash

set -euo pipefail

if [ $# -ne 2 ]; then
	(
		echo "Usage: $0 [HA_URL] [HA_API_TOKEN]"
		echo ""
		echo "[HA_URL] is the url of your Home Assistant server, such as: 'https://home-assistant.example.com'."
		echo '[HA_API_TOKEN] is a "Long-lived access token" created in your Home Assistant profile.'
	) >/dev/stderr

	exit 1
fi

ha_url=$1
ha_api_token=$2

cd "$(dirname "$0")"

project_root=$(realpath ../)

sed \
	-e "s,__WORKING_DIRECTORY__,$project_root,g" \
	-e "s,__HA_URL__,$ha_url,g" \
	-e "s,__HA_API_TOKEN__,$ha_api_token,g" \
	rest-sprinkler.service | sudo tee /etc/systemd/system/rest-sprinkler.service

systemctl daemon-reload
systemctl enable --now rest-sprinkler
