import sys
from pathlib import Path
from timeit import default_timer
from typing import Optional, Tuple

import click
from colorama import init
from ward._ward_version import __version__
from ward.collect import (
    get_info_for_modules,
    get_tests_in_modules,
    load_modules,
    search_generally,
)
from ward.config import set_defaults_from_config
from ward.rewrite import rewrite_assertions_in_tests
from ward.suite import Suite
from ward.terminal import SimpleTestResultWrite, get_exit_code

init()

sys.path.append(".")


@click.command()
@click.option(
    "--search",
    help="Search test names, bodies, descriptions and module names for the search query and only run matching tests.",
)
@click.option(
    "--fail-limit",
    type=int,
    help="The maximum number of failures that are allowed to occur in a run before it is automatically cancelled.",
)
@click.option(
    "--test-output-style",
    type=click.Choice(
        ["test-per-line", "dots-global", "dots-module"], case_sensitive=False,
    ),
    default="test-per-line",
)
@click.option(
    "--order",
    type=click.Choice(["standard", "random"], case_sensitive=False),
    default="standard",
    help="Specify the order in which tests should run.",
)
@click.option(
    "--exclude",
    type=click.STRING,
    multiple=True,
    help="Paths to ignore while searching for tests. Accepts glob patterns.",
)
@click.option(
    "--capture-output/--no-capture-output",
    default=True,
    help="Enable or disable output capturing.",
)
@click.version_option(version=__version__)
@click.option(
    "--config",
    type=click.Path(
        exists=False, file_okay=True, dir_okay=False, readable=True, allow_dash=False
    ),
    callback=set_defaults_from_config,
    help="Read configuration from PATH.",
    is_eager=True,
)
@click.option(
    "-p",
    "--path",
    type=click.Path(exists=True),
    multiple=True,
    is_eager=True,
    help="Look for tests in PATH.",
)
@click.option(
    "--show-slowest",
    type=int,
    help="Record and display duration of n longest running tests",
    default=0,
)
@click.option(
    "--dry-run/--no-dry-run",
    help="Print all tests without executing them",
    default=False,
)
@click.pass_context
def run(
    ctx: click.Context,
    path: Tuple[str],
    exclude: Tuple[str],
    search: Optional[str],
    fail_limit: Optional[int],
    test_output_style: str,
    order: str,
    capture_output: bool,
    config: str,
    config_path: Optional[Path],
    show_slowest: int,
    dry_run: bool,
):
    start_run = default_timer()
    paths = [Path(p) for p in path]
    mod_infos = get_info_for_modules(paths, exclude)
    modules = list(load_modules(mod_infos))
    unfiltered_tests = get_tests_in_modules(modules, capture_output)
    tests = list(search_generally(unfiltered_tests, query=search))

    # Rewrite assertions in each test
    tests = rewrite_assertions_in_tests(tests)

    time_to_collect = default_timer() - start_run

    suite = Suite(tests=tests)
    test_results = suite.generate_test_runs(order=order, dry_run=dry_run)

    writer = SimpleTestResultWrite(
        suite=suite, test_output_style=test_output_style, config_path=config_path,
    )
    results = writer.output_all_test_results(
        test_results, time_to_collect=time_to_collect, fail_limit=fail_limit
    )
    time_taken = default_timer() - start_run
    writer.output_test_result_summary(results, time_taken, show_slowest)

    exit_code = get_exit_code(results)

    sys.exit(exit_code.value)
