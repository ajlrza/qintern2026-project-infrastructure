# QMonitor Documentation

The following are the available modules from the QMonitor Package

* monitors
* loggers
* config

# Monitors

### `ec2_instance_monitorr()` **QMonitor.src.monitors.cloud.ec2.ec2_monitor.py**
> Extracts local machine hardware metrics through ```psutil``` and ```threading``` libraries.

#### Function Parameters

| Parameter | Type  | Required | Description |
| :--- | :--- | :--- | :--- |
| `experiment_function` | `Callable` | Yes | Callable and uninstantiated experiment function. |
| `params` | `Dict[str, Any]` | Yes | Experiment function parameters passed from helper function. |

#### Return Value

| Type | Description |
| :--- | :--- |
| `Dict` | Local machine metrics including: CPU usage, RAM usage, I/O disk latency |

Example Output
```json
{
  "Local CPU Usage: Thread 1": 14.5,
  "Local RAM Usage: Thread 1": 62.3,
  "Local I/O Disk Latency: Thread 1": "sdiskio(read_count=874312, write_count=349811, read_bytes=4294967296, write_bytes=1073741824, read_time=14502, write_time=3910, read_merged_count=12, write_merged_count=84, busy_time=18491)",
  "Local CPU Usage: Thread 2": 22.1,
  "Local RAM Usage: Thread 2": 63.8,
  "Local I/O Disk Latency: Thread 2": "sdiskio(read_count=874350, write_count=349900, read_bytes=4295967296, write_bytes=1074741824, read_time=14510, write_time=3915, read_merged_count=12, write_merged_count=84, busy_time=18500)",
  "Local CPU Usage: Thread 3": 18.3,
  "Local RAM Usage: Thread 3": 64.1,
  "Local I/O Disk Latency: Thread 3": "sdiskio(read_count=874400, write_count=350100, read_bytes=4296967296, write_bytes=1075741824, read_time=14520, write_time=3925, read_merged_count=12, write_merged_count=84, busy_time=18520)",
  "Datetime": "2026-07-21 12:11:44.123456+00:00"
}
```

### `ec2_instance_monitor()` **QMonitor.src.monitors.cloud.ec2.ec2_monitor.py**
> Extracts EC2 instance basic metrics through ```AWS Boto3``` EC2 client.

#### Function Parameters

| Parameter | Type  | Required | Description |
| :--- | :--- | :--- | :--- |
| `config` | `Object` | Yes | Initiated config dataclass for centralized credential management. |
| `experiment_function` | `Callable` | Yes | Callable and uninstantiated experiment function. |
| `params` | `Dict[str, Any]` | Yes | Experiment function parameters passed from helper function. |


a_metrics = [
        "CPUUtilization",
        "mem_used_percent",
        "NetworkIn",
        "NetworkOut",
        "DiskReadOps",
        "DiskWriteOps"
#### Return Value

| Type | Description |
| :--- | :--- |
| `Dict` | EC2 instance infrastructure and usage metrics including: CPU Utilization, Memory Used Percentage, Network I/O, Disk I/O |

Example Output
```json
{
  "usage_metrics": {
    "EC2_usage": {
      "instance_id": "i-0123456789abcdef0",
      "instance_type": "t3.xlarge",
      "time_used": "3 days, 14:22:05.819201"
    }
  },
  "infrastructure_metrics": [
    {
      "Label": "mem_used_percent",
      "Datapoints": [
        {
          "Timestamp": "2026-07-21T12:13:00Z",
          "Average": 48.35,
          "Unit": "Percent"
        }
      ],
      "ResponseMetadata": {
        "HTTPStatusCode": 200,
        "HTTPHeaders": { ... }
      },
      "RAM Summed Average": 48.35
    },
    {
      "Label": "CPUUtilization",
      "Datapoints": [
        {
          "Timestamp": "2026-07-21T12:13:00Z",
          "Average": 12.4,
          "Unit": "Percent"
        }
      ],
      "ResponseMetadata": { ... },
      "CPUUtilization Summed Average": 12.4
    },
    {
      "Label": "NetworkIn",
      "Datapoints": [
        {
          "Timestamp": "2026-07-21T12:13:00Z",
          "Average": 1048576.0,
          "Unit": "Bytes"
        }
      ],
      "ResponseMetadata": { ... },
      "NetworkIn Summed Average": 1048576.0
    },
    {
      "Label": "NetworkOut",
      "Datapoints": [
        {
          "Timestamp": "2026-07-21T12:13:00Z",
          "Average": 524288.0,
          "Unit": "Bytes"
        }
      ],
      "ResponseMetadata": { ... },
      "NetworkOut Summed Average": 524288.0
    },
    {
      "Label": "DiskReadOps",
      "Datapoints": [
        {
          "Timestamp": "2026-07-21T12:13:00Z",
          "Average": 150.0,
          "Unit": "Count"
        }
      ],
      "ResponseMetadata": { ... },
      "DiskReadOps Summed Average": 150.0
    },
    {
      "Label": "DiskWriteOps",
      "Datapoints": [
        {
          "Timestamp": "2026-07-21T12:13:00Z",
          "Average": 42.0,
          "Unit": "Count"
        }
      ],
      "ResponseMetadata": { ... },
      "DiskWriteOps Summed Average": 42.0
    }
  ]
}
```
### `local_user_monitor()` **QMonitor.src.monitors.local.local_monitor.py**
> Extracts local machine hardware metrics through ```psutil``` and ```threading``` libraries.

#### Function Parameters

| Parameter | Type  | Required | Description |
| :--- | :--- | :--- | :--- |
| `experiment_function` | `Callable` | Yes | Callable and uninstantiated experiment function. |
| `params` | `Dict[str, Any]` | Yes | Experiment function parameters passed from helper function. |

#### Return Value

| Type | Description |
| :--- | :--- |
| `Dict` | Local machine metrics including: CPU usage, RAM usage, I/O disk latency |

Example Output
```json
{
  "Local CPU Usage: Thread 1": 14.5,
  "Local RAM Usage: Thread 1": 62.3,
  "Local I/O Disk Latency: Thread 1": "sdiskio(read_count=874312, write_count=349811, read_bytes=4294967296, write_bytes=1073741824, read_time=14502, write_time=3910, read_merged_count=12, write_merged_count=84, busy_time=18491)",
  "Local CPU Usage: Thread 2": 22.1,
  "Local RAM Usage: Thread 2": 63.8,
  "Local I/O Disk Latency: Thread 2": "sdiskio(read_count=874350, write_count=349900, read_bytes=4295967296, write_bytes=1074741824, read_time=14510, write_time=3915, read_merged_count=12, write_merged_count=84, busy_time=18500)",
  "Local CPU Usage: Thread 3": 18.3,
  "Local RAM Usage: Thread 3": 64.1,
  "Local I/O Disk Latency: Thread 3": "sdiskio(read_count=874400, write_count=350100, read_bytes=4296967296, write_bytes=1075741824, read_time=14520, write_time=3925, read_merged_count=12, write_merged_count=84, busy_time=18520)",
  "Datetime": "2026-07-21 12:11:44.123456+00:00"
}
```



