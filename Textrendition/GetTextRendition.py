import requests
import json

headerDict = {}
paramDict = {}
baseUrl = 'https' + '://' + 'api.yuuvis.io'



headerDict['Ocp-Apim-Subscription-Key'] = 'your_API_Key_Here'



session = requests.Session()

response = session.get(str(baseUrl+'/dms/objects/f626d81b-1c27-4c36-91de-f65ed254eaf3/contents/renditions/text'), headers=headerDict)
print(response.content)

