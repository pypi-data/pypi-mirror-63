"""
Build manager base class
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import logging
from abc import abstractmethod
from pykrete.args import environ
from pykrete.builder.info.build_info import BuildInfo


class BuildManager:
    """Manages building a python package"""

    _logger = logging.getLogger(__name__)

    def __init__(self, build_info: BuildInfo):
        """Initializes this instance
        :type build_info: Build info
        """
        self._info = build_info
        self._project = environ('CI_TARGET', 'the name of the project under src')

    def run(self):
        """Runs the build process"""
        self._clean_distribution()
        self._set_package_version()
        self._build()
        if not self._info.upload:
            self._logger.info('Upload skipped')
            return
        self._upload()

    @abstractmethod
    def _clean_distribution(self):
        """Removes previous distribution files"""

    @abstractmethod
    def _set_package_version(self):
        """Sets the package version in the project's version file"""

    @abstractmethod
    def _build(self):
        """Performs the actual build using setup.py"""

    @abstractmethod
    def _upload(self):
        """Uploads the package"""

    def __str__(self):
        """Gets a string representation of this object"""
        return f'{self._info} of project "{self._project}"'
