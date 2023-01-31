import argparse
import os
import sys

from packageviewer.data_manager import DataManager
from packageviewer.distro_data import DistroData
import timer


class ManageDataCli:

    def __init__(self, argv):
        self.argv = argv
        self.SCRIPT_VERSION = "v1.0 beta"

    def get_parser(self, action=""):
        return argparse.ArgumentParser(
            prog = f"processdata {action}".strip(),
            description = "Process data",
            epilog=f"script version {self.SCRIPT_VERSION}",
        )

    def run(self):
        parser = self.get_parser()
        parser.add_argument("action",
        help = "Action wanted")

        args = parser.parse_args(self.argv[1:2])

        match args.action:
            case "add":
                self.parse_action_add()
            case "add-indexes":
                self.parse_action_add_indexes()
            case _:
                parser.error(f"Invalid action: '{args.action}'")

    def parse_action_add(self):
        parser = self.get_parser()
        parser.add_argument("--db", default="out.db",
            help = "Set database file to use")

        parser.add_argument("-d", "--distro", required=True,
            help = "Set the distribution")
        parser.add_argument("-v", "--version", default="DEFVERSION",
            help = "Set the distribution version")
        
        parser.add_argument("--reset-db", required=False, default=False, action="store_true",
            help = "Reset database if already existing")
        parser.add_argument("--add-indexes", required=False, default=False, action="store_true",
            help = "Reset database if already existing")

        self.args = parser.parse_args(self.argv[2:])

        self.do_action_add()

    def do_action_add(self):
        print(f"Operation requested : process '{self.args.distro}/{self.args.version}'")

        self.init_data_manager(self.args.reset_db)

        path = os.path.join("archives", self.args.distro, self.args.version)

        timer.call(
            self.data_manager.process_data_point,
            distro_name=self.args.distro, distro_version=self.args.version, dir_path=path
        )

    def parse_action_add_indexes(self):
        parser = self.get_parser()

        parser.add_argument("--db", default="out.db",
            help = "Set database file to use")

        self.args = parser.parse_args(self.argv[2:])
        
        self.do_action_add_indexes()

    def do_action_add_indexes(self):
        self.init_data_manager()

        self.data_manager.add_indexes()

    def init_data_manager(self, force_reset=False):
        need_init = False
        if force_reset:
            need_init = True
            if os.path.exists(self.args.db):
                os.remove(self.args.db)
        else:
            need_init = not os.path.exists(self.args.db)
        
        self.data_manager = DataManager(self.args.db)
        if need_init:
            self.data_manager.create_tables()


cli = ManageDataCli(sys.argv)
cli.run()