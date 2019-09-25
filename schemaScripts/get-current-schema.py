import requests

key = ""
base_url = 'https' + '://' + 'api.yuuvis.io'

header_dict = {}
header_dict['Ocp-Apim-Subscription-Key'] = key


response = requests.get(str(base_url+'/admin/schema'), headers=header_dict)
print(response.status_code)

schema_file = open("currentSchema.xml", "w")
schema_file.write(response.text)
schema_file.close()
