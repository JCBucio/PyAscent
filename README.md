# 🚴 PyAscent - Turn GPX into Climb Intelligence

PyAscent is a Streamlit web application that analyzes cycling routes from GPX files and identifies important climbs. It generates beautiful elevation profiles with color-coded climb markers and provides detailed statistics about each climb.

## Features

- 📊 **Interactive Elevation Profiles**: Visualize your cycling route with all climbs clearly marked
- 🏔️ **Automatic Climb Detection**: Intelligently identifies climbs based on gradient and elevation gain
- 🎨 **Color-Coded Categories**: Climbs are categorized (HC, 1, 2, 3, 4) based on difficulty
- 📈 **Detailed Statistics**: View distance, elevation gain, and average gradient for each climb
- ⚙️ **Customizable Settings**: Adjust climb detection parameters to suit your needs
- 💾 **Export Results**: Download elevation profile images

## Installation

1. Clone the repository:
```bash
git clone https://github.com/JCBucio/PyAscent.git
cd PyAscent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser and navigate to the URL shown (typically `http://localhost:8501`)

3. Upload a GPX file from your cycling computer or app

4. Explore the elevation profile and climb statistics

5. Adjust settings in the sidebar if needed

6. Download the generated elevation profile image

## How It Works

### Climb Detection
PyAscent analyzes the elevation profile of your route and identifies climbs based on:
- **Minimum Gradient**: Default 3% average gradient
- **Minimum Elevation Gain**: Default 20 meters

### Climb Categories
Climbs are categorized similar to Tour de France classifications:
- **HC (Hors Catégorie)**: Beyond categorization - the hardest climbs (>1200m gain or difficulty score >8000)
- **Category 1**: Very difficult climbs (>800m gain or difficulty score >5000)
- **Category 2**: Difficult climbs (>500m gain or difficulty score >3000)
- **Category 3**: Moderate climbs (>300m gain or difficulty score >1500)
- **Category 4**: Minor climbs (meets minimum elevation gain)

## Getting GPX Files

Most cycling apps and devices support GPX export:

- **Strava**: Activity page → Three dots menu → Export GPX
- **Garmin Connect**: Activity → Settings gear → Export Original
- **Wahoo**: Activity → Share → Export as GPX
- **Komoot**: Planned tour → Share → Export as GPX

## Project Structure

```
PyAscent/
├── app.py              # Main Streamlit application
├── gpx_parser.py       # GPX file parsing module
├── climb_detector.py   # Climb detection algorithm
├── visualizer.py       # Elevation profile visualization
├── requirements.txt    # Python dependencies
├── sample_route.gpx    # Sample GPX file for testing
└── README.md          # This file
```

## Requirements

- Python 3.7+
- streamlit
- gpxpy
- matplotlib
- numpy
- pandas
- Pillow

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Juan Carlos Bucio Tejeda

## Acknowledgments

- Climb categorization inspired by Tour de France classifications
- Built with Streamlit, gpxpy, matplotlib and seaborn
