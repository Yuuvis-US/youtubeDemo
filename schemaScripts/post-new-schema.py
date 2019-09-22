import requests

key = ""
baseUrl = 'https' + '://' + 'api.yuuvis.io'

headerDict = {}
headerDict['Ocp-Apim-Subscription-Key'] = key
headerDict['Content-Type'] = "application/xml"

response = requests.post(str(baseUrl+'/admin/schema'), data = open('slackSchema.xml', 'rb'), headers = headerDict)
print(response.status_code)
