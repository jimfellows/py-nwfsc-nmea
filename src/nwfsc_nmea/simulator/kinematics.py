import math
import time

class VesselState:
    """
    Simulates a vessel's physical state over time.
    Calculates updated lat/lon based on course and speed.
    """
    
    def __init__(self, lat=47.6, lon=-122.3, heading=0.0, speed_knots=10.0):
        # Position
        self.lat = lat
        self.lon = lon
        
        # Motion
        self.heading = heading  # Degrees True
        self.speed_knots = speed_knots
        
        # Environmental / Sensor
        self.depth_meters = 50.0
        self.water_temp_c = 12.0
        
        # Attitude
        self.pitch = 0.0
        self.roll = 0.0
        self.heave = 0.0
        
        # Trawl Specifics
        self.trawl_depth = 40.0
        self.trawl_distance = 150.0  # meters behind vessel
        self.trawl_door_spread = 50.0
        self.headrope_height = 5.0
        self.trawl_lat = self.lat
        self.trawl_lon = self.lon
        
        self.last_update = time.time()

    def update(self, dt=None):
        """
        Update the vessel's state by elapsed time `dt`.
        If dt is None, uses real elapsed time since last call.
        """
        now = time.time()
        if dt is None:
            dt = now - self.last_update
            
        self.last_update = now
        
        if dt <= 0:
            return

        # Simple Flat-Earth approximation for small dt
        # 1 knot = 1.852 km/h = 0.514444... m/s
        speed_ms = self.speed_knots * 0.514444
        distance_m = speed_ms * dt
        
        # Earth radius in meters
        R = 6378137.0
        
        # Offset in meters
        heading_rad = math.radians(self.heading)
        dx = distance_m * math.sin(heading_rad)
        dy = distance_m * math.cos(heading_rad)
        
        # Coordinate offsets in radians
        dlat = dy / R
        dlon = dx / (R * math.cos(math.radians(self.lat)))
        
        self.lat += math.degrees(dlat)
        self.lon += math.degrees(dlon)
        
        # Simulate some minor noise
        import random
        self.pitch = random.uniform(-2.0, 2.0)
        self.roll = random.uniform(-5.0, 5.0)
        self.heave = random.uniform(-0.5, 0.5)
        
        # Trawl position lags behind the vessel
        # Calculate trawl position opposite of current heading
        trawl_heading_rad = math.radians((self.heading + 180) % 360)
        tdx = self.trawl_distance * math.sin(trawl_heading_rad)
        tdy = self.trawl_distance * math.cos(trawl_heading_rad)
        self.trawl_lat = self.lat + math.degrees(tdy / R)
        self.trawl_lon = self.lon + math.degrees(tdx / (R * math.cos(math.radians(self.lat))))
        
        # Minor fluctuations in depth and temperature
        self.depth_meters += random.uniform(-0.1, 0.1)
        self.water_temp_c += random.uniform(-0.01, 0.01)

