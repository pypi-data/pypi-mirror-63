import json
import time
import subprocess as sp
from pprint import pformat
from typing import Optional, Generator
from contextlib import contextmanager
from dataclasses import dataclass

from .utils import translate_keys
from .config import TmuxConfig, NewPaneType


@dataclass(frozen=True)
class Pane:

    session_id: str
    window_id: str
    pane_id: str

    def close(self) -> None:
        sp.run(
            "tmux kill-pane -t '{}:{}.{}'".format(
                self.session_id,
                self.window_id,
                self.pane_id,
            ),
            shell=True,
        )
        return

    @classmethod
    def of_current(cls) -> Optional['Pane']:
        """ Construct Pane object from current focusing pane
        """
        output = sp.run(
            "tmux display-message -p '#{session_id}.#{window_id}.#{pane_id}'",
            shell=True,
            stdout=sp.PIPE,
        ).stdout.decode('utf-8')
        elms = output.strip().split('.')

        if len(elms) != 3:
            return None
        return Pane(
            session_id=elms[0],
            window_id=elms[1],
            pane_id=elms[2],
        )

    @classmethod
    def new(
        cls,
        new_pane_type: NewPaneType,
    ) -> Optional['Pane']:
        if new_pane_type == NewPaneType.NEW_SESSION:
            new_session_name = 'autmux_session_1'
            sp.run(
                f'tmux new-session -s {new_session_name} -d',
                shell=True,
            )
            # return newly created pane
            return Pane(
                new_session_name,
                '0',
                '0',
            )

        if new_pane_type == NewPaneType.NEW_WINDOW:
            sp.run('tmux new-window -c "$PWD"', shell=True)

        elif new_pane_type == NewPaneType.VERTICAL_SPLIT:
            sp.run('tmux split-window -v -c "$PWD"', shell=True)

        else:
            sp.run('tmux split-window -h -c "$PWD"', shell=True)

        res_pane = cls.of_current()
        return res_pane


@dataclass(frozen=True)
class TmuxClient:

    original_pane: Pane
    workspace_pane: Pane
    config: TmuxConfig

    @classmethod
    def of_config(
        cls,
        config: TmuxConfig
    ) -> Optional['TmuxClient']:

        print('==============================')
        print(f'config: {pformat(config, indent=2)}')
        print('==============================')

        # Set original pane
        original_pane = Pane.of_current()
        if original_pane is None:
            return None

        if not config.target:
            # if target is not set, create workspace
            workspace_pane = Pane.new(config.get_new_pane_type())
            if workspace_pane is None:
                return None
        else:
            parts = config.parse_target()
            if parts is None:
                return None
            workspace_pane = Pane(
                session_id=parts[0],
                window_id=parts[1],
                pane_id=parts[2],
            )

        if not config.change_focus:
            # Focus back to original window
            sp.run(
                "tmux select-window -t '{}:{}'".format(
                    original_pane.session_id,
                    original_pane.window_id,
                ),
                shell=True,
            )

            # Focus back to original pane
            sp.run(
                "tmux select-pane -t '{}'".format(
                    original_pane.pane_id,
                ),
                shell=True,
            )

        return TmuxClient(
            original_pane,
            workspace_pane,
            config,
        )

    def send_key(
        self,
        key: str,
        send_key_delay_ms: int
    ) -> None:
        time.sleep(send_key_delay_ms / 1000)
        cmd = "tmux send-keys -t '{}:{}.{}' '{}'".format(
            self.workspace_pane.session_id,
            self.workspace_pane.window_id,
            self.workspace_pane.pane_id,
            key,
        )
        sp.run(
            cmd,
            shell=True,
        )
        return

    def send(self, s: str) -> None:
        cmd = "tmux send-keys -t '{}:{}.{}' '{}'".format(
            self.workspace_pane.session_id,
            self.workspace_pane.window_id,
            self.workspace_pane.pane_id,
            s,
        )
        sp.run(cmd, shell=True)
        return

    def do(
        self,
        keystrokes: str,
        send_key_delay_ms: int,
    ) -> None:
        for key in translate_keys(keystrokes):
            self.send_key(key, send_key_delay_ms)

    def sleep(self, time_ms: int) -> None:
        time.sleep(time_ms / 1000)

    def close(self) -> None:
        self.workspace_pane.close()
        return

    def __repr__(self) -> str:
        return json.dumps(self.__dict__, indent=2)


@contextmanager
def open_pane(
    config: TmuxConfig
) -> Generator[TmuxClient, None, None]:
    client = TmuxClient.of_config(config)
    if client is None:
        raise Exception("Cannot generate Tmux Client")
    try:
        yield client
    finally:
        client.close()
