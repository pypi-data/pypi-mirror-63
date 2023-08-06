"""
Scenario of tmux automation
"""

from typing import Any, Dict, List, Optional
from os.path import exists
from dataclasses import dataclass

import yaml

from .jobs.do import DoJob
from .jobs.send import SendJob
from .jobs.job import Job
from .jobs.sleep import SleepJob

from .jobs.tmux_exec import TmuxExecJob

JOB_CLASSES_MAP = {
    job_class.get_job_name(): job_class for job_class in [
        SleepJob,
        DoJob,
        SendJob,
        TmuxExecJob,
    ]
}


@dataclass(frozen=True)
class JobDefinition:
    job: str
    description: str
    props: Dict[str, Any]

    def make_job(self) -> Optional[Job]:
        if self.job not in JOB_CLASSES_MAP:
            return None
        job = JOB_CLASSES_MAP[self.job].of(self.props)
        if job is None:
            return None
        return job


@dataclass(frozen=True)
class Scenario:

    name: str
    description: str
    steps: List[Job]

    @classmethod
    def of_file(cls, filepath: str) -> Optional['Scenario']:
        if not exists(filepath):
            return None
        with open(filepath) as f:
            d = yaml.load(f, Loader=yaml.BaseLoader)
        job_deifinitions = [
            JobDefinition(
                step_d['job'],
                step_d['description'],
                step_d['props'],
            ) for step_d in d['steps']
        ]
        maybe_jobs = [
            job_deifinition.make_job()
            for job_deifinition in job_deifinitions
        ]

        jobs: List[Job] = []
        for maybe_job in maybe_jobs:
            if maybe_job is None:
                return None
            jobs.append(maybe_job)

        return Scenario(
            d['name'],
            d['description'],
            jobs,
        )
