import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.authz as authz
from ckan.logic.action import get
import auth
import actions
import controller

# CKAN Extension Class Group Private Datasets
class Group_Private_DatasetsPlugin(plugins.SingletonPlugin):
    # Plugin implementations for authorization and the package controller
    plugins.implements(plugins.IAuthFunctions, inherit=True)
    plugins.implements(plugins.IPackageController, inherit=True)

    # Identify all overloaded authorization functions
    def get_auth_functions(self):
        return {'package_show': auth.package_show,
                'package_search': auth.package_search}

    # Before any package search, run this section of code.
    def before_search(self, search_params):

        # If the current context has a group member item,
        # update the search parameters
        if toolkit.c.group:

            # Collect a member list of all members of the group in context
            member_list = toolkit.get_action('member_list')(
                data_dict={'id': toolkit.c.group.name}
            )

            for member in member_list:

                # If a person is logged in and the second value
                # in the tuple is user
                if toolkit.c.userobj != None and member[1] == "user":

                    # Get the UID from the currently logged in user
                    username = authz.get_user_id_for_username(toolkit.c.user)

                    # If the UID matches the member UID, set the
                    # search parameters to show public and private datasets.
                    if member[0] == username:
                        search_params['fq'] = ''
                        return search_params

        # Return default search parameters if not in a group
        return search_params
