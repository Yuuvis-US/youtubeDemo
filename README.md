# yuuvis® Ultimate Demo: Slack Workspace Archiving


This repository houses the Python yuuvis® Ultimate Demo Application, which showcases how yuuvis® Ultimate can be used to archive third-party data structures and to provide the ability to query the full text of any binary file attachments, using the example of a Slack Workspace Export.
This demo includes a custom yuuvis® schema, a script for parsing and importing the Slack Workspace Export, and finally a browser interface to represent a rudimentary client application.

## Requirements

### yuuvis® Ultimate Subscription

As you may have guessed, you'll need an active yuuvis® Ultimate Subscription to use the scripts in this demo.
Acquire your free trial license today at [https://developer.yuuvis.com/](https://developer.yuuvis.com/), and once you're logged in, retrieve your Subscription Key from the [Subscriptions page](https://developer.yuuvis.com/Identity/Subscriptions).
You'll need to replace any instance of `Your_API_Key_Here` in this repository with your actual Subscription key.

#### Python

You will need to have Python installed on your machine. But how do you know if you already have it or not? Well on MAC's it is already installed so you can simply open up your favorite Terminal and type.
```
$ python --version
Python 3.7
```
If you are using Python 2.x, you might run into unforeseen problems with these scripts, as Python version 3.6 and higher were used for the development of this demo.

For Windows and to update your current version of Python on MAC you will need download it from [https://www.python.org/downloads/](https://www.python.org/downloads/).

#### Flask
Next you'll need Flask, the lightweight Web API library we used for this project. Install it in your python environment using `pip install flask` (or any other method you like) and you'll be ready to launch all scripts included in this repository.

## Instructions

Now let's go over how to use these scripts. The basics steps are:
1. Retrieve a Slack Workspace Export ([here's how](https://slack.com/help/articles/201658943-Export-your-workspace-data)), decompress it and place it in `importScripts/input` directory (you might need to create this directory)
2. Update the tenant schema with the provided `slackSchema.xml` custom schema (only the first time around or whenever you make changes to the data structure)
3. Import the messages and attachments described in the Slack Workspace Export using the `slackWorkspaceImport.py` script
4. Boot the Web interface in the `youtube_demo` directory to view the fruits of your labour

The detailed order for the script execution after the export has beed placed in the input directory is as follows:
#### Schema Initialization
1. Backup your current schema using `python schemaScripts/get-current-schema.py`. Skip this step if you haven't done anything with your [tenant schema](https://developer.yuuvis.com/Documentation/Schema-definition) yet.
2. Update the schema using `python schemaScripts/post-new-schema.py`.
#### Workspace import
3. Parse the Workspace Export into message and attachment objects and import them into your yuuvis® Ultimate tenant using `python importScripts/slackWorkspaceImport`. This may take some time if many binary attachments are referenced in the Workspace Export, as they need to be individually retrieved from the Slack File Servers.
4. Run the Flask api using `python youtube_demo/yuuvis_demo_site.py`, which will boot the Web Interface at http://localhost:80. You'll find a text Field for [Search query statements](https://developer.yuuvis.com/Documentation/Query-language) and an Output box displaying relevant information about each Search result.
