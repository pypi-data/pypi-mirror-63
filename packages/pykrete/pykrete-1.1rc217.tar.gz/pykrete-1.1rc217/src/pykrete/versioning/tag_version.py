"""
GIT tag-based version information manager
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import re
from pykrete.args import environ
from pykrete.repo import Git
from .revision_type import RevisionType
from .version import Version
from .ci_io import CiIo
from .ci_revision import CiRevision


class TagVersion(Version):
    """Handle version in CI environment
    A version is constructed from the last version tag (tag name format '<major>.<minor>.<build>'
     indicating a release version, with a message format of 'ci_base_build <build>' indicating the
     CI build number for the first release with this major-minor combo). In the case of a release,
     any following tag named 'bump_major' will increment the major version (at most once), otherwise
     any following tag named 'bump_minor' will increment the minor version (at most once).
    Build is calculated as the current CI project-build# variable, minus the build specified in the
     last version tag's message if this isn't a release, or 0 if it is a release.
    Revision is read from the CI environment variables CI_COMMIT_REF_NAME, CI_MERGE_REQUEST_TITLE
     and CI_JOB_NAME:
        Release (4) - master branch on a job who'se name doesn't contain '_rc_'
        RC (3) - non-WIP merge request, master branch on a job who'se name contains '_rc_'
        Beta (2) - merge request with 'WIP' in the title
        Alpha (1) - none of the above
    """
    def __init__(self, repo=Git(), ci_reader=environ, ci_spec=None):
        """Initializes this instance from CI environment

        :param repo: project's repository (optional, defaults to git for the current folder)
        :param ci_reader: (ci_variable, role)=>value function
         [see pykrete.args.environ behavior]
        :param ci_spec: dictionary of part to CI variable
         (parts are: 'major version', 'minor version', 'build version', 'branch name',
          'merge request title')
        """
        self.__ci_io = CiIo(ci_reader, ci_spec)
        self.__repo = repo
        self.__tags = self.__read_tags()
        self.__revision = CiRevision(self.__ci_io)
        self.__base_build = 0
        (major, minor, build) = self.__read_version_from_tags()
        super().__init__(major=major,
                         minor=minor,
                         revision=self.__revision.revision_type.value,
                         build=build,
                         revision_type=self.__revision.revision_type)

    def __read_tags(self):
        return self.__repo.get_tags_from(pattern=r'(\d+\.){2}\d+', is_must=False)

    def __read_version_from_tags(self):
        last_version_tag = self.__tags[0] if self.__tags else None
        version_parts, self.__base_build =\
            self.__get_version_parts_and_base_build_from(last_version_tag)
        version_parts = self.__advance_version(version_parts)
        return tuple(version_parts)

    @staticmethod
    def __get_version_parts_and_base_build_from(tag):
        if not tag:
            return [0, 0, 0], 0
        version_parts = [int(part) for part in tag[0].split('.')]
        message_build = re.findall(r'ci_base_build (\d+)', tag[1]) if tag[1] else None
        base_build = int(message_build[0]) if message_build else 0
        return version_parts, base_build

    def __advance_version(self, version_parts):
        ci_build = int(self.__ci_io.read_env('build version'))
        if self.__revision.revision_type != RevisionType.Release:
            return self.__advance_build_relative_to_base_build(version_parts, ci_build)
        return self.__advance_major_minor_from_last_change_details(version_parts, ci_build)

    def __advance_build_relative_to_base_build(self, version_parts, ci_build):
        version_parts[2] += ci_build - self.__base_build
        return version_parts

    def __advance_major_minor_from_last_change_details(self, version_parts, ci_build):
        change_details = self.__repo.get_head_change().details
        if '#major' in change_details:
            return [version_parts[0] + 1, 0, 0]
        if '#minor' in change_details:
            return [version_parts[0], version_parts[1] + 1, 0]
        return self.__advance_build_relative_to_base_build(version_parts, ci_build)
