#!/bin/bash

# Performance testing script for the weather visualization pipeline
# Tests the pipeline with different years and measures execution time

# Set directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="$SCRIPT_DIR/../output"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Create a log file for results
LOG_FILE="$OUTPUT_DIR/performance_test_results.txt"
echo "Performance Test Results" > "$LOG_FILE"
echo "======================" >> "$LOG_FILE"
echo "Date: $(date)" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# Test with a single year (1980)
echo "Testing with a single year (1980)..."
echo "Single Year Test (1980):" >> "$LOG_FILE"
START_TIME=$(date +%s)
"$SCRIPT_DIR/weather_pipeline.sh" 1980 false
END_TIME=$(date +%s)
ELAPSED_TIME=$((END_TIME - START_TIME))
echo "Execution time without PaSh: $ELAPSED_TIME seconds" >> "$LOG_FILE"

# Test with PaSh if available
if command -v pash &> /dev/null; then
    echo "Testing with PaSh..."
    START_TIME=$(date +%s)
    "$SCRIPT_DIR/weather_pipeline.sh" 1980 true
    END_TIME=$(date +%s)
    ELAPSED_TIME=$((END_TIME - START_TIME))
    echo "Execution time with PaSh: $ELAPSED_TIME seconds" >> "$LOG_FILE"
else
    echo "PaSh not installed. Skipping PaSh test."
    echo "PaSh not installed. Test skipped." >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"

# Test with multiple years (if data is available)
echo "Testing with multiple years..."
echo "Multiple Years Test:" >> "$LOG_FILE"

# Define years to test
YEARS=(1980 1981 1982 1983 1984 1985 1986 1987 1988 1989)

# Without PaSh
echo "Running without PaSh..."
START_TIME=$(date +%s)
for YEAR in "${YEARS[@]}"; do
    echo "Processing year $YEAR..."
    "$SCRIPT_DIR/download_data.sh" "$YEAR"
    "$SCRIPT_DIR/process_data.sh" "$YEAR"
    "$SCRIPT_DIR/visualize.py" "$YEAR"
done
END_TIME=$(date +%s)
ELAPSED_TIME=$((END_TIME - START_TIME))
echo "Execution time for 10 years without PaSh: $ELAPSED_TIME seconds" >> "$LOG_FILE"

# With PaSh (if available)
if command -v pash &> /dev/null; then
    echo "Running with PaSh..."
    START_TIME=$(date +%s)
    for YEAR in "${YEARS[@]}"; do
        echo "Processing year $YEAR with PaSh..."
        "$SCRIPT_DIR/weather_pipeline.sh" "$YEAR" true
    done
    END_TIME=$(date +%s)
    ELAPSED_TIME=$((END_TIME - START_TIME))
    echo "Execution time for 10 years with PaSh: $ELAPSED_TIME seconds" >> "$LOG_FILE"
else
    echo "PaSh not installed. Skipping PaSh test."
    echo "PaSh not installed. Test skipped." >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"
echo "Performance testing completed. Results saved to $LOG_FILE"