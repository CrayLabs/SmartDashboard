# BSD 2-Clause License
#
# Copyright (c) 2021-2024, Hewlett Packard Enterprise
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


class SSDashboardError(Exception):
    """Exception base class for displaying SmartDashboard exceptions"""

    def __init__(self, title: str, file: str, exception: Exception) -> None:
        """Initialize an SSDashboardError

        :param title: Title of the exception displayed in the dashboard
        :type title: str
        :param file: File associated with the exception to be displayed in the dashboard
        :type file: str
        :param exception: Exception caught to be displayed in the dashboard
        :type exception: Exception
        """
        super().__init__(title)
        self.title = title
        self.file = file
        self.exception = exception

    def __str__(self) -> str:
        """Return string representation of the exception

        :return: String representation of the exception
        :rtype: str
        """
        return f"{type(self).__name__}: {self.title}"


class ManifestError(SSDashboardError):
    """Exception raised for errors related to the manifest"""


class MalformedManifestError(ManifestError):
    """Exception raised for errors related to malformations of the manifest"""


class VersionIncompatibilityError(SSDashboardError):
    """Exception raised for errors related to version
    incompatibilities of the manifest"""
