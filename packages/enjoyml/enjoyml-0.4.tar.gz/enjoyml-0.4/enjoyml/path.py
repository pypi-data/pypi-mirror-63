"""
Helper function which are used for easier work with path values.
"""

import os


def make_dir_if_not_exist(dir_path: str):
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)
