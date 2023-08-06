import re
import string
import subprocess as sp
from typing import List, Generator
from dataclasses import dataclass

# -------------------------------------
# Session
# -------------------------------------


@dataclass(frozen=True)
class _Session:

    SESSION_LINE_RE = r'(?P<name>\w+): (?P<window_cnt>\d+) windows \((?P<date>.*)\)'  # noqa

    name: str
    window_cnt: int
    date_str: str

    @classmethod
    def get_sessions(cls) -> List['_Session']:
        output = sp.run(
            'tmux list-sessions',
            shell=True,
            stdout=sp.PIPE,
        ).stdout.decode('utf-8')
        return cls._parse_list_session_output_lines(output.split('\n'))

    @classmethod
    def _parse_list_session_output_lines(
        cls,
        lines: List[str],
    ) -> List['_Session']:
        res = []
        for line in lines:
            m = re.search(cls.SESSION_LINE_RE, line)
            if m is None:
                continue
            name = m.group('name')
            window_cnt = m.group('window_cnt')
            date_str = m.group('date')
            res.append(_Session(
                name,
                int(window_cnt),
                date_str,
            ))
        return res

    @classmethod
    def session_exists(cls, name: str) -> bool:
        return any([
            session.name == name
            for session in cls.get_sessions()
        ])


# -------------------------------------
# Window
# -------------------------------------


# -------------------------------------
# Pane
# -------------------------------------

def _parse_pane_nrs(output_lines: List[str]) -> List[int]:
    """ Parse output of `tmux list-panes` and return
    all pane numbers as List
    """
    return [
        int(line.split(':')[0])
        for line in output_lines
        if line.strip() != ''
    ]


def get_pane_nrs() -> List[int]:
    """ Get all pane numbers
    """
    output = sp.run(
        'tmux list-panes',
        shell=True,
        stdout=sp.PIPE,
    ).stdout.decode('utf-8')
    return _parse_pane_nrs(output.split('\n'))

# -------------------------------------
# Keystrokes
# -------------------------------------


def keystroke_generator(keystrokes: str) -> Generator[str, None, None]:
    """ From just keystrokes string, construct a generator,
    each of its yield is the sendable string.
    """
    DELIMITER_START = '<'
    DELIMITER_END = '>'

    in_delimiters = False
    tmp_buffer = ''

    for c in keystrokes:
        if not in_delimiters and c != DELIMITER_START:
            # Simple character
            yield c

        elif not in_delimiters and c == DELIMITER_START:
            # Start of delimiter
            tmp_buffer += c
            in_delimiters = True

        elif c != DELIMITER_END:
            tmp_buffer += c

        elif c == DELIMITER_END:
            tmp_buffer += c
            yield tmp_buffer
            tmp_buffer = ''
            in_delimiters = False


KEYSTROKE_MAP = {
    # Space
    ' ': 'Space',

    # Enter
    '<Enter>': 'Enter',
    '<CR>': 'Enter',
    '\n': 'Enter',

    # Tab
    '<Tab>': 'Tab',
    '\t': 'Tab',

    # BackSpace
    '<BS>': 'BSpace',

    # Escape
    '<ESC>': 'Escape',
}

EXTRA_VALID_DECORATED_KEYS = '!@#$%^&*(){}[]:;"\'<,>.?/'

# add ctrl-key
KEYSTROKE_MAP.update(
    {
        f'<C-{k}>': f'C-{k}'
        for k in string.ascii_uppercase + string.ascii_lowercase + EXTRA_VALID_DECORATED_KEYS  # noqa
    }
)

# add meta-key
KEYSTROKE_MAP.update(
    {
        f'<M-{k}>': f'M-{k}'
        for k in string.ascii_uppercase + string.ascii_lowercase + EXTRA_VALID_DECORATED_KEYS  # noqa
    }
)


def convert_single_keystroke(keystroke: str) -> str:
    if keystroke not in KEYSTROKE_MAP and len(keystroke) == 1:
        return keystroke

    if keystroke in KEYSTROKE_MAP:
        return KEYSTROKE_MAP[keystroke]

    raise ValueError


def translate_keys(keystrokes: str) -> List[str]:
    """ Transalate keystrokes(characters that appear in terminal when keystrokes
    are input) into tmux_keys (including Space and C-d)
    """

    keys = []

    for keystroke in keystroke_generator(keystrokes):
        keys.append(convert_single_keystroke(keystroke))
    return keys
