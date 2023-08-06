from pathlib import Path
import snakypy
from os.path import join


def generate_template(directory: str, data: dict):
    try:
        for key in data:
            snakypy.file.create(data[key], join(directory, key), force=True)
    except Exception:
        raise Exception('There was an error creating the template.')
