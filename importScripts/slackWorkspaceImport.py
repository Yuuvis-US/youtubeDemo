import os
from os.path import isfile, isdir, join, basename
import json
from datetime import datetime, timedelta, timezone

#establish export file structure
slackExportRootFolderPath = "../input/" + os.listdir("../input/").pop()+"/"
slackExportRootFiles = os.listdir(slackExportRootFolderPath)

metaFiles = [f for f in slackExportRootFiles if isfile(join(slackExportRootFolderPath, f))]
channelDirs = [f for f in slackExportRootFiles if isdir(join(slackExportRootFolderPath, f))]

#retrieve file paths for each channel
inputJsonFilePaths = {}
for channelDir in channelDirs:
    inputJsonFilePaths[channelDir] = []
    channelDirPath = join(slackExportRootFolderPath, channelDir)
    for inputFileName in os.listdir(channelDirPath):
        inputJsonFilePaths[channelDir].append(join(channelDirPath, inputFileName))

#print(inputJsonFilePaths)

#play around a bit

epoch = datetime(1601, 1, 1)

class Message:
    def __init__(self, author, text, createdAt, channel, attachments):
        self.author = author
        self.text = text
        self.createdAt = createdAt
        self.channel = channel
        self.attachments = attachments

class Attachment:
    def __init__(self, name, type, url):
        self.name = name
        self.type = type
        self.url = url

for channelDir in channelDirs:
    print('gathering messages for channel '+channelDir)
    for chatLogFile in inputJsonFilePaths[channelDir]:
        date = basename(chatLogFile).split('.')[0]
        print("date: "+ date)

        with open(chatLogFile, 'r') as inputFile:

            testSlackChatLog = json.load(inputFile)

            messages = []
            for x in testSlackChatLog:
                timestamp = (epoch + timedelta(microseconds = float(x['ts'])))
                time = timestamp.time().strftime("%H:%M:%S")

                createdAt = date+"T"+time

                message = Message(x['user'], x['text'], createdAt, channelDir, [])
                if 'files' in x:
                    fileAttachments = []
                    for file in x['files']:
                        fileAttachments.append(Attachment(file['name'], file['mimetype'], file['url_private_download']))
                    message.attachments = fileAttachments
                messages.append(message)

            for message in messages:
                print(message.author, message.text, message.createdAt)
                print(message.attachments)
