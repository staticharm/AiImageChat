import psutil
import os
import time
import csv
from datetime import datetime

LOG_FILE = "performance_log.csv"

def log_performance(app_name: str, query: str, func):
    """
    Logs latency, CPU, and memory usage for a given function call.
    """
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / (1024 * 1024)
    cpu_before = psutil.cpu_percent(interval=None)
    start_time = time.time()

    # Execute the provided function
    response = func(query)

    end_time = time.time()
    mem_after = process.memory_info().rss / (1024 * 1024)
    cpu_after = psutil.cpu_percent(interval=None)

    latency = round(end_time - start_time, 3)
    mem_change = round(mem_after - mem_before, 2)
    cpu_usage = round(abs(cpu_after - cpu_before), 2)

    # Log to CSV
    header = ["Timestamp", "App", "Query", "Latency (s)", "Memory Change (MB)", "CPU Usage (%)"]
    row = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_name, query, latency, mem_change, cpu_usage]

    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(header)
        writer.writerow(row)

    return response, {"Latency (s)": latency, "Memory Change (MB)": mem_change, "CPU Usage (%)": cpu_usage}
