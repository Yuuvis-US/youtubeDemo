from flask import Flask, render_template, request, send_file
import requests
import json


app = Flask(__name__)

header_dict = {}
param_dict = {}
base_url = 'https' + '://' + 'api.yuuvis.io'

header_dict['Content-Type'] = 'application/json'
header_dict['Ocp-Apim-Subscription-Key'] = '22f06d56c0224827989540a84ba46056'

session = requests.Session()

output_text = ""

objectId = ""

# function that starts the html page
@app.route("/getRendition")
def main():
    return render_template ('index.html')

# function that pulls from the html file
@app.route("/", methods=['POST'])
def getvalue():
    search_query = request.form.get('search_query')
    max_count = request.form.get('max_count')
    skip_count = request.form.get('skip_count')

    # print(search_query,max_count,skip_count)

    query_dict = {
        "query": {
          "statement": search_query,
          "skipCount": skip_count,
          "maxItems": max_count
        }
    }
    # print(query_dict)

    import_response = session.post(str(base_url+'/dms/objects/search'), data=json.dumps(query_dict), headers=header_dict)

    import_response_json = import_response.json()
    matched_objects = import_response_json['objects']

    output_text = ""

    for match in matched_objects:
        objectId = 	match['properties']['enaio:objectId']['value']
        createdAt = match['properties']['enaio:creationDate']['value']
        resultLine = objectId + "\n" + "\t created at:" + createdAt +"\n"
        print(resultLine)
        output_text += resultLine

    return render_template('index.html', response = output_text)




@app.route("/", methods=['GET'])
def get_text_rendition():
    objectId = request.args.get('objectId','')
    print("objectId: ", objectId)

    session = requests.Session()
    rendition_response = session.get(str(base_url+'/dms/objects/{objectId}/contents/renditions/text'), headers=header_dict)
    rendition_response_content = rendition_response.content
    print(rendition_response_content)

    return render_template('index.html', response = rendition_response_content)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
