import requests

key = ""
baseUrl = 'https' + '://' + 'api.yuuvis.io'

headerDict = {}
headerDict['Ocp-Apim-Subscription-Key'] = key


response = requests.get(str(baseUrl+'/admin/schema'), headers=headerDict)
print(response.status_code)

schemaFile = open("currentSchema.xml", "w")
schemaFile.write(response.text)
schemaFile.close()
