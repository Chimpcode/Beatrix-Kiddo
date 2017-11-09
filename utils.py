import re

FIELDS_LINE_CODE = '    {{field_name}} = '\
                   'models.{{field_type}}({{field_options}})\n'

TEST_INIT_DATA = [{'model1': ['fieldA(IntegerField[max_length=3])',
                              'fieldB(CharField[max_length=3])',
                              'fieldC(TextField[])',
                              'fieldD(CharField[])']},
                  {'model2': ['fieldA(IntegerField[max_length=3])']}]


def get_models(be_build):
    model_list = []
    for model_chunk in be_build['models']:
        model_list.append(list(model_chunk.keys())[0])

    return model_list


def process_build_mode(build_mode):
    if len(build_mode) is 1:
        if build_mode[0] is 'dev':
            print('developin dev project')
        elif build_mode[0] is 'test':
            print('developin test project')
        elif build_mode[0] is 'prod':
            print('developin prod project')
        else:
            raise ValueError('please choose one of build modes enabled : '
                             '\'dev\', \'test\' and/or \'prod\'')
    if len(build_mode) > 1:
            print('several modes')


def process_field(field_stringified, line_code):
    (field_name, util_chunk) = field_stringified.split('(')[0:2]
    type_field = util_chunk.split('[')[0]
    constraints = re.findall("\[(.*?)\]", field_stringified)[0]

    modified_line = line_code.replace('{{field_name}}', field_name) \
        .replace('{{field_type}}', type_field) \
        .replace('{{field_options}}', constraints)

    # print(modified_line)
    return modified_line


# be['models'][0]
def process_fields(model_stringified, template_file):
    template_data = open('templates/models_be')

    for line_code in template_data.readlines():
        if line_code == FIELDS_LINE_CODE:
            new_line_code = ''
            for field_item in list(model_stringified.values())[0]:
                new_line_code = new_line_code + \
                                process_field(field_item, line_code)
            modified_template_file = template_file.replace(line_code,
                                                           new_line_code)
            line_code = new_line_code
            return modified_template_file
            # print(modified_template_file)
            break


# be['models']
def process_models(models_stringified):
    template_file = open('templates/models_be').read()
    model_chunks = []
    for model in models_stringified:
        # model name
        model_name = list(model.keys())[0]
        modified_template_data = process_fields(model, template_file)
        model_chunks.append(modified_template_data.replace('{{model_name}}',
                            model_name))

    return model_chunks


def write_on_models_py(model_file_path, models_section):

    model_chunks = process_models(models_section)
    models_py = open(model_file_path, 'a')
    models_py.write('\n')
    models_py.write('\n')
    for i, chunk in enumerate(model_chunks):
        if i == (len(model_chunks) - 1):
            models_py.write(chunk)
        else:
            models_py.write(chunk)
            models_py.write('\n')

    models_py.close()
    clear_final_line(model_file_path)


def write_on_serializers_py(be_build):
    SERIALIZER_TEMPLATE_PATH = 'templates/serializers_be'
    TEMPLATE_CLASS_SERIALIZER = 'class {{ModelSerializer}} ' \
                                '(serializers.ModelSerializer):\n' \
                                '    class Meta:\n' \
                                '        model = {{model}}\n' \
                                '        fields = \'__all__\'\n'

    template_file = ''
    with open(SERIALIZER_TEMPLATE_PATH, 'r') as f:
        template_file = f.read()

    models = get_models(be_build)
    import_models_data = ', '.join(get_models(be_build))

    template_adapted = template_file.replace('{{models}}', import_models_data)

    serializer_classes = ''
    for i, model in enumerate(models):
        serializer_class = TEMPLATE_CLASS_SERIALIZER \
                                .replace('{{model}}', model) \
                                .replace('{{ModelSerializer}}', model +
                                         'Serializer')
        serializer_classes = serializer_classes + serializer_class
        if i != (len(models) - 1):
            serializer_classes = serializer_classes + '\n\n'

    serializer_file_buff = template_adapted.replace('{{foreach_model}}',
                                                    serializer_classes)

    DESTINY_FILE_PATH = be_build['app_name'] + '/api/serializers.py'
    buff_file = open(DESTINY_FILE_PATH, 'w')
    buff_file.write(serializer_file_buff)
    buff_file.close()


def write_on_views(be_build):
    VIEW_CLASS_TMPL = 'class {{model}}ViewSet(viewsets.ModelViewSet):\n' \
                      '    queryset = {{model}}.objects.all()\n' \
                      '    serializer_class = {{ModelSerializer}}\n'

    template_views = ''
    with open('templates/views_be', 'r') as f:
        template_views = f.read()

    # [models]
    models = get_models(be_build)
    model_serializers = [model + 'Serializer' for model in models]
    template_views = template_views.replace('{{models}}',
                                            ', '.join(models))
    template_views = template_views.replace('{{modelsSerializers}}',
                                            ', '.join(model_serializers))

    view_classes = ''
    for i, model in enumerate(models):
        view_classes += VIEW_CLASS_TMPL.replace('{{model}}', model) \
                        .replace('{{ModelSerializer}}', model_serializers[i])
        if i != (len(models) - 1):
            view_classes = view_classes + '\n\n'

    template_views = template_views.replace('{{view_classes}}', view_classes)

    views_py = open(be_build['app_name'] + '/api/views.py', 'r+')
    views_py.write(template_views)
    views_py.close()


def edit_project_urls_py(be_build):
    TEMPLATE_REGISTER_ROUTES = 'router.register(r\'{{model}}\',' \
                               ' views.{{ModelViewSet}})\n'

    urls_buff = ''
    with open('templates/urls_be', 'r') as f:
        urls_buff = f.read()

    models = get_models(be_build)

    register_routes = ''
    for model in models:
        register_routes += TEMPLATE_REGISTER_ROUTES \
                                .replace('{{model}}', model.lower()) \
                                .replace('{{ModelViewSet}}', model+'ViewSet')

    urls_buff = urls_buff.replace('{{router.register}}',
                                  register_routes)

    urls_py = open(be_build['app_name'] + '/' + be_build['app_name'] +
                   '/urls.py', 'w')
    urls_py.write(urls_buff)
    urls_py.close()


def create_api_urls_py(be_build):
    api_urls_buff = ''
    with open('templates/api_urls_be', 'r') as f:
        api_urls_buff = f.read()

    api_urls_py = open(be_build['app_name'] + '/api/urls.py', 'w')
    api_urls_py.write(api_urls_buff)
    api_urls_py.close()


def clear_final_line(file_path):
    readFile = open(file_path)
    lines = readFile.readlines()
    readFile.close()

    w = open(file_path, 'w')
    w.writelines([item for item in lines[:-1]])
    w.close()


# write_on_models_py('assets_tests/models.py')
