"""
CI environment-based version information manager
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
from pykrete.args import environ
from .version import Version
from .ci_io import CiIo
from .ci_revision import CiRevision


class CiVersion(Version):
    """Handle version in CI environment
    Version parts are read from CI variables CI_VERSION_MAJOR, CI_VERSION_MINOR and CI_PIPELINE_IID
    Revision is read from CI_COMMIT_REF_NAME, CI_MERGE_REQUEST_TITLE and CI_JOB_NAME:
        Release - in master branch and job's name doesn't contain '_rc_'
        RC - in non-WIP merge request, or in master branch with a job who'se name contains '_rc_'
        Beta - in merge request with 'WIP' in the title
        Alpha - none of the above
    """
    def __init__(self, ci_reader=environ, ci_spec=None):
        """Initializes this instance from CI environment

        :param ci_reader: (ci_variable, role)=>value function [see pykrete.args.environ behavior]
        :param ci_spec: dictionary of part to CI variable
         (parts are: 'major version', 'minor version', 'build version', 'branch name',
          'merge request title')
        """
        ci_io = CiIo(ci_reader, ci_spec)
        revision_type = CiRevision(ci_io).revision_type
        super().__init__(major=ci_io.read_env('major version'),
                         minor=ci_io.read_env('minor version'),
                         revision=revision_type.value,
                         build=ci_io.read_env('build version'),
                         revision_type=revision_type)
