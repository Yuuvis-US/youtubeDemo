import requests

key = "Your_API_Key_Here"
base_url = 'https' + '://' + 'api.yuuvis.io'

header_dict = {}
header_dict['Ocp-Apim-Subscription-Key'] = key
header_dict['Content-Type'] = "application/xml"

response = requests.post(str(base_url+'/admin/schema'), data = open('slackSchema.xml', 'rb'), headers = header_dict)
print(response.status_code)
