#!/bin/bash

# Script to install PaSh for parallelization

echo "Installing PaSh..."

# Create a temporary directory
TMP_DIR=$(mktemp -d)
cd "$TMP_DIR"

# Clone the PaSh repository
git clone https://github.com/binpash/pash.git
cd pash

# Run the installation script
./scripts/distro-deps.sh
./scripts/setup-pash.sh

echo "PaSh installation completed."
echo "You can now use PaSh to parallelize the weather pipeline."
echo "Run the weather pipeline with PaSh: ./weather_pipeline.sh 1980 true"