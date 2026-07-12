import os
from dataclasses import dataclass

@dataclass
class Gates:
    H: int
    CNOT: int
    Others: int

@dataclass
class CircParams:
    qubits: int
    depth: int
    shots: int
    gates: Gates

@dataclass
class Metrics:
    circuit_fidelity_dR2: float
    shot_noise_converged_at: int
    cv_value: float
    local_vs_sv1_ks_pvalue: float
    gate_error_rate_tested: float
    fidelity_under_noise: float
    measurement_bias_pvalue: float
    runtime_seconds: float
    cloud_overhead_seconds: float

@dataclass
class Environ:
    braket_sdk_version: str
    python_version: str
    instance_type: str

@dataclass
class ExpConfig:
    experiment_id: str
    benchmark_type: str
    timestamp: str
    simulator: str
    circuit_params: CircParams
    metrics: Metrics
    environment: dict
    notes: str