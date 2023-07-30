"""
A simple shell for the "ilt" application.
"""
from cmd import Cmd
from enum import Enum
from re import findall
import iltlib as lib
from iltexceptions import *


class Shell(Cmd):
    """
    A concise command interpreter class for the "ilt" application, inherited from the Cmd class.

    """

    # region Fields

    _NO_UNKNOWN_EXT_LIST_KEY = '-e'
    _NO_FILES_LIST_KEY = '-f'

    ruler = '-'
    about = f"""
About application
{ruler * 74}
ilt - insert license text!
This application can help you quickly insert license text into your files.
Version 1.
Copyright (c) 2023 imlystyi, licensed by GPL-3.0.
    """
    intro = 'Welcome to ilt v1.\nType "help" to list commands.\n'
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
            print(self.about)

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
        allowed_keys = self._NO_FILES_LIST_KEY, self._NO_UNKNOWN_EXT_LIST_KEY

        if any(key not in allowed_keys for key in keys):
            self.default('Incorrect keys.', self._MessageType.ERROR)

        license_name, path, year, copyright_owner, special_line = '', '', '', '', ''
        ignored_exts = []

        match len(params):
            case 5:  # No ignored extensions.
                license_name = params[0]
                path = params[1]
                year = params[2]
                copyright_owner = params[3]
                special_line = params[4]
            case 6:  # Ignored extensions exist.
                license_name = params[0]
                path = params[1]
                year = params[2]
                copyright_owner = params[3]
                special_line = params[4]
                ignored_exts = self._get_ignored_exts(params[5])
            case value if value < 5:
                self.default('Too few parameters.', self._MessageType.ERROR)
                return
            case value if value > 6:
                self.default('Too many parameters.', self._MessageType.ERROR)
                return
            case _:
                self.default('Incorrect parameters number.', self._MessageType.ERROR)

        try:
            license_text = lib.get_license_text(license_name, year, copyright_owner, special_line)
        except LicenseNameException as exception:
            self.default(exception.message, self._MessageType.ERROR)
            return

        try:
            success, unknown_exts = lib.auto_insert(license_text, path, ignored_exts)

            if len(success) > 0:
                self.result('ilt has done inserting license texts.', self._MessageType.SUCCESS)

                if self._NO_FILES_LIST_KEY not in keys:
                    self.result('List of formatted files: ', self._MessageType.NO_JAW)
                    self._display_items(success)
            else:
                self.result('ilt could not find any matching files.', self._MessageType.WARNING)

            if self._NO_UNKNOWN_EXT_LIST_KEY not in keys and len(unknown_exts) > 0:
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
    autoins <license_name> "<path>" <year> <copyright_holder> <special_line> <ignored_exts> <keys>
*** Parameters:
    <license_name>: license name - must be without quotes. Enter "licenses" to display all licenses;
    <path>: path to the root folder - must be in double quotes;
    <year>: year to be inserted in the license text - must be without quotes. Enter 0 if you don't 
    need it;
    <copyright_holder>: copyright holder name to be inserted into the license text. - must be double-quoted. Enter empty 
    quotes ("") if you don't need it;
    <special_line>: special line to be inserted into the license text. Enter empty quotes ("") if you don't need it;
    <ignored_exts> (optionally): list of file extensions that will not be formatted - must be in double quotes. Each 
    extension is separated by a space.
*** Keys:
    -e: will not list unknown extensions at the end;
    -f: will not list formatted files at the end.
*** Example:
    * without ignored extensions (with keys):
        auto lgpl "C:\\Code" 2023 "imlystyi" "ilt - insert license text!" -c -s
    * with ignored extensions (without keys):
        auto lgpl "C:\\Code" 2023 "imlystyi" "ilt - insert license text!" ".js .c .cpp"\n''')

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
        allowed_key = self._NO_FILES_LIST_KEY

        if any(key != allowed_key for key in keys):
            self.default('Incorrect keys.', self._MessageType.ERROR)

        license_name, path, ext, comment, year, copyright_owner, special_line = '', '', '', '', '', '', ''

        match len(params):
            case 6:  # Specified file inserting.
                license_name = params[0]
                path = params[1]
                comment = params[2]
                year = params[3]
                copyright_owner = params[4]
                special_line = params[5]
            case 7:  # Specified extension inserting.
                license_name = params[0]
                path = params[1]
                ext = params[2]
                comment = params[3]
                year = params[4]
                copyright_owner = params[5]
                special_line = params[6]
            case value if value < 6:
                self.default('Too few parameters.', self._MessageType.ERROR)
                return
            case value if value > 7:
                self.default('Too many parameters.', self._MessageType.ERROR)
                return
            case _:
                self.default('Incorrect parameters number.', self._MessageType.ERROR)

        try:
            license_text = lib.get_license_text(license_name, year, copyright_owner, special_line)
        except LicenseNameException as exception:
            self.default(exception.message, self._MessageType.ERROR)
            return

        try:
            if ext == '':
                _ = lib.special_file_insert(license_text, path, comment)
                self.result('ilt has done inserting license text.', self._MessageType.SUCCESS)
                return
            else:
                success = lib.special_ext_insert(license_text, path, ext, comment)

                if len(success) > 0:
                    self.result('ilt has done inserting license text.', self._MessageType.SUCCESS)

                    if self._NO_FILES_LIST_KEY not in keys:
                        self.result('List of formatted files: ', self._MessageType.NO_JAW)
                        self._display_items(success)
                else:
                    self.result('ilt could not find files with the specified extension.', self._MessageType.WARNING)

                return
        except FileException as exception:
            self.default(exception.message)
            return

    def help_special(self) -> None:
        """
        Displays help to "special" command.

        """
        self.stdout.write('''*** Summary:
    Inserts the license text into the specified file or files with the specified extension.
*** Format: 
    * inserting into a specified file:
        special <license_name> "<path>" "<comments_format>" <year> <copyright_holder> <special_line>
    * inserting into the files with the specified extension:
        special <license_name> "<path>"" "<ext>" "<comments_format>" <year> <copyright_holder> <special_line>
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
*** Keys:
    -f: will not list formatted files at the end.
*** Example:
    * inserting into a specified file:
        special lgpl "C:\\Code" ".py" "#" 2023 "imlystyi" "ilt - insert license text!"
    * inserting into the files with the specified extension:
        special lgpl "C:\\Code\\code.py" "#" 2023 "imlystyi" "ilt - insert license text!"\n''')

    def _display_items(self, items: list):
        for item in items:
            self.stdout.write(item + '\n')

    def _get_keys(self, args: str) -> list[str]:
        return [kk for kk in args.split() if kk[0] == '-']

    def _get_params_(self, args: str) -> tuple:
        found = findall(r'"([^"]+)"|(\S+)', args)
        matches = tuple(match[0] or match[1] for match in found)
        return tuple(match for match in matches if match[0] != '-')

    def _get_ignored_exts(self, exts: str) -> list[str]:
        return exts.split(' ')

    # endregion