from dataclasses import dataclass, field

@dataclass
class Gates:
    H: int = 0
    CNOT: int = 0
    Others: int = 0

@dataclass
class CircParams:
    qubits: int = 0
    depth: int = 0
    shots: int = 0
    gates: Gates = field(default_factory=Gates)  # Properly nested

@dataclass
class Metrics:
    circuit_fidelity_dR2: float = 0.0
    shot_noise_converged_at: int = 0
    cv_value: float = 0.0
    local_vs_sv1_ks_pvalue: float = 0.0
    gate_error_rate_tested: float = 0.0
    fidelity_under_noise: float = 0.0
    measurement_bias_pvalue: float = 0.0
    runtime_seconds: float = 0.0
    cloud_overhead_seconds: float = 0.0

@dataclass
class Environ:
    braket_sdk_version: str = ""
    python_version: str = ""
    instance_type: str = ""

@dataclass
class ExpConfig:
    experiment_id: str = ""
    benchmark_type: str = ""
    timestamp: str = ""
    simulator: str = ""
    notes: str = ""

@dataclass
class CredsConfig:
    sts_client: object = None