import threading, time, os, boto3, psutil
from datetime import datetime, timezone, timedelta
from src.classes import Monitor
from botocore.exceptions import ClientError, NoCredentialsError, EndpointConnectionError


def ec2_instance_monitor(config, experiment_function, experiment_params):

    ec2_instance_description = None

    try:
        ec2_instance_description = config.creds["ec2_client"].describe_instances()

    except ClientError:
        print("Client error has occured, would you like to route to local monitor?")
        response = input("Enter Y/N")

        if (response == "Y"):
                
                local_monitor = Monitor()
                local_monitor_metrics = local_monitor.monitor_local(
                    experiment_function, experiment_params
                )

                return local_monitor_metrics
        
        elif (response == "N"):
                
                try:
                    
                    cw_new_client = boto3.client(
                        "cloudwatch",
                        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"),
                        aws_secret_access_key=os.environ.get("AWS_SECRET_KEY"),
                        region_name="us-east-1",
                    )

                except NoCredentialsError as E:
                    print(f"{E} has occured, defaulting to local monitor...")

                    local_monitor = Monitor()
                    local_monitor_metrics = local_monitor.monitor_local(
                        experiment_function, experiment_params
                    )

                    return local_monitor_metrics

    except NoCredentialsError:
        print("No credentials used, would you like to route to local monitor or redo?")
        response = input("Enter Y/N")

        if (response == "Y"):
                
                local_monitor = Monitor()
                local_monitor_metrics = local_monitor.monitor_local(
                    experiment_function, experiment_params
                )

                return local_monitor_metrics
        
        elif (response == "N"):
                
                print("Defaulting to local monitor..")

                try:

                    cw_new_client = boto3.client(
                        "cloudwatch",
                        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"),
                        aws_secret_access_key=os.environ.get("AWS_SECRET_KEY"),
                        region_name="us-east-1",
                    )

                except NoCredentialsError as E:
                    print(f"{E} has occured, defaulting to local monitor...")

                    local_monitor = Monitor()
                    local_monitor_metrics = local_monitor.monitor_local(
                        experiment_function, experiment_params
                    )

                    return local_monitor_metrics

    except EndpointConnectionError:
        print("Connection error, defaulting to local monitor..")

        local_monitor = Monitor()
        local_monitor_metrics = local_monitor.monitor_local(
            experiment_function, experiment_params
        )

        return local_monitor_metrics

    instance_types = config.creds["ec2_client"].describe_instance_types(
        InstanceTypes=["t3.micro", "m5.large"]
    )

    ec2_instance_attributes = {}

    for instance in instance_types["InstanceTypes"]:
        result = {
            "Instance": f"{instance['InstanceType']}",
            "vCPUs": f"{instance['VCpuInfo']['DefaultVCpus']}",
            "Memory": f"{instance['MemoryInfo']['SizeInMiB']} MiB",
            "Processor": f"{instance.get('ProcessorInfo', 'N/A')}",
            "GPU": f"{instance.get('GpuInfo', 'No GPU')}",
            "Hypervisor": f"{instance.get('Hypervisor', 'N/A')}",
        }

        ec2_instance_attributes[f"Instance {instance}"] = result

    ec2_logged_data = {
        "ec2_instance": ec2_instance_description,
        "ec2_instance_attributes": ec2_instance_attributes,
    }

    return ec2_logged_data


