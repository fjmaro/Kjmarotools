"""
------------------------------------------------------------------------------
Here are allocated all the Kjmaro Conventions (Kiko/Francisco Mata Aroco)
------------------------------------------------------------------------------
Folder Date-In-Name (DIN) bounds
    - Separators
        - '-' separate the same date-fields
        - '_' separate two dates (For year intervals '-' can be also used)
    - Valid combination of folder names
        - YYYY abcdefg1
        - YYYY-YYYY abcdefg2
        - YYYY_YYYY abcdefg3
        - YYYY-MM abcdefg4
        - YYYY-MM-DD abcdefg5
        - YYYY-MM_MM abcdefg6
        - YYYY-MM-DD_DD abcdefg7
        - YYYY-MM_YYYY-MM abcdefg8
        - YYYY-MM-DD_MM-DD abcdefg9
        - YYYY-MM-DD_YYYY-MM-DD abcdefg10
------------------------------------------------------------------------------
Files Date-In-Name (DIN)
    - YYYYMMDD-HHMMSS*
    - eg: 20210102-201005
    - eg: 20210102-201005.jpg
    - eg: 20210102-201005 .jpg
    - eg: 20210102-201005 test.jpg
    - eg: 20130502-235959 test2.jpg
    - ...
------------------------------------------------------------------------------
Files Edition Date-In-Name (EDIN) <[files to be edited by scripts]>
    - *++YYYY-MM-DD+HH-MM-SS++*
    - eg: test++1999-01-16+12-21-02++one.jpg
    - eg: test++1999-01-16+12-21-02++.jpg
    - eg: ++1999-01-16+12-21-02++one.jpg
    - ...
------------------------------------------------------------------------------
Files with DIN and Date-To-Review (TRDIN) <[files to be manually reviewed]>
- This is because the program couldn't determinate a valid date of the file.
    - YYYYMMDD-HHMMSS(DTR)*
    - eg: 20210102-201005(DTR).jpg
    - eg: 20130502-235959(DTR) test2.jpg
    - ...
"""
from typing import Tuple
from pathlib import Path
import datetime


