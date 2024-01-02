import streamlit as st
from sdv.datasets.demo import download_demo
from sdv.metadata import MultiTableMetadata
from sdv.multi_table import HMASynthesizer
from sdv.evaluation.multi_table import run_diagnostic, evaluate_quality
import pandas as pd
import os

def create_synthetic_data(real_data, metadata):
    synthesizer = HMASynthesizer(metadata=metadata)
    synthesizer.fit(real_data)
    synthetic_data = synthesizer.sample(scale=1)
    return synthetic_data

st.title('Synthetic Data Generation Tool')

with st.sidebar:
    st.subheader('Data Options')
    uploaded_file = st.file_uploader("Upload a CSV File", type='csv')
    use_example = st.checkbox('Use Example Data')

if st.button('Start Synthesis'):
    if uploaded_file:
        file_name = uploaded_file.name
        file_name = file_name.split('.')[0]
        real_data = pd.read_csv(uploaded_file)
        real_data = {file_name: real_data}
        metadata = MultiTableMetadata()
        metadata.detect_from_dataframes(real_data)
        metadata.save_to_json('./data/metadata.json')
        metadata = MultiTableMetadata.load_from_json('./data/metadata.json')
        print('Metadata created successfully')
        st.write('Uploaded data processed.')
    elif use_example:

        real_data, metadata = download_demo(
             modality='multi_table',
            dataset_name='fake_hotels'
        )
        st.write('Using example data.')
    else:
        st.error('Please upload a data file or select "Use Example Data"')
        st.stop()

    # Generate Synthetic Data
    synthetic_data = create_synthetic_data(real_data, metadata)

    # Display Results
    table_name = list(synthetic_data.keys())[0]  # Get the first table name
    df_to_display = synthetic_data[table_name]  # Get the DataFrame

    # Display the DataFrame
    st.subheader(f'Synthetic Data for Table: {table_name}')
    st.write(df_to_display.head())
    # Diagnostic and Evaluation (Optional)
    st.subheader('Diagnostic and Evaluation')

    diagonistic = run_diagnostic(
        real_data=real_data,
        synthetic_data=synthetic_data,
        metadata=metadata,
    )
    quality_report = evaluate_quality(
        real_data=real_data,
        synthetic_data=synthetic_data,
        metadata=metadata,
    )
    st.write("Data Validation")
    st.write('Data Validation refers to the process of verifying whether the synthetic data possesses the same statistical properties as the real data. Note: The score is presented in an integer format, which is the percentage divided by 100.')
    properties = diagonistic.get_properties()
    st.write(properties)
    st.write('Quality Report')
    st.write('The quality report is a summary of the quality of the synthetic data. The quality of the synthetic data is measured by comparing the statistical properties of the synthetic data with the real data. The score is presented in an integer format, which is the percentage divided by 100.')
    st.write(quality_report.get_details("Column Shapes"))
