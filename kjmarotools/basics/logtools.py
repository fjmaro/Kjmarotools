"""logging tools"""
from pathlib import Path
import datetime
import logging


def progress(uni_value: float, tale_text2add="", print_result=False) -> str:
    """Simple progress to string in '%' converter"""
    txt = f"{uni_value * 100:>5.2f}% " + tale_text2add
    if print_result:
        print(txt)
    return txt


def get_fast_logger(name: str, base_path=Path.cwd(), tofile=True,
                    initialize=True, log_level="DEBUG") -> logging.Logger:
    """
    ----------------------------------------------------------------------
    Initialize a simple logger with its CMD and FILE <name.log> handlers
    (if enabled) and return its handler (logging.Logger())
    - name: Name of the logger
    - base_path: path of the logger if tofile=True (base_path/name.log)
    - tofile: If enabled the logs will be recorded in a file
    - initialize: If enabled initialization prints/messages will be shown
    ----------------------------------------------------------------------
    """
    log_file = base_path.joinpath(name + '.log')
    if tofile:
        with open(log_file, "a", encoding="utf-8") as fle:
            if initialize:
                curr_tme = datetime.datetime.now()
                fle.write("-" * 41 + "\n")
                fle.write("NEW EXECUTION: " + str(curr_tme) + "\n")
                fle.write("-" * 41 + "\n")

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    hlrs = [isinstance(x, logging.FileHandler) for x in logger.handlers]
    has_file_handlers = True in hlrs

    hlrs = [isinstance(x, logging.StreamHandler) for x in logger.handlers]
    has_cmd_handlers = True in hlrs

    log_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-5.5s | %(message)s")

    if not has_file_handlers and tofile:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(log_formatter)
        file_handler.setLevel(log_level)
        logger.addHandler(file_handler)

    if not has_cmd_handlers:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        console_handler.setLevel(log_level)
        logger.addHandler(console_handler)

    if initialize:
        logger.info("Logger initialized in '%s.log'", logger.name)
    return logger
