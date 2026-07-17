import boto3, os
import numpy as np
import matplotlib.pyplot as plt
from braket.circuits import Circuit
from braket.devices import LocalSimulator
from src.classes import ExperimentMonitor, InfrastructureMonitor

sts = boto3.client(
    'sts',
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_KEY"),
    region_name=os.environ.get("AWS_DEFAULT_REGION"),
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

experiment_result = quantum_rng(n_bits=4, shots=10000)

experiment_monitor_class = ExperimentMonitor(results=experiment_result)
experiment_monitor_class.monitor_local(sts, quantum_rng)
experiment_monitor_class.monitor_cloud(sts, quantum_rng)

infrastructure_monitor_class = InfrastructureMonitor(
    region_name = os.environ.get("AWS_DEFAULT_REGION"),
    access_key = os.environ.get("AWS_ACCESS_KEY"),
    secret_key=os.environ.get("AWS_SECRET_KEY"),
)
