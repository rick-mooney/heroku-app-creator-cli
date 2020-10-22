import os
# import pandas as pd
import subprocess as proc
# from dotenv import load_dotenv
# load_dotenv()

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
    CONFIGS['S3ACCESSKEYID']=os.getenv("S3ACCESSKEYID")
    CONFIGS['S3BUCKET']=os.getenv("S3BUCKET")
    CONFIGS['S3REGION']=os.getenv("S3REGION")
    CONFIGS['S3SECRETACCESSKEY']=os.getenv("S3SECRETACCESSKEY")
    CONFIGS['S3ASSUMEROLEARN']=os.getenv("S3ASSUMEROLEARN")
    CONFIGS['S3ASSUMEROLEENABLED']=os.getenv("S3ASSUMEROLEENABLED")
## Azure
def addAzure():
    CONFIGS['AZURE_STORAGE_ACCOUNT_NAME']=''
    CONFIGS['AZURE_ACCOUNT_ACCESS_KEY']=''
    CONFIGS['AZURE_CONTAINER_NAME']=''
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

def add_defaults_to_remove():
    CONFIGS['APP_NAME']=''
    CONFIGS['BONSAI_URL']=''
    CONFIGS['DEBUGGING']=''
    CONFIGS['ENGAGEMENTGRAPH_ADMINPWD']=''
    CONFIGS['ENGAGEMENTGRAPH_ADMINUSER']=''
    CONFIGS['ENGAGEMENTGRAPH_APIURL']=''
    CONFIGS['ENGAGEMENTGRAPH_APIVERSION']=''
    CONFIGS['ENGAGEMENTGRAPH_URL']=''
    CONFIGS['GIT_USER_ID']=''
    CONFIGS['GRAX_ASYNCH_TIMER']=''
    CONFIGS['GRAX_AUDITTRAIL_OFF']=''
    CONFIGS['GRAX_ENV']=''
    CONFIGS['GRAX_ENV_ASYNC_ATTACHMENT_PROCESSOR_ORGANIZATION_IDS']=''
    CONFIGS['GRAX_ENV_ASYNC_BULK_LOAD_ORGANIZATION_IDS']=''
    CONFIGS['GRAX_ENV_ASYNC_INTERVAL_MINUTES']=''
    CONFIGS['GRAX_ENV_METADATA_BACKUP_ORGANIZATION_IDS']=''
    CONFIGS['GRAX_ENV_ODATA_ORGANIZATION_IDS']=''
    CONFIGS['GRAX_ENV_SYNC_SALESFORCE_SOURCE_ORGANIZATION_IDS']=''
    CONFIGS['GRAX_ESMAXBULK']=''
    CONFIGS['GRAX_FORCE_ENV_CONFIG']=''
    CONFIGS['GRAX_MAX_RESTORE']=''
    CONFIGS['GRAX_OBJECT_TYPES_TO_RESTORE']=''
    CONFIGS['GRAX_S3_OFF']=''
    CONFIGS['GRAX_SFDC_PASSWORD']=''
    CONFIGS['GRAX_SFDC_TOKEN']=''
    CONFIGS['GRAX_SFDC_URL']=''
    CONFIGS['GRAX_SFDC_USERNAME']=''
    CONFIGS['GRAX_SYNCHID']=''
    CONFIGS['RETRIEVE_SALESFORCE_METADATA']=''
    CONFIGS['S3ACCESSKEYID']=''
    CONFIGS['S3BUCKET']=''
    CONFIGS['S3REGION']=''
    CONFIGS['S3SECRETACCESSKEY']=''

def set_configs(app_name, storage='S3'):
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

def unset_configs(app_name):
    setDefaultConfigs(app_name)
    addS3()
    addAzure()
    addGoogle()
    add_defaults_to_remove()
    config_vars = ' '.join(list(CONFIGS.keys()))
    run_command = run(f'heroku config:unset -a {app_name} {config_vars}')
    with open('unset-command.txt', mode='w') as file:
        file.write(run_command)
    log(f'configs unset for app {app_name}')
        
addons = ['engagementgrapgh:hpt-test', 'scheduler:standard']
def install_addons(app_name):
    for addon in addons:
        run(f'heroku addons:create {addon} -a {app_name} --json')
    log('addons added to app')

def create_app(app_name, region, space, team, storage):
    run(f'heroku create {app_name} --remote=https://github.com/HardingPoint/grax-secure.git --region={region} --space={space} --team={team} --json')
    install_addons(app_name)
    set_configs(app_name, storage)

def update_app(app_name):
    run(f'heroku git:remote -a {app_name}')
    run('git push heroku master')

def list_apps(team=None):
    function = 'heroku apps'
    if team:
        function += ' --team ' + team
    else:
        function += ' -A'
    result = run(function)
    apps = result.split('\n')
    return [i for i in apps if i] # removes empty strings from cli response

