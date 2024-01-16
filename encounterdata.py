import requests
import json
import settings
from typing import Any, Dict 
from googleapiclient import discovery



class EncounterData:
    def __init__(self, livDataClient) -> None:
        self.livDataClient = livDataClient

    def get_encounter_by_patient_id(self, fhirPatientId):
            api_url = f"https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/Encounter?patient=erXuFYUfucBZaryVksYEcMg3"
           
            data = self.livDataClient.get(api_url)

            if(data == ""):
                return
            
            entries = []

            for item in data["entry"]:
                if item["resource"]["resourceType"] == "Encounter":    
                    resournce_entry = EncounterData.transform_subject('432c87fa-9e32-4589-8e16-6734da32bbc5',item["resource"])
                    resournce_entry =  EncounterData.drop_location('51f1e6f-73e7-4c0d-8e8e-07383e3bd9ed', resournce_entry)
                    resournce_entry = EncounterData.transform_individual_practitioner('16229604-8303-4aa1-bb50-15c87367ed7c', resournce_entry)
                    resournce_entry = EncounterData.drop_partof_encounter('51f1e6f-73e7-4c0d-8e8e-07383e3bd9ed', resournce_entry)
                    entry = { "resource" : resournce_entry,  "request": { "method": "POST", "url": "Encounter" }}                
                    entries.append(entry) 

            bundle_encounter_resource = {
                 "resourceType": "Bundle",
                 "type": "transaction",
                 "entry": entries
            }

            #print(entries[0])
            #print(bundle_encounter_resource)
            EncounterData.execute_bundle('eastern-art-408003','us-central1', 'pehrdataset', 'pehrfiresore1',bundle_encounter_resource)
            return data
    
    def transform_subject(patient_id, data):
         if "subject" in data:
              data["subject"]["reference"] = f"Patient/{patient_id}"
        
         return data
    
    def drop_partof_encounter(encounter_id, data):
         if "partOf" in data:
              data.pop("partOf", None)  
        
         return data
    
    def drop_location(location_id, data):
         data.pop("location", None)    

         return data

    def transform_individual_practitioner(practitioner_id, data):
         if "participant" in data:
            for item in data["participant"]:
                item["individual"]["reference"] = f"Practitioner/{practitioner_id}"

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

        

        # print(f"Executed bundle from file: {bundle}")
        # print(json.dumps(resource, indent=2))

     

if __name__ == "__main__":
    print('get patinet condition')
    from livdatahttpclient import LivDataClient

    livDataClient = LivDataClient()

    encounterData = EncounterData(livDataClient)

    encounterData.get_encounter_by_patient_id('51f1e6f-73e7-4c0d-8e8e-07383e3bd9ed')
#     EncounterData.execute_bundle('eastern-art-408003','us-central1', 'pehrdataset', 'pehrfiresore1',
#                                      {
# 	"resourceType": "Bundle",
# 	"type": "transaction",
# 	#"total": 1,
# 	"link": [
# 		{
# 			"relation": "self",
# 			"url": "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/Encounter?patient=432c87fa-9e32-4589-8e16-6734da32bbc5"
# 		}
# 	],
# 	"entry": [
# 		{
			
