"""The Database as a Python object"""
import datetime

from .task import Task
from .day import Day
from ..schedule import Schedule, Task as ScheduleTask


class Database:
    def __init__(self, day_start: datetime.time, day_end: datetime.time,
            tasks: list[Task]=[]) -> None:
        self.day_start = day_start
        self.day_end = day_end
        self.tasks = tasks

    def to_dict(self) -> dict:
        """This class as a dictionary for JSON encoding"""
        return {'day_start': self.day_start.isoformat(),
                'day_end': self.day_end.isoformat(),
                'tasks': [t.to_dict() for t in self.tasks]}

    @classmethod
    def from_dict(cls, d:dict) -> "Database":
        """This class from a dictionary for JSON encoding"""
        return cls(day_start=datetime.time.fromisoformat(d['day_start']),
                   day_end=datetime.time.fromisoformat(d['day_end']),
                   tasks=[Task.from_dict(t) for t in d['tasks']])

    def proposed_schedule(self, date: datetime.date) -> Schedule:
        """Return a Schedule object with recurring tasks from this 
           database
        """
        todays_tasks = []
        for task in self.tasks:
            converted_task = ScheduleTask.from_database_task(task)
            if Day.DAILY in task.recur:
                todays_tasks.append(converted_task)
            elif date.weekday() in [d.value for d in task.recur]:
                todays_tasks.append(converted_task)

        return Schedule(day_start=self.day_start,
                        day_end=self.day_end,
                        tasks=todays_tasks)
