import requests
s = requests.session()
url = "https://h2oai.oktapreview.com/oauth2/auso8hjdmTjOgNDhK1d6/v1/token"
username = 'sergio.perez@h2o.ai'
password = 'FuE9zhYa20!'
payload='grant_type=password&username='+username+'&password='+password+'&scope=openid%20profile%20email'
headers = {
    'Accept': 'application/json',
    'Authorization': 'Basic MG9hb3pmNWJ2U2lWRDlFUDQxZDY6b2I2VUZIam1KRmF1UENzODJKSDJHcTJhTm9iR1V1Z2JNSHNSeDlfdA==',
    'Content-Type': 'application/x-www-form-urlencoded',
}
response = s.post(url, headers=headers, data=payload)
print('~~~~~~~~~~~~~~~~~~~~~~~~~')
print(response.json())
print('~~~~~~~~~~~~~~~~~~~~~~~~~')