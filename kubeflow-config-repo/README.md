## Kubeflow Configuration Repository (kubeflow-config-repo)

Dedicated to Kubeflow-specific configurations and pipelines, this repository hosts the definitions of ML workflows, custom resource definitions (CRDs) for Kubeflow operators, and other customization for Kubeflow components to fit the needs of the distributed ML system.

this repository is used to version-control the ML pipelines and related configurations, enabling reproducible ML workflows. the pipeline definitions and component specifications also included here

leverage github action to setup CICD pipeline to manage the A/B testing of model serving

the kubeflow system also provice manually trigger the workflow by running
```
curl -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token GITHUB_TOKEN" \
  https://api.github.com/repos/OWNER/REPO/dispatches \
  -d '{"event_type": "custom-event", "client_payload": {"action": "trigger-workflow"}}'
```