def get_folder_kdin_bounds(folder: Path, year_bounds=(1800, 2300)
                           ) -> Tuple[datetime.datetime, datetime.datetime]:
    """
    --------------------------------------------------------------------------
    Find the date bounds in the folder-name following the Kjmaro convention.
    It returns the initial date as t0 and the final date t1 as +1 Year or
    Month or Date (depending on the case).
    if not valid date is found it returns datetime(1, 1, 1), datetime(1, 1, 1)
    Bounds are given including the days indicated
        - for 2021       -> 2021-01-01 to 2022-01-01
        - for 2021-10-26 -> 2021-10-26 to 2021-10-27
        - for 2021-10_11 -> 2021-10-01 to 2021-12-01
    --------------------------------------------------------------------------
    - Kjmaro Convention
        > '-' separate the same date-fields
        > '_' separate two dates (For year intervals '-' can be also used)
    - Kjmaro Valid combination of folder names
        - YYYY abcdefg1
        - YYYY-YYYY abcdefg2
        - YYYY_YYYY abcdefg3
        - YYYY-MM abcdefg4
        - YYYY-MM-DD abcdefg5
        - YYYY-MM_MM abcdefg6
        - YYYY-MM-DD_DD abcdefg7
        - YYYY-MM_YYYY-MM abcdefg8
        - YYYY-MM-DD_MM-DD abcdefg9
        - YYYY-MM-DD_YYYY-MM-DD abcdefg10
    --------------------------------------------------------------------------
    """
    # pylint: disable=too-many-locals, too-many-statements, too-many-branches
    fields = folder.name.split()[0].strip()
    date0 = datetime.datetime(1, 1, 1)
    date1 = datetime.datetime(1, 1, 1)
    deltaday = datetime.timedelta(days=1)

    # CASE1: YYYY:
    if len(fields) == 4 and fields.isdigit():
        in_bounds = year_bounds[0] <= int(fields) <= year_bounds[1]
        if in_bounds:
            date0 = datetime.datetime(int(fields), 1, 1)
            date1 = datetime.datetime(int(fields) + 1, 1, 1)

    # CASE2&3: YYYY-YYYY or YYYY_YYYY
    mid_bar = len(fields.split("-")) == 2
    low_bar = len(fields.split("_")) == 2
    if len(fields) == 9 and (mid_bar or low_bar):
        year0_str, year1_str = fields.split("-" if mid_bar else "_")
        if year0_str.isdigit() and year1_str.isdigit():
            in_bounds0 = year_bounds[0] <= int(year0_str) <= year_bounds[1]
            in_bounds1 = year_bounds[0] <= int(year1_str) <= year_bounds[1]
            if in_bounds0 and in_bounds1:
                date0 = datetime.datetime(int(year0_str), 1, 1)
                date1 = datetime.datetime(int(year1_str) + 1, 1, 1)

    # CASE4: YYYY-MM
    if len(fields) == 7 and len(fields.split("-")) == 2:
        year0_str, mnth0_str = fields.split("-")
        if year0_str.isdigit() and mnth0_str.isdigit():
            in_bounds_yr = year_bounds[0] <= int(year0_str) <= year_bounds[1]
            in_bounds_mt = 1 <= int(mnth0_str) <= 12
            if in_bounds_yr and in_bounds_mt:
                date0 = datetime.datetime(int(year0_str), int(mnth0_str), 1)
                date1 = date0 + datetime.timedelta(days=31)
                date1 = datetime.datetime(date1.year, date1.month, 1)

    # CASE5: YYYY-MM-DD
    if len(fields) == 10 and len(fields.split("-")) == 3:
        year0_str, mnth0_str, day_str = fields.split("-")
        if year0_str.isdigit() and mnth0_str.isdigit() and day_str.isdigit():
            in_bounds_yr = year_bounds[0] <= int(year0_str) <= year_bounds[1]
            in_bounds_mt = 1 <= int(mnth0_str) <= 12
            if in_bounds_yr and in_bounds_mt:
                try:
                    date0 = datetime.datetime(int(year0_str), int(mnth0_str),
                                              int(day_str))
                    date1 = date0 + datetime.timedelta(days=1)
                except ValueError:
                    pass

    # CASE6: YYYY-MM_MM
    tst0 = len(fields.split("-")) == 2
    tst1 = len(fields.split("_")) == 2
    if len(fields) == 10 and tst0 and tst1:
        year0_str = fields.split("-")[0]
        mnth0_str = fields.split("-")[1].split("_")[0]
        mnth1_str = fields.split("-")[1].split("_")[1]
        if year0_str.isdigit() and mnth0_str.isdigit() and mnth1_str.isdigit():
            in_bounds_yr = year_bounds[0] <= int(year0_str) <= year_bounds[1]
            in_bounds_mt0 = 1 <= int(mnth0_str) <= 12
            in_bounds_mt1 = 1 <= int(mnth1_str) <= 12
            if in_bounds_yr and in_bounds_mt0 and in_bounds_mt1:
                date0 = datetime.datetime(int(year0_str), int(mnth0_str), 1)
                date1 = datetime.datetime(int(year0_str), int(mnth1_str), 1)
                date1 = date1 + datetime.timedelta(days=31)
                date1 = datetime.datetime(date1.year, date1.month, 1)

    # CASE7: YYYY-MM-DD_DD
    tst0 = len(fields.split("-")) == 3
    tst1 = len(fields.split("_")) == 2
    if len(fields) == 13 and tst0 and tst1:
        year0_str = fields.split("-")[0]
        mnth0_str = fields.split("-")[1]
        day0_str = fields.split("-")[2].split("_")[0]
        day1_str = fields.split("-")[2].split("_")[1]
        days_are_digis = day0_str.isdigit() and day1_str.isdigit()
        if year0_str.isdigit() and mnth0_str.isdigit() and days_are_digis:
            in_bounds_yr = year_bounds[0] <= int(year0_str) <= year_bounds[1]
            in_bounds_mt = 1 <= int(mnth0_str) <= 12
            if in_bounds_yr and in_bounds_mt:
                try:
                    date0 = datetime.datetime(int(year0_str), int(mnth0_str),
                                              int(day0_str))
                    date1 = datetime.datetime(int(year0_str), int(mnth0_str),
                                              int(day1_str))
                    date1 = date1 + deltaday
                except ValueError:
                    pass

    # CASE8: YYYY-MM_YYYY-MM
    tst0 = len(fields.split("-")) == 3
    tst1 = len(fields.split("_")) == 2
    if len(fields) == 15 and tst0 and tst1:
        year0_str = fields.split("_")[0].split("-")[0]
        mnth0_str = fields.split("_")[0].split("-")[1]
        year1_str = fields.split("_")[1].split("-")[0]
        mnth1_str = fields.split("_")[1].split("-")[1]
        years_aredigit = year0_str.isdigit() and year1_str.isdigit()
        mnths_aredigit = mnth0_str.isdigit() and mnth1_str.isdigit()
        if years_aredigit and mnths_aredigit:
            in_bounds_yr0 = year_bounds[0] <= int(year0_str) <= year_bounds[1]
            in_bounds_yr1 = year_bounds[0] <= int(year1_str) <= year_bounds[1]
            in_bounds_mt0 = 1 <= int(mnth0_str) <= 12
            in_bounds_mt1 = 1 <= int(mnth1_str) <= 12
            yr_in_bounds = in_bounds_yr0 and in_bounds_yr1
            mt_in_bounds = in_bounds_mt0 and in_bounds_mt1
            if yr_in_bounds and mt_in_bounds:
                date0 = datetime.datetime(int(year0_str), int(mnth0_str), 1)
                date1 = datetime.datetime(int(year1_str), int(mnth1_str), 1)
                date1 = date1 + datetime.timedelta(days=31)
                date1 = datetime.datetime(date1.year, date1.month, 1)

    # CASE9: YYYY-MM-DD_MM-DD
    tst0 = len(fields.split("-")) == 4
    tst1 = len(fields.split("_")) == 2
    if len(fields) == 16 and tst0 and tst1:
        year0_str = fields.split("_")[0].split("-")[0]
        mnth0_str = fields.split("_")[0].split("-")[1]
        day0_str = fields.split("_")[0].split("-")[2]
        mnth1_str = fields.split("_")[1].split("-")[0]
        day1_str = fields.split("_")[1].split("-")[1]
        mnths_aredigit = mnth0_str.isdigit() and mnth1_str.isdigit()
        days_aredigit = day0_str.isdigit() and day1_str.isdigit()
        if year0_str.isdigit() and mnths_aredigit and days_aredigit:
            in_bounds_yr0 = year_bounds[0] <= int(year0_str) <= year_bounds[1]
            in_bounds_mt0 = 1 <= int(mnth0_str) <= 12
            in_bounds_mt1 = 1 <= int(mnth1_str) <= 12
            if in_bounds_yr0 and in_bounds_mt0 and in_bounds_mt1:
                try:
                    date0 = datetime.datetime(int(year0_str), int(mnth0_str),
                                              int(day0_str))
                    date1 = datetime.datetime(int(year0_str), int(mnth1_str),
                                              int(day1_str))
                    date1 = date1 + deltaday
                except ValueError:
                    pass

    # CASE10: YYYY-MM-DD_YYYY-MM-DD
    tst0 = len(fields.split("-")) == 5
    tst1 = len(fields.split("_")) == 2
    if len(fields) == 21 and tst0 and tst1:
        year0_str = fields.split("_")[0].split("-")[0]
        mnth0_str = fields.split("_")[0].split("-")[1]
        day0_str = fields.split("_")[0].split("-")[2]
        year1_str = fields.split("_")[1].split("-")[0]
        mnth1_str = fields.split("_")[1].split("-")[1]
        day1_str = fields.split("_")[1].split("-")[2]
        years_aredigit = year0_str.isdigit() and year1_str.isdigit()
        mnths_aredigit = mnth0_str.isdigit() and mnth1_str.isdigit()
        days_aredigit = day0_str.isdigit() and day1_str.isdigit()
        if years_aredigit and mnths_aredigit and days_aredigit:
            in_bounds_yr0 = year_bounds[0] <= int(year0_str) <= year_bounds[1]
            in_bounds_yr1 = year_bounds[0] <= int(year1_str) <= year_bounds[1]
            in_bounds_mt0 = 1 <= int(mnth0_str) <= 12
            in_bounds_mt1 = 1 <= int(mnth1_str) <= 12
            years_in_bounds = in_bounds_yr0 and in_bounds_yr1
            mnths_in_bounds = in_bounds_mt0 and in_bounds_mt1
            if years_in_bounds and mnths_in_bounds:
                try:
                    date0 = datetime.datetime(int(year0_str), int(mnth0_str),
                                              int(day0_str))
                    date1 = datetime.datetime(int(year1_str), int(mnth1_str),
                                              int(day1_str))
                    date1 = date1 + deltaday
                except ValueError:
                    pass
    return date0, date1


