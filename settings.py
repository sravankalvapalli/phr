
access_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJ1cm46b2lkOmZoaXIiLCJjbGllbnRfaWQiOiJiNTFjMzgxMS0wNDllLTRlNGItYmI4OS01YjY2Mzk0ODU3ODciLCJlcGljLmVjaSI6InVybjplcGljOk9wZW4uRXBpYy1jdXJyZW50IiwiZXBpYy5tZXRhZGF0YSI6Ik5fRFF6ck92M2NFeUtwWkxxbThhdEtHOUk1WXJURlQyOHNxTnpGa2pja2Z3ajlKNGpSX1RzYVZ1SjlSNUVtWGM0Z0trWUtaci14clRZQ2txZWdpOFc5MkJfSEpScEQ5dnoxNlJiOVBBOXNCZXBjLTZKMnJMZkVpUVd5YzF4SUMyIiwiZXBpYy50b2tlbnR5cGUiOiJhY2Nlc3MiLCJleHAiOjE3MDUzNTUzMDEsImlhdCI6MTcwNTM1MTcwMSwiaXNzIjoidXJuOm9pZDpmaGlyIiwianRpIjoiNDIxM2YyMWItZGVkNy00ZTdiLTkwZTktZDNhNzNhY2M1ZGFiIiwibmJmIjoxNzA1MzUxNzAxLCJzdWIiOiJlYjRHaWE3RnlpanRQbVhrcnRqUnBQdzMifQ.dniWIQRjOSdHNKSCsXnDHNuBMDXxrGgfbCXAQIO4Rlo_b6GEdlyKM1UcnP6rciz-RSZOtbLXnBfNPYWJdqV8gcmBSndzylBbOMc1Bun5RtXgHoA80M2z9TTqdMUm_OyyOJ7izeX5cQc3OqycDs1hW5LVItB4b0GpIq4GKSQJ81MjcNnVbkvavFIK1D6BcfnYm1JrYJHiILU8SyWHvyBekY8fAJiezx6Nn8xg3BlBtELjwSnvmCAQJ9qgMo5DLoNGHdUl8DiahESnf9w85Jx7yiepd67BJHoWTF8e1I_bviPBxcKJ4d4sdSF9ooAo3A8WPG6oMauCP2I2SZCKfL33Hw'

epic_fhir_headers = {
                        'Authorization': f'Bearer {access_token}',
                        'Content-Type': 'application/fhir+json', 
                        'Accept': 'application/fhir+json'
                    }

fhir_url = {
    "patient_url" : "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/Patient/"
}