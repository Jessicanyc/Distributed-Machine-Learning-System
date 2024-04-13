#!/bin/bash

# Script to update Kubernetes cluster managed by Kops

echo "Fetching the latest cluster state from S3..."
kops get cluster --state ${KOPS_STATE_STORE}

echo "Applying changes to the cluster..."
kops update cluster --name mycluster.example.com --yes --state ${KOPS_STATE_STORE}

echo "Waiting for the cluster update to complete..."
kops rolling-update cluster --name mycluster.example.com --yes --state ${KOPS_STATE_STORE}

echo "Cluster update completed."
