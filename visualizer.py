"""
Visualization Module for PyAscent
Creates images marking important climbs on cycling routes.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from io import BytesIO
from typing import List, Dict, Optional


class RouteVisualizer:
    """Create visualizations of cycling routes with climb markers."""
    
    def __init__(self, route_data: Dict, climbs: List[Dict]):
        """
        Initialize the route visualizer.
        
        Args:
            route_data: Dictionary containing route information
            climbs: List of detected climbs
        """
        self.route_data = route_data
        self.climbs = climbs
    
    def create_elevation_profile(self, figsize=(14, 6), dpi=100, title: Optional[str] = None, climb_names: Optional[Dict[int, str]] = None):
        """
        Create an elevation profile with marked climbs.
        
        Args:
            figsize: Figure size tuple (width, height)
            dpi: Dots per inch for image resolution
            title: Custom title for the graph (optional)
            climb_names: Dictionary mapping climb index to custom name (optional)
        
        Returns:
            BytesIO object containing the image
        """
        fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
        
        distances = self.route_data['distances']
        elevations = self.route_data['elevations']
        
        # Plot elevation profile
        ax.plot(distances, elevations, linewidth=2, color='#2E86AB', label='Elevation')
        ax.fill_between(distances, elevations, alpha=0.3, color='#A8DADC')
        
        # Unified climb color
        climb_color = '#f5cf23'
        
        # Mark climbs on the profile
        for climb_idx, climb in enumerate(self.climbs):
            start_idx = climb['start_idx']
            end_idx = climb['end_idx']
            
            # Highlight climb section with unified color
            ax.fill_between(
                distances[start_idx:end_idx+1],
                elevations[start_idx:end_idx+1],
                alpha=0.6,
                color=climb_color
            )
            
            # Add climb marker at the peak
            ax.scatter(
                distances[end_idx], 
                elevations[end_idx], 
                color=climb_color, 
                s=150, 
                zorder=5,
                edgecolors='white',
                linewidths=2
            )
            
            # Format climb label
            if climb_names and climb_idx in climb_names and climb_names[climb_idx]:
                climb_label = climb_names[climb_idx]
            else:
                climb_label = f"{climb['elevation_gain']:.0f} m Climb {climb_idx + 1} ({climb['distance']:.1f} km at {climb['avg_gradient']:.1f}%)"
            
            # Add climb label
            ax.annotate(
                climb_label,
                xy=(distances[end_idx], elevations[end_idx]),
                xytext=(0, 20),
                textcoords='offset points',
                ha='center',
                fontsize=10,
                fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor=climb_color, alpha=0.8, edgecolor='white'),
                color='black'
            )
            
        # Adjust y-axis limits
        min_elevation = elevations.min()
        max_elevation = elevations.max()
        elevation_range = max_elevation - min_elevation

        # Add 10% padding to the bottom and 15% to the top
        y_min = min_elevation - (elevation_range * 0.1)
        y_max = max_elevation + (elevation_range * 0.15)
        ax.set_ylim(y_min, y_max)
        
        # Set labels and title
        ax.set_xlabel('Distance (km)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Elevation (m)', fontsize=12, fontweight='bold')
        graph_title = title if title else 'Cycling Route Elevation Profile with Climbs'
        ax.set_title(graph_title, fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        
        # Save to BytesIO
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=dpi, bbox_inches='tight')
        buf.seek(0)
        plt.close(fig)
        
        return buf
    
    def create_climb_summary_table(self, climb_names: Optional[Dict[int, str]] = None):
        """
        Create a summary of all climbs.
        
        Args:
            climb_names: Dictionary mapping climb index to custom name (optional)
        
        Returns:
            List of dictionaries with formatted climb information
        """
        summary = []
        for i, climb in enumerate(self.climbs):
            climb_name = 'Unknown'
            if climb_names and i in climb_names and climb_names[i]:
                climb_name = climb_names[i]
            else:
                climb_name = f"{climb['elevation_gain']:.0f} m Climb {i + 1}"
            
            summary.append({
                'Climb #': i + 1,
                'Climb Name': climb_name,
                'Start (km)': f"{climb['start_distance']:.2f}",
                'End (km)': f"{climb['end_distance']:.2f}",
                'Distance (km)': f"{climb['distance']:.2f}",
                'Elevation Gain (m)': f"{climb['elevation_gain']:.0f}",
                'Avg Gradient (%)': f"{climb['avg_gradient']:.1f}",
                'Category': climb['category']
            })
        return summary