def scale_dynos(app_name, dyno_type, amount=1):
    run(f'heroku ps:scale {dyno_type}={amount} -a {app_name}')

def create_kibana(app_name, bonsai_url, version, space=None, team=None):
    if not bonsai_url.endswith(':443'):
        ans = input('Warning: Your Bonsai URL does not include port 443 (most common).  Would you like us to append the default port? (Y / N): ')
        if ans.lower() == 'y':
            bonsai_url = bonsai_url + ':443'
    # run(f'git remote rm heroku')
    run(f'heroku login')
    buildpack = 'https://github.com/omc/heroku-buildpack-kibana'
    if space is not None:
        run(f'heroku create {app_name} --buildpack={buildpack} --team={team} --space={space}')
    elif team is not None:
        run(f'heroku create {app_name} --buildpack={buildpack} --team={team}')
    else:
        run(f'heroku create {app_name} --buildpack={buildpack}')

    run(f'heroku config:set -a {app_name} ELASTICSEARCH_URL={bonsai_url} ELASTICSEARCH_VERSION={version}')
    run(f'heroku git:remote -a {app_name}')
    run(f'git push heroku master')

def create_switch_app(app_name, space=None, team=None):
    # run(f'git remote rm heroku')
    run(f'heroku login')
    buildpack = 'https://github.com/rick-mooney/'
    run(f'heroku create {app_name}')
    run(f'heroku addons:create heroku-postgresql:hobby-dev -a {app_name} --json')
    # run(f'heroku addons:create scheduler:standard -a {app_name} --json')
    run(f'git push heroku git@github.com:rick-mooney/grax-sfswitch.git')

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

def remote_update(team=None):
    apps = list_apps(team)
    for app in apps:
        log(f'updating {app}')
        update_app(app)
        print(f'{app} update complete')
    print('All apps have been updated')

def log(message):
    if TRACE == 'FINE':
        print(message)

def bulk_setup(appname, region, key, secret, shield=False):
    drain_url = 'syslog+tls://logs2.papertrailapp.com:39736'
    run('heroku login')
    run(f'heroku config:add -a {appname} AWS_ACCESS_KEY_ID={key} AWS_SECRET_ACCESS_KEY={secret} AWS_REGION={region} GRAX_FLAGS=xray SENTRY_URL=https://69e6c5227efd4b37a3592464b91c3798@o401886.ingest.sentry.io/5262138')
    run(f'heroku labs:enable runtime-dyno-metadata -a {appname}')
    run(f'heroku drains:add {drain_url} -a {appname}')
    run(f'heroku drains -a {appname}')
    log(f'please run heroku drains -a {appname} to get your papertrail id')
    if not shield:
        run(f'heroku run ./graxctl tm-index -a {appname}')
    else:
        log('WARNING: Shield environments cannot execute run commands without an ssh key. Please run the time machine index script in Kibana directly')
    log('bulk setup complete')

def query_db():
    password = ''
    endpoint = ''
    port = ''
    dbname = ''
    print(f'psql postgres://postgres:{password}@{endpoint}:{port}/{dbname}')

def kill_all_apps(app_list):
    run('heroku login')
    for app in app_list:
        try:
            scale_dynos(app, 'web', amount=0)
            scale_dynos(app, 'grax-asynch', amount=0)
        except Exception as ex:
            print(f'failed to kill app {app}')
            print(ex)
        
#**** Configurations ****#
DEBUG = False
TRACE = 'FINE'
RUN_SCRIPT = False # set to False for One Time Execution

#**** Bulk update or create heroku apps ****#
if RUN_SCRIPT:
    if __name__ == '__main__':
        source = pd.read_csv('heroku_settings.csv', na_filter=False)
        apps = source.to_dict(orient='records')
        for app in apps:
            if app['Method'] == 'create':
                log(f'begin create process for app {app}')
                create_app(app['AppName'], app['Region'],app['Space'], app['Team'], app['Storage'])
            elif app['Method'] == 'update':
                log(f'begin update process for app {app}')
                update_app(app['AppName'])
else:
    apps = []
    #**** One Time Execution ****#
    # print('running one time execution')
    # enter your code here for one off execution.  Here is an example creating a Kibana App
    # bonsai_url = ''
    # create_kibana('', 
    #                 bonsai_url, '', 
    #                 team='', 
    #                 space=''
    #             )

    ## Bulk Setup ##
    # appname = ''
    # region = ''
    # accessid = ''
    # secretkey = ''
    # shield = False
    # bulk_setup(appname, region, accessid, secretkey, shield=shield)

    ## Postgres Connection ##
    # query_db()

    ## Scale Down Apps
    apps = []
    kill_all_apps(apps)