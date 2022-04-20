"""py photography tools"""
from pathlib import Path
from typing import Dict, Tuple

from pyexifmgr import PyExifManager

from .basics import logtools, filetools, convert


def raw_arranger(output_folder: Path, raw_extensions=("NEF", "RAW"),
                 folders2scan=("1.*", "2.*", "3.*", "4.*", "5.*")):
    """
    --------------------------------------------------------------------------
              MOVE THE NEGATIVES REPLICATING THE PICTURES FOLDERS
    --------------------------------------------------------------------------
    > folders2scan:   Folders to scan for negatives to move into output_folder
    > output_folder:  Negatives folder (destination folder of the negatives)
    > raw_extensions: These files are considered the 'negatives'

    Info
    ------
    > 'output_folder' must be allocated in the same path of 'folders2scan'

    Folder structure required
    ---------------------------
    - PicturesFolder (directory with the pictures and negative folders)
        - 1. folderA
        - 2. folderB
        - other fldr
        - negatives_folder (this is the 'output_folder')

    This script does the following:
    --------------------------------------------------------------------------
    > FOLDER SCAN / CHECK
    1) Scan the folders in source and destination folders.
    2) Verify that all folders in destination already exist in source.

    > FILES SCAN / CHECK
    3) Scan all the negative-files to move.
    4) Verify that none of these files already exist in destionation folder.

    > DUPLICATE FOLDERS AND MOVE FILES
    5) Duplicate the folder structure from source into destination folder.
    6) Move the negative-files into the destination folder.
    --------------------------------------------------------------------------
    """
    # pylint: disable=too-many-locals

    # Initial path
    log = logtools.get_fast_logger("rawArranger")
    input_chk = f"\n> END reached with ERRORS (see '{log.name}.log' for"
    input_chk += " more info).\n> Press <ENTER> to close."

    if not output_folder.is_absolute():
        err_msg = f"output_folder '{output_folder}' if not an absolute path."
        log.error(err_msg)
        input(input_chk)
        return
    if not output_folder.exists():
        err_msg = f"output_folder '{output_folder}' does not exists."
        log.error(err_msg)
        input(input_chk)
        return

    negative_path = output_folder
    pictures_path = negative_path.parent

    # Get the source tree including only the desired folders
    src_fldrs_tree = filetools.get_folders_tree(pictures_path, folders2scan)

    # Get all the destination tree
    dst_fldrs_tree = filetools.get_folders_tree(negative_path)

    # Verify that all the destination folders exist also in origin
    src_rel_fldrs = filetools.paths_abs2rel(src_fldrs_tree, pictures_path)
    dst_rel_fldrs = filetools.paths_abs2rel(dst_fldrs_tree, negative_path)
    out1 = filetools.find_lost_folders(src_rel_fldrs, dst_rel_fldrs, log)

    # Verify that none of the files to be moved exist also in destination
    src_files_tree = filetools.get_files_tree(src_fldrs_tree, raw_extensions)
    dst_files_tree = filetools.get_files_tree(dst_fldrs_tree, raw_extensions)
    src_rel_files = filetools.paths_abs2rel(src_files_tree, pictures_path)
    dst_rel_files = filetools.paths_abs2rel(dst_files_tree, negative_path)
    out2 = filetools.find_existing_files(src_rel_files, dst_rel_files, log)

    # If conflicts found exit the program, else continue.
    if out1 or out2:
        err_msg = "Conflicts found during the folder/file system check,"
        err_msg += f" see <{log.name}.log> for more information."
        log.error("END reached with ERRORS")
        print(err_msg)
        input("\n> END reached with ERRORS. Press <ENTER> to close")
        return

    # Get only the needed folders to create based on the files to move
    abs_req_folders = filetools.get_folders_from_files(src_files_tree)
    rel_req_folders = filetools.paths_abs2rel(abs_req_folders, pictures_path)

    # Create the folders if those not exist
    filetools.replicate_folders_in_path(rel_req_folders, negative_path, log)

    # Move the files into the folders
    filetools.move_files2destination(src_rel_files, pictures_path,
                                     negative_path, log)

    # Process finalized
    log.info("END of process reached")
    input("> END of process SUCCESSFULY reached. Press <ENTER> to close")


def scan4extensions(base_path: Path, combine_uppers=True, log_results=True
                    ) -> Tuple[Dict[str, int], Dict[str, list]]:
    """
    --------------------------------------------------------------------------
    Get a list of all the file-extensions in path
    - files without extension are stored as .<!>
    - if combine_uppers=True uppers/lowers are considered the same (JPG+jpg)

    > return (Dict(ext, count), Dict(ext, list_of_files))
    --------------------------------------------------------------------------
    """
    fld_tree = filetools.get_folders_tree(base_path)
    fls_tree = filetools.get_files_tree(fld_tree)

    ext_count: Dict[str, int] = {}
    ext_found: Dict[str, list] = {}
    files2check = len(fls_tree)

    for fle_idx, file in enumerate(fls_tree):
        print(f"{fle_idx/files2check * 100:>5.2f}%", file)
        extns = file.suffix if file.suffix else ".<!>"
        extns = extns.lower() if combine_uppers else extns

        if extns not in ext_count:
            ext_count[extns] = 1
            ext_found[extns] = [file]
        else:
            ext_count[extns] += 1
            ext_found[extns].append(file)

    if log_results:
        log = logtools.get_fast_logger("scan4extensions")
        log.info("scan4extensions in %s", base_path)
        for kwd in list(ext_count.keys()):
            log.info("Total files with extension %s = %s",
                     kwd, ext_count[kwd])

        for kwd in list(ext_found.keys()):
            for sub_kwd in ext_found[kwd]:
                log.info("Ext= %s | %s", kwd, sub_kwd)
    return ext_count, ext_found


