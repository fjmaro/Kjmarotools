"""tools related with the operative system"""
from pathlib import Path
import datetime
import hashlib
import os


def get_file_create_date(filepath: Path) -> datetime.datetime:
    """get the file creation date"""
    return datetime.datetime.fromtimestamp(os.path.getctime(filepath))


def get_file_modify_date(filepath: Path) -> datetime.datetime:
    """get the file modification date"""
    return datetime.datetime.fromtimestamp(os.path.getmtime(filepath))


def get_file_access_date(filepath: Path) -> datetime.datetime:
    """get the file access date"""
    return datetime.datetime.fromtimestamp(os.path.getatime(filepath))


def set_file_modify_date(filepath: Path, date: datetime.datetime):
    """set the file modify date immediately"""
    st_atime = os.stat(filepath).st_atime
    os.utime(filepath, (st_atime, int(datetime.datetime.timestamp(date))))


def set_file_access_date(filepath: Path, date: datetime.datetime):
    """set the file access date immediately"""
    st_mtime = os.stat(filepath).st_mtime
    os.utime(filepath, (int(datetime.datetime.timestamp(date)), st_mtime))


def md5checksum(filepath: Path, buffer=2**20) -> str:
    """return the MD5 value of the file"""
    with open(filepath, "rb") as fle:
        hashmd5 = hashlib.md5()
        while buff := fle.read(buffer):
            hashmd5.update(buff)
        return hashmd5.hexdigest()
