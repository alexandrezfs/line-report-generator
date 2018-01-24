#!/usr/bin/env bash

CONFIG_DIR=/opt/line/config

set -o allexport
source ${CONFIG_DIR}/config
set +o allexport

ansible-playbook /opt/line/line_report_generator/build_scripts/ansible/firstboot/firstboot.yml -e config_dir=${CONFIG_DIR}
