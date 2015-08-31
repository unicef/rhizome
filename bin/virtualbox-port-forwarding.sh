#!/bin/bash

DOCKER_MACHINE_NAME=dev
EXPOSED_PORTS=(5432 8000)

for i in ${EXPOSED_PORTS[@]}; do
    PORT_NAME="tcp-port-${i}"
    VBoxManage controlvm $DOCKER_MACHINE_NAME natpf1 delete $PORT_NAME
    VBoxManage controlvm $DOCKER_MACHINE_NAME natpf1 "$PORT_NAME,tcp,127.0.0.1,${i},,${i}"
done

exit 0