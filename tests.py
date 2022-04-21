"""test"""
from pathlib import Path
from kjmarotools.basics import conventions


def folder_naming_test():
    """folder_naming_test"""
    # pylint: disable=too-many-locals
    case1 = Path("2021")
    case2 = Path("2021-2022")
    case3 = Path("2021_2022")
    case4 = Path("2021-10")
    case5 = Path("2021-10-26")
    case6 = Path("2021-10_11")
    case7 = Path("2021-10-11_15")
    case8 = Path("2021-10_2022-11")
    case9 = Path("2021-10-15_11-12")
    case10 = Path("2021-10-15_2022-01-12")

    tst1 = conventions.get_folder_kdin_bounds(case1)
    tst2 = conventions.get_folder_kdin_bounds(case2)
    tst3 = conventions.get_folder_kdin_bounds(case3)
    tst4 = conventions.get_folder_kdin_bounds(case4)
    tst5 = conventions.get_folder_kdin_bounds(case5)
    tst6 = conventions.get_folder_kdin_bounds(case6)
    tst7 = conventions.get_folder_kdin_bounds(case7)
    tst8 = conventions.get_folder_kdin_bounds(case8)
    tst9 = conventions.get_folder_kdin_bounds(case9)
    tst10 = conventions.get_folder_kdin_bounds(case10)

    print(conventions.is_folder_kdin(case1), tst1)
    print(conventions.is_folder_kdin(case2), tst2)
    print(conventions.is_folder_kdin(case3), tst3)
    print(conventions.is_folder_kdin(case4), tst4)
    print(conventions.is_folder_kdin(case5), tst5)
    print(conventions.is_folder_kdin(case6), tst6)
    print(conventions.is_folder_kdin(case7), tst7)
    print(conventions.is_folder_kdin(case8), tst8)
    print(conventions.is_folder_kdin(case9), tst9)
    print(conventions.is_folder_kdin(case10), tst10)


def file_date_in_name_test():
    """file_date_in_name_test"""
    nam1 = Path.cwd().joinpath("20210203-151603")
    nam2 = Path.cwd().joinpath("20210203-151603.jpg")
    nam3 = Path.cwd().joinpath("20210203-151603 cas.jpg")

    tst1 = conventions.get_file_kdin(nam1)
    tst2 = conventions.get_file_kdin(nam2)
    tst3 = conventions.get_file_kdin(nam3)

    print(conventions.is_file_kdin(nam1), tst1)
    print(conventions.is_file_kdin(nam2), tst2)
    print(conventions.is_file_kdin(nam3), tst3)


def file_date_in_name_edition_test():
    """file_date_in_name_edition_test"""
    nam1 = Path.cwd().joinpath("++2021-02-03+15-16-03++")
    nam2 = Path.cwd().joinpath("++2021-02-03+15-16-03++.jpf")
    nam3 = Path.cwd().joinpath("++2021-02-03+15-16-03++csc.jof")
    nam4 = Path.cwd().joinpath("asd++2021-02-03+15-16-03++csc.jof")

    tst1 = conventions.get_file_ekdin(nam1)
    tst2 = conventions.get_file_ekdin(nam2)
    tst3 = conventions.get_file_ekdin(nam3)
    tst4 = conventions.get_file_ekdin(nam4)

    print(conventions.is_file_ekdin(nam1), tst1)
    print(conventions.is_file_ekdin(nam2), tst2)
    print(conventions.is_file_ekdin(nam3), tst3)
    print(conventions.is_file_ekdin(nam4), tst4)


if __name__ == "__main__":
    folder_naming_test()
    file_date_in_name_test()
    file_date_in_name_edition_test()
