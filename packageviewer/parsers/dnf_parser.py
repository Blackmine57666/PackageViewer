import os
import sqlite3

from packageviewer.distro_data import DistroData
from packageviewer import utils

class DnfParser:

    def __init__(self, distro_name: str, distro_version: str, dir_path: str) -> None:
        self.distro_name = distro_name
        self.distro_version = distro_version
        self.dir_path = dir_path


    def _parse_sum_file_(self, filepath, repo):
        print(filepath)
        conn = sqlite3.connect(filepath)

        cursor = conn.execute("SELECT pkgId, name, version, release, epoch FROM packages")

        for row in cursor:
            yield {"pkgId": row[0], "name": row[1], "version": row[2], "release": row[3], "epoch": row[4]}
        
        conn.close()


    def _parse_files_file_(self, filepath, repo):
        conn = sqlite3.connect(filepath)

        cursor = conn.execute("SELECT pkgKey, dirname, filenames, filetypes FROM filelist")

        for row in cursor:
            for filename, filetype in zip(row[2].split("/"), row[3]):
                if filetype == 'f':
                    yield {"repo": repo, "package_id": row[0], "dirname": row[1], "filename": filename}
        
        conn.close()


    def parse_sums(self):
        for repo, full_repo in utils.loop_dirs(self.dir_path):
            yield self._parse_sum_file_(os.path.join(full_repo, "primary.sqlite"), repo)

    def parse_files(self):
        for repo, full_repo in utils.loop_dirs(self.dir_path):
            yield self._parse_files_file_(os.path.join(full_repo, "filelists.sqlite"), repo)