import hashlib
from io import BytesIO
from typing import Union

class HashError(Exception):
    """Custom exception for hashing errors."""
    pass


def generate_file_hash(file: Union[str, BytesIO]) -> str:
    """
    Generate a SHA-256 hash for the content of a file.

    Parameters:
        file (Union[str, io.BytesIO]): The path to the file or a BytesIO object.

    Returns:
        str: The hexadecimal representation of the file's hash.

    Raises:
        HashError: If the file does not exist or cannot be read.
    """
    hash_func = hashlib.sha256()

    if isinstance(file, str):
        with open(file, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
    else:
        file.seek(0)  # Ensure reading from the start
        for chunk in iter(lambda: file.read(4096), b""):
            hash_func.update(chunk)

    return hash_func.hexdigest()


def generate_unique_hash(string: str) -> str:
    """
    Generate a SHA-256 hash for a given string.

    Parameters:
        string (str): The input string.

    Returns:
        str: The hexadecimal representation of the string's hash.

    Raises:
        HashError: If the input string is empty or None.
    """
    if not string or not string.strip():
        raise HashError("Input string must not be empty or only whitespace.")

    return hashlib.sha256(string.strip().encode("utf-8")).hexdigest()
