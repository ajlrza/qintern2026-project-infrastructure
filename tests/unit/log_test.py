import boto3, os
import numpy as np
import matplotlib.pyplot as plt
from braket.circuits import Circuit
from braket.devices import LocalSimulator
from src.logger.logger import log_to_repo
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

# Test
experiment_params = {"n_bits": 4, "shots":10000}

experiment_monitor_class = ExperimentMonitor()
experiment_result = experiment_monitor_class.monitor_local(quantum_rng, experiment_params)

log = log_to_repo(
    sts_client=sts,
    experiment_function=quantum_rng, 
    monitored_results=experiment_result, 
    notes="Test", 
    benchmark_type="RNG"
)