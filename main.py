import psutil,time
from datetime import datetime

# Set this flag externally to control monitoring
PM_mode = True  

def System_Monitor():
    """Monitors system performance and sends data periodically."""
    try:
            # Capture memory information
            vm = psutil.virtual_memory()
            memory_info = f"{vm.total},{vm.used},{vm.available},{vm.percent}"

            # Capture battery percentage (handle systems without a battery)
            battery = psutil.sensors_battery()
            battery_percent = battery.percent if battery else "N/A"

            # Capture network interface details
            net_stats = psutil.net_if_stats()
            network_info = "_".join(
                f"{iface},{'Up' if stats.isup else 'Down'},{stats.speed}"
                for iface, stats in net_stats.items()
            )

            # Capture last 10 process details
            processes = []
            for pid in psutil.pids()[-10:]:  
                try:
                    p = psutil.Process(pid)
                    processes.append(f"{pid},{p.name()},{p.status()},{p.cpu_percent()}%,{p.num_threads()}")
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue  

            process_info = "_".join(processes)

            # Format collected data
            data = f"{datetime.now()} | Battery: {battery_percent}% | Network: {network_info} | Memory: {memory_info} | Processes: {process_info}"
            return data
        
    except Exception as e:
            print(f"Error: {e}")

    

# Run the monitor
if __name__ == "__main__":
    System_Monitor()
