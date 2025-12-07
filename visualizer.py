"""
Visualization Module for PyAscent
Creates images marking important climbs on cycling routes.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from io import BytesIO
from typing import List, Dict


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
    
    def create_elevation_profile(self, figsize=(14, 6), dpi=100):
        """
        Create an elevation profile with marked climbs.
        
        Args:
            figsize: Figure size tuple (width, height)
            dpi: Dots per inch for image resolution
        
        Returns:
            BytesIO object containing the image
        """
        fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
        
        distances = self.route_data['distances']
        elevations = self.route_data['elevations']
        
        # Plot elevation profile
        ax.plot(distances, elevations, linewidth=2, color='#2E86AB', label='Elevation')
        ax.fill_between(distances, elevations, alpha=0.3, color='#A8DADC')
        
        # Color mapping for climb categories
        category_colors = {
            'HC': '#E63946',  # Red - Hardest
            '1': '#F77F00',   # Orange
            '2': '#FCBF49',   # Yellow
            '3': '#06A77D',   # Green
            '4': '#457B9D',   # Blue
            'Uncategorized': '#A8A8A8'  # Gray
        }
        
        # Mark climbs on the profile
        for climb in self.climbs:
            start_idx = climb['start_idx']
            end_idx = climb['end_idx']
            color = category_colors.get(climb['category'], '#A8A8A8')
            
            # Highlight climb section
            ax.fill_between(
                distances[start_idx:end_idx+1],
                elevations[start_idx:end_idx+1],
                alpha=0.6,
                color=color
            )
            
            # Add climb marker at the peak
            ax.scatter(
                distances[end_idx], 
                elevations[end_idx], 
                color=color, 
                s=150, 
                zorder=5,
                edgecolors='white',
                linewidths=2
            )
            
            # Add climb category label
            if climb['category'] != 'Uncategorized':
                ax.annotate(
                    f"Cat {climb['category']}",
                    xy=(distances[end_idx], elevations[end_idx]),
                    xytext=(0, 20),
                    textcoords='offset points',
                    ha='center',
                    fontsize=10,
                    fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.5', facecolor=color, alpha=0.8, edgecolor='white'),
                    color='white'
                )
        
        # Set labels and title
        ax.set_xlabel('Distance (km)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Elevation (m)', fontsize=12, fontweight='bold')
        ax.set_title('Cycling Route Elevation Profile with Climbs', fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # Add legend for climb categories
        if self.climbs:
            legend_elements = []
            categories_present = set(climb['category'] for climb in self.climbs)
            for category in ['HC', '1', '2', '3', '4']:
                if category in categories_present:
                    legend_elements.append(
                        mpatches.Patch(color=category_colors[category], label=f'Category {category}')
                    )
            if legend_elements:
                ax.legend(handles=legend_elements, loc='upper right', fontsize=10)
        
        plt.tight_layout()
        
        # Save to BytesIO
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=dpi, bbox_inches='tight')
        buf.seek(0)
        plt.close(fig)
        
        return buf
    
    def create_climb_summary_table(self):
        """
        Create a summary of all climbs.
        
        Returns:
            List of dictionaries with formatted climb information
        """
        summary = []
        for i, climb in enumerate(self.climbs, 1):
            summary.append({
                'Climb #': i,
                'Start (km)': f"{climb['start_distance']:.2f}",
                'End (km)': f"{climb['end_distance']:.2f}",
                'Distance (km)': f"{climb['distance']:.2f}",
                'Elevation Gain (m)': f"{climb['elevation_gain']:.0f}",
                'Avg Gradient (%)': f"{climb['avg_gradient']:.1f}",
                'Category': climb['category']
            })
        return summary
