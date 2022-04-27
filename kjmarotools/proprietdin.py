""" Here are allocated all the Proprietary name conventions"""
from abc import ABC, abstractmethod
from pathlib import Path
import datetime
import os

from .basics import conventions


def is_proprietary_din(file: Path, year_bounds=(1800, 2300)) -> bool:
    """
    --------------------------------------------------------------------------
    Return if the filename is in one of the accepted proprietary DIN
    conventions
    --------------------------------------------------------------------------
    """
    for prop_class in BaseProprietary.__subclasses__():
        if prop_class().is_din(file, year_bounds):  # type: ignore
            return True
    return False


def kdin_from_proprietary_din(file: Path, year_bounds=(1800, 2300)) -> Path:
    """
    --------------------------------------------------------------------------
    - Get the file path with the KDIN from the given proprietary DIN
    --------------------------------------------------------------------------
    """
    # pylint: disable=protected-access
    for prop_class in BaseProprietary.__subclasses__():
        init_class = prop_class()  # type: ignore
        if init_class.is_din(file, year_bounds):
            dtt_date = init_class.get_din(file, year_bounds)
            str_date = dtt_date.strftime(init_class._din_fmt)
            new_name = "".join(file.name.split(str_date))
            tail0, tail1 = "", ""
            if init_class._tail:
                tail0 = " " + init_class._tail
                tail1 = tail0 + " "
            if not new_name:
                new_name = conventions.date2kdin(dtt_date) + tail0
            elif new_name == file.suffix or new_name[0] == " ":
                new_name = conventions.date2kdin(dtt_date) + tail0 + new_name
            else:
                new_name = conventions.date2kdin(dtt_date) + tail1 + new_name
            new_path = file.parent.joinpath(new_name)
            return new_path
    return file


def rename_proprietary_din_file(file: Path, year_bounds=(1800, 2300)) -> Path:
    """
    --------------------------------------------------------------------------
    - Rename the proprietary file with KDIN and return the new file path.
    - If the renamed file already exists it does nothing and returns the
    original filename.
    --------------------------------------------------------------------------
    """
    new_path = kdin_from_proprietary_din(file, year_bounds)
    if new_path != file:
        if new_path.exists():
            return file
        os.rename(file, new_path)
    return new_path


class BaseProprietary(ABC):
    """
    --------------------------------------------------------------------------
    Base Class for every proprietary convention. For including new conventions
    just add a new subclass at the bottom of the file. See the already added
    ones (Like Google, Screenshot, Whatsapp...) as example.
    --------------------------------------------------------------------------
    - _tail: To include a trace of the proprietary convention in the name
    - _din_fmt: Format of the date-in-name to obtain
    - _conditions_ok(): To define here special conditions to accomplish
    - _clean_datename(): Return the datename clean (only static values)
    --------------------------------------------------------------------------
    - NOTE: Only the abstract methods must be overwritten
    --------------------------------------------------------------------------
    """
    @property
    @abstractmethod
    def _tail(self) -> str:
        """
        ----------------------------------------------------------------------
        This must include a text to add after the KDIN and before the rest of
        the name of the file (only to include if it is desired to know the
        source of the original name-format or convention of the file)
        e.g: IMG, Whatsapp, Nokia, Nikon, etc.
        ----------------------------------------------------------------------
        """
        return ""

    @property
    @abstractmethod
    def _din_fmt(self) -> str:
        """
        ----------------------------------------------------------------------
        This must return the DIN format according to its convention, it can
        include static parts of the name
        ----------------------------------------------------------------------
        """
        return ""

    @staticmethod
    @abstractmethod
    def _conditions_ok(file: Path) -> bool:
        """
        ----------------------------------------------------------------------
        Here will be included for each specific Proprietary convention the
        specific conditions to accomplish for considering it valid DIN
        ----------------------------------------------------------------------
        """
        return False

    @staticmethod
    @abstractmethod
    def _clean_datename(file: Path) -> str:
        """
        ----------------------------------------------------------------------
        Return the date-in-name without any DIN variable fields (statics can
        be maintained) information in the text
        ----------------------------------------------------------------------
        """
        return ""

    def get_din(self, file: Path, year_bounds=(1800, 2300)
                ) -> datetime.datetime:
        """
        ----------------------------------------------------------------------
        Return the file DIN according to the selected proprietary convention.
        - If the DIN is not found, datetime(1, 1, 1) is returned
        ----------------------------------------------------------------------
        """
        try:
            if not self._conditions_ok(file):
                raise ValueError
            clean_name = self._clean_datename(file)
            new_date = datetime.datetime.strptime(clean_name, self._din_fmt)
            if year_bounds[0] <= new_date.year <= year_bounds[1]:
                return new_date
            raise ValueError
        except ValueError:
            return datetime.datetime(1, 1, 1)

    def is_din(self, file: Path, year_bounds=(1800, 2300)) -> bool:
        """
        ----------------------------------------------------------------------
        Return if the file has in the name the selected proprietary convention
        ----------------------------------------------------------------------
        """
        return self.get_din(file, year_bounds).year != 1


