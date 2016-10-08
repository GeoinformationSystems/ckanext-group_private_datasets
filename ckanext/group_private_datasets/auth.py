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
    print "COOL!!"
    if (context['auth_user_obj'] != None):
        context['ignore_capacity_check'] = True
    return {'success': True}

@toolkit.auth_allow_anonymous_access
def package_show(context, data_dict=None):
    group = model.Group.get('cool-group')
    limit = 10
    result = toolkit.get_action('package_search')(context, {
        'fq': 'groups:{0}'.format(group.name),
        'rows': limit,
    })
    print result
    package = get_package_object(context, data_dict)
    print "PACKAGE: " + str(package) + "\n\n"
    # If the package isn't private, allow anyone to view the dataset
    if (package.private):
        user = context.get('user')
        print "USER NAME: " + user + "\n\n"

        all_groups = get.group_list(context, data_dict)
        print "ALL GROUPS: " + str(all_groups) + "\n\n"
        for group in all_groups:
            current_group = get.group_package_show(context, {'id': group})
            print "CURRENT GROUP: " + str(current_group) + "\n\n"
            if (len(current_group) > 0):
                for i in range(len(current_group)):
                    group_package_title = str(current_group[i]['name'])
                    print "PACKAGE TITLE: " + str(package.name)
                    print "GROUP PACKAGE TITLE: " + group_package_title
                    print authz.users_role_for_group_or_org(group, user)
                    if ((group_package_title == str(package.name)) and (authz.users_role_for_group_or_org(group, user) != None)):#(authz.has_user_permission_for_group_or_org(group, user, 'manage_group'))):
                        #group_member_list = get.member_list(context, {'id': group})
                        #print group_member_list
                        #print get.organization_list_for_user(context,data_dict)
                        print "SUCCESS!!"
                        return {'success': True}
        return {'success': False}
    return {'success': True}
