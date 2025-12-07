"""
GPX Parser Module for PyAscent
Handles parsing GPX files and extracting route data.
"""

import gpxpy
import numpy as np
from typing import List, Tuple, Dict


class GPXParser:
    """Parse GPX files and extract cycling route data."""
    
    def __init__(self, gpx_file):
        """
        Initialize the GPX parser.
        
        Args:
            gpx_file: File object or path to GPX file
        """
        self.gpx = gpxpy.parse(gpx_file)
        self.points = []
        self.elevations = []
        self.distances = []
        self.latitudes = []
        self.longitudes = []
        self._extract_data()
    
    def _extract_data(self):
        """Extract points, elevations, and distances from GPX."""
        total_distance = 0.0
        previous_point = None
        
        for track in self.gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    self.points.append(point)
                    self.elevations.append(point.elevation if point.elevation else 0)
                    self.latitudes.append(point.latitude)
                    self.longitudes.append(point.longitude)
                    
                    if previous_point:
                        distance = point.distance_3d(previous_point)
                        if distance:
                            total_distance += distance
                    
                    self.distances.append(total_distance)
                    previous_point = point
        
        # Convert to numpy arrays for easier processing
        self.elevations = np.array(self.elevations)
        self.distances = np.array(self.distances) / 1000.0  # Convert to km
        self.latitudes = np.array(self.latitudes)
        self.longitudes = np.array(self.longitudes)
    
    def get_route_data(self) -> Dict:
        """
        Get the complete route data.
        
        Returns:
            Dictionary containing route information
        """
        return {
            'distances': self.distances,
            'elevations': self.elevations,
            'latitudes': self.latitudes,
            'longitudes': self.longitudes,
            'total_distance': self.distances[-1] if len(self.distances) > 0 else 0,
            'elevation_gain': self._calculate_elevation_gain(),
            'max_elevation': np.max(self.elevations) if len(self.elevations) > 0 else 0,
            'min_elevation': np.min(self.elevations) if len(self.elevations) > 0 else 0
        }
    
    def _calculate_elevation_gain(self) -> float:
        """Calculate total elevation gain."""
        gain = 0.0
        for i in range(1, len(self.elevations)):
            diff = self.elevations[i] - self.elevations[i-1]
            if diff > 0:
                gain += diff
        return gain
