from flask import Flask, render_template, request
import requests
import json


app = Flask(__name__)

headerDict = {}
paramDict = {}
baseUrl = 'https' + '://' + 'api.yuuvis.io'

headerDict['Content-Type'] = 'application/json'
headerDict['Ocp-Apim-Subscription-Key'] = '47daefb18a974163a9fbc388d36a97ae'

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
    
    print(search_query,max_count,skip_count)

    return render_template('index.html', search_query=search_query, max_count=max_count, skip_count=skip_count)
    

# function that make the search call
@app.route("/")
def SearchCall():
    search_query, max_count, skip_count = getvalue()
   
    QueryDict = {
    "query": {
      "statement": search_query,
      "skipCount": skip_count,
      "maxItems": max_count
    }
  }
    print(QueryDict)

    response = session.post(str(baseUrl+'/dms/objects/search'), data=QueryDict, headers=headerDict)
    print(response.json())
    return render_template('index.html', response = response.json())


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
