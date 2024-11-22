import hashlib

class HashError(Exception):
    """Custom exception for hashing errors."""
    pass


def generate_file_hash(file_path: str) -> str:
    """
    Generate a SHA-256 hash for the content of a file.

    Parameters:
        file_path (str): The path to the file.

    Returns:
        str: The hexadecimal representation of the file's hash.

    Raises:
        HashError: If the file does not exist or cannot be read.
    """
    hash_func = hashlib.sha256()
    try:
        with open(file_path, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                hash_func.update(chunk)
    except FileNotFoundError:
        raise HashError(f"File not found: {file_path}")
    except IOError as e:
        raise HashError(f"An error occurred while reading the file: {e}")

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