def get_file_kdin(file: Path, year_bounds=(1800, 2300)) -> datetime.datetime:
    """
    --------------------------------------------------------------------------
    Get the file date-in-name following the Kjmaro convention. Returns the
    date found in the filename > For not found dates return datetime(1, 1, 1)
    --------------------------------------------------------------------------
    - Kjmaro Convention
        > YYYYMMDD-HHMMSS*
        > eg: 20210102-201005
        > eg: 20210102-201005.jpg
        > eg: 20210102-201005 .jpg
        > eg: 20210102-201005 test.jpg
        > eg: 20130502-235959 test2.jpg
        > eg: 20130502-235959(DTR) test2.jpg
        > ...
    --------------------------------------------------------------------------
    """
    date = datetime.datetime(1, 1, 1)
    filename = file.name
    if len(filename) < 15:
        return date

    if filename[8] == "-":
        try:
            year, mnth, day = filename[:4], filename[4:6], filename[6:8]
            hour, mnts, sec = filename[9:11], filename[11:13], filename[13:15]
            if year_bounds[0] <= int(year) <= year_bounds[1]:
                date = datetime.datetime(int(year), int(mnth), int(day),
                                         int(hour), int(mnts), int(sec))
        except ValueError:
            pass
        except TypeError:
            pass
    return date


