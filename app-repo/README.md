Application Code Repositories

application that interacts with or is part of the ML system, maintain a separate repository. This includes services for model serving, front-end applications, and any backend services required for managing the ML lifecycle.

This repository adopt containerization for each component and include Kubernetes deployment manifests or Helm charts within the respective repositories. Implement CI/CD pipelines to automate the build, test, and deployment processes, utilizing Argo CD for continuous delivery to Kubernetes