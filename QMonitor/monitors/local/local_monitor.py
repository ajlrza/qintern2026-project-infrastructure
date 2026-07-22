import threading
import psutil
import time
from typing import Callable, Any, Dict
from datetime import datetime, timezone

def local_user_monitor(experiment_function: Callable, params: Dict[str, Any]):
    # Initialize arrays to store metrics over time
    monitor_results = {
        "Local CPU Usage": [],
        "Local RAM Usage": [],
        "Local I/O Disk Latency": []
    }
    time.sleep(1)

    thread = threading.Thread(target=experiment_function, kwargs=params)
    thread.start()

    while thread.is_alive():
        print("Experiment function is currently running...")
        time.sleep(0.5)

        if psutil.virtual_memory().percent >= 98.00:
            print("Out Of Memory Risk...")
            print("Sleeping for 10 seconds..")
            time.sleep(10)

        # Append metrics to the arrays instead of creating new keys
        monitor_results["Local CPU Usage"].append(psutil.cpu_percent(interval=0.1))
        monitor_results["Local RAM Usage"].append(psutil.virtual_memory().percent)
        monitor_results["Local I/O Disk Latency"].append(psutil.disk_io_counters()._asdict())

    thread.join(timeout=1)
    monitor_results["Datetime"] = str(datetime.now(timezone.utc))

    print(monitor_results)
    return monitor_results