import unittest
# import os
import shutil
from beatrix_kiddo.scratch import scaffold_project, be_build
from beatrix_kiddo.utils import process_fields


class ScaffoldingProjectTest(unittest.TestCase):
    def test_correct_scaffolding(self):
        self.assertTrue(scaffold_project(be_build))

    def test_receive_models(self):
        self.assertGreaterEqual(len(be_build['models']), 2)

    def tearDown(self):
        shutil.rmtree('undefinedxD')


if __name__ == '__main__':
    unittest.main()
