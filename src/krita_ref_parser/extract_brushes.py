"""
"""

from pathlib import Path

RESOURCES_FOLDER = "./input/bundles/"
#/home/eclair/.var/app/org.kde.krita/data/krita/

for rootdir_path, dirlist, filelist in Path(RESOURCES_FOLDER).walk():
    pass
