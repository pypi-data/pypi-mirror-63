
from abc import ABCMeta, abstractmethod, abstractclassmethod
from typing import Any, Dict, Optional

from autmux.tmux.tmux_client import TmuxClient


class Job(metaclass=ABCMeta):

    @classmethod
    @abstractclassmethod
    def of(cls, props: Dict[str, Any]) -> Optional['Job']:
        raise NotImplementedError

    @classmethod
    @abstractclassmethod
    def get_job_name(cls) -> str:
        raise NotImplementedError

    @abstractmethod
    def run(self, tmux_client: TmuxClient) -> None:
        raise NotImplementedError
