#!/bin/bash

# Script to validate Kubernetes cluster managed by Kops

echo "Validating cluster configuration and node status..."
kops validate cluster --state ${KOPS_STATE_STORE}

if [ $? -eq 0 ]; then
    echo "Cluster validation successful."
else
    echo "Cluster validation failed."
    exit 1
fi
