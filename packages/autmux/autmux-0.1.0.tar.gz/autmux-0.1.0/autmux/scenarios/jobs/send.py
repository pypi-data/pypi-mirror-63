from typing import Any, Dict, Optional

from autmux.tmux.tmux_client import TmuxClient
from .job import Job


class SendJob(Job):

    chars: str

    @classmethod
    def of(cls, props: Dict[str, Any]) -> Optional[Job]:
        job = SendJob()
        if 'chars' not in props:
            return None

        job.chars = props['chars']
        return job

    @classmethod
    def get_job_name(cls) -> str:
        return 'send'

    def run(self, tmux_client: TmuxClient) -> None:
        tmux_client.send(self.chars)
        tmux_client.send('Enter')
        return
