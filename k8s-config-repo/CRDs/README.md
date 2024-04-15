## CRD

CRDs Define Structure: outline what configurations are possible and how they should be structured but do not include operational settings.

## CR

CRs Set Operational Values: provide specific values for the configurations defined in the CRD, tailoring the behavior of Kubernetes resources like pods or services to meet specific needs

### create cr 

```
kubectl create -f inference-service.yaml
```
- after run this command KServe automatically handles the deployment of the underlying resources, including pods, without requiring you to manually define separate Pod YAML files
- 
### Resource Creation by KServe: 

Once the KServe controller detects a new or updated InferenceService, it automatically orchestrates the creation of the necessary Kubernetes resources to serve the model. This includes:

- Pods: Containers configured to run the model serving software (like TensorFlow Serving, PyTorch Serve, etc.) as specified in the InferenceService definition.
- Deployments: KServe usually creates a Kubernetes Deployment to manage the lifecycle of the pods, including scaling up and down as necessary based on the autoscaling configuration.
- Services: To expose the pods, KServe creates a Kubernetes Service, which provides a stable endpoint for accessing the model servers inside the pods.
- Autoscaling: If autoscaling parameters are defined, KServe configures this through Kubernetes Horizontal Pod Autoscaler (HPA) or Knative Serving mechanisms, depending on the setup.