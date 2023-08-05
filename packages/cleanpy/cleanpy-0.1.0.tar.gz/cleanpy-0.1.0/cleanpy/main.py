#!/usr/bin/env python3

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import logging
from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter
from logging import Logger
from textwrap import dedent
from typing import AbstractSet

from .__version__ import __version__
from ._const import BUILD_CACHE_DIRS, IGNORE_DIRS, Category, LogLevel
from ._finder import Finder
from ._manipulator import DirEntryManipulator


def parse_option() -> Namespace:
    parser = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        description=dedent(
            """\
            Remove cache files and temporary files that related to Python.

            Skip directories from recursive search: {}
            """.format(
                ", ".join(IGNORE_DIRS)
            )
        ),
        epilog=dedent(
            """\
            Issue tracker: https://github.com/thombashi/cleanpy/issues
            """
        ),
    )
    parser.add_argument("-V", "--version", action="version", version="%(prog)s " + __version__)

    parser.add_argument(
        "target_dirs", metavar="DIR_PATH", nargs="+", help="path to a root directory to search"
    )

    parser.add_argument(
        "--follow-symlinks", action="store_true", default=False, help="follow symlinks"
    )
    parser.add_argument("--dry-run", action="store_true", default=False, help="do no harm.")

    group = parser.add_argument_group("Remove Target")
    group.add_argument(
        "-a",
        "--all",
        action="store_true",
        default=False,
        help="remove all of the caches and teporary files.",
    )
    group.add_argument(
        "--include-builds",
        action="store_true",
        default=False,
        help="remove files/directories that related build: {}, docs/_build".format(
            ", ".join(BUILD_CACHE_DIRS)
        ),
    )
    group.add_argument(
        "--include-envs", action="store_true", default=False, help="remove virtual environments."
    )
    group.add_argument(
        "--include-metadata", action="store_true", default=False, help="remove metadata."
    )
    group.add_argument(
        "--include-testing",
        action="store_true",
        default=False,
        help="remove test results and coverage files.",
    )
    group.add_argument(
        "--exclude",
        metavar="PATTERN",
        help=dedent(
            """\
            a regular expression that matches files and
            directories that should be excluded on recursive searches.
            """
        ),
    )
    group.add_argument(
        "--exclude-envs", action="store_true", default=False, help="exclude virtual environments."
    )

    loglevel_dest = "log_level"
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-v",
        "--verbose",
        dest=loglevel_dest,
        action="store_const",
        const=logging.INFO,
        default=LogLevel.DEFAULT,
        help="shows verbose output.",
    )
    group.add_argument(
        "--debug",
        dest=loglevel_dest,
        action="store_const",
        const=logging.DEBUG,
        default=LogLevel.DEFAULT,
        help="for debug print.",
    )
    group.add_argument(
        "--quiet",
        dest=loglevel_dest,
        action="store_const",
        const=LogLevel.QUIET,
        default=LogLevel.DEFAULT,
        help="suppress execution log messages.",
    )

    return parser.parse_args()


def get_logger(log_level: int) -> Logger:
    logging.basicConfig(
        format="[%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S",
    )

    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    if log_level == LogLevel.QUIET:
        logging.disable(logging.NOTSET)

    return logger


def extract_log_level(log_level: int, dry_run: bool) -> int:
    if dry_run:
        return min(log_level, logging.INFO)

    return log_level


def extract_categories(options) -> AbstractSet[str]:
    category_set = {Category.CACHE}

    if options.all:
        category_set |= set(Category.ALL)

    if options.include_builds:
        category_set.add(Category.BUILD)
    if options.include_envs:
        category_set.add(Category.ENV)
    if options.include_metadata:
        category_set.add(Category.METADATA)
    if options.include_testing:
        category_set.add(Category.TESTING)

    if options.exclude_envs:
        category_set.remove(Category.ENV)

    return category_set


def main():
    options = parse_option()
    logger = get_logger(extract_log_level(options.log_level, options.dry_run))
    manipulator = DirEntryManipulator(
        logger, follow_symlinks=options.follow_symlinks, dry_run=options.dry_run
    )
    finder = Finder(
        logger,
        manipulator=manipulator,
        exclude_pattern=options.exclude,
        include_categories=extract_categories(options),
    )
    target_dirs = set(options.target_dirs)

    logger.debug(f"target_dirs: {target_dirs}")

    for target_dir in target_dirs:
        logger.debug(f"scan dir: {target_dir}")
        finder.traverse(target_dir)

    for delete_entry in finder.get_delete_entries():
        entry, remove_target = delete_entry

        try:
            manipulator.remove(entry, remove_target)
        except OSError as e:
            logger.error(e)

    for entry_type, count in manipulator.remove_count.items():
        logger.info(f"removed {count} {entry_type}")

    for entry_type, count in manipulator.error_count.items():
        logger.error(f"failed to remove {count} {entry_type}")


if __name__ == "__main__":
    main()
