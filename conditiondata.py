import requests
import json
import settings


class Conditiondata:
    def __init__(self) -> None:
        pass

    def get_patient_condition_fhir_data(name, access_token, fhirPatientId):
        access_token = settings.access_token
         
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/fhir+json',  # Adjust the content type if needed
            'Accept': 'application/fhir+json'
        }
        
        api_url = f"https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/condition?patient=erXuFYUfucBZaryVksYEcMg3"
        result = requests.get(api_url, headers=headers)
 

        data = json.loads(result.text)

        # selected_encounters = [item["resource"]["subject"]["reference"] for item in data["entry"]]

        selected_encounters = [item["resource"]["encounter"]["reference"] for item in data["entry"] if "resource" in item and "encounter" in item["resource"]]
       

        print(set( selected_encounters))

        for item in selected_encounters:
            encounter_id = item.replace("Encounter/","")
            print(encounter_id)

        for item in data["entry"]:
            if item["resource"]["resourceType"] == "Condition":
                item["resource"]["subject"]["reference"] = f'Patient/f{fhirPatientId}' 
                # print(item["resource"])
                # print('Call to Create FHIR Resource')

        # data["fhirId"] = fhirId

        # keys_to_remove = ['extension', 'identifier', 'generalPractitioner', 'managingOrganization']

        # for key in keys_to_remove:
        #     if key in data:
        #         data.pop(key)


        # # Specify the nested property to remove
        # property_to_remove = 'rank'

        # # Check if the top-level property exists
        # if property_to_remove in data['telecom']:
        #     # Check if the nested property exists
        #     if property_to_remove in data['telecom'][property_to_remove]:
        #         # Remove the nested property
        #         data['telecom'][property_to_remove].pop(property_to_remove)

        # Convert the modified data back to JSON
        updated_json_data = json.dumps(data)

        return json.loads( updated_json_data )
    
if __name__ == "__main__":
    print('get patinet condition')
    Conditiondata.get_patient_condition_fhir_data('test','test','51f1e6f-73e7-4c0d-8e8e-07383e3bd9ed')
    print('end patient condition')

