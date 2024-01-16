import json
import requests
import settings

class LivDataClient:

    def __init__(self) -> None:
        pass

    def get(self, api_url):         
            result = requests.get(api_url, headers=settings.epic_fhir_headers)   
            return json.loads(result.text)
    
if __name__ == "__main__":
    print('getting data')
    livDataClient = LivDataClient()
    result = livDataClient.get("https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/Encounter?patient=erXuFYUfucBZaryVksYEcMg3")
    print(result)
    print('end getting data')
