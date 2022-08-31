import os
import unittest

import env
from controls.utils import to_hex


class ControlsTestCase(unittest.TestCase):
    user_id = 33123
    line_pattern = '"#%s" : EAP "0x%s"\n'

    @classmethod
    def setUpClass(cls) -> None:
        env.SECRETS_PATTERN = 'testfile.%s.txt'
        from сontrols.controls_stroke import _controls
        cls.controls = _controls
        open(env.SECRETS_PATTERN % cls.user_id, 'w').close()

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove(env.SECRETS_PATTERN % cls.user_id)

    def setUp(self) -> None:
        open(env.SECRETS_PATTERN % self.user_id, 'wb').close()
        self.user1, self.pass1 = 'username1', 'password1'
        self.user2, self.pass2 = 'username2', 'password2'
        self.user3, self.pass3 = 'username3', 'password3'
        self.user4, self.pass4 = 'username4', 'password4'
        self.line1 = self.line_pattern % (to_hex(self.user1), to_hex(self.pass1))
        self.line2 = self.line_pattern % (to_hex(self.user2), to_hex(self.pass2))
        self.line3 = self.line_pattern % (to_hex(self.user3), to_hex(self.pass3))
        self.line4 = self.line_pattern % (to_hex(self.user4), to_hex(self.pass4))
        self.position1 = self.controls.add_user(self.user_id, self.user1, self.pass1)
        self.position2 = self.controls.add_user(self.user_id, self.user2, self.pass2)
        self.position3 = self.controls.add_user(self.user_id, self.user3, self.pass3)
        self.position4 = self.controls.add_user(self.user_id, self.user4, self.pass4)

    def test_add_users(self):
        expected = self.line1 + self.line2 + self.line3 + self.line4
        with open(env.SECRETS_PATTERN % self.user_id) as f:
            actual = f.read()
        self.assertEqual(0, self.position1)
        self.assertEqual(len(self.line1), self.position2)
        self.assertEqual(expected, actual)

    def test_remove_user_middle(self):
        expected = self.line1 + self.line3 + self.line4
        diff = self.controls.remove_user(self.user_id, self.position2)
        with open(env.SECRETS_PATTERN % self.user_id) as f:
            actual = f.read()
        self.assertEqual(len(self.line2), diff)
        self.assertEqual(expected, actual)

    def test_remove_user_last(self):
        expected = self.line1 + self.line2 + self.line3
        diff = self.controls.remove_user(self.user_id, self.position4)
        with open(env.SECRETS_PATTERN % self.user_id) as f:
            actual = f.read()
        self.assertEqual(len(self.line4), diff)
        self.assertEqual(expected, actual)

    def test_remove_user_end_file(self):
        expected = self.line1 + self.line2 + self.line3 + self.line4
        diff = self.controls.remove_user(self.user_id, self.position4 + len(self.line4))
        with open(env.SECRETS_PATTERN % self.user_id) as f:
            actual = f.read()
        self.assertEqual(0, diff)
        self.assertEqual(expected, actual)

    def test_remove_user_out_of_scope(self):
        expected = self.line1 + self.line2 + self.line3 + self.line4
        diff = self.controls.remove_user(self.user_id, self.position4 + len(self.line4) + 1)
        with open(env.SECRETS_PATTERN % self.user_id) as f:
            actual = f.read()
        self.assertIsNone(diff)
        self.assertEqual(expected, actual)

    def test_set_password_equals(self):
        password = self.pass2[::-1]  # reversed str
        line2 = self.line_pattern % (to_hex(self.user2), to_hex(password))
        expected = self.line1 + line2 + self.line3 + self.line4
        diff = self.controls.set_password(self.user_id, self.position2, password)
        with open(env.SECRETS_PATTERN % self.user_id) as f:
            actual = f.read()
        self.assertEqual(0, diff)
        self.assertEqual(expected, actual)

    def test_set_password_greater(self):
        password = 'long_password'
        line2 = self.line_pattern % (to_hex(self.user2), to_hex(password))
        expected = self.line1 + line2 + self.line3 + self.line4
        diff = self.controls.set_password(self.user_id, self.position2, password)
        with open(env.SECRETS_PATTERN % self.user_id) as f:
            actual = f.read()
        self.assertEqual(len(to_hex(password)) - len(to_hex(self.pass2)), diff)
        self.assertEqual(expected, actual)

    def test_set_password_less(self):
        password = 'pass'
        line2 = self.line_pattern % (to_hex(self.user2), to_hex(password))
        expected = self.line1 + line2 + self.line3 + self.line4
        diff = self.controls.set_password(self.user_id, self.position2, password)
        with open(env.SECRETS_PATTERN % self.user_id) as f:
            actual = f.read()
        self.assertEqual(len(to_hex(password)) - len(to_hex(self.pass2)), diff)
        self.assertEqual(expected, actual)

    def test_set_password_out_of_range(self):
        expected = self.line1 + self.line2 + self.line3 + self.line4
        diff = self.controls.set_password(self.user_id, self.position4 + len(self.line4), 'password')
        with open(env.SECRETS_PATTERN % self.user_id) as f:
            actual = f.read()
        self.assertIsNone(diff)
        self.assertEqual(expected, actual)

    def test_set_username_equals(self):
        username = self.user2[::-1]  # reversed str
        line2 = self.line_pattern % (to_hex(username), to_hex(self.pass2))
        expected = self.line1 + line2 + self.line3 + self.line4
        diff = self.controls.set_username(self.user_id, self.position2, username)
        with open(env.SECRETS_PATTERN % self.user_id) as f:
            actual = f.read()
        self.assertEqual(0, diff)
        self.assertEqual(expected, actual)

    def test_set_username_greater(self):
        username = 'long_username'
        line2 = self.line_pattern % (to_hex(username), to_hex(self.pass2))
        expected = self.line1 + line2 + self.line3 + self.line4
        diff = self.controls.set_username(self.user_id, self.position2, username)
        with open(env.SECRETS_PATTERN % self.user_id) as f:
            actual = f.read()
        self.assertEqual(len(to_hex(username)) - len(to_hex(self.user2)), diff)
        self.assertEqual(expected, actual)

    def test_set_username_less(self):
        username = 'user'
        line2 = self.line_pattern % (to_hex(username), to_hex(self.pass2))
        expected = self.line1 + line2 + self.line3 + self.line4
        diff = self.controls.set_username(self.user_id, self.position2, username)
        with open(env.SECRETS_PATTERN % self.user_id) as f:
            actual = f.read()
        self.assertEqual(len(to_hex(username)) - len(to_hex(self.user2)), diff)
        self.assertEqual(expected, actual)

    def test_set_username_out_of_range(self):
        expected = self.line1 + self.line2 + self.line3 + self.line4
        diff = self.controls.set_username(self.user_id, self.position4 + len(self.line4), 'username')
        with open(env.SECRETS_PATTERN % self.user_id) as f:
            actual = f.read()
        self.assertIsNone(diff)
        self.assertEqual(expected, actual)

    def test_get_account(self):
        user = self.controls.get_account(self.user_id, self.position2)
        self.assertIsNotNone(user)
        self.assertEqual(self.user2, user[0])
        self.assertEqual(self.pass2, user[1])

    def test_get_account_out_of_range(self):
        user = self.controls.get_account(self.user_id, self.position4 + len(self.line4))
        self.assertIsNone(user)

    def test_get_accounts(self):
        users = self.controls.get_accounts(self.user_id, self.position1, self.position4)
        self.assertEqual(self.user1, users[0][0])
        self.assertEqual(self.pass1, users[0][1])
        self.assertEqual(self.user4, users[1][0])
        self.assertEqual(self.pass4, users[1][1])


if __name__ == '__main__':
    unittest.main()
