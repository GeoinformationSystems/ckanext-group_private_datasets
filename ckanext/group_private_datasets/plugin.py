import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

def package_show(context, data_dict=None):
    user_name = context['user']

    return {'success': False, 'msg': "Testing This Working"}

class Group_Private_DatasetsPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IAuthFunctions)

    def get_auth_functions(self):
        return {'package_show': package_show}
