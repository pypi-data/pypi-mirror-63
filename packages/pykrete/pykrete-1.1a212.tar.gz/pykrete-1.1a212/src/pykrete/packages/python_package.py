"""
Python package
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
from pkg_resources import require
from pykrete.versioning import Formatting, TagVersion, VersionPyVersion


class PythonPackage:
    """Python package"""

    @property
    def project(self):
        """
        :return: (string) name of project package under 'src'.
        """
        return self._project

    @property
    def version(self):
        """
        :return: (string) The project's version
        """
        return self._version

    def __init__(self, project, package_fallback=False):
        """Initializes this instance to analyze the specified project

        :param project: name of project package under 'src'
        """
        self._project = project
        self._package_fallback = package_fallback
        self._version = self._get_version()

    @property
    def long_description(self):
        """Gets the contents of the README.md file

        :return: Long description
        """
        with open('README.md', 'r') as readme:
            return readme.read()

    def _get_version(self):
        """Gets the package version

        :return: The version
        :exception IndexError: Version not found
        :exception IOError: Version read failed
        """
        try:
            version = TagVersion()
        except SystemError:
            try:
                version = VersionPyVersion(self._project)
            except IOError:
                if not self._package_fallback:
                    raise
                version_from_current_package = require(self._project)[0].version
                return version_from_current_package
        return Formatting(version).for_python

    def __str__(self):
        return f'{self._project} v{self._version}'
