import streamlit as st 
from sdv.datasets.demo import download_demo  
from sdv.metadata import MultiTableMetadata  
from sdv.multi_table import HMASynthesizer  
from sdv.evaluation.multi_table import run_diagnostic, evaluate_quality  
import pandas as pd 
import os  

def create_synthetic_data(real_data, metadata):
    # This function takes real data and its metadata to generate synthetic data using the HMASynthesizer.
    synthesizer = HMASynthesizer(metadata=metadata)  # Initialize the synthesizer with the provided metadata
    synthesizer.fit(real_data)  # Fit the synthesizer to the real data
    synthetic_data = synthesizer.sample(scale=1)  # Generate synthetic data
    return synthetic_data  # Return the synthetic data

# Setting the title of the Streamlit app
st.title('Synthetic Data Generation Tool')

# Streamlit sidebar for data upload and example data selection
with st.sidebar:
    st.subheader('Data Options')
    uploaded_file = st.file_uploader("Upload a CSV File", type='csv')  # File uploader for CSV files
    use_example = st.checkbox('Use Example Data')  # Checkbox to use example data instead of uploading

# Button to start the data synthesis process
if st.button('Start Synthesis'):
    if uploaded_file:  # If a file is uploaded
        file_name = uploaded_file.name.split('.')[0]  # Extract the file name without extension
        real_data = pd.read_csv(uploaded_file)  # Read the uploaded CSV file into a pandas DataFrame
        real_data = {file_name: real_data}  # Create a dictionary with the table name as the key
        metadata = MultiTableMetadata()  # Initialize an empty MultiTableMetadata object
        metadata.detect_from_dataframes(real_data)  # Automatically detect metadata from the DataFrame
        metadata.save_to_json('metadata.json')  # Save the detected metadata to a JSON file
        metadata = MultiTableMetadata.load_from_json('metadata.json')  # Reload the metadata from the JSON file
        st.write('Uploaded data processed.')  # Notify the user that the upload process is complete
    elif use_example:  # If the user opts to use example data
        real_data, metadata = download_demo(
            modality='multi_table',
            dataset_name='fake_hotels'
        )  # Download example data and metadata
        st.write('Using example data.')  # Notify the user that example data is being used
    else:  # If neither a file is uploaded nor example data is selected
        st.error('Please upload a data file or select "Use Example Data"')
        st.stop()  # Stop execution

    synthetic_data = create_synthetic_data(real_data, metadata)  # Generate synthetic data

    table_name = list(synthetic_data.keys())[0]  # Get the name of the first table in the synthetic data
    df_to_display = synthetic_data[table_name]  # Extract the DataFrame from the synthetic data

    st.subheader(f'Synthetic Data for Table: {table_name}')
    st.write(df_to_display.head())  

    st.subheader('Diagnostic and Evaluation')  # Section for diagnostics and evaluation

    # Run diagnostics to compare real and synthetic data
    diagnostic = run_diagnostic(
        real_data=real_data,
        synthetic_data=synthetic_data,
        metadata=metadata,
    )

    # Evaluate the quality of the synthetic data
    quality_report = evaluate_quality(
        real_data=real_data,
        synthetic_data=synthetic_data,
        metadata=metadata,
    )

    # Displaying information about data validation and quality report
    st.write("Data Validation")
    st.write('Data Validation refers to the process of verifying whether the synthetic data possesses the same statistical properties as the real data. Note: The score is presented in an integer format, which is the percentage divided by 100.')
    properties = diagnostic.get_properties()  # Get diagnostic properties
    st.write(properties)  # Display diagnostic properties

    st.write('Quality Report')
    st.write('The quality report is a summary of the quality of the synthetic data. The quality of the synthetic data is measured by comparing the statistical properties of the synthetic data with the real data. The score is presented in an integer format, which is the percentage divided by 100.')
    st.write(quality_report.get_details("Column Shapes"))  # Display quality report details

    os.remove('metadata.json')  # Clean up by removing the metadata JSON file
