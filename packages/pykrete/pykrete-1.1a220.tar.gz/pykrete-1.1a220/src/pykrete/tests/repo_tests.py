"""
Pykrete repo tests
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""

import unittest
import logging
from pykrete.repo import Git
from .helpers import get_full_path


class PythonRepoTestCase(unittest.TestCase):
    """Unit tests for pykrete's repo module
    """

    _logger = logging.getLogger(__name__)

    def test_get_all_tags(self):
        """Verifies getting all tags from repo
        """
        self._assert_get_tags(lambda git: git.get_all_tags(),
                              ('1.0.0', None), ('1.0.1', 'bug fix'))

    def test_get_tags_from_existing(self):
        """Verifies getting all tags from repo starting from a specific tag
        """
        self._assert_get_tags(lambda git: git.get_tags_from(r'.*?0\.1', True),
                              ('1.0.1', 'bug fix'))

    def test_get_tags_from_must_but_non_existing(self):
        """Verifies getting all tags from repo
        """
        with self.assertRaises(KeyError):
            self._assert_get_tags(lambda git: git.get_tags_from(r'no such tag', True))

    def test_get_tags_from_non_must_non_existing(self):
        """Verifies getting all tags from repo
        """
        self._assert_get_tags(lambda git: git.get_tags_from(r'no such tag', False),
                              None, ('1.0.0', None), ('1.0.1', 'bug fix'))

    def test_get_head_change(self):
        """Verifies a non-empty head-change returned from repo"""
        target = self._make_target()
        change = target.get_head_change()
        self.assertIsNotNone(change, 'empty change returned')
        self._logger.debug(change)
        self.assertIsNotNone(change.log, 'empty log returned')
        self.assertIsNotNone(change.details, 'empty log returned')

    def _assert_get_tags(self, getter, *expected):
        """Verifies tags from repo

        :param getter: tag getter (lambda on Git object)
        :param expected: expected returned tags
        :return:
        """
        target = self._make_target()
        tags = getter(target)
        self._logger.debug(tags)
        self.assertTrue(tags, 'Got empty tags')
        self.assertTrue(len(tags) >= len(expected), 'too few tags returned')
        for test in zip(expected, tags):
            self.assertEqual(test[0], test[1], 'wrong tag returned')

    @staticmethod
    def _make_target():
        test_repo_path = get_full_path('git-tag-example', True)
        return Git(test_repo_path)


if __name__ == '__main__':
    unittest.main()
