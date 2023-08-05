# Copyright (c) 2017, The MITRE Corporation. All rights reserved.
# See LICENSE.txt for complete terms.

import unittest

from mixbox.vendor.six import u

from cybox.objects.win_user_account_object import WinGroup, WinGroupList, WinPrivilege, WinPrivilegeList, WinUser
from cybox.test import EntityTestCase
from cybox.test.objects import ObjectTestCase


class TestWinGroup(EntityTestCase, unittest.TestCase):
    klass = WinGroup

    _full_dict = {
        'name': u("LocalAdministrators"),
        'xsi:type': 'WindowsGroupType',
    }


class TestWinGroupList(EntityTestCase, unittest.TestCase):
    klass = WinGroupList

    _full_dict = [
        TestWinGroup._full_dict,
        TestWinGroup._full_dict,
    ]


class TestWinPrivilege(EntityTestCase, unittest.TestCase):
    klass = WinPrivilege

    _full_dict = {
        'user_right': u("SeDebugPrivilege"),
        'xsi:type': 'WindowsPrivilegeType',
    }


class TestWinPrivilegeList(EntityTestCase, unittest.TestCase):
    klass = WinPrivilegeList

    _full_dict = [
        TestWinPrivilege._full_dict,
        TestWinPrivilege._full_dict,
    ]


class TestWinUser(ObjectTestCase, unittest.TestCase):
    object_type = "WindowsUserAccountObjectType"
    klass = WinUser

    _full_dict = {
        # Account-specific fields
        'disabled': False,
        'domain': u('ADMIN'),
        # UserAccount-specific fields
        'password_required': True,
        'full_name': u("Steve Ballmer"),
        'group_list': TestWinGroupList._full_dict,
        'home_directory': u("C:\\\\Users\\\\ballmer\\\\"),
        'last_login': "2011-05-12T07:14:01+07:00",
        'privilege_list': TestWinPrivilegeList._full_dict,
        'username': u("ballmer"),
        'user_password_age': u("P180D"),
        # WinUser-specific fields
        'security_id': u("S-1-5-21-3623811015-3361044348-30300820-1013"),
        'security_type': u("SidTypeUser"),
        'xsi:type': object_type,
    }


if __name__ == "__main__":
    unittest.main()
