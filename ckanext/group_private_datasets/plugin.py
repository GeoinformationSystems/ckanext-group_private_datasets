import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.authz as authz
from ckan.logic.action import get
import auth

class Group_Private_DatasetsPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IAuthFunctions, inherit=True)
    plugins.implements(plugins.IPackageController, inherit=True)

    def get_auth_functions(self):
        return {'package_show': auth.package_show, 'package_search': auth.package_search}#, 'group_show': auth.group_show}

    def before_search(self, search_params):
        if (toolkit.c.group):
            member_list = toolkit.get_action('member_list')(data_dict={'id': toolkit.c.group.name})
            for member in member_list:
                if (toolkit.c.userobj != None and member[1] == "user"):
                    username = authz.get_user_id_for_username(toolkit.c.user)
                    if (member[0] == username):
                        search_params['fq'] = ''
                        return search_params
        return search_params