# 			"fullUrl": "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/Encounter/eGmO0h.1.UQQrExl4bfM7OQ3",
# 			"resource": {
# 				"resourceType": "Encounter",
# 				"id": "eGmO0h.1.UQQrExl4bfM7OQ3",
# 				"identifier": [
# 					{
# 						"use": "usual",
# 						"system": "urn:oid:1.2.840.114350.1.13.0.1.7.3.698084.8",
# 						"value": "29545"
# 					}
# 				],
# 				"status": "unknown",
# 				"class": {
# 					"system": "urn:oid:1.2.840.114350.1.72.1.7.7.10.696784.13260",
# 					"code": "10",
# 					"display": "Surgery Log"
# 				},
# 				"type": [
# 					{
# 						"coding": [
# 							{
# 								"system": "urn:oid:1.2.840.114350.1.13.0.1.7.10.698084.30",
# 								"code": "51",
# 								"display": "Surgery"
# 							}
# 						],
# 						"text": "Surgery"
# 					}
# 				],
# 				"subject": {
# 					"reference": "Patient/432c87fa-9e32-4589-8e16-6734da32bbc5",
# 					"display": "Lopez, Camila Maria"
# 				},
# 				"participant": [
# 					{
# 						"individual": {
# 							"reference": "Practitioner/5601851b-afe9-4c2f-b819-5e8a0aa276b3",
# 							"type": "Practitioner",
# 							"display": "Physician"
# 						}
# 					}
# 				],
# 				"period": {
# 					"start": "2023-06-06T16:20:00Z",
# 					"end": "2023-06-06T17:35:00Z"
# 				},
# 				# "location": [
# 				# 	{
# 				# 		"location": {
# 				# 			"reference": "Location/efR3SIdpRKF9BFBM5qakt9F5X1mWxjiAGu2hNTKbqOdI3",
# 				# 			"display": "EMH Operating Room"
# 				# 		}
# 				# 	}
# 				# ],
# 				# "partOf": {
# 				# 	"reference": "Encounter/eoK8nLRcEypNjtns4dgnF3Q3",
# 				# 	"identifier": {
# 				# 		"use": "usual",
# 				# 		"system": "urn:oid:1.2.840.114350.1.13.0.1.7.3.698084.8",
# 				# 		"value": "29547"
# 				# 	},
# 				# 	"display": "Emergency Department"
# 				# }
# 			},
# 			"request": {
# 				"method": "POST",
#                  "url": "Encounter"
# 			}
# 		},
# 		{
#             "link": [
#                 {
#                     "relation": "self",
#                     "url": "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/Encounter/eMT95RPaM-HxLc3NeIA5qlQ3"
#                 }
#             ],
#             "fullUrl": "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/Encounter/eMT95RPaM-HxLc3NeIA5qlQ3",
#             "resource": {
#                 "resourceType": "Encounter",
#                 "id": "eMT95RPaM-HxLc3NeIA5qlQ3",
#                 "identifier": [
#                     {
#                         "use": "usual",
#                         "system": "urn:oid:1.2.840.114350.1.13.0.1.7.3.698084.8",
#                         "value": "29544"
#                     }
#                 ],
#                 "status": "in-progress",
#                 "class": {
#                     "system": "urn:oid:1.2.840.114350.1.72.1.7.7.10.696784.13260",
#                     "code": "13",
#                     "display": "Support OP Encounter"
#                 },
#                 "type": [
#                     {
#                         "coding": [
#                             {
#                                 "system": "urn:oid:1.2.840.114350.1.13.0.1.7.10.698084.30",
#                                 "code": "101",
#                                 "display": "Office Visit"
#                             }
#                         ],
#                         "text": "Office Visit"
#                     }
#                 ],
#                 "subject": {
#                     "reference": "Patient/432c87fa-9e32-4589-8e16-6734da32bbc5",
#                     "display": "Lopez, Camila Maria"
#                 },
#                 "participant": [
#                     {
#                         "individual": {
#                             "reference": "Practitioner/5601851b-afe9-4c2f-b819-5e8a0aa276b3",
#                             "type": "Practitioner",
#                             "display": "Physician"
#                         }
#                     }
#                 ],
#                 "period": {
#                     "start": "2023-06-02",
#                     "end": "2023-06-02"
#                 },
#                 # "location": [
#                 #     {
#                 #         "location": {
#                 #             "reference": "Location/e4W4rmGe9QzuGm2Dy4NBqVc0KDe6yGld6HW95UuN-Qd03",
#                 #             "display": "EMC Family Medicine"
#                 #         }
#                 #     }
#                 # ]
#             },
#            	"request": {
# 				"method": "POST",
#                  "url": "Encounter"
# 			}
#         },
        
#         ]
# }
# )
    
    
    print('end patient condition')

