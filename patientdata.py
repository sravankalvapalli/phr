import requests
import json


class PehrDataClient:
    def __init__(self) -> None:
        pass

    
    def get_patient_fhir_data(name, access_token, fhirId):
        access_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJ1cm46b2lkOmZoaXIiLCJjbGllbnRfaWQiOiJiNTFjMzgxMS0wNDllLTRlNGItYmI4OS01YjY2Mzk0ODU3ODciLCJlcGljLmVjaSI6InVybjplcGljOk9wZW4uRXBpYy1jdXJyZW50IiwiZXBpYy5tZXRhZGF0YSI6Ikx0R1kycHZSSVFiRUVnWFdyblFiejNSVVNPZkgzbXJ5QWhUQUJrN1VOQkxJNWtTUkxwd1dUSU9nY0lUMWJuYkVXVUNSZ1FVNUZzTUxtQVFlLUJvR0NTTTVIU1Jacko3dEFfeU1lcFVvcEhXV1p3SEdVZlZ5NmJCVFFUYmp6Q2NTIiwiZXBpYy50b2tlbnR5cGUiOiJhY2Nlc3MiLCJleHAiOjE3MDQzOTEwNjksImlhdCI6MTcwNDM4NzQ2OSwiaXNzIjoidXJuOm9pZDpmaGlyIiwianRpIjoiODU4ODI1ZjEtZTE1ZC00ZDdjLWEyNGEtN2IxNjY5ZGE4MmVhIiwibmJmIjoxNzA0Mzg3NDY5LCJzdWIiOiJlYjRHaWE3RnlpanRQbVhrcnRqUnBQdzMifQ.jSgu2kdQISvQJHbLeNipd8KlKUNihZDbINFnkxzm43SqbMvnITEBCnmMol-cjr8829UnZcXBsvjwB-8StpmdAO_HVUeH3u_uhgiEgWubhMkixSrrO5tifU7LUXuzLFIKTPOetljLRJid8kUTU4KKXB97cXW5uwnq7b9ajV4gkkj88Zz8HzGMoIVW1XJQ2VmTQvJHGfLj86GaSsOMVKjE-lMXwg7T7RUWwyNZu48z-YPIaZXIVZUfQ1Wg9lVuh4Fva9Pkih7CK8cYvLiouu9Dqyapru09HxZ6AJuddckYIB2zGonJA9E-bbzrAX7VF8BQ6ONMkF1wqVbmjxb_TGB23w'
         
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/fhir+json',  # Adjust the content type if needed
            'Accept': 'application/fhir+json'
        }
        
        api_url = f"https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/Patient/erXuFYUfucBZaryVksYEcMg3"
        result = requests.get(api_url, headers=headers)



        data = json.loads(result.text)

        # data["fhirId"] = fhirId

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
        print( PehrDataClient.get_patient_fhir_data('test', 'test', 'test')  )
    except requests.exceptions.RequestException as e:
        print(f"Error making GET request: {e}")