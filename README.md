# 📊 Tufte-Style NYC Weather Visualization

This project recreates Edward Tufte's iconic New York City weather visualization featured in *The Visual Display of Quantitative Information, 2nd Ed.* (Page 30). Using shell scripts and Python, the pipeline automates the retrieval, processing, and visualization of historical weather data in a Tufte-inspired minimalist style.

## 📋 Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.x
- Required Python packages:
  - pandas
  - numpy
  - matplotlib
- Bash shell (for Unix-based systems)
- bc (for floating-point arithmetic)
- PaSh (optional, for parallel processing)

## 📁 Project Structure

```
/Tufte Weather Project/
├── data/                  # Raw and processed weather data
│   └── processed/        # Extracted and formatted data files
├── output/               # Generated visualizations
└── scripts/              # Pipeline scripts
    ├── download_data.sh  # Downloads weather data from NOAA
    ├── process_data.sh   # Extracts and formats the data
    ├── visualize.py      # Creates the Tufte-style visualization
    ├── weather_pipeline.sh # Main orchestration script
    ├── install_pash.sh   # Script to install PaSh
    └── performance_test.sh # Performance testing script
```

## 🚀 Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd "Tufte-Weather-Project"
```

2. Install Python dependencies:
```bash
pip install pandas numpy matplotlib
```

3. (Optional) Install PaSh for parallel processing:
```bash
./scripts/install_pash.sh
```

4. Make scripts executable:
```bash
chmod +x scripts/*.sh scripts/*.py
```

## ▶️ Running the Pipeline

The pipeline can be run in two ways:

### Basic Usage
```bash
./scripts/weather_pipeline.sh [YEAR]
```
Example:
```bash
./scripts/weather_pipeline.sh 1980
```

### With PaSh Parallelization
```bash
./scripts/weather_pipeline.sh [YEAR] true
```
Example:
```bash
./scripts/weather_pipeline.sh 1980 true
```

### Pipeline Steps

1. **Data Download**: The script downloads historical weather data for NYC from NOAA
2. **Data Processing**: Raw data is processed and formatted for visualization
3. **Visualization**: Creates a Tufte-style visualization showing:
   - Daily temperature ranges
   - Precipitation data
   - Humidity levels
   - Monthly averages

The output will be saved as a PNG file in the `output` directory: `nyc_weather_[YEAR]_tufte_style.png`

## 🔍 Features

- Historical weather data visualization in Tufte's minimalist style
- Support for any year's data (with fallback to generated sample data if download fails)
- Optional parallel processing with PaSh
- Automatic data processing and formatting
- High-resolution output suitable for printing

## ⚠️ Notes

- If the NOAA data download fails, the script will generate sample data for testing
- The visualization is optimized for print quality
- PaSh parallelization is optional and only used if installed





