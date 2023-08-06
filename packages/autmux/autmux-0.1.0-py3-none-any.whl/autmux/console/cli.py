import os
import sys
from typing import Any

import click
from click_help_colors import HelpColorsGroup, HelpColorsCommand

from autmux.tmux.config import TmuxConfig
from autmux.tmux.tmux_client import open_pane
from autmux.scenarios.scenario import Scenario

CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
    max_content_width=120,
)
DEFAULT_COLOR_OPTIONS = dict(
    help_headers_color='white',
    help_options_color='cyan',
)


def panic(message: str) -> None:
    """ Panic with the given message
    """
    print(message, file=sys.stderr)
    sys.exit(1)
    return


@click.group(
    cls=HelpColorsGroup,
    context_settings=CONTEXT_SETTINGS,
    **DEFAULT_COLOR_OPTIONS,  # type: ignore
)
def cli() -> None:
    """ Tmux automation CLI.
    """
    return


def autmux_sub_command(f: Any) -> Any:
    """ autmux's default subcommand decorator
    """
    return cli.command(
        cls=HelpColorsCommand,
        context_settings=CONTEXT_SETTINGS,
        **DEFAULT_COLOR_OPTIONS,
    )(f)


#  @autmux_sub_command
@cli.command(
    cls=HelpColorsCommand,
    context_settings=CONTEXT_SETTINGS,
    **DEFAULT_COLOR_OPTIONS,
)
@click.argument('scenario_path', nargs=1)
@click.option(
    '-t', '--target', default='',
    help="Target of working pane. (same format of tmux's target option)"
)
@click.option(
    '--change-focus/--nochange-focus', default=True,
    help='If `change-focus` is set, pane focus will be changed to workspace.'
)
@click.option(
    '--new-session', is_flag=True,
    help=(
        'If set, new tmux session will be opened. '
        '(Note that this option is valid when the current process is'
        'not running on tmux or `$TMUX` is not set)'
    )
)
@click.option(
    '--new-window', is_flag=True,
    help='If set, new tmux window will be opened'
)
@click.option(
    '--split-vertical/--split-horizontal', default=False,
    help=(
        'Configuring whether pane is split vertical or horizontal. '
        '(This is valid when `--new_window` flag is not provided.)'
    )
)
def run(
    scenario_path: str,
    target: str,
    change_focus: bool,
    new_window: bool,
    new_session: bool,
    split_vertical: bool,
) -> None:
    """ Run tmux automation procedure defined in yaml file (<scenario_path>)
    """
    # load scenario
    scenario = Scenario.of_file(scenario_path)
    if scenario is None:
        panic(f'Cannot open {scenario_path}')
        return

    config = TmuxConfig(
        os.getenv('TMUX', '') != '',
        target,
        change_focus,
        new_window,
        new_session,
        split_vertical,
    )

    err_msg = config.validate()
    if err_msg:
        print(err_msg, file=sys.stderr)
        sys.exit(1)

    # open workspace pane
    with open_pane(config) as tmux_client:
        for job in scenario.steps:
            job.run(tmux_client)
    return


def main() -> None:
    cli()
