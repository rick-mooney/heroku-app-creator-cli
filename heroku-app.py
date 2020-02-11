import os
import pandas as pd
import subprocess as proc


CONFIGS = {}
# Salesforce
def addSalesforce():
    CONFIGS['GRAX_SFDC_USERNAME']=''
    CONFIGS['GRAX_SFDC_PASSWORD']=''
    CONFIGS['GRAX_SFDC_TOKEN']=''
    CONFIGS['GRAX_SFDC_URL']=''

# Storage
## S3
def addS3():
    CONFIGS['S3ACCESSKEYID']=''
    CONFIGS['S3BUCKET']=''
    CONFIGS['S3REGION']=''
    CONFIGS['S3SECRETACCESSKEY']=''
## Azure
def addAzure():
    CONFIGS['AZURE_STORAGE_ACCOUNT_NAME']=''
    CONFIGS['AZURE_ACCOUNT_ACCESS_KEY']=''
    CONFIGS['AZURE_CONTAINER_NAME=']=''
    CONFIGS['GRAX_STORAGE_PROVIDER_NAME']=''

## Google
def addGoogle():
    CONFIGS['GRAX_STORAGE_PROVIDER_NAME']=''
    CONFIGS['GOOGLE_PROJECT_ID']=''
    CONFIGS['GOOGLE_BUCKET_NAME']=''
    CONFIGS['GOOGLE_PRIVATE_KEY_ID']=''
    CONFIGS['GOOGLE_CLIENT_EMAIL']=''
    CONFIGS['GOOGLE_CLIENT_ID']=''
    CONFIGS['GOOGLE_PRIVATE_KEY']=''


def setDefaultConfigs(app_name):
    # Grax
    CONFIGS['APP_NAME'] = app_name
    CONFIGS['BONSAI_URL']=''
    CONFIGS['GRAX_ENV']=app_name
    # Default
    CONFIGS['DEBUGGING']='true'
    CONFIGS['GRAX_ASYNCH_TIMER']='10'
    CONFIGS['GRAX_ESMAXBULK']='300'
    CONFIGS['GRAX_S3_OFF']='false'
    CONFIGS['GRAX_AUDITTRAIL_OFF']='true'
    CONFIGS['GRAX_DESTINATION_SFDC_PASSWORD']=''
    CONFIGS['GRAX_DESTINATION_SFDC_TOKEN']=''
    CONFIGS['GRAX_DESTINATION_SFDC_URL']=''
    CONFIGS['GRAX_DESTINATION_SFDC_USERNAME']=''
    CONFIGS['GRAX_MAX_RESTORE']='1000'
    CONFIGS['GRAX_OBJECT_TYPES_TO_RESTORE']=''
    CONFIGS['GRAX_SYNCHID']='GRAX_RESTORE'
    CONFIGS['GRAX_FORCE_ENV_CONFIG']='true'
    addSalesforce()
    log('default configs added')

def setConfigs(app_name, storage='S3'):
    output = ''
    setDefaultConfigs(app_name)
    if storage == 'S3':
        addS3()
        log('added S3 Storage vars')
    elif storage == 'Azure':
        addAzure()
        log('added Azure Storage vars')
    elif storage == 'Google':
        addGoogle()
        log('added Google Storage var')

    for k in CONFIGS:
        if CONFIGS[k] != '':
            output += k + '=' + CONFIGS[k] + ' '
    run(f'heroku config:set -a {app_name} {output}')
    log(f'configs set for app {app_name}')

addons = ['engagementgrapgh:hpt-test', 'scheduler:standard']
def installAddOns(app_name):
    for addon in addons:
        run(f'heroku addons:create {addon} -a {app_name} --json')
    log('addons added to app')

def createApp(app_name, region, space, team, storage):
    create = run('heroku create {app_name} --remote=https://github.com/HardingPoint/grax-secure.git --region={region} --space={space} --team={team} --json')
    installAddOns(app_name)
    setConfigs(app_name, storage)

def updateApp(app_name):
    run(f'heroku git:remote -a {app_name}')
    run('git push heroku master')

def listApps(team=None):
    function = 'heroku apps'
    if team:
        function += ' --team ' + team
    else:
        function += ' -A'
    result = run(function)
    apps = result.split('\n')
    return [i for i in apps if i] # removes empty strings from cli response

def scaleDynos(app_name, dyno_type, amount=1):
    run(f'heroku ps:scale {dyno_type}={amount} -a {app_name}')

def run(function):
    if DEBUG:
        print(f'running {function} ...')
        return function
    else:
        try:
            s = proc.run(function, shell=True, check=True, stdout=proc.PIPE, universal_newlines=True)
            output = s.stdout
            return output
        except FileNotFoundError as e:
            print(e)

def updateAppsRemotely(team=None):
    apps = listApps(team)
    for app in apps:
        log(f'updating {app}')
        updateApp(app)
        print(f'{app} update complete')
    print('All apps have been updated')

def log(message):
    if TRACE == 'FINE':
        print(message)
        
# Before running this script, you'll need to authenticate.
# In the terminal run heroku login -i, then enter your username and password
DEBUG = True
TRACE = 'FINE'
if __name__ == '__main__':
    source = pd.read_csv('heroku_settings.csv', na_filter=False)
    apps = source.to_dict(orient='records')
    for app in apps:
        if app['Method'] == 'create':
            log(f'begin create process for app {app}')
            createApp(app['AppName'], app['Region'],app['Space'], app['Team'], app['Storage'])
        elif app['Method'] == 'update':
            log(f'begin update process for app {app}')
            updateApp(app['AppName'])
