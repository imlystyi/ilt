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
