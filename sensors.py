import carla
import time

def measure_sensor_latency(world, sensor_bp, transform, vehicle):
    # Spawn the sensor
    sensor = world.spawn_actor(sensor_bp, transform, attach_to=vehicle)
    
    # Initialize a container to store the latency
    latencies = []

    # Define a callback function to capture the first reading
    def callback(data):
        nonlocal latencies
        latency = int((time.time() - start_time) * 1e9)  # Higher precision timer
        latencies.append(latency)
        print(f'{sensor_bp.id} latency: {latency} nanoseconds')
        sensor.stop()  # Stop listening after the first reading
        sensor.destroy()  # Destroy the sensor after capturing the reading

    # Start the measurement
    start_time = time.time()
    sensor.listen(callback)
    
    # Wait until the callback function completes
    while not latencies:
        time.sleep(0.1)  # Reduced sleep time for better responsiveness

# Connect to CARLA
def main():
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    world = client.get_world()
    blueprint_library = world.get_blueprint_library()
    
    # Spawn a vehicle to attach sensors to
    vehicle_bp = blueprint_library.find('vehicle.tesla.model3')
    spawn_points = world.get_map().get_spawn_points()
    spawn_point = spawn_points[12] if len(spawn_points) > 12 else spawn_points[0]  # Check for valid spawn point
    vehicle = world.spawn_actor(vehicle_bp, spawn_point)
    
    # Define a transform to attach sensors to the vehicle
    transform = carla.Transform(carla.Location(x=0.0, y=0.0, z=2.0))
    
    # List of sensor blueprints to check
    sensor_list = [
        'sensor.camera.rgb',
        'sensor.camera.depth',
        'sensor.camera.semantic_segmentation',
        'sensor.camera.optical_flow',
        'sensor.camera.dvs',
        'sensor.lidar.ray_cast',
        'sensor.lidar.ray_cast_semantic',
        'sensor.other.radar',
        'sensor.other.imu',
        'sensor.other.gnss',
    ]
    
    # Loop through each sensor blueprint, measure and print latency
    for sensor_id in sensor_list:
        sensor_bp = blueprint_library.find(sensor_id)
        measure_sensor_latency(world, sensor_bp, transform, vehicle)

    # Destroy the vehicle after all measurements
    vehicle.destroy()
    
main()
    

