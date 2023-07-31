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
A simple shell for the "ilt" application.

"""
import iltlib as lib
from cmd import Cmd
from enum import Enum
from re import findall
from iltexceptions import *


class Shell(Cmd):
    """
    A concise command interpreter class for the "ilt" application, inherited from the Cmd class.

    """

    # region Fields

    _IGNORE_DIRS_KEY = '-d'
    _IGNORE_EXTS_KEY = '-e'
    _NO_UNKNOWN_EXTS_LIST_KEY = '-u'
    _NO_FILES_LIST_KEY = '-f'
    _SPECIAL_EXTS_MODE = 'ext'
    _SPECIAL_FILE_MODE = 'file'

    ruler = '-'
    about = f"""
About application
{ruler * 100}
ilt  Copyright (C) 2023  imlystyi
This program comes with ABSOLUTELY NO WARRANTY; for details see a1.
This is free software, and you are welcome to redistribute it
under certain conditions; see a2 for details.

a1.
THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE LAW. 
EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES 
PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, 
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS 
FOR A PARTICULAR PURPOSE. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE 
PROGRAM IS WITH YOU. SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF 
ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

a2.
You may make, run and propagate covered works that you do not convey, without conditions so 
long as your license otherwise remains in force. You may convey covered works to others for 
the sole purpose of having them make modifications exclusively for you, or provide you with 
facilities for running those works, provided that you comply with the terms of this License 
in conveying all material for which you do not control copyright. Those thus making or running 
the covered works for you must do so exclusively on your behalf, under your direction and control,
on terms that prohibit them from making any copies of your copyrighted material outside their 
relationship with you.\n
"""
    intro = 'Welcome to ilt v2.\nType "help" to list commands.\n'
    nohelp = '[ERROR] There is no help on %s.'
    prompt = '> '

    # endregion

    # region Nested classes

    class _MessageType(Enum):
        NO_JAW = 0
        SUCCESS = 1
        WARNING = 2
        UNKNOWN_SYNTAX = 3
        ERROR = 4

    # endregion

    # region Methods

    def default(self, message: str, message_type=_MessageType.UNKNOWN_SYNTAX) -> None:
        """
        Called on an input line when an error occurs.
        :param message: Message to display.
        :param message_type: Message type.

        """
        match message_type:
            case self._MessageType.UNKNOWN_SYNTAX:
                self.stdout.write(f'[ERROR] Unknown syntax: {message}\n')
            case self._MessageType.ERROR:
                self.stdout.write(f'[ERROR] {message}\n')
            case _:
                self.stdout.write(f'[ERROR] Unexpected message.\n')

    def result(self, message: str, message_type=_MessageType.SUCCESS) -> None:
        """
        Called on an input line to display the result.
        :param message: Message to display.
        :param message_type: Message type.

        """
        match message_type:
            case self._MessageType.NO_JAW:
                self.stdout.write(f'{message}\n')
            case self._MessageType.SUCCESS:
                self.stdout.write(f'[SUCCESS] {message}\n')
            case self._MessageType.WARNING:
                self.stdout.write(f'[WARNING] {message}\n')
            case _:
                self.stdout.write(f'[ERROR] Unexpected message.\n')

        return

    def help_help(self) -> None:
        """
        Displays help to "help" command.

        """
        self.stdout.write('List available commands with "help" or detailed help with "help <topic>".\n')

    def do_about(self, args: str):
        """
        Command that displays information about the program on the screen.

        """
        params, keys = self._get_params_(args), self._get_keys(args)

        if len(params) > 0:
            self.default('This command has no parameters.', self._MessageType.ERROR)
        elif len(keys) > 0:
            self.default('This command has no keys.', self._MessageType.ERROR)
        else:
            self.stdout.write(self.about)

    def help_about(self):
        """
        Displays help to "about" command.

        """
        self.stdout.write('Displays information about the application.\n')

    def do_auto(self, args: str):
        """
        Command that allows you to do the automatic license text inserting.

        """
        params, keys = self._get_params_(args), self._get_keys(args)
        allowed_keys = self._IGNORE_DIRS_KEY, self._IGNORE_EXTS_KEY, \
            self._NO_FILES_LIST_KEY, self._NO_UNKNOWN_EXTS_LIST_KEY

        if any(key not in allowed_keys for key in keys):
            self.default('Incorrect keys.', self._MessageType.ERROR)

        license_name, path, year, copyright_owner, special_line = '', '', '', '', ''
        ignored_exts = None
        ignored_dirs = None

        match len(params):
            case 5:  # No ignored extensions/directories.
                license_name = params[0]
                path = params[1]
                year = params[2]
                copyright_owner = params[3]
                special_line = params[4]
            case 6:  # Ignored extensions or directories exist (one thing).
                license_name = params[0]
                path = params[1]
                year = params[2]
                copyright_owner = params[3]
                special_line = params[4]
                if self._IGNORE_DIRS_KEY in keys and len(params) == 6:
                    ignored_dirs = self._get_ignored_dirs(params[5])
                elif self._IGNORE_EXTS_KEY in keys and len(params) == 6:
                    ignored_exts = self._get_ignored_exts(params[5])
            case 7:  # Ignored extensions and directories exist (both).
                license_name = params[0]
                path = params[1]
                year = params[2]
                copyright_owner = params[3]
                special_line = params[4]
                ignored_dirs = self._get_ignored_dirs(params[5])
                ignored_exts = self._get_ignored_exts(params[6])
            case value if value < 6:
                self.default('Too few parameters.', self._MessageType.ERROR)
                return
            case value if value > 7:
                self.default('Too many parameters.', self._MessageType.ERROR)
                return

        try:
            license_text = lib.get_license_text(license_name, year, copyright_owner, special_line)
        except LicenseNameException as exception:
            self.default(exception.message, self._MessageType.ERROR)
            return

        try:
            success, unknown_exts = lib.auto_insert(license_text, path, ignored_exts, ignored_dirs)

            if len(success) > 0:
                self.result('ilt has done inserting license texts.', self._MessageType.SUCCESS)

                if self._NO_FILES_LIST_KEY not in keys:
                    self.result('List of formatted files: ', self._MessageType.NO_JAW)
                    self._display_items(success)
            else:
                self.result('ilt could not find any matching files.', self._MessageType.WARNING)

            if self._NO_UNKNOWN_EXTS_LIST_KEY not in keys and len(unknown_exts) > 0:
                self.result('ilt encountered unknown extensions.', self._MessageType.WARNING)
                self.result('List of unknown extensions: ', self._MessageType.NO_JAW)
                self._display_items(unknown_exts)

            return
        except FileException as exception:
            self.default(exception.message, self._MessageType.ERROR)
            return

    def help_auto(self) -> None:
        """
        Displays help to "auto" command.

        """
        self.stdout.write('''*** Summary:
    Automatically inserts the license text into files in the specified root folder.
*** Format: 
    auto <license_name> "<path>" <year> "<copyright_holder>" "<special_line>" "<ignored_dirs>" "<ignored_exts>" <keys>
*** Parameters:
    <license_name>: license name - must be without quotes. Enter "licenses" to display all licenses;
    <path>: path to the root folder - must be in double quotes;
    <year>: year to be inserted in the license text - must be without quotes. Enter 0 if you don't 
    need it;
    <copyright_holder>: copyright holder name to be inserted into the license text. - must be double-quoted. Enter empty 
    quotes ("") if you don't need it;
    <special_line>: special line to be inserted into the license text. Enter empty quotes ("") if you don't need it;
    <ignored_dirs> (optionally, enter the "-d" key): list of directories files in that will not be formatted - 
    must be in double quotes. Ignores the subdirectories too. Each directory name must be separated by a space.
    <ignored_exts> (optionally, enter the "-e" key): list of file extensions that will not be formatted - 
    must be in double quotes. Each extension must be separated by a space.
*** Keys:
    -d: enable directories ignoring;
    -e: enable extensions ignoring;
    -u: will not list unknown extensions at the end;
    -f: will not list formatted files at the end.
*** Example:
    * without ignored directories and files (with "-c" and "-s" keys):
        auto lgpl "C:\\Code" 2023 "imlystyi" "ilt - insert license text!" -c -s
    * with ignored directories and files (with "-d" and "-e" keys and ignored directories and extensions):
        auto lgpl "C:\\Code" 2023 "imlystyi" "ilt - insert license text!" ".idea tsProj" ".js .c .cpp" -d -e\n''')

    def do_exit(self, args: str) -> None:
        """
        Command that exits the application.

        """
        params, keys = self._get_params_(args), self._get_keys(args)

        if len(params) > 0:
            self.default('This command has no parameters.', self._MessageType.ERROR)
            return
        elif len(keys) > 0:
            self.default('This command has no keys.', self._MessageType.ERROR)
            return
        else:
            exit(0)

    def help_exit(self) -> None:
        """
        Displays help to "exit" command.

        """
        self.stdout.write('Exits the application.\n')

    def do_licenses(self, args: str) -> None:
        """
        Command that displays a list of all available licenses on the screen.

        """
        params, keys = self._get_params_(args), self._get_keys(args)

        if len(params) > 0:
            self.default('This command has no parameters.', self._MessageType.ERROR)
            return
        elif len(keys) > 0:
            self.default('This command has no keys.', self._MessageType.ERROR)
            return
        else:
            self._display_items(lib.LICENSES)

    def help_licenses(self) -> None:
        """
        Displays help to "licenses" command.

        """
        self.stdout.write('Displays a list of all available licenses on the screen.\n')

    def do_special(self, args: str) -> None:
        """
        Command that allows you to do special license text inserting.

        """
        params, keys = self._get_params_(args), self._get_keys(args)
        allowed_mods = self._SPECIAL_EXTS_MODE, self._SPECIAL_FILE_MODE
        allowed_keys = self._IGNORE_DIRS_KEY, self._NO_FILES_LIST_KEY

        if any(key not in allowed_keys for key in keys):
            self.default('Incorrect keys.', self._MessageType.ERROR)

        license_name, path, ext, comment, year, copyright_owner, special_line = '', '', '', '', '', '', ''
        ignored_dirs = None

        mode = params[0]

        if mode not in allowed_mods:
            self.default('Incorrect mode.')

        match mode:
            case self._SPECIAL_EXTS_MODE:
                if len(params) < 8:
                    self.default('Too few parameters.', self._MessageType.ERROR)
                    return
                elif len(params) > 9:
                    self.default('Too many parameters.', self._MessageType.ERROR)
                    return
                else:
                    license_name = params[1]
                    path = params[2]
                    ext = params[3]
                    comment = params[4]
                    year = params[5]
                    copyright_owner = params[6]
                    special_line = params[7]

                    if self._IGNORE_DIRS_KEY in keys and len(params) > 9:
                        ignored_dirs = self._get_ignored_dirs(params[8])
            case self._SPECIAL_FILE_MODE:
                if len(params) < 7:
                    self.default('Too few parameters.', self._MessageType.ERROR)
                elif len(params) > 7:
                    self.default('Too many parameters.', self._MessageType.ERROR)
                license_name = params[1]
                path = params[2]
                comment = params[3]
                year = params[4]
                copyright_owner = params[5]
                special_line = params[6]

        try:
            license_text = lib.get_license_text(license_name, year, copyright_owner, special_line)
        except LicenseNameException as exception:
            self.default(exception.message, self._MessageType.ERROR)
            return

        try:
            if mode == self._SPECIAL_FILE_MODE:
                _ = lib.special_file_insert(license_text, path, comment)
                self.result('ilt has done inserting license text.', self._MessageType.SUCCESS)
                return
            else:
                success = lib.special_ext_insert(license_text, path, ext, comment, ignored_dirs)

                if len(success) > 0:
                    self.result('ilt has done inserting license text.', self._MessageType.SUCCESS)

                    if self._NO_FILES_LIST_KEY not in keys:
                        self.result('List of formatted files: ', self._MessageType.NO_JAW)
                        self._display_items(success)
                else:
                    self.result('ilt could not find files with the specified extension.', self._MessageType.WARNING)

                return
        except FileException as exception:
            self.default(exception.message, self._MessageType.ERROR)
            return

    def help_special(self) -> None:
        """
        Displays help to "special" command.

        """
        self.stdout.write('''*** Summary:
    Inserts the license text into the specified file or files with the specified extension.
*** Format: 
    * inserting into a specified file:
        special file <license_name> "<path>" "<comments_format>" <year> "<copyright_holder>" "<special_line>"
    * inserting into the files with the specified extension:
        special ext <license_name> "<path>" "<ext>" "<comments_format>" <year> "<copyright_holder>" "<special_line>" 
        "<ignored_folders>"
*** Parameters:
    <license_name>: license name - must be without quotes. Enter "licenses" to display all licenses;
    <path>: path to the root folder or to the specified file - must be in double quotes;
    <ext>: specified file extension - must be in double quotes;
    <comments_format>: comment format in this file or files with the specified extension - must be in double quotes;
    <year>: year to be inserted in the license text - must be without quotes. Enter 0 if you don't 
    need it;
    <copyright_holder>: copyright holder name to be inserted into the license text. - must be double-quoted. Enter empty 
    quotes ("") if you don't need it;
    <special_line>: special line to be inserted into the license text. Enter empty quotes ("") if you don't need it.
    <ignored_dirs> (optionally, enter the "-d" key): list of directories files in that will not be formatted - 
    must be in double quotes. Ignores the subdirectories too. Each directory name must be separated by a space.
*** Keys:
    -d: enable directories ignoring;
    -f: will not list formatted files at the end;
    -u: will not list unknown extensions at the end.    
*** Example:
    * inserting into a specified file:
        special file lgpl "C:\\Code\\code.py" "#" 2023 "imlystyi" "ilt - insert license text!"
    * inserting into the files with the specified extension (without keys):
        special ext lgpl "C:\\Code" ".py" "#" 2023 "imlystyi" "ilt - insert license text!"
    * inserting into the files with the specified extension (with "-d" key and ignored directories):
        special ext lgpl "C:\\Code" ".py" "#" 2023 "imlystyi" "ilt - insert license text!" ".idea tsProj" -d\n''')

    def _display_items(self, items: list):
        for item in items:
            self.stdout.write(item + '\n')

    def _get_ignored_dirs(self, folders: str) -> list[str]:
        return folders.split(' ')

    def _get_ignored_exts(self, exts: str) -> list[str]:
        return exts.split(' ')

    def _get_keys(self, args: str) -> list[str]:
        return [kk for kk in args.split() if kk[0] == '-']

    def _get_params_(self, args: str) -> tuple:
        found = findall(r'"([^"]+)"|(\S+)', args)
        matches = tuple(match[0] or match[1] for match in found)
        return tuple(match for match in matches if match[0] != '-')

    # endregion
