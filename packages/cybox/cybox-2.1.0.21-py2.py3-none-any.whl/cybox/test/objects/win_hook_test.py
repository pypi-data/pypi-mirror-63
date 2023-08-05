# Copyright (c) 2017, The MITRE Corporation. All rights reserved.
# See LICENSE.txt for complete terms.

import unittest

from mixbox.vendor.six import u

from cybox.objects.win_hook_object import WinHook
from cybox.test.objects import ObjectTestCase
from cybox.test.objects.win_handle_test import TestWinHandle


class TestWinHook(ObjectTestCase, unittest.TestCase):
    object_type = "WindowsHookObjectType"
    klass = WinHook

    _full_dict = {
        'type': u("Test Hook"),
        'handle': TestWinHandle._full_dict,
        'hooking_function_name': u("test_function"),
        #TODO: add 'hooking_module'
        'thread_id': 2,
        'xsi:type': object_type,
    }


if __name__ == "__main__":
    unittest.main()
