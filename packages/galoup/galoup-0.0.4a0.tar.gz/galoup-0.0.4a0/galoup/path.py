import glob
import os
import pathlib
import re


def relative_to_project_folder(path: str, project_folder: str) -> str:
    return str(pathlib.Path(os.path.realpath(path)).relative_to(os.path.join(os.getcwd(), project_folder)))


def mkdirp(path: str):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def replace_in_files(file_pattern: str, regex_match: str, repl: str):
    paths = glob.glob(file_pattern)
    for location in paths:
        # Read whole file
        contents = pathlib.Path(location).read_text()
        # Replace
        new_contents = re.sub(regex_match, repl, contents)
        # Replace file
        pathlib.Path(location).write_text(new_contents)
