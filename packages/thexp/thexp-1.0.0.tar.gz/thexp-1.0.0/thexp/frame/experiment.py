"""
    Copyright (C) 2020 Shandong University

    This program is licensed under the GNU General Public License 3.0 
    (https://www.gnu.org/licenses/gpl-3.0.html). 
    Any derivative work obtained under this license must be licensed 
    under the GNU General Public License as published by the Free 
    Software Foundation, either Version 3 of the License, or (at your option) 
    any later version, if this derivative work is distributed to a third party.

    The copyright for the program is owned by Shandong University. 
    For commercial projects that require the ability to distribute 
    the code of this program as part of a program that cannot be 
    distributed under the GNU General Public License, please contact 
            
            sailist@outlook.com
             
    to purchase a commercial license.
"""
import atexit
import hashlib
import inspect
import json
# from .trainer import BaseTrainer
import os
import sys
from collections import Iterable, defaultdict
from datetime import datetime
from datetime import timedelta

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from ..base_classes.tree import tree
from ..utils import generel_util as gu
from ..utils.pickledb import PickleDB

__all__ = ["Experiment", "ExperimentViewer"]
import pprint as pp


class Experiment:
    _instance = None

    @property
    def dbfile(self):
        dbfile = os.path.join(self.dbpath, self.dbfilename)
        return os.path.normpath(dbfile)

    def __init__(self, exps_dir=None, dbfilename=None, dbpath=None):
        if dbfilename is None:
            dbfilename = "thexp.json"
        self.dbfilename = dbfilename
        if dbpath is None:
            dbpath = gu.home_dir()
        self.dbpath = dbpath

        self.initial_exp_info()

        if exps_dir is None:
            main_dir = os.path.abspath(os.path.split(sys.argv[0])[0])
            exps_dir = os.path.join(main_dir, "experiment")
        self.exp_dir = exps_dir
        os.makedirs(self.exp_dir, exist_ok=True)

        self.db = PickleDB(self.dbfile, auto_dump=True)

        self.event_handler = ExperimentEventHandler()
        self.observer = Observer()
        self.snap_member = []
        self.keycode(sys.modules["__main__"])
        atexit.register(self.end_exp)
        # self.exithook = gu.exithook()

    def initial_exp_info(self):
        exp_info = tree()
        exp_info["start_time"] = gu.curent_date()
        self.exp_info = exp_info

    def _cacu_hash(self, str):
        hl = hashlib.md5()
        hl.update(str.encode(encoding='utf-8'))
        return hl.hexdigest()[:16]

    def hold_exp_part(self, dir, exts: Iterable = (), observe=True):
        path = os.path.join(self.exp_dir, dir)
        os.makedirs(path, exist_ok=True)
        if observe:
            for i in exts:
                self.event_handler.add_prefix(i)
            self.observer.schedule(self.event_handler, path, recursive=True)
        return path

    def add_event_listener(self, func, exts: Iterable = ()):
        assert len(list(exts)) != 0
        self.event_handler.add_event_listener(func, exts=exts)

    def start_exp(self):
        self.observer.start()
        for member in self.snap_member:
            name = member.__name__
            code = inspect.getsource(member)
            fn = inspect.getfile(member)
            hash = gu.string_hash(code)

            i = 0

            refn = os.path.split(fn)[1]

            snap_path = os.path.join(self.hold_exp_part("code", observe=False), "{}-{}-{}".format(refn, name, i))

            while os.path.exists(snap_path) and gu.file_hash(snap_path) != hash:
                i += 1
                snap_path = os.path.join(self.hold_exp_part("code", observe=False), "{}-{}-{}".format(refn, name, i))

            self.snapshot(code, snap_path)
            self.exp_info["snap"][name] = dict(
                fn=fn,
                hash=hash,
                snap=snap_path,
            )

        self.exp_info["args"] = sys.argv
        self.exp_info["files"] = self.event_handler.file_dict

    def end_exp(self):
        self.exp_info["end_time"] = gu.curent_date()
        exp_dir = self.hold_exp_part("exp", observe=False)
        datekey = gu.curent_date()
        with open(os.path.join(exp_dir, "{}.json".format(datekey)), "w", encoding="utf-8") as w:
            json.dump(self.exp_info, w, indent=2)

        self.db.set(datekey, self.exp_info)
        print("\nexp info saved in {},key='{}'".format(self.dbfile, datekey))

    def snapshot(self, code, path):
        with open(path, "w", encoding="utf-8") as w:
            w.write(code)

    def keycode(self, member=None):
        if member is not None:
            self.snap_member.append(member)
            return

        def func(member):
            self.snap_member.append(member)
            return member

        return func

    def summary(self):
        pp.pprint(self.exp_info)


