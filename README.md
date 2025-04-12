# Recreating Tufte's Famous Weather Illustration

This project recreates Edward Tufte's famous weather illustration from the New York Times as featured in his book "The Visual Display of Quantitative Information, 2nd Ed." (page 30). The project combines shell scripting with visualization tools to process weather data and generate a similar visualization.

## Project Structure
/Users/aayam/Documents/US Applications/Brown University/Tufte Weather Trae/
├── data/                  # Raw and processed weather data
│   └── processed/         # Extracted and formatted data files
├── output/                # Generated visualizations
└── scripts/               # Pipeline scripts
    ├── download_data.sh   # Downloads weather data from NOAA
    ├── process_data.sh    # Extracts and formats the data
    ├── visualize.py       # Creates the visualization
    └── weather_pipeline.sh # Main pipeline script

# Running the Tufte Weather Visualization Pipeline
To run the weather visualization pipeline, follow these steps:

Open Terminal on your Mac
Navigate to the project directory:
bash
Run
cd "/Users/aayam/Documents/US Applications/Brown University/Tufte Weather Trae"
Make sure all scripts are executable:
bash
Run
chmod +x scripts/*.sh scripts/*.py
Run the pipeline with the default year (1980):
bash
Run
./scripts/weather_pipeline.sh
Or specify a different year:
bash
Run
./scripts/weather_pipeline.sh 2000
If you want to use PaSh for parallelization (if available):
bash
Run
./scripts/weather_pipeline.sh 2000 true
The visualization will be saved to the output directory as nyc_weather_YEAR_tufte_style.png.

You can view the generated image using:

bash
Run
open output/nyc_weather_1980_tufte_style.png
The pipeline will automatically:

Download weather data from NOAA
Process the data into the required format
Generate the Tufte-style visualization
If the data download fails, the script will automatically generate sample data for testing purposes.