## Prerequisites
* Text Editor, like visual studio code (https://code.visualstudio.com/download)
* A github (https://github.com/) account
* Heroku CLI (https://devcenter.heroku.com/articles/heroku-cli)
* Python (https://www.python.org/downloads/) 3.6 or greater
* Access to the customer’s Heroku Account with permissions to manage and deploy

## Setup
 1. Install dependecies in Pipfile
 2. Set debug & trace variables

## Create apps
### Update the heroku_settings.csv file
*** ToDo create MD table of values ***

## Update apps

## Scale apps

## Create Kibana
1. Confirm configuration variables
Set DEBUG = False <br>
Set RUN_SCRIPT = False

2. update kibana variables
Add the following code in the "One Time Execution" section of the heroku-app.py script and update the variables for your app

    bonsai_url = 'https://your-kibana-url.net'
    create_kibana('new-heroku-app-name', bonsai_url, 'bonsai-version', team='heroku-team-name', space='heroku-private-space-name')

3. In a new terminal, run python heroku-app.py