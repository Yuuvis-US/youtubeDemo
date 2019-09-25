from flask import Flask, render_template, request
import requests
import json


app = Flask(__name__)

headerDict = {}
paramDict = {}
baseUrl = 'https' + '://' + 'api.yuuvis.io'

headerDict['Content-Type'] = 'application/json'
headerDict['Ocp-Apim-Subscription-Key'] = 'Your_API_Key_Here'

session = requests.Session()

# function that starts the html page
@app.route("/")
def main():
    return render_template ('index.html')

# function that pulls from the html file
@app.route("/", methods=['POST'])
def getvalue():
    search_query = request.form.get('search_query')
    max_count = request.form.get('max_count')
    skip_count = request.form.get('skip_count')

    # print(search_query,max_count,skip_count)

    QueryDict = {
        "query": {
          "statement": search_query,
          "skipCount": skip_count,
          "maxItems": max_count
        }
      }
    # print(QueryDict)

    response = session.post(str(baseUrl+'/dms/objects/search'), data=json.dumps(QueryDict), headers=headerDict)
    # print(response.content)


    return render_template('index.html', response = response.content)
    
    


@app.route("/", methods=['GET'])
def getNewValue():
      
      headerDict = {}
      paramDict = {}
      baseUrl = 'https' + '://' + 'api.yuuvis.io'
      
      headerDict['Ocp-Apim-Subscription-Key'] = 'Your_API_Key_Here'
      
      objectId = request.form('objectId')
      print("something", objectId)
      session = requests.Session()
      response = session.get(str(baseUrl+'/dms/objects/{objectId}/contents/renditions/text'), headers=headerDict)
      print(response.content)
      print(response)

      return render_template('index.html', response = response.content)
 
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
    

