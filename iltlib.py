"""
A module that provides file formatting for inserting license text into them.
"""
from iltexceptions import *
from os.path import isdir, join, splitext
from os import getcwd, walk

# region Fields

LICENSES = ["apache", "bsl", "bsd2", "bsd3", "agpl", "gpl2", "gpl3", "lgpl", "mit", "unlicense"]
"""
List of licenses that are currently available in ilt "auto" mode.
"""

# endregion


# region Methods

def auto_insert(license_text: str, root: str, ignored_exts: list[str]) -> (list[str], list[str]):
    """
    Automatically inserts the specified license text into the specified files.
    :param license_text: Specified license text to be inserted into the files.
    :param root: Path to the root folder.
    :param ignored_exts: List of ignored file extensions.
    :return: Tuple pair from the list of successfully formatted files and the list of unknown extensions list.

    """
    root = _get_correct_path(root)
    files = _get_files(root)
    success, unknown_exts = [], []

    for file in files:
        _, ext = splitext(file)

        if ext in ignored_exts:
            continue

        comment = _get_comment(ext)

        if comment == '':
            unknown_exts.append(ext)
        else:
            if special_file_insert(license_text, file, comment):
                success.append(file)

    return success, unknown_exts


def get_license_text(license_name: str, year='', copyright_holder='', special_line='') -> str:
    """
    Gets the text of the license with the specified name and parameters.
    :param license_name: License name.
    :param year: Year to be inserted in the license text.
    :param copyright_holder: Copyright holder name to be inserted into the license text.
    :param special_line: Special line to be inserted into the license text.
    :return: License text.

    """
    text = ''

    with open(getcwd() + r'\LICENSE_TEXTS') as file:
        copy = False

        for line in file:
            if line[0] == ';':
                continue
            elif line.strip() == license_name:
                copy = True
            elif line.strip() == '+end':
                copy = False
            elif copy:
                text += line.strip() + '\n'

    lines = text.splitlines()

    if len(lines) == 0:
        raise LicenseNameException(license_name)
    elif lines and not lines[-1].strip():
        lines.pop()

    license_text = '\n'.join(lines)

    if year == 0:
        license_text = license_text .replace('[year]', '').replace('[copyright_owner]', copyright_holder)
    else:
        license_text = license_text.replace('[year]', str(year)).replace('[copyright_owner]', copyright_holder)

    if special_line != '':
        license_text = license_text.replace('[special_line]', special_line)
    else:
        license_text = license_text.split('\n', 1)[1]

    return license_text


def special_ext_insert(license_text: str, root: str, searched_ext: list[str], comment: str) -> list[str]:
    """
    Inserts the specified license text into files with the specified extension and comment format.
    :param license_text: Specified license text to be inserted into the files.
    :param root: Path to the root folder.
    :param searched_ext: List of searched file extensions.
    :param comment: Comment format in files with the searched extension.
    :return: List of successfully formatted files.

    """
    root = _get_correct_path(root)
    files = _get_files(root)
    success = []

    for file in files:
        _, ext = splitext(file)

        if ext == searched_ext:
            if special_file_insert(license_text, file, comment):
                success.append(file)

    return success


def special_file_insert(license_text: str, file: str, comment: str) -> bool:
    """
    Inserts the specified license text into the specified file with the specified comment format.
    :param license_text: Specified license text to be inserted into the file.
    :param file: Path to the file.
    :param comment: Comment format in the file.
    :return: Formatting success.

    """
    file = _get_correct_path(file)
    try:
        license_lines = license_text.split('\n')
        header = '\n'.join([comment + ' ' + line for line in license_lines])

        with open(file, 'r+') as io:
            content = io.read()
            content = '\n' + content

            io.seek(0)

            io.write(header + content)

        return True
    except (OSError, IOError):
        raise FileException(f'Failed file access: {file} (OSError/IOError).')


def _get_comment(ext: str) -> str:
    match ext:
        case '.c' | '.cc' | '.cpp' | '.cxx' | '.cs' | '.dpr' | '.drc' | '.go' | '.java' | '.js' | '.php' | '.swift' \
             | '.ts':
            return '//'
        case '.f' | '.for' | '.f90':
            return '!'
        case '.py' | '.pyc' | '.pyi' | '.rb':
            return '#'
        case '.vb':
            return '\''
        case _:
            return ''


def _get_correct_path(path: str) -> str:
    return path.replace('/', '\\')


def _get_files(path: str) -> list[str]:
    if not isdir(path):
        raise FileException('Invalid path.')
    else:
        files = []

        for dirpath, dirnames, filenames in walk(path):
            for name in filenames:
                files.append(join(dirpath, name))

        return files

# endregion
