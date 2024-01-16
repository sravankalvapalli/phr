import json
from googleapiclient import discovery
from typing import Any, Dict 


class FhirHealtCareApi:
    def __init__(self) -> None:
        pass

    def execute_bundle(project_id, location, dataset_id, fhir_store_id, bundle):

        """Executes the operations in the given bundle.

        See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/fhir
        before running the sample."""
        # Imports Python's built-in "os" module
        import os

        # Imports the google.auth.transport.requests transport
        from google.auth.transport import requests

        # Imports a module to allow authentication using a service account
        from google.oauth2 import service_account

        # Gets credentials from the environment.
        credentials = service_account.Credentials.from_service_account_file(
            "c:\\Users\\srava\Projects\\application_default_credentials.json"
        )
        scoped_credentials = credentials.with_scopes(
            ["https://www.googleapis.com/auth/cloud-platform"]
        )
        # Creates a requests Session object with the credentials.
        session = requests.AuthorizedSession(scoped_credentials)

        # URL to the Cloud Healthcare API endpoint and version
        base_url = "https://healthcare.googleapis.com/v1"

        url = f"{base_url}/projects/{project_id}/locations/{location}"

        resource_path = "{}/datasets/{}/fhirStores/{}/fhir".format(
            url, dataset_id, fhir_store_id
        )

        headers = {"Content-Type": "application/fhir+json;charset=utf-8"}

        # with open(bundle) as bundle_file:
        #     bundle_file_content = bundle_file.read()

        bundle_file_content = json.dumps(bundle)
        
        try:
            response = session.post(resource_path, headers=headers, data=bundle_file_content)
            if response.status_code != 200:
                print(f'res: {response.text}')
                raise Exception(response.text)
            resource = response.json()
            print(json.dumps(resource, indent=2))
            print('created bundle')
            return resource
        except Exception as e:
            # print(f"Error making GET request: {e.args}")
             print(f"Error making GET request: {e.args}")
    
    def update_resource(resource_id: str,patient_body: any) -> Dict[str, Any]:
        """Updates the entire contents of a FHIR resource.

        Creates a new current version if the resource already exists, or creates
        a new resource with an initial version if no resource already exists with
        the provided ID.

    
        Args:
        project_id: The project ID or project number of the Cloud project you want
            to use.
        location: The name of the parent dataset's location.
        dataset_id: The name of the parent dataset.
        fhir_store_id: The name of the FHIR store.
        resource_type: The type of the FHIR resource.
        resource_id: The "logical id" of the resource. The ID is assigned by the
            server.

        Returns:
        A dict representing the updated FHIR resource.
        """
        # Imports the Google API Discovery Service.
        from googleapiclient import discovery

        api_version = "v1"
        service_name = "healthcare"

        # Returns an authorized API client by discovering the Healthcare API
        # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
        client = discovery.build(service_name, api_version)

        # TODO(developer): Uncomment these lines and replace with your values.
        project_id = 'eastern-art-408003' # 'constant-cubist-405316'
        location = 'us-central1'
        dataset_id = 'pehrdataset' # 'persondataset_1'
        fhir_store_id = 'pehrfiresore1' # 'my-fhir-store-1'
        resource_type = 'Patient'
        resource_id = 'b682d-0e-4843-a4a9-78c9ac64'
        fhir_store_parent = (
            f"projects/{project_id}/locations/{location}/datasets/{dataset_id}"
        )
        fhir_resource_path = f"{fhir_store_parent}/fhirStores/{fhir_store_id}/fhir/{resource_type}/{resource_id}"

        # The following sample body works with a Patient resource and isn't guaranteed
        # to work with other types of FHIR resources. If necessary,
        # supply a new body with data that corresponds to the resource you
        # are updating.
        patient_body = {
            "resourceType": resource_type,
            "active": False,
            "id": resource_id,
            "name": [{"use": "official", "family": "Smith", "given": ["Darcy"]}],
            "gender": "female",
            "birthDate": "1970-01-01",
        }

        request = (
            client.projects()
            .locations()
            .datasets()
            .fhirStores()
            .fhir()
            .update(name=fhir_resource_path, body=patient_body)
        )
        # Sets required application/fhir+json header on the googleapiclient.http.HttpRequest.
        request.headers["content-type"] = "application/fhir+json;charset=utf-8"
        response = request.execute()

        print(
            f"Updated {resource_type} resource with ID {resource_id}:\n"
            f" {json.dumps(response, indent=2)}"
        )

        return response

    def create_patient_resource(patient_body_input) -> Dict[str, Any]:
        # """Creates a new Patient resource in a FHIR store.


        # Args:
        #   project_id: The project ID or project number of the Cloud project you want
        #     to use.
        #   location: The name of the parent dataset's location.
        #   dataset_id: The name of the parent dataset.
        #   fhir_store_id: The name of the FHIR store that holds the Patient resource.

        # Returns:
        #   A dict representing the created Patient resource.
        # """


        api_version = "v1"
        service_name = "healthcare"


        
        # credentials = service_account.Credentials.from_service_account_file(
        #     filename=os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
        #     scopes=["https://www.googleapis.com/auth/cloud-platform"],
        # )

        # Returns an authorized API client by discovering the Healthcare API
        # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
        client = discovery.build(service_name, api_version)

        # TODO(developer): Uncomment these lines and replace with your values.
        # 'constant-cubist-405316', 'us-central1', 'persondataset_1', 'my-fhir-store-1'
        project_id = 'eastern-art-408003' # 'constant-cubist-405316'
        location = 'us-central1'
        dataset_id = 'pehrdataset' # 'persondataset_1'
        fhir_store_id = 'pehrfiresore1' # 'phrfhirstore'
        fhir_store_parent = (
            f"projects/{project_id}/locations/{location}/datasets/{dataset_id}"
        )
        fhir_store_name = f"{fhir_store_parent}/fhirStores/{fhir_store_id}"

        patient_body = patient_body_input   

        # patient_body = {
        # "name": [{"use": "official", "family": "Smith", "given": ["Darcy"]}],
        # "gender": "female",
        # "birthDate": "1970-01-01",
        # "resourceType": "Patient",
        # }
        
        request = (
            client.projects()
            .locations()
            .datasets()
            .fhirStores()
            .fhir()
            .create(parent=fhir_store_name, type="Condition", body=patient_body)
        )
        
        # Sets required application/fhir+json header on the googleapiclient.http.HttpRequest.
        request.headers["content-type"] = "application/fhir+json;charset=utf-8"

        try:
            # request.headers["Accept"] = "application/fhir+json;charset=utf-8"
            response = request.execute()
            print(f"Created Patient resource with ID {response['id']}")
            return response
        except Exception as e:
            print(f"Unexpected Error: {e.args}")

    