def get_file_ekdin(file: Path, year_bounds=(1800, 2300)) -> datetime.datetime:
    """
    --------------------------------------------------------------------------
    Get the file edit-date-in-name following the Kjmaro convention. Returns
    the date found in the filename > Not found dates return datetime(1, 1, 1)
    --------------------------------------------------------------------------
    This convention is used to automate the date modification of a file. The
    date is written in the filename and this means that the user want to add
    this date to the file.
    --------------------------------------------------------------------------
    - Kjmaro Convention
        > *++YYYY-MM-DD+HH-MM-SS++*
        > eg: test++1999-01-16+12-21-02++one.jpg
        > eg: test++1999-01-16+12-21-02++.jpg
        > eg: ++1999-01-16+12-21-02++one.jpg
        > ...
    --------------------------------------------------------------------------
    """
    # pylint: disable=too-many-locals
    date = datetime.datetime(1, 1, 1)
    filename_lst = file.name.split("++")

    if len(filename_lst) == 3:
        datename = str(filename_lst[1])
        blkok = len(datename.split("-")) == 5
        pckok = len(datename.split("+")) == 2
        sepok = datename[10] == "+"
        lnedte = datename[4] == "-" and datename[7] == "-"
        lnehur = datename[13] == "-" and datename[16] == "-"

        if blkok and pckok and sepok and lnedte and lnehur:
            year, mth, day = datename[:4], datename[5:7], datename[8:10]
            hour, mnt, sec = datename[11:13], datename[14:16], datename[17:19]
            try:
                if year_bounds[0] <= int(year) <= year_bounds[1]:
                    date = datetime.datetime(int(year), int(mth), int(day),
                                             int(hour), int(mnt), int(sec))
            except ValueError:
                pass
            except TypeError:
                pass
    return date