class ExperimentEventHandler(FileSystemEventHandler):
    """用来获取试验过程中的模型保存和日志输出的变化 TODO """

    def __init__(self):
        self.file_dict = tree()
        self.ext_set = set()
        self.listener_dict = defaultdict(list)

    def add_prefix(self, ext: str):
        assert ext.startswith(".")
        self.ext_set.add(ext.lower())

    def add_event_listener(self, func, exts: Iterable):
        """
        if file created/modified/deleted and its ext in 'exts', func(file, mode) will be called.
        :param func:  functions with 2 args
        :param exts:
        :return:
        """
        for ext in exts:
            assert ext.startswith("."), "ext must have '.', like '.png', '.log'"
            ext = ext.lower()
            self.listener_dict[ext].append(func)

    def update(self, fn, mode):
        ext = os.path.splitext(fn)[1].lower()

        if ext in self.listener_dict:
            for func in self.listener_dict[ext]:
                func(fn, mode)

        if ext in self.ext_set:
            self.file_dict[fn]["mode"] = mode
            if os.path.exists(fn):
                if os.path.exists("{}.json".format(fn)):
                    self.file_dict[fn]["info"] = "{}.json".format(fn)
                self.file_dict[fn]["hash"] = gu.file_atime_hash(fn)
                self.file_dict[fn]["atime"] = gu.file_atime2date(fn)
                self.file_dict[fn]["exist"] = True
            else:
                self.file_dict[fn]["exist"] = False

    def on_created(self, event):
        super(ExperimentEventHandler, self).on_created(event)
        if not event.is_directory:
            fn = event.src_path
            self.update(fn, "created")

    def on_deleted(self, event):
        super(ExperimentEventHandler, self).on_deleted(event)
        if not event.is_directory:
            fn = event.src_path
            self.update(fn, "deleted")

    def on_modified(self, event):
        super(ExperimentEventHandler, self).on_modified(event)
        if not event.is_directory:
            fn = event.src_path
            self.update(fn, "modified")


class ExperimentViewer:
    @property
    def dbfile(self):
        dbfile = os.path.join(self.dbpath, self.dbfilename)
        return dbfile

    @property
    def db(self) -> PickleDB:
        return self.__db

    def __init__(self, dbfilename=None, dbpath=None):
        if dbfilename is None:
            dbfilename = "thexp.json"
        self.dbfilename = dbfilename
        if dbpath is None:
            dbpath = gu.home_dir()
        self.dbpath = dbpath

        self.__db = PickleDB(self.dbfile, auto_dump=False)

    def reload(self):
        self.__db = PickleDB(self.dbfile, auto_dump=False)

    def list(self):
        return list(self.__db.getall())

    def recent(self, day=0, mouth=0, year=0, timedeltaobj=None):
        """
        mouth和year不精确，mouth = 30*day, year = 365*day
        :param day:
        :param mouth:
        :param year:
        :return:
        """
        if timedeltaobj is not None:
            history = datetime.now() - timedeltaobj
        else:
            history = datetime.now() - timedelta(day + mouth * 30 + year * 365)
        return [date for date in self.list() if gu.curent_date(dateobj=history) < date]

    def drop(self):
        self.__db.deldb()

    def backtracking(self, fn):
        checkhash = os.path.exists(fn)
        if checkhash:
            tfhash = gu.file_atime_hash(fn)
        path = tree()

        for dkey in self.__db.getall():
            exp = self.__db.get(dkey)  # type:dict

            for dk, dv in exp.items():
                if dk == "files":
                    for k, v in dv.items():  # type:(str,Any)
                        if gu.path_in(fn, k):
                            if checkhash:
                                fhash = v["hash"]
                                if fhash != tfhash:
                                    path[dkey][dk][k] = self.check_file_state(fn, v)
                                else:
                                    path[dkey][dk][k] = v
                            else:
                                path[dkey][dk][k] = v
                elif dk == "snap":
                    for k, v in dv.items():
                        if gu.path_in(fn, v["fn"]) or gu.path_in(fn, v["snap"]):
                            path[dkey][dk] = dv
        return path

    def check_snap_state(self, file, oldstat):
        res = dict()
        if not os.path.exists(file):
            res["mode"] = "deleted"
        else:
            nhash = gu.file_atime_hash(file)
            if oldstat["hash"] != nhash:
                res["mode"] = "replacement"
                res["atime"] = oldstat["atime"]
        return res

    def check_file_state(self, file, oldstat):
        res = dict()
        if not os.path.exists(file):
            res["mode"] = "deleted"
        else:
            nhash = gu.file_atime_hash(file)
            if oldstat["hash"] != nhash:
                res["mode"] = "replacement"
                res["atime"] = oldstat["atime"]
        return res

    def exp_info(self, datekey):
        return self.__db.get(datekey)

    def exp_code(self, datekey):
        return self.__db.get(datekey)["snap"]


if __name__ == '__main__':
    pass
