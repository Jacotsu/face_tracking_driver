from setuptools import setup
import os
import re


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

def read(*names, **kwargs):
    with open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


classifiers = [
    "Natural Language :: English",
    "Programming Language :: Python :: 3.7"
]

setup(
    name='face_tracker_driver',
    install_requires = [
        "face_recognition",
        "opencv-python"
    ],
    python_requires='>=3.7',
    packages = ['face_tracker'],
    description = "Control a webcam with facetracking",
    classifiers = classifiers,
)
