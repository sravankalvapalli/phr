import os
import json
import logging
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import requests

from google.oauth2 import service_account
# Imports the Google API Discovery Service.
from googleapiclient import discovery

from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam import DoFn

# Imports the types Dict and Any for runtime type hints.
from typing import Any, Dict  # noqa: E402

from patientdata import PehrDataClient
from fhirpatientresource import PatientResource

class GetDataForPatients(beam.DoFn):
    def process(self, element):
        # Process each row and make a REST API call
        processed_row = {
            'token': element['AccessToken'],  
            'name': element['FirstName'],  
            'fhirid': element['MyChartId'],  
        }

        # Make REST API call
        response = PehrDataClient.get_patient_fhir_data(processed_row['name'].upper(),processed_row['token'],processed_row['fhirid'])


        # Yield the processed row if needed
        yield response

class CreateUpdatePatientFHIRDetails(DoFn):

    def process(self, element):
        # element.pop('fhirId')  
        PatientResource.create_patient_resource(element)
class FhirDataFlow:
    def __init__(self) -> None:
        pass


    def run_pipeline():
        # Set up pipeline options
        pipeline_options = PipelineOptions([
            '--runner=DirectRunner',  # Use the DirectRunner for local execution DataflowRunner
            '--project=eastern-art-408003',
            '--region=us-central1',
            '--temp_location=gs://pehr_tempus/temp/',
            '--staging_location=gs://pehr_tempus/staging/'
        ])

        # Create the pipeline
        with beam.Pipeline(options=pipeline_options) as p:
            
            # Read data from BigQuery
            data = (
                p
                | 'Read from BigQuery' >> beam.io.ReadFromBigQuery(
                    query='SELECT * FROM [eastern-art-408003.PEHR.patient]'
                )
            )
            
            # Secured Rest API Call
            processed_data = data | 'Process Data' >> beam.ParDo(GetDataForPatients())

            # Create or Update patient FHIR resource
            processed_data | 'FHIRWriteData' >>  beam.ParDo(CreateUpdatePatientFHIRDetails())


if __name__ == "__main__":
    print("Started pr fhirdataflow")
    # run data pipeline
    try:
        FhirDataFlow.run_pipeline()        
    except requests.exceptions.RequestException as e:
        print(f"Error making GET request: {e}")

    print("test from fhirdataflow")