def ec2_machine_cloud_monitor(config, experiment_function, experiment_params):

    infra_metrics = [
        "CPUUtilization",
        "mem_used_percent",
        "NetworkIn",
        "NetworkOut",
        "DiskReadOps",
        "DiskWriteOps",
    ]
    infra_results = []

    usage_results = {}

    ram_response = None
    ram_average = 0

    cw_client_instance = config.creds["cw_client"]

    try:
        cw_client_instance.list_dashboards(PaginationConfig={"MaxItems": 1})

    except ClientError:
        print("Client error has occured, would you like to route to local monitor?")
        response = input("Enter Y/N")

        if (response == "Y"):
                
                local_monitor = Monitor()
                local_monitor_metrics = local_monitor.monitor_local(
                    experiment_function, experiment_params
                )

                return local_monitor_metrics
        
        elif (response == "N"):
                print("Defaulting to local monitor..")

                try:

                    cw_new_client = boto3.client(
                        "cloudwatch",
                        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"),
                        aws_secret_access_key=os.environ.get("AWS_SECRET_KEY"),
                        region_name="us-east-1",
                    )

                    cw_client_instance = cw_new_client

                except NoCredentialsError as E:
                    print(f"{E} has occured, defaulting to local monitor...")

                    local_monitor = Monitor()
                    local_monitor_metrics = local_monitor.monitor_local(
                        experiment_function, experiment_params
                    )

                    return local_monitor_metrics

    except NoCredentialsError:
        print("No credentials used, would you like to route to local monitor or redo?")
        response = input("Enter Y/N")

        if (response == "Y"):
                
                local_monitor = Monitor()
                local_monitor_metrics = local_monitor.monitor_local(
                    experiment_function, experiment_params
                )

                return local_monitor_metrics
        
        elif (response == "N"):
                
                print("Defaulting to local monitor..")

                try:

                    cw_new_client = boto3.client(
                        "cloudwatch",
                        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"),
                        aws_secret_access_key=os.environ.get("AWS_SECRET_KEY"),
                        region_name="us-east-1",
                    )

                    cw_client_instance = cw_new_client

                except NoCredentialsError as E:
                    print(f"{E} has occured, defaulting to local monitor...")

                    local_monitor = Monitor()
                    local_monitor_metrics = local_monitor.monitor_local(
                        experiment_function, experiment_params
                    )

                    return local_monitor_metrics

    except EndpointConnectionError:
        print("Connection error, defaulting to local monitor..")

        local_monitor = Monitor()
        local_monitor_metrics = local_monitor.monitor_local(
            experiment_function, experiment_params
        )

        return local_monitor_metrics

    for metric in infra_metrics:

        if metric == "mem_used_percent":
            ram_response = cw_client_instance.get_metric_statistics(
                Namespace="CWAgent",
                MetricName=metric,
                Dimensions=[{"Name": "InstanceId", "Value": "i-0123456789abcdef0"}],
                StartTime=str(datetime.now(timezone.utc) - timedelta(minutes=5)),
                EndTime=str(datetime.now(timezone.utc)),
                Period=300,
                Statistics=["Average"],
            )

            if not ram_response["Datapoints"]:
                ram_response["Average"] = 0.0
            else:
                datapoints_count = len(ram_response["Datapoints"])
                sum_datapoints = []
                for i in range(0, datapoints_count):
                    sum_datapoints.append(ram_response["Datapoints"][i]["Average"])
                ram_average = sum(sum_datapoints) / len(sum_datapoints)

            ram_response["RAM Summed Average"] = ram_average

            infra_results.append(ram_response)

        average = 0
        metrics = cw_client_instance.get_metric_statistics(
            Namespace="AWS/EC2",
            MetricName=metric,
            Dimensions=[{"Name": "InstanceId", "Value": "ami-0123456789abcdef0"}],
            StartTime=str(datetime.now(timezone.utc) - timedelta(minutes=5)),
            EndTime=str(datetime.now(timezone.utc)),
            Period=300,
            Statistics=["Average"],
        )

        if not metrics["Datapoints"]:
            metrics["Average"] = 0.0

        else:
            datapoints_count = len(metrics["Datapoints"])
            sum_datapoints = []
            for i in range(0, datapoints_count):
                sum_datapoints.append(metrics["Datapoints"][i]["Average"])
            average = sum(sum_datapoints) / len(sum_datapoints)

        metrics[f"${metric} Summed Average"] = average

        infra_results.append(metrics)

    ec2_usage = config.creds["ec2_client"].describe_instances(
        Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
    )

    reservations = ec2_usage.get("Reservations", [])

    for reservation in reservations:
        instances = reservation.get("Instances", [])
        for instance in instances:
            launch_time = instance.get("LaunchTime")
            if not launch_time:
                continue

            current_time = str(datetime.now(timezone.utc))
            compute_time_used = current_time - launch_time

            usage_results["EC2_usage"] = {
                "instance_id": instance.get("InstanceId"),
                "instance_type": instance.get("InstanceType"),
                "time_used": str(compute_time_used),
            }

    ec2_logged_metrics = {
        "infrastructure_metrics": infra_results,
        "usage_metrics": usage_results,
    }

    return ec2_logged_metrics


