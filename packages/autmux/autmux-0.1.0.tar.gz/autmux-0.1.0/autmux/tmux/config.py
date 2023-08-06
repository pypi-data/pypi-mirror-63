from enum import Enum, auto
from typing import List, Optional
from dataclasses import dataclass


class NewPaneType(Enum):

    VERTICAL_SPLIT = auto()
    HORIZONTAL_SPLIT = auto()
    NEW_WINDOW = auto()
    NEW_SESSION = auto()


@dataclass(frozen=True)
class TmuxConfig:

    in_tmux: bool
    target: str
    change_focus: bool
    uses_new_window: bool
    uses_new_session: bool
    splits_vertical: bool

    def validate(self) -> str:
        """ Check if configuration is valid.
        """

        return ''

    def get_new_pane_type(self) -> NewPaneType:
        if self.uses_new_session:
            return NewPaneType.NEW_SESSION

        if self.uses_new_window:
            return NewPaneType.NEW_WINDOW

        if self.splits_vertical:
            return NewPaneType.VERTICAL_SPLIT

        else:
            return NewPaneType.HORIZONTAL_SPLIT

    def parse_target(self) -> Optional[List[str]]:
        """ Parse `target` and return [`session`, `window`, `pane`]
        """
        session_and_other = self.target.split(':')
        if len(session_and_other) != 2:
            return None
        session_part = session_and_other[0]
        other = session_and_other[1]

        window_and_pane = other.split('.')
        if len(window_and_pane) != 2:
            return None
        window_part, pane_part = window_and_pane
        return [
            session_part,
            window_part,
            pane_part,
        ]