def files_without_exif_dates(base_path: Path, log_results=True
                             ) -> list:
    """
    --------------------------------------------------------------------------
    return all the files found with exif creation date.

    returns:
    - List of files without Exif creation date
    - List of files with non-compatible format
    --------------------------------------------------------------------------
    """
    fld_tree = filetools.get_folders_tree(base_path)
    fls_tree = filetools.get_files_tree(fld_tree)
    mgr = PyExifManager()
    files_without_date = []

    if log_results:
        log = logtools.get_fast_logger("noexifdates")
        log.info("noexifdates in %s", base_path)

    for file in fls_tree:
        mgr.load_file(file)
        not_exif = mgr.has_exif_create_date
        not_mov = mgr.has_mov_create_date
        if not_mov and not_exif:
            files_without_date.append(file)
            if log_results:
                log.info(file)
    return files_without_date


def files_mismatching_folder_name(base_path: Path, relative=False,
                                  log_results=True) -> Tuple[list, list]:
    """
    --------------------------------------------------------------------------
    return all the files mismatching its respectives folder year (and month
    if found). if 'relative=True' the output is in RELATIVE path files.

    > If the file format is NON-COMPATIBLE the file modification date is used
    > If the date is not found in folder, the file is considered MISMATCHING

    returns Tuple[List(Matching), List(Mismatching)]:
    - List of files matching dates
    - List of files mismatching dates
    --------------------------------------------------------------------------
    """
    # pylint: disable=too-many-locals
    fld_tree = filetools.get_folders_tree(base_path)
    fls_tree = filetools.get_files_tree(fld_tree)

    files_matching = []
    files_mismatching = []
    files2check = len(fls_tree)

    for fle_idx, file in enumerate(fls_tree):
        print(f"{fle_idx/files2check * 100:>5.2f}%", file)
        mgr = PyexifManager()
        mgr.load_file(file)
        if mgr.has_exif_create_date:
            dtt = mgr.get_exif_create_date()
        else:
            dtt = mgr.get_file_modify_date()

        # Find the folder date in its name
        date0, date1 = filetools.find_folder_date_bounds(file.parent, True)
        dtfld_txt = f"({date0.year:4d}-{date0.month:02d}-{date0.day:02d} | "
        dtfld_txt += f"{date1.year:4d}-{date1.month:02d}-{date1.day:02d})"

        file_txt = str(file)
        if relative:
            file_txt = str(file.relative_to(base_path))
        txt2show = convert.datetime2string(dtt)[:10], dtfld_txt, file_txt

        # If the date is not found in folder
        if date0.year == 1:
            files_mismatching.append(txt2show)

        # Else get check if the file is in range
        else:
            if date0 <= dtt < date1:
                files_matching.append(txt2show)
            else:
                files_mismatching.append(txt2show)

    if log_results:
        log = logtools.get_fast_logger("files_mismatching_folder_analysis")
        log.info("files_mismatching_folder_analysis in %s", base_path)
        log.info("FILE DATE  FOLDER START|END DATE     FILENAME ANALYSED")
        for fle in files_mismatching:
            log.warning(fle[0] + " " + fle[1] + " " + fle[2])
        for fle in files_matching:
            log.info(fle[0] + " " + fle[1] + " " + fle[2])
    return files_matching, files_mismatching


def beta_files_exif_analysis(base_path: Path, print_info=True
                        ) -> Tuple[list, list, list]:
    """
    --------------------------------------------------------------------------
    return all the files found with exif, without exif and with non-compatible
    extension format

    returns:
    - List of files with Exif data
    - List of files without Exif data
    - List of files with non-compatible format
    --------------------------------------------------------------------------
    """
    fld_tree = tools.get_folders_tree(base_path)
    fls_tree = tools.get_files_tree(fld_tree)
    mgr = ExifManager()
    valid_formats = ["." + x for x in mgr.valid_mgr_formats]

    files_chked_w = []
    files_chked_wo = []
    files_not_comptbl = []

    for file in fls_tree:
        if file.suffix and file.suffix.upper() in valid_formats:
            mgr.load_file(file)
            if mgr.valid_date_taken:
                files_chked_w.append(file)
            else:
                files_chked_wo.append(file)
        else:
            files_not_comptbl.append(file)

    if print_info:
        print("Files with exif:    ", len(files_chked_w))
        print("Files without exif:  ", len(files_chked_wo))
        print("Files not compatible:", len(files_not_comptbl))
    strtools.progress(1)
    return files_chked_w, files_chked_wo, files_not_comptbl
