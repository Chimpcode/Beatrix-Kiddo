import unittest
# import os
from utils import process_fields


class ScaffoldingProjectTest(unittest.TestCase):
    def test_getting_fields(self):
        self.assertEqual(process_fields('fieldA(IntegerField[max_length=3])'),
                                       ('fieldA', 'IntegerField',
                                        'max_length=3'))

    def test_getting_fields_with_several_conditions(self):
        self.assertEqual(process_fields('fieldA(IntegerField[max_length=3'
                                        ',null=True])'),
                                       ('fieldA', 'IntegerField',
                                        'max_length=3,null=True'))


if __name__ == '__main__':
    unittest.main()