def experiment_dual_monitor(config, experiment_function, params: dict):
    """Monitors the experiment both locally and in the cloud through ec2, cloudwatch, and braket."""

    infra_metrics = [
        "CPUUtilization",
        "mem_used_percent",
        "NetworkIn",
        "NetworkOut",
        "DiskReadOps",
        "DiskWriteOps",
    ]

    ec2_ram_metrics = None
    ram_average = 0

    cw_client_instance = config.creds["cw_client"]

    monitor_results = {}

    thread = threading.Thread(target=experiment_function, kwargs=params)
    thread.start()

    thread_count = 0

    time.sleep(1)

    while thread.is_alive():

        thread_count = thread_count + 1
        print("Experiment function is currently running,.")
        time.sleep(0.5)

        if monitor_results["Total Local RAM Usage"] >= 98.00:
            print("Out Of Memory Risk...")
            print("Sleeping for 10 seconds..")
            time.sleep(10)

        monitor_results[f"Local CPU Usage: Thread {thread_count}"] = psutil.cpu_percent(
            interval=0.1
        )
        monitor_results[f"Local RAM Usage: Thread {thread_count}"] = (
            psutil.virtual_memory().percent
        )
        monitor_results[f"Local I/O Disk Latency: Thread {thread_count}"] = (
            psutil.disk_io_counters()
        )
        monitor_results[f"Total Local RAM Usage"] = (
            psutil.virtual_memory().percent
        ) + monitor_results[f"Local CPU Usage: Thread {thread_count}"]

        for metric in infra_metrics:

            if metric == "mem_used_percent":
                ec2_ram_metrics = cw_client_instance.get_metric_statistics(
                    Namespace="CWAgent",
                    MetricName=metric,
                    Dimensions=[{"Name": "InstanceId", "Value": "i-0123456789abcdef0"}],
                    StartTime=str(datetime.now(timezone.utc) - timedelta(minutes=5)),
                    EndTime=str(datetime.now(timezone.utc)),
                    Period=300,
                    Statistics=["Average"],
                )

                if not ec2_ram_metrics["Datapoints"]:
                    ec2_ram_metrics["Average"] = 0.0
                else:
                    datapoints_count = len(ec2_ram_metrics["Datapoints"])
                    sum_datapoints = []
                    for i in range(0, datapoints_count):
                        sum_datapoints.append(ec2_ram_metrics["Datapoints"][i]["Average"])
                    ram_average = sum(sum_datapoints) / len(sum_datapoints)

                ec2_ram_metrics["RAM Summed Average"] = ram_average

                monitor_results["EC2 Instance Ram Usage"] = ec2_ram_metrics

            average = 0
            ec2_metrics = cw_client_instance.get_metric_statistics(
                Namespace="AWS/EC2",
                MetricName=metric,
                Dimensions=[{"Name": "InstanceId", "Value": "ami-0123456789abcdef0"}],
                StartTime=str(datetime.now(timezone.utc) - timedelta(minutes=5)),
                EndTime=str(datetime.now(timezone.utc)),
                Period=300,
                Statistics=["Average"],
            )

            if not ec2_metrics["Datapoints"]:
                ["Average"] = 0.0

            else:
                datapoints_count = len(ec2_metrics["Datapoints"])
                sum_datapoints = []
                for i in range(0, datapoints_count):
                    sum_datapoints.append(ec2_metrics["Datapoints"][i]["Average"])
                average = sum(sum_datapoints) / len(sum_datapoints)

            ec2_metrics[f"${metric} Summed Average"] = average

            monitor_results[f"EC2 Instance Metrics Set {thread_count}"] = ec2_metrics

    thread.join()

    return monitor_results
