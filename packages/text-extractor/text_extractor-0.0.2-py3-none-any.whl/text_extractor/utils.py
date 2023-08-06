import mimetypes


class ExtensionNotSupported(Exception):
    """This error is raised with unsupported extensions"""
    def __init__(self, ext):
        self.ext = ext

    def __str__(self):
        return f"The filename extension {self.ext} is not yet \
                supported"


def check_mimetype(filepath):
    """
    Checks MIME type of file.
    
    Args:
    filepath (str): filepath of file to check
    
    Returns:
    MIME type of file as str
    """
    file_mime,_ = mimetypes.guess_type(filepath)
    return file_mime  