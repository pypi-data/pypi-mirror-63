# Copyright (c) 2017, The MITRE Corporation. All rights reserved.
# See LICENSE.txt for complete terms.

from mixbox import entities
from mixbox import fields

import cybox.bindings.user_account_object as user_account_binding
from cybox.common import DateTime, Duration, String
from cybox.objects.account_object import Account


class Group(entities.Entity):
    """An abstract class for account groups."""
    _binding = user_account_binding
    _binding_class = user_account_binding.GroupType
    _namespace = 'http://cybox.mitre.org/objects#UserAccountObject-2'
    _XSI_TYPE = None  # overridden by subclasses

    def to_dict(self):
        d = super(Group, self).to_dict()

        if self._XSI_TYPE:
            d['xsi:type'] = self._XSI_TYPE

        return d


class GroupList(entities.EntityList):
    _binding = user_account_binding
    _binding_class = user_account_binding.GroupListType
    _namespace = 'http://cybox.mitre.org/objects#UserAccountObject-2'

    group = fields.TypedField("Group", Group, multiple=True)


class Privilege(entities.Entity):
    """An abstract class for account privileges."""
    _binding = user_account_binding
    _binding_class = user_account_binding.PrivilegeType
    _namespace = 'http://cybox.mitre.org/objects#UserAccountObject-2'
    _XSI_TYPE = None  # overridden by subclasses

    def to_dict(self):
        d = super(Privilege, self).to_dict()

        if self._XSI_TYPE:
            d['xsi:type'] = self._XSI_TYPE

        return d


class PrivilegeList(entities.EntityList):
    _binding = user_account_binding
    _binding_class = user_account_binding.PrivilegeListType
    _namespace = 'http://cybox.mitre.org/objects#UserAccountObject-2'

    privilege = fields.TypedField("Privilege", Privilege, multiple=True)


class UserAccount(Account):
    _binding = user_account_binding
    _binding_class = user_account_binding.UserAccountObjectType
    _namespace = 'http://cybox.mitre.org/objects#UserAccountObject-2'
    _XSI_NS = "UserAccountObj"
    _XSI_TYPE = "UserAccountObjectType"

    password_required = fields.TypedField('password_required')
    full_name = fields.TypedField('Full_Name', String)
    home_directory = fields.TypedField('Home_Directory', String)
    last_login = fields.TypedField('Last_Login', DateTime)
    script_path = fields.TypedField('Script_Path', String)
    username = fields.TypedField('Username', String)
    user_password_age = fields.TypedField('User_Password_Age', Duration)

    # These should be overridden by subclasses
    group_list = fields.TypedField('Group_List', GroupList)
    privilege_list = fields.TypedField('Privilege_List', PrivilegeList)