def is_folder_kdin(folder: Path, year_bounds=(1800, 2300)) -> bool:
    """
    --------------------------------------------------------------------------
    returns if the folder matches the Kjmaro naming convention
    --------------------------------------------------------------------------
    """
    date0, _ = get_folder_kdin_bounds(folder, year_bounds)
    return date0 != datetime.datetime(1, 1, 1)


def is_file_kdin(file: Path, year_bounds=(1800, 2300)) -> bool:
    """
    --------------------------------------------------------------------------
    returns if the file matches the Kjmaro date-in-name convention
    --------------------------------------------------------------------------
    This convention defines the date of the file when its metadata-date can
    not be edited. It must be placed at the beginning of the name.
    - Note: For Kjmaro date-edit convention see 'is_edit_kdin()' which has a
            differentiated date format.
    --------------------------------------------------------------------------
    """
    return get_file_kdin(file, year_bounds).year != 1


def is_file_ekdin(file: Path, year_bounds=(1800, 2300)) -> bool:
    """
    --------------------------------------------------------------------------
    returns if the file matches the Kjmaro file edit-date-in-name convention
    --------------------------------------------------------------------------
    This convention is used to automate the date modification of the file. The
    date is written in the filename and this means that the user want to add
    this date to the file.
    --------------------------------------------------------------------------
    """
    return get_file_ekdin(file, year_bounds).year != 1


def is_file_trkdin(file: Path, year_bounds=(1800, 2300)) -> bool:
    """
    --------------------------------------------------------------------------
    returns if the file matches the Kjmaro file To-Review Date-In-Name
    convention
    --------------------------------------------------------------------------
    """
    is_kdin = is_file_kdin(file, year_bounds)
    kdin_txt = date2kdin(get_file_kdin(file, year_bounds))
    return is_kdin and (kdin_txt + "(DTR)") in file.name


def date2kdin(date: datetime.datetime) -> str:
    """Convert a datetime to KDIN format"""
    return date.strftime(r'%Y%m%d-%H%M%S')


def date2ekdin(date: datetime.datetime) -> str:
    """Convert a datetime to EKDIN (edit KDIN) format"""
    return date.strftime(r'++%Y-%m-%d+%H-%M-%S++')


def file_ekdin2clean(file: Path) -> Path:
    """
    --------------------------------------------------------------------------
    Remove the Kjmaro edit-date-in-name convention from the file
    - EditionConvention: [*++YYYY-MM-DD+HH-MM-SS++*]
    --------------------------------------------------------------------------
    """
    clean_filename = file.name.split("++")
    clean_filename.pop(1)
    new_path = file.parent.joinpath(("".join(clean_filename)).strip())
    if new_path.parent != file.parent:
        new_path = new_path.joinpath(" ")
    return new_path


def file_ekdin2kdin(file: Path, year_bounds=(1800, 2300)) -> Path:
    """
    --------------------------------------------------------------------------
    Convert the filename from Kjmaro Edit-DIN to DIN Convention
    > EditionDINConvention: [*++YYYY-MM-DD+HH-MM-SS++*]
    > DateInNameConvention: [YYYYMMDD-HHMMSS*]
    --------------------------------------------------------------------------
    """
    kdin_as_str = date2kdin(get_file_ekdin(file, year_bounds))
    clean_file = file_ekdin2clean(file)
    if clean_file.name == " ":
        new_name = kdin_as_str
    elif clean_file.name == file.suffix or clean_file.name[0] == " ":
        new_name = kdin_as_str + clean_file.name
    else:
        new_name = kdin_as_str + " " + clean_file.name
    return file.parent.joinpath(new_name)


def file_clean2trkdin(file: Path, date2add: datetime.datetime) -> Path:
    """
    --------------------------------------------------------------------------
    Convert the filename to Kjmaro TRDIN Convention (date to review)
    > DateInNameConventionToReview: [YYYYMMDD-HHMMSS(DTR)*]
    --------------------------------------------------------------------------
    """
    kdin_date = date2kdin(date2add)
    if not file.suffix and file.name[0] == ".":
        new_name = file.with_name(kdin_date + "(DTR)" + file.name)
    else:
        new_name = file.with_name(kdin_date + "(DTR) " + file.name)
    return new_name
