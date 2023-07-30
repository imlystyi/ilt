# ilt - insert license text
# Copyright (C) 2023  imlystyi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
A module with the special exceptions of the "ilt" application.

"""


class FileException(Exception):
    """
    Occurs if an error occurred while accessing, reading, or writing to the file.
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class LicenseNameException(Exception):
    """
    Occurs if a license with that name could not be found in the list of available licenses.
    """
    def __init__(self, license_name):
        self.message = f'There are no license with the "{license_name}" name.'
        super().__init__(self.message)
