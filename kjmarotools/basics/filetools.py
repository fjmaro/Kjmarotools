"""File with basic file management tools in python"""
from typing import List, Tuple, Optional
from logging import Logger
from pathlib import Path
import shutil
import os


def itername(file: Path, separator="-", idx=1) -> Path:
    """
    --------------------------------------------------------------------------
    iterate the filename adding '{separator}{count}' starting from {idx} if
    the file exists and return a new file[path] for avoid overwriting
    --------------------------------------------------------------------------
    """
    if not file.exists():
        return file

    new_filename = Path(file)
    sfix = new_filename.suffix
    clean_name = new_filename.stem

    while new_filename.exists():
        new_name = clean_name + separator + f"{idx}" + sfix
        new_filename = file.parent.joinpath(new_name)
        idx += 1
    return new_filename


def get_folders_tree(base_folder: Path, filter_scan: Tuple[str, ...] = ()
                     ) -> List[Path]:
    """
    ---------------------------------------------------------------------------
    Get all the folders-tree allocated in a given <base_folder>

    - base_folder: Base path to get the folders tree.
    - filter_scan: [optional] Include a list of pattern-names in to scan in the
                   base_folder such as [*1*, stuffs*, *A, etc...] and the rest
                   of the folders in base_folder will be skiped.

    - Structure Example
        BaseFolder
            | FolderLvl1_A
            | ...
            | FolderLvl1_Z
    ---------------------------------------------------------------------------
    """
    assert base_folder.is_absolute(), "'base_folder' must be an absolute path."

    if not filter_scan:
        full_tree = [Path(x[0]) for x in os.walk(base_folder)]
        full_tree.sort()
        full_tree.pop(full_tree.index(base_folder))
        return full_tree

    # Get the folders matching the patterns to be scanned
    folders2scan = []
    for kwd in filter_scan:
        folders2scan += list(base_folder.glob(kwd))

    # Get the initial tree including only the desired folders
    folders_tree = [Path(x[0]) for x in os.walk(base_folder)]
    folders_tree = [x for x in folders_tree if x in folders2scan]
    folders_tree.sort()

    # Get all the complete tree of the folders in origin
    full_tree = []
    for folder in folders_tree:
        full_tree += [Path(x[0]) for x in os.walk(folder)]
    full_tree.sort()
    return full_tree


def get_files_tree(folders_tree: List[Path], extensions: Tuple[str, ...] = (),
                   upper_lower=True) -> List[Path]:
    """
    --------------------------------------------------------------------------
    Get all the files (absolute paths) matching the desired extensions 'ext'
    in a list of directories (If <extensions=())> it scans for ALL the files)

    - extensions: Tuple['NEF', 'JPG', etc...] (extensions without the '.')
    - upper_lower: if enabled, it looks for the extension in both upper+lower
    ---------------------------------------------------------------------------
    """
    exts = ["." + x for x in extensions]
    if extensions:
        for extension in extensions:
            assert_txt = f"The extensions must not contain '.' <{extensions}>"
            assert extension[0] != ".", assert_txt
        if upper_lower:
            exts = [x.upper() for x in exts]
            exts = list(exts) + [x.lower() for x in exts]

    full_files = []
    for folder in folders_tree:
        files_found = [folder.joinpath(x) for x in folder.glob("*")]
        files_found = [x for x in files_found if x.is_file()]
        if exts:
            files_found = [x for x in files_found if x.suffix in exts]
        if files_found:
            full_files += files_found
    full_files.sort()
    return full_files


def get_folders_from_files(files_tree: List[Path]) -> List[Path]:
    """
    --------------------------------------------------------------------------
    - Get a list of ABSOLUTE folders for a given ABSOLUTE files tree
    --------------------------------------------------------------------------
    """
    paths2create = []
    for file in files_tree:
        assert file.is_absolute(), "'files_tree' must contain absolute paths."
        assert file.is_file(), "'files_tree' must contain only file paths."
        if file.parent not in paths2create:
            paths2create.append(file.parent)
    return paths2create


def replicate_folders_in_path(relative_dirs2create: List[Path],
                              destination_path: Path,
                              logger: Optional[Logger] = None,
                              log_header: str = "") -> List[Path]:
    """
    --------------------------------------------------------------------------
    Create all the RELATIVE folders in <relative_dirs2create> into the
    <destination_path>
    - 'logger' to include a process log
    - 'log_header' to add a header before the message log
    --------------------------------------------------------------------------
    """
    folders_created: List[Path] = []
    for rel_folder in relative_dirs2create:
        new_folder = destination_path.joinpath(rel_folder)
        if not new_folder.exists():
            os.makedirs(new_folder)
            folders_created.append(rel_folder)
            if logger is not None:
                hdr = log_header if log_header else "Folder created:"
                logger.info(hdr + " %s", rel_folder)
    return folders_created


def move_files2destination(files_relative_tree: List[Path],
                           src_parent_folder: Path,
                           dst_parent_folder: Path,
                           logger: Optional[Logger] = None,
                           log_header: str = "") -> List[Path]:
    """
    --------------------------------------------------------------------------
    Move all the relative files from the <source_parent_folder> to the
    <destination_parent_folder>. (this does not create intermediate folder
    if needed, for this use 'replicate_folders_in_path').
    - 'files_rel_tree' must be list of RELATIVE folders
    - 'src_parent_folder' must be the origin parent folder
    - 'dst_parent_folder' must be the destination parent folder
    - 'logger' to include a process log
    - 'log_header' to add a header before the message log
    - Returns a list with all files moved
    --------------------------------------------------------------------------
    """
    files_moved: List[Path] = []
    err1 = "All files to move must exist in Origin: "
    err2 = "All files to move must NOT exist in Destination: "
    for file in files_relative_tree:
        origin_file = src_parent_folder.joinpath(file)
        destiny_file = dst_parent_folder.joinpath(file)
        assert origin_file.is_file(), err1 + str(file)
        assert not destiny_file.exists(), err2 + str(file)
        shutil.move(origin_file, destiny_file)
        files_moved.append(file)
        if logger is not None:
            hdr = log_header if log_header else "File moved:"
            logger.info(hdr + " %s", file)
    return files_moved
