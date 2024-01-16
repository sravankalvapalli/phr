import requests
import json
import settings

class PatientData:
    def __init__(self, livDataClient) -> None:
        self.livDataClient = livDataClient

    
    def get_patient_fhir_data(self, name, access_token, fhirId):
               
        api_url = settings.fhir_url["patient_url"] # f"https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/Patient/erXuFYUfucBZaryVksYEcMg3"

        data = self.livDataClient.get(f"{api_url}/{fhirId}")

        if(data == ""):
            return

        keys_to_remove = ['extension', 'identifier', 'generalPractitioner', 'managingOrganization']

        for key in keys_to_remove:
            if key in data:
                data.pop(key)


        # Specify the nested property to remove
        property_to_remove = 'rank'

        # Check if the top-level property exists
        if property_to_remove in data['telecom']:
            # Check if the nested property exists
            if property_to_remove in data['telecom'][property_to_remove]:
                # Remove the nested property
                data['telecom'][property_to_remove].pop(property_to_remove)

        # Convert the modified data back to JSON
        updated_json_data = json.dumps(data)

        return json.loads( updated_json_data)


    
if __name__ == "__main__":
    print("test from fhirdataflow")
    # run data pipeline
    try:
        from livdatahttpclient import LivDataClient
        livDataClient = LivDataClient()
        patientData = PatientData(livDataClient)
        print( patientData.get_patient_fhir_data('test', 'test', 'erXuFYUfucBZaryVksYEcMg3') )
        # print( PehrDataClient.get_patient_fhir_data('test', 'test', 'test', 'test')  )
    except requests.exceptions.RequestException as e:
        print(f"Error making GET request: {e}")