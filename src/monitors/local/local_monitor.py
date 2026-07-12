import threading
import time

def monitor_experiment(infra_monitor_class, experiment_monitor_class, experiment_function, params: dict):
        infra_monitor_instance = infra_monitor_class()
        
        initial_metrics = experiment_monitor_class.__get_metrics()
        cloud_infra_initial_metrics = infra_monitor_instance.get_ec2_infrastructure_metrics()
        monitor_results = {}

        thread = threading.Thread(target=experiment_function, kwargs=params)
        thread.start()

        monitor_results["Cloud Machine Data"] = infra_monitor_instance.get_ec2_infrastructure_metrics()
        monitor_results["Total Cloud CPU Usage"] = infra_monitor_instance.get_ec2_infrastructure_metrics()["CPU_usage"] 
        monitor_results["Total Cloud RAM Usage"] = infra_monitor_instance.get_ec2_infrastructure_metrics()["RAM_usage"]
        
        thread_count = 0

        time.sleep(1) 

        while (thread.is_alive()):
            thread_count = thread_count + 1
            print("Experiment function is currently running,.")
            time.sleep(0.5)

            monitor_results[f"Local Machine Data {thread_count}"] = experiment_monitor_class.__get_metrics()
            monitor_results["Total Local CPU Usage"] = [f"Local Machine Data {thread_count}"]["CPU_usage"] + [f"Local Machine Data {thread_count}"]["CPU_usage"]
            monitor_results["Total Local RAM Usage"] = [f"Local Machine Data {thread_count}"]["RAM_usage"] + [f"Local Machine Data {thread_count}"]["RAM_usage"]

        thread.join()

        monitor_results["Cloud Machine Data"] = infra_monitor_instance.get_ec2_infrastructure_metrics()
        monitor_results["Total Cloud CPU Usage"] = infra_monitor_instance.get_ec2_infrastructure_metrics()["CPU_usage"] 
        monitor_results["Total Cloud RAM Usage"] = infra_monitor_instance.get_ec2_infrastructure_metrics()["RAM_usage"]
    
        return monitor_results