class GooglePhotos(BaseProprietary):
    """GooglePhotos Proprietary Convention"""
    @property
    def _tail(self) -> str:
        return super()._tail

    @property
    def _din_fmt(self) -> str:
        return r"IMG_%Y%m%d_%H%M%S"

    @staticmethod
    def _conditions_ok(file: Path) -> bool:
        if len(file.name) >= 19:
            if file.name[:4] == "IMG_" and file.name[12] == "_":
                return True
        return False

    @staticmethod
    def _clean_datename(file: Path) -> str:
        return file.name[:19]


class Screenshot(BaseProprietary):
    """Screenshot Proprietary Convention"""
    @property
    def _tail(self) -> str:
        return super()._tail

    @property
    def _din_fmt(self) -> str:
        return r"%Y-%m-%d %H.%M.%S"

    @staticmethod
    def _conditions_ok(file: Path) -> bool:
        if len(file.name) >= 19:
            spacers0 = file.name[10] == " "
            spacers1 = file.name[4] == file.name[7] == "-"
            spacers2 = file.name[13] == file.name[16] == "."
            if spacers0 and spacers1 and spacers2:
                return True
        return False

    @staticmethod
    def _clean_datename(file: Path) -> str:
        return file.name[:19]


class Whatsapp(BaseProprietary):
    """Whatsapp Proprietary Convention"""
    @property
    def _tail(self) -> str:
        return super()._tail

    @property
    def _din_fmt(self) -> str:
        return r"WhatsApp Image %Y-%m-%d at %H.%M.%S"

    @staticmethod
    def _conditions_ok(file: Path) -> bool:
        if len(file.name) >= 37:
            tst_blk0 = file.name[:15] == "WhatsApp Image "
            spacers0 = file.name[19] == file.name[22] == "-"
            spacers1 = file.name[31] == file.name[34] == "."
            if tst_blk0 and spacers0 and spacers1:
                return True
        return False

    @staticmethod
    def _clean_datename(file: Path) -> str:
        return file.name[:37]


if __name__ == "__main__":
    # ========================================================================
    # For executing these examples remove the '.' in the '.infodtb' import
    # ========================================================================
    print("=" * 79)
    _TST = Path.cwd().joinpath("IMG_20210105_010203ckasa")
    print(GooglePhotos().is_din(_TST))
    print(GooglePhotos().get_din(_TST))
    # ========================================================================
    _TST = Path.cwd().joinpath("2021-01-05 01.02.03ckasa")
    print(Screenshot().is_din(_TST))
    print(Screenshot().get_din(_TST))
    # ========================================================================
    _TST = Path.cwd().joinpath("WhatsApp Image 2018-09-22 at 18.11.39sdgasg")
    print(Whatsapp().is_din(_TST))
    print(Whatsapp().get_din(_TST))
    # =======================================================================
    print("=" * 79)
