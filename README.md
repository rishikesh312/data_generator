# Synthetic Data Generation Tool

## Overview
This tool is designed to generate synthetic data using Streamlit and the Synthetic Data Vault (SDV) library. It allows users to either upload their own data or use example data to create a synthetic version that maintains the statistical properties of the original data.

## Features
- Upload your own CSV data.
- Option to use example data.
- Generate synthetic data that mimics the real data.
- Data validation and quality evaluation.

## Installation

### Prerequisites
- Python 3.6 or higher

### Setup
1. Clone the repository:
   ```
   git clone https://github.com/rishikesh312/data_generator.git
   ```
2. Navigate to the project directory:
   ```
   cd data_generator
   ```

### Install Dependencies
Install the required packages using:
```
pip install -r requirements.txt
```

## Usage
To run the application locally, execute the following command in the project directory:
```
streamlit run app.py
```
Navigate to the provided URL to interact with the tool.

### Uploading Data
- Use the sidebar to upload your CSV file.
- Optionally, select "Use Example Data" if you do not have a dataset.

### Generating Synthetic Data
- Click 'Start Synthesis' to begin the data generation process.
- The synthetic data, along with diagnostic and evaluation reports, will be displayed.
