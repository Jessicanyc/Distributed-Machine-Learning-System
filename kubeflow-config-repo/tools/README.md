
# tools/api

## API for Triggering GitHub Actions Workflows

### Overview
This API is designed to trigger GitHub Actions workflows programmatically via a RESTful interface. It is used for integrating external systems that need to interact with the CI/CD processes, such as triggering deployments or workflow runs based on certain conditions or external events.

### Purpose
The primary purpose of this API is to provide a flexible, programmable way to initiate GitHub Actions workflows from external systems, applications, or even manually, without needing to interact directly with GitHub's UI. This enables automation and integration of your CI/CD pipeline with other parts of your software ecosystem.

### Requirements
To run this API, you will need Python and several dependencies listed in the `requirements.txt` file.

### Dependencies
- Flask
- Requests

Install the necessary Python packages by running:
```bash
pip install -r requirements.txt
```

## Setup Instructions
1. **Clone the Repository:**
   Ensure that you have a local copy of the repository.
   ```bash
   git clone <repository-url>
   cd kubeflow-config-repo/tools/api
   ```

2. **Install Dependencies:**
   Install the required Python libraries using:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration:**
   Set up the necessary environment variables. For security reasons, do not hardcode sensitive information like your GitHub token in the script.
   - `GITHUB_TOKEN`: Your GitHub Personal Access Token with the appropriate permissions.
   - `REPO_NAME`: The name of the repository where the workflows will be triggered.
   - `REPO_OWNER`: The owner of the repository.

   These can be set in your environment or directly in a secure configuration file.

## Usage
To run the API server, execute:
```bash
python trigger_workflow.py
```

### Calling the API
The API can be accessed via HTTP POST requests. Below is an example of how to trigger the workflow using `curl`:

```bash
curl -X POST http://localhost:5000/trigger-workflow \
     -H 'Content-Type: application/json' \
     -d '{"environment": "dev", "action": "deploy"}'
```

This request would trigger the GitHub Actions workflow configured for development environment deployments.

## Deployment
For production deployment, consider using a WSGI server like Gunicorn and a cloud provider like AWS, Google Cloud, or Azure to host the API.

### Example Gunicorn Command:
```bash
gunicorn -w 4 -b 0.0.0.0:8000 trigger_workflow.py:app
```
- `w 4`: This specifies the number of worker processes for handling requests. More workers allow the application to serve more requests at the same time.
- `b 0.0.0.0:8000`: This binds the server to all IP addresses of the host at port 8000, making the server accessible on all network interfaces.
- `trigger_workflow.py:app`: This points to the WSGI application callable that Gunicorn will serve. Here, trigger_workflow.py is the file, and app is the Flask application instance.
Deploying to a cloud provider often involves additional configurations for security, logging, and monitoring, so refer to your provider's best practices for Python applications.

## Monitoring and Logging
Set up monitoring and logging to track API usage and capture errors or unusual activity. Tools like Prometheus for monitoring and ELK Stack or Google Stackdriver for logging can be configured depending on your deployment environment.
