import unittest
from utils import write_on_views, edit_settings_py

# consts
TEST_DATA = {
                'app_name': 'notetaking',
                'models': [
                    {'Notes': ["message(TextField[max_length=300])",
                               "time_created(DateTimeField"
                               "[auto_now=True])"]},
                    {'Users': ["fullname(CharField[max_length=300])",
                               "nickname(CharField[max_length=300])"]}
                ]
            }


class UtilsTest(unittest.TestCase):
    def test_write_on_views(self):
        self.assertEqual(write_on_views(TEST_DATA), None)

    def test_edit_settings_py(self):
        self.assertEqual(edit_settings_py(TEST_DATA), None)


if __name__ == '__main__':
    unittest.main()
