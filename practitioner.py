import json
import requests
import settings
from typing import Any, Dict 
from googleapiclient import discovery

class Practitioner:
        def __init__(self) -> None:
            pass

        def get_general_practitioner(practitioner_id):
            access_token = settings.access_token
            
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/fhir+json',  # Adjust the content type if needed
                'Accept': 'application/fhir+json'
            }
            
            api_url = f"https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/Practitioner/eM5CWtq15N0WJeuCet5bJlQ3"
            result = requests.get(api_url, headers=headers)
    

            data = json.loads(result.text)

            print(data)

            Practitioner.create_practitioner_resource(data)

            return data
        
        def create_practitioner_resource(patient_body_input) -> Dict[str, Any]:
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
                .create(parent=fhir_store_name, type="Practitioner", body=patient_body)
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

        def update_resource(
            project_id: str,
            location: str,
            dataset_id: str,
            fhir_store_id: str,
            patient_body: any,
            resource_type: str,
            resource_id: str,
        ) -> Dict[str, Any]:
            """Updates the entire contents of a FHIR resource.

            Creates a new current version if the resource already exists, or creates
            a new resource with an initial version if no resource already exists with
            the provided ID.
           
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
            # project_id = 'my-project'
            # location = 'us-central1'
            # dataset_id = 'my-dataset'
            # fhir_store_id = 'my-fhir-store'
            # resource_type = 'Patient'
            # resource_id = 'b682d-0e-4843-a4a9-78c9ac64'
            fhir_store_parent = (
                f"projects/{project_id}/locations/{location}/datasets/{dataset_id}"
            )
            fhir_resource_path = f"{fhir_store_parent}/fhirStores/{fhir_store_id}/fhir/{resource_type}/{resource_id}"

            # The following sample body works with a Patient resource and isn't guaranteed
            # to work with other types of FHIR resources. If necessary,
            # supply a new body with data that corresponds to the resource you
            # are updating.
            # patient_body = {
            #     "resourceType": resource_type,
            #     "active": True,
            #     "id": resource_id,
            # }

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
            try:
                response = request.execute()
                return response
            except Exception as e:
                 print(f"exceptopn {e.args}")

            # print(
            #     f"Updated {resource_type} resource with ID {resource_id}:\n"
            #     f" {json.dumps(response, indent=2)}"
            # )

            # return response
        
        def create_general_practitoner(data):
            pass

    
if __name__ == "__main__":
    print('creating patient')
    Practitioner.get_general_practitioner('test')
    #Practitioner.get_general_practitioner('eM5CWtq15N0WJeuCet5bJlQ3')
#     Practitioner.create_practitioner_resource({
#     "resourceType": "Practitioner",
#     "id": "eM5CWtq15N0WJeuCet5bJlQ3",
#     "identifier": [
#         {
#             "use": "usual",
#             "type": {
#                 "text": "NPI"
#             },
#             "system": "http://hl7.org/fhir/sid/us-npi",
#             "value": "1627363736"
#         },
#         {
#             "use": "usual",
#             "type": {
#                 "text": "INTERNAL"
#             },
#             "system": "urn:oid:1.2.840.114350.1.13.0.1.7.2.697780",
#             "value": "  FAMMD"
#         },
#         {
#             "use": "usual",
#             "type": {
#                 "text": "EXTERNAL"
#             },
#             "system": "urn:oid:1.2.840.114350.1.13.0.1.7.2.697780",
#             "value": "FAMMD"
#         },
#         {
#             "use": "usual",
#             "type": {
#                 "text": "PROVID"
#             },
#             "system": "urn:oid:1.2.840.114350.1.13.0.1.7.5.737384.6",
#             "value": "1000"
#         },
#         {
#             "use": "usual",
#             "type": {
#                 "text": "EPIC"
#             },
#             "system": "urn:oid:1.2.840.114350.1.13.0.1.7.5.737384.7",
#             "value": "207Q00000X"
#         },
#         {
#             "use": "usual",
#             "type": {
#                 "text": "NPI"
#             },
#             "system": "urn:oid:1.2.840.114350.1.13.0.1.7.5.737384.60",
#             "value": "1627363736"
#         },
#         {
#             "use": "usual",
#             "type": {
#                 "text": "Epic"
#             },
#             "system": "urn:oid:1.2.840.114350.1.13.0.1.7.5.737384.63",
#             "value": "6011"
#         },
#         {
#             "use": "usual",
#             "type": {
#                 "text": "INTERNAL"
#             },
#             "system": "urn:oid:1.2.840.114350.1.13.0.1.7.2.836982",
#             "value": "   E1000"
#         },
#         {
#             "use": "usual",
#             "type": {
#                 "text": "EXTERNAL"
#             },
#             "system": "urn:oid:1.2.840.114350.1.13.0.1.7.2.836982",
#             "value": "E1000"
#         }
#     ],
#     "active": True,
#     "name": [
#         {
#             "use": "usual",
#             "text": "Physician",
#             "given": [
#                 "Physician"
#             ],
#             "_family": {
#                 "extension": [
#                     {
#                         "valueCode": "masked",
#                         "url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason"
#                     }
#                 ]
#             }
#         }
#     ],
#     "gender": "male",
    
# })
    print('created patient')