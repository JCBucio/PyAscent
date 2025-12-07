"""
PyAscent - Streamlit Web App
Turn GPX files into Climb Intelligence
"""

import streamlit as st
import pandas as pd
from gpx_parser import GPXParser
from climb_detector import ClimbDetector
from visualizer import RouteVisualizer


def main():
    """Main Streamlit application."""
    
    # Page configuration
    st.set_page_config(
        page_title="PyAscent - Climb Intelligence",
        page_icon="🚴",
        layout="wide"
    )
    
    # Header
    st.title("🚴 PyAscent - Turn GPX into Climb Intelligence")
    st.markdown("""
    Upload a GPX file from your cycling route, and PyAscent will identify and visualize 
    all the important climbs with their categories.
    """)
    
    # Sidebar for settings
    st.sidebar.header("⚙️ Climb Detection Settings")
    min_gradient = st.sidebar.slider(
        "Minimum Gradient (%)", 
        min_value=1.0, 
        max_value=10.0, 
        value=3.0, 
        step=0.5,
        help="Minimum average gradient to consider as a climb"
    )
    min_elevation_gain = st.sidebar.slider(
        "Minimum Elevation Gain (m)", 
        min_value=10, 
        max_value=100, 
        value=20, 
        step=5,
        help="Minimum elevation gain to consider as a climb"
    )
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a GPX file", 
        type=['gpx'],
        help="Upload a GPX file from your cycling computer or app"
    )
    
    if uploaded_file is not None:
        try:
            # Process the GPX file
            with st.spinner("🔄 Parsing GPX file..."):
                parser = GPXParser(uploaded_file)
                route_data = parser.get_route_data()
            
            # Display route summary
            st.success("✅ GPX file loaded successfully!")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Distance", f"{route_data['total_distance']:.2f} km")
            with col2:
                st.metric("Elevation Gain", f"{route_data['elevation_gain']:.0f} m")
            with col3:
                st.metric("Max Elevation", f"{route_data['max_elevation']:.0f} m")
            with col4:
                st.metric("Min Elevation", f"{route_data['min_elevation']:.0f} m")
            
            # Detect climbs
            with st.spinner("🔍 Detecting climbs..."):
                detector = ClimbDetector(
                    route_data['distances'],
                    route_data['elevations'],
                    min_gradient=min_gradient,
                    min_elevation_gain=min_elevation_gain
                )
                climbs = detector.detect_climbs()
            
            if climbs:
                st.info(f"🏔️ Found {len(climbs)} climb(s) in this route!")
                
                # Create visualization
                with st.spinner("📊 Creating elevation profile..."):
                    visualizer = RouteVisualizer(route_data, climbs)
                    img_buffer = visualizer.create_elevation_profile()
                
                # Display the elevation profile
                st.subheader("📈 Elevation Profile with Climbs")
                st.image(img_buffer, use_container_width=True)
                
                # Display climb summary table
                st.subheader("📋 Climb Summary")
                climb_summary = visualizer.create_climb_summary_table()
                df = pd.DataFrame(climb_summary)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Download option for the image
                st.subheader("💾 Download")
                img_buffer.seek(0)
                st.download_button(
                    label="Download Elevation Profile",
                    data=img_buffer,
                    file_name="elevation_profile_with_climbs.png",
                    mime="image/png"
                )
                
            else:
                st.warning("⚠️ No significant climbs detected in this route with the current settings. Try adjusting the minimum gradient or elevation gain in the sidebar.")
        
        except Exception as e:
            st.error(f"❌ Error processing GPX file: {str(e)}")
            st.info("Please ensure you uploaded a valid GPX file.")
    
    else:
        # Instructions when no file is uploaded
        st.info("👆 Upload a GPX file to get started!")
        
        with st.expander("ℹ️ How to use PyAscent"):
            st.markdown("""
            1. **Upload a GPX file**: Click the file uploader above and select a GPX file from your device
            2. **Adjust settings** (optional): Use the sidebar to customize climb detection parameters
            3. **View results**: PyAscent will automatically detect climbs and display:
               - An elevation profile with color-coded climbs
               - A detailed table with climb statistics
               - Climb categories based on difficulty (HC, 1, 2, 3, 4)
            4. **Download**: Save the elevation profile image to your device
            
            **Climb Categories** (inspired by Tour de France):
            - **HC** (Hors Catégorie): Beyond categorization - the hardest climbs
            - **Category 1**: Very difficult climbs
            - **Category 2**: Difficult climbs
            - **Category 3**: Moderate climbs
            - **Category 4**: Minor climbs
            """)
        
        with st.expander("📖 About GPX Files"):
            st.markdown("""
            GPX (GPS Exchange Format) is a standard file format for GPS data. Most cycling computers 
            and apps (Strava, Garmin Connect, Wahoo, etc.) allow you to export your rides as GPX files.
            
            **How to get a GPX file:**
            - From Strava: Go to your activity → Click the three dots → Export GPX
            - From Garmin Connect: Open activity → Settings (gear icon) → Export Original
            - From most cycling apps: Look for Export, Share, or Download options
            """)


if __name__ == "__main__":
    main()
