"""
Pykrete versioning.tag_version tests
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""

import unittest
import logging
from pykrete.versioning import TagVersion, RevisionType, Version
from pykrete.repo import Change
from .versioning import PykreteVersioningTestCase
from .repo_testbed import RepoTestbed


class PykreteVersioningTagVersionTestCase(PykreteVersioningTestCase):
    """Unit tests for pykrete's versioning module's TagVersion class
    """

    _logger = logging.getLogger(__name__)

    def test_tag_version_server(self):
        """Verifies handling of CI-environment version
        NOTE: THIS TEST WILL FAIL LOCALLY, SAFE TO IGNORE
        """
        self._logger.info('NOTE: THIS TEST WILL FAIL LOCALLY, SAFE TO IGNORE')
        self._assert_version_pattern(TagVersion())

    def test_tag_version_local_alpha_no_tags(self):
        """Verifies handling of no simulated tags present"""
        self._assert_tag_version_local(
            spec={'build version': '3',
                  'branch name': 'custom',
                  'merge request title': 'None'},
            tags=[None],
            change_details="",
            expected_version=Version((0, 0, 1, 3, RevisionType.Alpha)))

    def test_tag_version_local_alpha_first_minor_bump(self):
        """Verifies handling of simulated minor bump without a previous release on non-release"""
        self._assert_tag_version_local(
            spec={'build version': '4',
                  'branch name': 'custom',
                  'merge request title': 'None'},
            tags=[None],
            change_details="this won't cause a #minor bump",
            expected_version=Version((0, 0, 1, 4, RevisionType.Alpha)))

    def test_tag_version_local_release_first_minor_bump(self):
        """Verifies handling of simulated minor bump without a previous release on release"""
        self._assert_tag_version_local(
            spec=self._make_release_spec_for_build('4'),
            tags=[None],
            change_details="this will cause a #minor bump",
            expected_version=Version((0, 1, 4, 0, RevisionType.Release)))

    def test_tag_version_local_beta_major_bump(self):
        """Verifies handling of simulated major bump after a previous release on non-release"""
        self._assert_tag_version_local(
            spec={'build version': '111',
                  'branch name': 'custom',
                  'merge request title': 'WIP: something'},
            tags=[('0.7.56', 'ci_base_build 106')],
            change_details="this won't cause a #major bump",
            expected_version=Version((0, 7, 2, 61, RevisionType.Beta)))

    def test_tag_version_local_release_major_bump(self):
        """Verifies handling of simulated major bump after a previous release on release"""
        self._assert_tag_version_local(
            spec=self._make_release_spec_for_build(111),
            tags=[('0.7.56', 'ci_base_build 106')],
            change_details="this will cause a #major bump",
            expected_version=Version((1, 0, 4, 0, RevisionType.Release)))

    def test_tag_version_local_rc_disabled_bump_on_merge_request(self):
        """Verifies handling of simulated minor after major bump after a previous release
        on non-release
        """
        self._assert_tag_version_local(
            spec={'build version': '1234',
                  'branch name': 'custom',
                  'merge request title': 'something'},
            tags=[('1.2.34', 'ci_base_build 1198')],
            change_details="this won't cause a #minor not a #major bump",
            expected_version=Version((1, 2, 3, 70, RevisionType.RC)))

    def test_tag_version_local_rc_disabled_bump_on_master(self):
        """Verifies handling of simulated minor after major bump after a previous release
        on non-release
        """
        self._assert_tag_version_local(
            spec={'build version': '1234',
                  'branch name': 'custom',
                  'merge request title': 'something',
                  'job name': 'some_rc_job'},
            tags=[('1.2.34', 'ci_base_build 1198')],
            change_details="this won't cause a #minor not a #major bump",
            expected_version=Version((1, 2, 3, 70, RevisionType.RC)))

    def test_tag_version_local_release_minor_and_major_bumps(self):
        """Verifies handling of simulated minor after major bump after a previous release
        on release where only the major bump should be used
        """
        self._assert_tag_version_local(
            spec=self._make_release_spec_for_build('1234'),
            tags=[('1.2.34', 'ci_base_build 1198')],
            change_details="this won't cause a #minor but a #major bump",
            expected_version=Version((2, 0, 4, 0, RevisionType.Release)))

    @staticmethod
    def _make_release_spec_for_build(build):
        return {'build version': build,
                'branch name': 'master',
                'merge request title': 'None',
                'job name': 'some_job'}

    def _assert_tag_version_local(self, spec, tags, change_details, expected_version):
        change = Change()
        change.append_details(change_details)
        repo = RepoTestbed(tags, change)
        target = TagVersion(repo, self._echo, spec)
        self._assert_version_pattern(target)
        self.assertEqual(expected_version, target,
                         f'version not as expected: should be {expected_version}')


if __name__ == '__main__':
    unittest.main()
