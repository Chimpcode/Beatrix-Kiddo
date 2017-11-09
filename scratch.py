from subprocess import call, CalledProcessError
from utils import write_on_models_py, write_on_serializers_py, \
                write_on_views, edit_project_urls_py, create_api_urls_py
import json
import sys

def register_api_models_admin(be_build):
    ADMIN_PY = '\n' \
               'from api.models import '
    REGISTER_MODELS_ADMIN = 'admin.site.register({{model_name}})'

    api_admin_file = open(be_build['app_name']+'/'+'api'+'/admin.py', 'a')

    for i, model in enumerate(be_build['models']):
        if i == 0:
            ADMIN_PY = ADMIN_PY + list(model.keys())[0]
        else:
            ADMIN_PY = ADMIN_PY + ', ' + list(model.keys())[0]

    api_admin_file.write(ADMIN_PY)
    api_admin_file.write('\n\n')

    for i, model in enumerate(be_build['models']):
        api_admin_file.write(
            REGISTER_MODELS_ADMIN.replace(
                                '{{model_name}}',
                                list(model.keys())[0]))
        api_admin_file.write('\n')


def modify_settings_py(app_name):

    DEFAULT_INSTALLED_APPS_CHUNK = 'INSTALLED_APPS = [\n' \
                                   '    \'django.contrib.admin\',\n' \
                                   '    \'django.contrib.auth\',\n' \
                                   '    \'django.contrib.contenttypes\',\n' \
                                   '    \'django.contrib.sessions\',\n' \
                                   '    \'django.contrib.messages\',\n' \
                                   '    \'django.contrib.staticfiles\',\n' \
                                   ']'

    MODIFIED_INSTALLED_APPS_CHUNK = 'DJANGO_APPS = [\n' \
                                    '    \'django.contrib.admin\',\n' \
                                    '    \'django.contrib.auth\',\n' \
                                    '    \'django.contrib.contenttypes\',\n' \
                                    '    \'django.contrib.sessions\',\n' \
                                    '    \'django.contrib.messages\',\n' \
                                    '    \'django.contrib.staticfiles\',\n' \
                                    ']\n' \
                                    '\n' \
                                    'THIRD_PARTY_APPS = [\n' \
                                    '    \'rest_framework\',\n' \
                                    ']\n' \
                                    '\n' \
                                    'LOCAL_APPS = [\n' \
                                    '    \'api\'\n' \
                                    ']\n' \
                                    '\n' \
                                    'INSTALLED_APPS = ' \
                                    'DJANGO_APPS + THIRD_PARTY_APPS + ' \
                                    'LOCAL_APPS'

    settings_file = open(app_name+'/'+app_name+'/settings.py').read()
    settings_file_modified = settings_file.replace(
                                DEFAULT_INSTALLED_APPS_CHUNK,
                                MODIFIED_INSTALLED_APPS_CHUNK)

    settings_buff = open(app_name+'/'+app_name+'/settings.py', 'w')
    settings_buff.seek(0)
    settings_buff.write(settings_file_modified)
    settings_buff.truncate()
    settings_buff.close()
    # print(settings_file_modified)


# modify_settings_py('notetaking')


def build_models_task(be_build):
    write_on_models_py(be_build['app_name']+'/api/models.py',
                       be_build['models'])
    modify_settings_py(be_build['app_name'])
    edit_project_urls_py(be_build)
    write_on_serializers_py(be_build)
    write_on_views(be_build)
    register_api_models_admin(be_build)
    create_api_urls_py(be_build)
    call(['python', 'manage.py', 'makemigrations'],
         cwd=be_build['app_name']+'/')
    call(['python', 'manage.py', 'migrate'],
         cwd=be_build['app_name']+'/')


def scaffold_project(be_build):
    try:
        call(['django-admin', 'startproject', be_build['app_name']])
        call(['python', 'manage.py', 'startapp', 'api'],
             cwd=be_build['app_name']+'/')
        return True
    except CalledProcessError as e:
        print(e.output)


def read_scaffolding_file(PATH_FILE):
    raw_data = open(PATH_FILE).read()
    be_build = json.loads(raw_data)
    return be_build


def build_task():
    # 'sandbox/sample_project.json'
    be_build = read_scaffolding_file(sys.argv[1])
    scaffold_project(be_build)
    build_models_task(be_build)


def build_and_run_task():
    # 'sandbox/sample_project.json'
    be_build = read_scaffolding_file(sys.argv[1])
    scaffold_project(be_build)
    build_models_task(be_build)
    try:
        call(['python', 'manage.py', 'runserver'],
             cwd=be_build['app_name']+'/')
    except KeyboardInterrupt:
        print('*** Ctrl C ***')
    else:
        print('no exception')


def write_schemas():
    return True


build_and_run_task()

# print(raw_data)
# build_mode = be_build['config']['build_mode']
# project_name = be_build['app_name']
# print(list(be_build['models'][0].values())[0])
# be_build = read_scaffolding_file('sandbox/sample_project.json')
# print(be_build['models'])
# process_build_mode(build_mode)
