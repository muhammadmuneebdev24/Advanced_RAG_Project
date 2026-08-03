import hashlib


def calculate_file_hash(file_path: str ):
    sha256 = hashlib.sha256()

    with open (file_path, "rb") as f:
        chunk = f.read(8192)
        while chunk:
            sha256.update(chunk)
            chunk = f.read(8192)

    return sha256.hexdigest() 

