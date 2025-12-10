"""
Climb Detection Module for PyAscent
Identifies significant climbs in cycling routes.
"""

import numpy as np
from typing import List, Dict, Tuple


class ClimbDetector:
    """Detect and categorize climbs in cycling routes."""
    
    def __init__(self, distances, elevations, min_gradient=3.0, min_elevation_gain=20.0, min_distance=0.3):
        """
        Initialize the climb detector.
        
        Args:
            distances: Array of distances in km
            elevations: Array of elevations in meters
            min_gradient: Minimum average gradient to consider as climb (%)
            min_elevation_gain: Minimum elevation gain to consider (meters)
            min_distance: Minimum distance to consider as a climb (km)
        """
        self.distances = distances
        self.elevations = elevations
        self.min_gradient = min_gradient
        self.min_elevation_gain = min_elevation_gain
        self.min_distance = min_distance
    
    def detect_climbs(self) -> List[Dict]:
        """
        Detect climbs in the route.
        
        Returns:
            List of climb dictionaries with details
        """
        climbs = []
        in_climb = False
        climb_start_idx = 0
        climb_start_elevation = 0
        
        # Smooth the elevation data to reduce noise
        window_size = min(5, len(self.elevations) // 10)
        if window_size > 1:
            smoothed_elevations = np.convolve(
                self.elevations, 
                np.ones(window_size)/window_size, 
                mode='same'
            )
        else:
            smoothed_elevations = self.elevations
        
        for i in range(1, len(self.distances)):
            elevation_diff = smoothed_elevations[i] - smoothed_elevations[i-1]
            distance_diff = self.distances[i] - self.distances[i-1]
            
            if distance_diff > 0:
                gradient = (elevation_diff / (distance_diff * 1000)) * 100
                
                if not in_climb and gradient > self.min_gradient:
                    # Start of a climb
                    in_climb = True
                    climb_start_idx = i
                    climb_start_elevation = smoothed_elevations[i]
                
                elif in_climb and gradient < 0:
                    # End of climb (descent starts)
                    elevation_gain = smoothed_elevations[i-1] - climb_start_elevation
                    
                    if elevation_gain >= self.min_elevation_gain:
                        climb_distance = self.distances[i-1] - self.distances[climb_start_idx]
                        avg_gradient = (elevation_gain / (climb_distance * 1000)) * 100 if climb_distance > 0 else 0
                        
                        if climb_distance >= self.min_distance:
                            climbs.append({
                                'start_idx': climb_start_idx,
                                'end_idx': i-1,
                                'start_distance': self.distances[climb_start_idx],
                                'end_distance': self.distances[i-1],
                                'start_elevation': self.elevations[climb_start_idx],
                                'end_elevation': self.elevations[i-1],
                                'elevation_gain': elevation_gain,
                                'distance': climb_distance,
                                'avg_gradient': avg_gradient,
                                'category': self._categorize_climb(elevation_gain, avg_gradient)
                            })
                    
                    in_climb = False
        
        # Handle case where route ends on a climb
        if in_climb:
            elevation_gain = smoothed_elevations[-1] - climb_start_elevation
            if elevation_gain >= self.min_elevation_gain:
                climb_distance = self.distances[-1] - self.distances[climb_start_idx]
                avg_gradient = (elevation_gain / (climb_distance * 1000)) * 100 if climb_distance > 0 else 0
                
                if climb_distance >= self.min_distance:
                    climbs.append({
                        'start_idx': climb_start_idx,
                        'end_idx': len(self.distances) - 1,
                        'start_distance': self.distances[climb_start_idx],
                        'end_distance': self.distances[-1],
                        'start_elevation': self.elevations[climb_start_idx],
                        'end_elevation': self.elevations[-1],
                        'elevation_gain': elevation_gain,
                        'distance': climb_distance,
                        'avg_gradient': avg_gradient,
                        'category': self._categorize_climb(elevation_gain, avg_gradient)
                    })
        
        return climbs
    
    def _categorize_climb(self, elevation_gain: float, avg_gradient: float) -> str:
        """
        Categorize climb difficulty based on elevation gain and gradient.
        
        Args:
            elevation_gain: Total elevation gain in meters
            avg_gradient: Average gradient in percentage
        
        Returns:
            Category string (HC, 1, 2, 3, 4, or Uncategorized)
        """
        # Simplified categorization inspired by Tour de France categories
        difficulty_score = elevation_gain * avg_gradient
        
        if difficulty_score > 8000 or elevation_gain > 1200:
            return "HC"  # Hors Catégorie (beyond categorization)
        elif difficulty_score > 5000 or elevation_gain > 800:
            return "1"
        elif difficulty_score > 3000 or elevation_gain > 500:
            return "2"
        elif difficulty_score > 1500 or elevation_gain > 300:
            return "3"
        elif elevation_gain >= self.min_elevation_gain:
            return "4"
        else:
            return "Uncategorized"
