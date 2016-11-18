import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.authz as authz
import ckan.model as model
import ckan.logic as logic
from ckan.logic.action import get
from ckan.logic.auth import get_package_object

# Starting from CKAN 2.2, you need to explicitly flag authorization functions
# that allow anonymous access or the will not work. The decorator
# @toolkit.auth_allow_anonymous_access provides that.
@toolkit.auth_allow_anonymous_access
def package_search(context, data_dict=None):
    # If the user is not authenticated, do not show any private datasets
    if ('q' in data_dict.keys() and 'auth_user_obj' in context.keys() and context['auth_user_obj'] != None and ('group' in context or "groups" in data_dict['q'])):
        context['ignore_capacity_check'] = True
    return {'success': True}

@toolkit.auth_allow_anonymous_access
def package_show(context, data_dict=None):
    # Identify the current package
    package = get_package_object(context, data_dict)

    # If the package isn't private, allow anyone to view the dataset
    if (package.private):
        # Check the currently logged in user
        user = context.get('user')

        # If the user is part of the organization that
        # owns this dataset, allow access as normal.
        if (authz.users_role_for_group_or_org(package.owner_org, user) != None):
            return {'success': True}

        # Get all groups in the CKAN instance
        all_groups = get.group_list(context, data_dict)

        # Iterate through all of the groups
        for group in all_groups:

            # Use the group ID to collect all packages owned by a group
            current_group = get.group_package_show(context, {'id': group})

            # Skip if the current group has no packages
            if (len(current_group) > 0):

                # Iterate through all packages in a group
                for i in range(len(current_group)):

                    # Get the title of the package
                    group_package_title = str(current_group[i]['name'])

                    # If the user has any affiliation with the group that
                    # contains this package, allow access to the package.
                    if ((group_package_title == str(package.name)) and (authz.users_role_for_group_or_org(group, user) != None)):
                        return {'success': True}
        # Otherwise deny access to the package.
        return {'success': False}
    # If the package isn't private, allow access to the package.
    return {'success': True}
