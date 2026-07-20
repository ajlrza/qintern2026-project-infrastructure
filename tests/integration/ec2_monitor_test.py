import boto3
import os
import requests
import json
import base64
from datetime import datetime
from braket.circuits import Circuit
from braket.devices import LocalSimulator
from src.classes import Monitor

ec2_client = boto3.client(
    "ec2",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test",
)

sts = boto3.client(
    "sts",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1",
)

test_instance = ec2_client.run_instances(
    ImageId="ami-0123456789abcdef0",
    MinCount=1,
    MaxCount=1,
    InstanceType="t3.micro",
    MetadataOptions={
        "HttpTokens": "required",
        "HttpEndpoint": "enabled",
        "HttpPutResponseHopLimit": 2,
    },
)


def quantum_rng(n_bits, shots=10000):
    """
    Generate quantum random bits using Hadamard gates.
    n_bits: number of qubits (= number of random bits per shot)
    shots: number of measurements
    """
    circuit = Circuit()
    for i in range(n_bits):
        circuit.h(i)

    device = LocalSimulator()
    result = device.run(circuit, shots=shots).result()

    return result.measurement_counts


def automated_test(experiment_function, experiment_params=None, tests=0):
    test_results = []
    experiment_monitor_result = None

    token = os.environ.get("PAT_TOKEN")
    owner = os.environ.get("GITHUB_USERNAME")
    repo = os.environ.get("REPOSITORY_NAME")

    datetime.now()
    path = f"test_logs/ec2_monitor_test_{datetime.now()}"
    branch = "main"

    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}.md"

    file_content = None

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    if tests > 0:
        test_iteration = 0
        while test_iteration != tests:
            test_iteration += 1

            experiment_monitor = Monitor()

            experiment_monitor_result = experiment_monitor.monitor_cloud(
                experiment_monitor.config, quantum_rng
            )

            test_results.append(experiment_monitor_result)

        file_content = json.dumps(test_results, indent=2)
        encoded_content = base64.b64encode(file_content.encode("utf-8")).decode("utf-8")

        payload = {
            "message": f"{test_iteration} EC2 Monitor Test/s",
            "content": encoded_content,
            "branch": branch,
        }
        response = requests.put(url, json=payload, headers=headers, timeout=5)
        print(response)

    elif tests == 0:
        experiment_monitor = Monitor()

        experiment_monitor_result = experiment_monitor.monitor_cloud(
            experiment_monitor.config, quantum_rng
        )

        file_content = json.dumps(experiment_monitor_result, indent=2)
        encoded_content = base64.b64encode(file_content.encode("utf-8")).decode("utf-8")

        payload = {
            "message": "EC2 Monitor Test 1",
            "content": encoded_content,
            "branch": branch,
        }
        response = requests.put(url, json=payload, headers=headers, timeout=5)
        print(response)


# Test
test = automated_test(quantum_rng, experiment_params=None)
