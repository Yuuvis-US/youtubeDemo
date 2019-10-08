import os
from os.path import isfile, isdir, join, basename
import json
from datetime import datetime, timedelta, timezone
import requests

key = "Your_API_Key_Here"
header_dict = {}

header_dict['Ocp-Apim-Subscription-Key'] = key


#establish export file structure
slack_export_root_folder_path = "./input/" + os.listdir("./input/").pop()+"/"
slack_export_root_files = os.listdir(slack_export_root_folder_path)

meta_files = [f for f in slack_export_root_files if isfile(join(slack_export_root_folder_path, f))]
channel_dirs = [f for f in slack_export_root_files if isdir(join(slack_export_root_folder_path, f))]

print(slack_export_root_folder_path)
print(slack_export_root_files)
print(channel_dirs)

#retrieve file paths for each channel
input_json_file_paths = {}
for channel_dir in channel_dirs:
    input_json_file_paths[channel_dir] = []
    channel_dirPath = join(slack_export_root_folder_path, channel_dir)
    for input_file_name in os.listdir(channel_dirPath):
        input_json_file_paths[channel_dir].append(join(channel_dirPath, input_file_name))

#print(input_json_file_paths)



epoch = datetime(1601, 1, 1)

class Message:
    def __init__(self, author, text, created_at, channel, attachments):
        self.author = author
        self.text = text
        self.created_at = created_at
        self.channel = channel
        self.attachments = attachments
class Attachment:
    def __init__(self, name, type, url):
        self.name = name
        self.type = type
        self.url = url


for channel_dir in channel_dirs:
    messages = []
    print('gathering messages for channel '+channel_dir)
    for chat_log_file in input_json_file_paths[channel_dir]:
        date = basename(chat_log_file).split('.')[0]

        with open(chat_log_file, 'r') as inputFile:

            test_slack_chat_log = json.load(inputFile)
            for x in test_slack_chat_log:
                timestamp = (epoch + timedelta(microseconds = float(x['ts'])))
                time = timestamp.time().strftime("%H:%M:%S")

                created_at = date+"T"+time

                message = Message(x['user'], x['text'], created_at, channel_dir, [])
                if 'files' in x:
                    file_attachments = []
                    for file in x['files']:
                        file_attachments.append(Attachment(file['name'], file['mimetype'], file['url_private_download']))
                    message.attachments = file_attachments
                messages.append(message)
    print('importing '+str(len(messages))+ ' messages')
    for message in messages:
        #create message object
        message_object = {}
        message_properties = {}
        message_properties["enaio:objectTypeId"] = {"value": "message"}
        message_properties["author"] = {"value": message.author}
        message_properties["text"] = {"value": message.text}
        message_properties["createdAt"] = {"value": message.created_at}
        message_properties["numOfAttachments"] = {"value": str(len(message.attachments))}
        message_object["properties"] = message_properties


        #import message object

        request_body_message = {
            'data': ('message.json', json.dumps({'objects': [message_object]}), 'application/json')
        }
        
        
        response_message = requests.post("https://api.yuuvis.io/dms-core/objects", files = request_body_message, headers=header_dict)
        response_message_json = response_message.json()

        if response_message.status_code == 422:
            print({'objects': [message_object]})
            print(response_message.content)

        if len(message.attachments)>0 :
            message_id = response_message_json['objects'][0]['properties']['enaio:objectId']['value']
            #create attachment objects objects if attachments exist
            attachment_ids = []
            for attachment in message.attachments:
                attachment_object = {}
                attachment_properties = {}
                attachment_properties["enaio:objectTypeId"] = {"value": "attachment"}
                attachment_properties["createdAt"] = {"value": message.created_at}
                attachment_properties["Name"] = {"value": attachment.name}
                attachment_properties["text"] = {"value": message.text}
                attachment_properties["author"] = {"value": message.author}
                attachment_properties["messageId"] = {"value": message_id}
                attachment_object["properties"] = attachment_properties

                attachment_object["contentStreams"] = [{
                    "fileName": attachment.name,
                    "mimeType": attachment.type,
                    "cid": "cid_63apple"
                }]
                
                #import attachment object
                response_attachment_file = requests.get(attachment.url)
                request_body_attachment = {
                    'data': ('attachment.json', json.dumps({'objects': [attachment_object]}), 'application/json'),
                    'cid_63apple': (attachment.name, response_attachment_file.content , attachment.type)
                }
                
                response_attachment = requests.post("https://api.yuuvis.io/dms-core/objects", files = request_body_attachment, headers = header_dict)
                response_attachment_json = response_attachment.json()
                attachment_ids.append(response_attachment_json['objects'][0]['properties']['enaio:objectId']['value'])
                