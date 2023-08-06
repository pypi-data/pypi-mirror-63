from typing import Any, Dict, List, Union, Optional

from autmux.tmux.tmux_client import TmuxClient

from .job import Job


class DoJob(Job):

    keystrokes: Union[str, List[str]]
    before_sleep_ms: int = 100
    after_sleep_ms: int = 0
    key_interval_ms: int = 100

    @classmethod
    def of(cls, props: Dict[str, Any]) -> Optional[Job]:
        job = DoJob()
        if 'keystrokes' not in props:
            return None

        job.keystrokes = props['keystrokes']

        if 'before-sleep-ms' in props:
            job.before_sleep_ms = int(props['before-sleep-ms'])

        if 'after-sleep-ms' in props:
            job.after_sleep_ms = int(props['after-sleep-ms'])

        if 'key-interval-ms' in props:
            job.key_interval_ms = int(props['key-interval-ms'])
        return job

    @classmethod
    def get_job_name(cls) -> str:
        return 'do'

    def _do(self, tmux_client: TmuxClient) -> None:
        if isinstance(self.keystrokes, str):
            tmux_client.do(self.keystrokes, self.key_interval_ms)

        elif isinstance(self.keystrokes, List):
            for _keystrokes in self.keystrokes:
                tmux_client.do(_keystrokes, self.key_interval_ms)
                tmux_client.do('<CR>', self.key_interval_ms)

    def run(self, tmux_client: TmuxClient) -> None:
        tmux_client.sleep(self.before_sleep_ms)
        self._do(tmux_client)
        tmux_client.sleep(self.after_sleep_ms)
        return
