from typing import Any, Dict, Optional

from autmux.tmux.tmux_client import TmuxClient
from .job import Job


class SleepJob(Job):

    sleep_ms: int

    @classmethod
    def of(cls, props: Dict[str, Any]) -> Optional[Job]:
        job = SleepJob()
        if 'sleep-ms' not in props:
            return None
        job.sleep_ms = int(props['sleep-ms'])
        return job

    @classmethod
    def get_job_name(cls) -> str:
        return 'sleep'

    def run(self, tmux_client: TmuxClient) -> None:
        tmux_client.sleep(self.sleep_ms)
        return
