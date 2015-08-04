#!/usr/bin/env python

import os
import shutil
import tempfile
from unittest import TestCase
from coverage_tools import utils
from coverage.misc import file_be_gone

class CombineTestCase(TestCase):
    def setUp(self):
        dummy, self.output_file = tempfile.mkstemp()

        dummy, self.cov_data_1 = tempfile.mkstemp()
        shutil.copy(os.path.abspath('tests/data/coverage.3x.1'), self.cov_data_1)

        dummy, self.cov_data_2 = tempfile.mkstemp()
        shutil.copy(os.path.abspath('tests/data/coverage.3x.2'), self.cov_data_2)


    def tearDown(self):
        file_be_gone(self.output_file)
        file_be_gone(self.cov_data_1)
        file_be_gone(self.cov_data_2)

class BasicCombineTestCase(CombineTestCase):
    def test_combine(self):
        """
            This is a basic test to execute the combine
            function with different coverage versions.
        """
        utils.combine([self.cov_data_1, self.cov_data_2], self.output_file)


if __name__ == "__main__":
    unittest.main()
