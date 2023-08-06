"""
Pykrete packages tests
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""

import unittest
import logging
from pykrete.packages import PythonPackage
from .helpers import get_full_path


class PythonPackageTestCase(unittest.TestCase):
    """Unit tests for pykrete's args module
    """

    _logger = logging.getLogger(__name__)

    def test_release_version_good(self):
        """Verifies reading of a release package's version
        """
        self._assert_good_package('african_swallow', '12.34.56')

    def test_rc_version_good(self):
        """Verifies reading of a release-candidate package's version
        """
        self._assert_good_package('european_swallow', '12.34rc56')

    def test_missing_version_in_file(self):
        """Verifies handling of a bad version file
        """
        with self.assertRaises(IOError):
            self._logger.debug(str(PythonPackage(get_full_path('a_duck'))))

    def test_missing_version_file(self):
        """Verifies handling of a missing version file
        """
        with self.assertRaises(FileNotFoundError):
            self._logger.debug(str(PythonPackage(get_full_path('a_witch'))))

    def _assert_good_package(self, project, expected_version):
        """Assert version as expected"""
        target = PythonPackage(get_full_path(project))
        self.assertEqual(expected_version, target.version, 'Wrong version read')


if __name__ == '__main__':
    unittest.main()
