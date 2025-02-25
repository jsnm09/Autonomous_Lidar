import numpy as np
import matplotlib.pyplot as plt
from rplidar import RPLidar, RPLidarException

# Set up RPLIDAR
PORT_NAME = "/dev/ttyUSB0"  # Change if necessary
lidar = RPLidar(PORT_NAME)

# Increase spin speed (but not too high)
lidar.set_pwm(800)  # 600-900 is stable; 1000 may cause issues

# Set up Matplotlib plot
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.set_ylim(0, 4000)  # Set max detection range

def update_scan():
    """Reads LiDAR data and updates the plot in real-time."""
    try:
        print("Flushing LiDAR buffer...")
        lidar.clear_input()  # Clears old data to prevent mismatches
        
        for _, scan in enumerate(lidar.iter_scans(max_buf_meas=200)):  # Limit buffer size
            ax.clear()
            ax.set_ylim(0, 4000)  # Keep range consistent

            angles = [np.radians(d[1]) for d in scan]  # Convert to radians
            distances = [d[2] for d in scan]  # Get distance data
            
            ax.scatter(angles, distances, s=5, c='red', alpha=0.75)  # Update points
            plt.pause(0.005)  # Faster refresh rate (reduce delay)

    except RPLidarException as e:
        print(f"\nLIDAR Error: {e}. Restarting...")
        lidar.clear_input()  # Clear buffer and restart safely
        update_scan()

    except KeyboardInterrupt:
        print("\nStopping visualization...")
    finally:
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()
        print("LiDAR Stopped Successfully.")

# Run the visualization
print("Starting real-time LiDAR visualization with faster scanning. Press Ctrl+C to stop.")
update_scan()

