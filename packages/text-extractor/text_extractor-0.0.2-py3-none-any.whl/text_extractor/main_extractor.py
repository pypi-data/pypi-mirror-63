from .utils import ExtensionNotSupported
import os
import importlib

_SUPPORTED_EXTENSIONS = {".txt": ".txt",
#                        "":".txt",
                         ".md":".txt",
                        ".pdf":".pdf"}

_SCRIPT_SUFFIX = "_extractor"
_SCRIPT_PREFIX = ".extractors"

def text_extraction(filepath:str, **kwargs) -> str:
    """High level function to automatically
    detect file extension and use the corresponding file format extractor.
    
    Args:
    filepath (str): Filepath of file to load text from
    kwargs: Additional keyword arguments for the file format extractors that are being
        used.
        
    Return:
    Text extracted from specified filepath as a string.
    
    """
    _, ext = os.path.splitext(filepath)
    ext = ext.lower()
    if ext not in _SUPPORTED_EXTENSIONS:
        raise ExtensionNotSupported(ext)
    ext = _SUPPORTED_EXTENSIONS[ext]
    print(f"Loading file as {ext} file format")
    matched_extractor = importlib.import_module(_SCRIPT_PREFIX+ext+_SCRIPT_SUFFIX,package=__package__)
    return matched_extractor.extract(filepath,**kwargs)