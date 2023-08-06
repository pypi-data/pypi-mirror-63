from typing import Any, Dict, Optional
import subprocess as sp

from autmux.tmux.tmux_client import TmuxClient
from .job import Job


class TmuxExecJob(Job):

    command: str

    @classmethod
    def of(cls, props: Dict[str, Any]) -> Optional[Job]:
        job = TmuxExecJob()
        if 'command' not in props:
            return None
        job.command = props['command']
        return job

    @classmethod
    def get_job_name(cls) -> str:
        return 'tmux_exec'

    def run(self, tmux_client: TmuxClient) -> None:
        sp.run(
            f'tmux {self.command}',
            shell=True,
            stdout=sp.PIPE,
        )
        return
