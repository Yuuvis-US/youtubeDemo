from flask import Flask, render_template, request, send_file, g
import requests
import json


app = Flask(__name__)

header_dict = {}
param_dict = {}
base_url = 'https' + '://' + 'api.yuuvis.io'

header_dict['Content-Type'] = 'application/json'
header_dict['Ocp-Apim-Subscription-Key'] = 'Your_API_Key_Here'

session = requests.Session()

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
    print(query_dict)

    search_response = session.post(str(base_url+'/dms-core/objects/search'), data=json.dumps(query_dict), headers=header_dict)

    status = search_response.status_code
    print(status)
    if status == 200:
        search_response_json = search_response.json()
        print("search returned ", str(search_response_json['totalNumItems']), " objects")
        if 'objects' in search_response_json:
            matched_objects = search_response_json['objects']

            output_text = ''

            for match in matched_objects:
                match_properties = match['properties']
                object_id = match_properties['enaio:objectId']['value']
                created_at = match_properties['enaio:creationDate']['value']
                if 'Name' in match_properties:
                    name = match_properties['Name']['value']
                    result_line = str("\n objectId:\t" + object_id + "\n" + "created at:\t" + created_at + "\n" + "name: \t\t" + name + "\n")
                    output_text += result_line
                    print(result_line)

                else:
                    result_line = str("objectId:" + object_id + "\n" + "created at:\t" + created_at + "\n")
                    output_text += result_line
                    print(result_line)
            g.output_text = output_text
        else:
            g.output_text = "no objects matched the given query."
    else:
        g.output_text = "something went wrong."
    return render_template('index.html', response =  g.output_text)



@app.route("/", methods=['GET'])
def get_text_rendition():
    object_id = request.args.get('objectId','').strip()
    print("objectId: ", object_id)
    if len(object_id) > 0:
        session = requests.Session()
        rendition_response = session.get(str(base_url+'/dms-view/objects/'+object_id+'/contents/renditions/text'), headers=header_dict)
        if rendition_response.status_code != 404:
            rendition_response_content = rendition_response.content
            #print(rendition_response_content)
            #download response
            download_file = open("content.text", "wb")
            download_file.write(rendition_response_content)
            download_file.close()
            #return send_file(rendition_response_content, attachment_filename="")
            g.output_text = "successfully downloaded content of " + object_id + " as Text"
        else:
            g.output_text = "could not download Text content of " + object_id
        return render_template('index.html', response = g.output_text)
    else:
        if 'output_text' in g:
            return render_template('index.html', response = g.output_text)
        else:
            g.output_text = ""
            return render_template('index.html', response = g.output_text)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
