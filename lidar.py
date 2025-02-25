import time
from rplidar import RPLidar, RPLidarException

PORT_NAME = "/dev/ttyUSB0"  # Check with `ls /dev/ttyUSB*`
lidar = RPLidar(PORT_NAME)

try:
    print("Starting RPLIDAR A1...\nPress Ctrl+C to stop.")
    
    for i, scan in enumerate(lidar.iter_scans()):
        print(f"Scan {i}: {scan}")  # Print distance and angle data
        time.sleep(0.5)  # Small delay to avoid buffer overload
        
        if i == 5:  # Stop after 5 scans (to test controlled stopping)
            break

except RPLidarException as e:
    print(f"\nLIDAR Error: {e}")

except KeyboardInterrupt:
    print("\nKeyboard Interrupt detected. Stopping LIDAR...")

finally:
    print("Stopping LIDAR...")
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
    print("LIDAR successfully stopped.")

