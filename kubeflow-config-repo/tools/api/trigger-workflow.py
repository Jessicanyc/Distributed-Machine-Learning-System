from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/trigger-workflow', methods=['POST'])
def trigger_workflow():
    environment = request.json['environment']  # 'dev' or 'prod'
    action = request.json['action']  # 'deploy', 'retrain', etc.

    url = "https://api.github.com/repos/<username>/<repository>/dispatches"
    payload = {
        "event_type": "deploy-event",
        "client_payload": {
            "environment": environment,
            "action": action
        }
    }
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {github_token}"
    }

    response = requests.post(url, json=payload, headers=headers)
    return {"status": "Workflow triggered!", "response": response.status_code}

if __name__ == '__main__':
    app.run(debug=True, port=5000)
